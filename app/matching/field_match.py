"""
Shared field-of-study matching helpers for hard filters and scoring.

Uses exact / token-boundary matching for short PSCED codes (e.g. IT) to avoid
substring false positives (e.g. 'it' inside 'architecture').
"""

from __future__ import annotations

import re

from app.taxonomy.psced_fields import FIELD_HIERARCHY, PSCED_SPECIFIC_COURSES

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
    """Broad field plus FIELD_HIERARCHY parents, lowercased."""
    if not field_broad or not str(field_broad).strip():
        return []
    broad = str(field_broad).strip()
    fields = [_norm(broad)]
    parents = FIELD_HIERARCHY.get(broad)
    if parents:
        fields.extend(_norm(p) for p in parents)
    return fields


def broad_maps_to_specific_eligible(field_broad: str | None, eligible_specific: list) -> bool:
    """Bridge broad field (e.g. Medical) to eligible_courses_specific (e.g. BS Nursing)."""
    if not field_broad or not eligible_specific:
        return False
    key = str(field_broad).strip()
    mapped = {_norm(c) for c in PSCED_SPECIFIC_COURSES.get(key, [])}
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
