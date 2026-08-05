"""
Shared field-of-study matching helpers for hard filters and scoring.

Uses exact / token-boundary matching for short PSCED codes (e.g. IT) to avoid
substring false positives (e.g. 'it' inside 'architecture').
"""

from __future__ import annotations

import re

from app.taxonomy.psced_fields import (
    FIELD_HIERARCHY,
    PSCED_SPECIFIC_COURSES,
    resolve_field_ancestors,
    resolve_normalized_field,
)

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _norm(value: str | None) -> str:
    return str(value or "").strip().lower()


def _tokens(value: str) -> set[str]:
    return set(_TOKEN_RE.findall(_norm(value)))


def psced_code_matches(profile_field: str, eligible_code: str) -> bool:
    """Match PSCED broad codes (IT, STEM, Medical, …) without substring traps."""
    pf, ec = _norm(profile_field), _norm(eligible_code)
    if not pf or not ec:
        return False
    if pf == ec:
        return True
    # Short codes (<=3 chars) require exact equality only.
    if len(pf) <= 3 or len(ec) <= 3:
        return pf == ec
    if pf in ec or ec in pf:
        return True
    # Token overlap for multi-word labels (e.g. "information technology")
    return bool(_tokens(pf) & _tokens(ec))


_DEGREE_STOP_TOKENS = frozenset({
    "bs", "ba", "ab", "ma", "ms", "phd", "beed", "bsed", "bse", "nc", "ii", "iii",
})


def specific_course_matches(profile_course: str, eligible_course: str) -> bool:
    """Match specific course names (requires meaningful token overlap, not just 'bs')."""
    pc, ec = _norm(profile_course), _norm(eligible_course)
    if not pc or not ec:
        return False
    if pc == ec:
        return True
    if len(pc) >= 6 and len(ec) >= 6 and (pc in ec or ec in pc):
        return True
    shared = _tokens(pc) & _tokens(ec)
    meaningful = {t for t in shared if t not in _DEGREE_STOP_TOKENS and len(t) >= 4}
    return bool(meaningful)


def profile_fields_for_matching(field_broad: str | None) -> list[str]:
    """Normalized field plus transitive FIELD_HIERARCHY ancestors, lowercased."""
    return resolve_field_ancestors(field_broad)


def broad_maps_to_specific_eligible(field_broad: str | None, eligible_specific: list) -> bool:
    """Bridge broad field (e.g. Medical) to eligible_courses_specific (e.g. BS Nursing)."""
    if not field_broad or not eligible_specific:
        return False
    key = str(field_broad).strip()
    mapped = {_norm(c) for c in PSCED_SPECIFIC_COURSES.get(key, [])}
    if not mapped:
        resolved = resolve_normalized_field(key)
        if resolved:
            mapped = {_norm(c) for c in PSCED_SPECIFIC_COURSES.get(resolved, [])}
    if not mapped:
        return False
    for ec in eligible_specific:
        if not ec:
            continue
        ec_n = _norm(ec)
        if ec_n in mapped:
            return True
        if any(specific_course_matches(m, ec_n) for m in mapped):
            return True
    return False


def _case_insensitive_hierarchy_key(field: str) -> str | None:
    if field in FIELD_HIERARCHY:
        return field
    lower = field.lower()
    for key in FIELD_HIERARCHY:
        if key.lower() == lower:
            return key
    return None


def _immediate_parent(field: str | None) -> str | None:
    if not field:
        return None
    resolved = resolve_normalized_field(field)
    if not resolved:
        return None
    key = _case_insensitive_hierarchy_key(resolved)
    if not key:
        return None
    parents = FIELD_HIERARCHY.get(key) or []
    return parents[0] if parents else None


def _level_rank(level: str) -> int:
    return {
        "exact": 4,
        "sibling": 3,
        "broad": 3,
        "discipline": 2,
        "partial": 1,
        "none": 0,
    }.get(level, 0)


def compute_field_match_level(
    profile_field_broad: str | None,
    profile_field_specific: str | None,
    profile_preferred_courses: list,
    profile_needs: list,
    eligible_psced: list,
    eligible_specific: list,
    needs_tags: list,
) -> str:
    """
    Four-level field match (DATA-03 / B7): exact > sibling > discipline > none.

    Legacy level names ``broad`` and ``partial`` remain accepted downstream in
    scoring and explanations as aliases.
    """
    eligible_psced_norm = [_norm(x) for x in (eligible_psced or []) if x]
    eligible_specific_norm = [_norm(x) for x in (eligible_specific or []) if x]
    needs_tags_norm = [_norm(x) for x in (needs_tags or []) if x]
    profile_needs_norm = [_norm(x) for x in (profile_needs or []) if x]
    profile_specific_norm = _norm(profile_field_specific)

    preferred_courses = [_norm(x) for x in (profile_preferred_courses or []) if x]
    courses_to_check = preferred_courses or ([profile_specific_norm] if profile_specific_norm else [])

    best = "none"

    def bump(level: str) -> None:
        nonlocal best
        if _level_rank(level) > _level_rank(best):
            best = level

    for course in courses_to_check:
        if not course or not eligible_specific_norm:
            continue
        if course in eligible_specific_norm:
            bump("exact")
            continue
        if any(specific_course_matches(course, es) for es in eligible_specific_norm):
            bump("exact")

    if profile_specific_norm and eligible_specific_norm:
        if profile_specific_norm in eligible_specific_norm:
            bump("exact")
        elif any(specific_course_matches(profile_specific_norm, ps) for ps in eligible_specific_norm):
            bump("exact")

    if not eligible_psced_norm and not eligible_specific_norm:
        return best

    chain = resolve_field_ancestors(profile_field_broad)
    profile_field_lc = chain[0] if chain else ""
    profile_resolved = resolve_normalized_field(profile_field_broad or "")

    for restr_raw in eligible_psced_norm:
        restr_resolved = resolve_normalized_field(restr_raw)
        restr_lc = _norm(restr_resolved or restr_raw)

        if profile_field_lc and profile_field_lc == restr_lc:
            bump("exact")
            continue

        if profile_field_lc and restr_lc in chain[1:]:
            bump("discipline")
            continue

        if profile_resolved and restr_resolved:
            profile_parent = _immediate_parent(profile_resolved)
            restr_parent = _immediate_parent(restr_resolved)
            if (
                profile_parent
                and restr_parent
                and profile_parent.lower() == restr_parent.lower()
                and profile_field_lc != restr_lc
            ):
                bump("sibling")
                continue
            if profile_parent and profile_parent.lower() == restr_lc:
                bump("discipline")
                continue

        if profile_field_lc and psced_code_matches(profile_field_lc, restr_lc):
            bump("discipline")

    if profile_needs_norm and needs_tags_norm:
        for pn in profile_needs_norm:
            for nt in needs_tags_norm:
                if pn in nt or nt in pn:
                    bump("discipline")

    if (
        best == "none"
        and (profile_field_broad or profile_needs_norm)
        and (eligible_psced_norm or eligible_specific_norm)
    ):
        bump("partial")

    return best
