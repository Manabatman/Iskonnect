"""
Eligibility migration v1 — additional hard-gate evaluators behind per-gate feature flags.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from app.config import settings
from app.matching.eligibility_result import RequirementCheck, RequirementResult, RequirementVerification
from app.taxonomy.affiliations import profile_has_affiliation
from app.utils.json_helpers import parse_json_list


def _na(key: str, label: str) -> RequirementCheck:
    return RequirementCheck(key, label, "hard", RequirementResult.NOT_APPLICABLE, RequirementVerification.VERIFIED)


def _unknown(key: str, label: str, msg: str) -> RequirementCheck:
    return RequirementCheck(
        key, label, "hard", RequirementResult.UNKNOWN, RequirementVerification.UNVERIFIED, msg
    )


def _met(key: str, label: str, evidence: str) -> RequirementCheck:
    return RequirementCheck(
        key, label, "hard", RequirementResult.MET, RequirementVerification.VERIFIED, evidence
    )


def _unmet(key: str, label: str, evidence: str) -> RequirementCheck:
    return RequirementCheck(
        key, label, "hard", RequirementResult.UNMET, RequirementVerification.VERIFIED, evidence
    )


def evaluate_prior_tertiary_units(profile: dict, sch: dict) -> RequirementCheck:
    if not settings.gate_prior_units:
        return _na("prior_units", "Prior tertiary units")
    max_units = sch.get("max_prior_tertiary_units")
    if max_units is None:
        return _na("prior_units", "Prior tertiary units")
    prior = profile.get("prior_tertiary_units")
    if prior is None:
        return _unknown(
            "prior_units",
            f"Prior tertiary units (max {max_units})",
            "Prior tertiary units not provided",
        )
    if prior <= max_units:
        return _met("prior_units", f"Prior tertiary units (max {max_units})", f"Your units: {prior}")
    return _unmet(
        "prior_units",
        f"Prior tertiary units (max {max_units})",
        f"Your units: {prior}",
    )


def evaluate_entry_path(profile: dict, sch: dict) -> RequirementCheck:
    if not settings.gate_entry_path:
        return _na("entry_path", "Entry path (transferee/shiftee/first degree)")
    status = (profile.get("enrollment_status") or "").strip().lower()
    checks: list[tuple[str, bool | None, str]] = [
        ("transferee", sch.get("allow_transferee"), "Transferees"),
        ("shiftee", sch.get("allow_shiftee"), "Shiftees"),
    ]
    applicable = [c for c in checks if c[1] is not None]
    if sch.get("first_undergraduate_only"):
        applicable.append(("first_undergraduate", True, "First undergraduate degree only"))
    if not applicable:
        return _na("entry_path", "Entry path")
    if not status:
        return _unknown("entry_path", "Entry path", "Enrollment status not provided")
    if status == "transferee" and sch.get("allow_transferee") is False:
        return _unmet("entry_path", "Transferees not eligible", "You declared: transferee")
    if status == "shiftee" and sch.get("allow_shiftee") is False:
        return _unmet("entry_path", "Shiftees not eligible", "You declared: shiftee")
    if sch.get("first_undergraduate_only") and profile.get("prior_tertiary_units", 0) not in (None, 0):
        prior = profile.get("prior_tertiary_units")
        if prior is None:
            return _unknown("entry_path", "First undergraduate degree only", "Prior tertiary units not provided")
        if prior > 0:
            return _unmet("entry_path", "First undergraduate degree only", f"Prior units: {prior}")
    return _met("entry_path", "Entry path", f"Status: {status}")


def evaluate_min_residency(profile: dict, sch: dict) -> RequirementCheck:
    if not settings.gate_residency_years:
        return _na("residency_years", "Local residency duration")
    min_years = sch.get("min_residency_years")
    if min_years is None:
        return _na("residency_years", "Local residency duration")
    years = profile.get("residency_years_in_locality")
    if years is None:
        return _unknown(
            "residency_years",
            f"Local residency (≥ {min_years} years)",
            "Years of residency in locality not provided",
        )
    if years >= min_years:
        return _met("residency_years", f"Local residency (≥ {min_years} years)", f"Your residency: {years} years")
    return _unmet(
        "residency_years",
        f"Local residency (≥ {min_years} years)",
        f"Your residency: {years} years",
    )


def evaluate_required_affiliations(profile: dict, sch: dict) -> RequirementCheck:
    required = parse_json_list(sch.get("required_affiliation_codes")) or []
    if not required:
        return _na("required_affiliation", "Required affiliation / registry")
    # Evaluate when required codes exist even if GATE_AFFILIATIONS is off (pre-gate-rollout compatibility).
    for code in required:
        if profile_has_affiliation(profile, str(code)):
            return _met(
                "required_affiliation",
                f"Affiliation ({code})",
                f"You declared: {code}",
            )
    labels = ", ".join(str(c) for c in required)
    return _unmet(
        "required_affiliation",
        f"Affiliation ({labels})",
        "Required affiliation not declared in profile",
    )


def evaluate_conflict_scopes(profile: dict, sch: dict) -> RequirementCheck:
    if not settings.gate_conflicts:
        return _na("conflict_scope", "Grant exclusivity")
    scopes = parse_json_list(sch.get("conflict_scope_codes")) or []
    if not scopes:
        return _na("conflict_scope", "Grant exclusivity")
    active = set(str(c).strip().lower() for c in (profile.get("active_grant_scope_codes") or []) if c)
    for scope in scopes:
        sc = str(scope).strip().lower()
        if sc in active:
            return _unmet(
                "conflict_scope",
                f"No active {sc} grant",
                f"You reported an active {sc} grant (self-reported)",
            )
    return _met("conflict_scope", "Grant exclusivity", "No conflicting active grants reported")


def evaluate_parent_salary_grade(profile: dict, sch: dict) -> RequirementCheck:
    if not settings.gate_parent_salary_grade:
        return _na("parent_salary_grade", "Parent salary grade")
    max_grade = sch.get("max_parent_salary_grade")
    if max_grade is None:
        return _na("parent_salary_grade", "Parent salary grade")
    grade = profile.get("parent_salary_grade")
    if grade is None:
        return _unknown(
            "parent_salary_grade",
            f"Parent salary grade (≤ {max_grade})",
            "Parent salary grade not provided",
        )
    if grade <= max_grade:
        return _met(
            "parent_salary_grade",
            f"Parent salary grade (≤ {max_grade})",
            f"Declared grade: {grade}",
        )
    return _unmet(
        "parent_salary_grade",
        f"Parent salary grade (≤ {max_grade})",
        f"Declared grade: {grade}",
    )


def _check_gwa(profile: dict, sch: dict) -> tuple[RequirementResult, str | None]:
    min_gwa = sch.get("min_gwa_normalized")
    if min_gwa is None:
        return RequirementResult.NOT_APPLICABLE, None
    gwa = profile.get("gwa_normalized")
    if gwa is None:
        return RequirementResult.UNKNOWN, "GWA not provided"
    if gwa >= min_gwa:
        return RequirementResult.MET, f"GWA {gwa}% ≥ {min_gwa}%"
    return RequirementResult.UNMET, f"GWA {gwa}% < {min_gwa}%"


def _check_rank(profile: dict, sch: dict) -> tuple[RequirementResult, str | None]:
    max_rank = sch.get("max_class_rank")
    if max_rank is None:
        return RequirementResult.NOT_APPLICABLE, None
    rank = profile.get("class_rank")
    if rank is None:
        return RequirementResult.UNKNOWN, "Class rank not provided"
    if rank <= max_rank:
        return RequirementResult.MET, f"Rank {rank} ≤ top {max_rank}"
    return RequirementResult.UNMET, f"Rank {rank} > top {max_rank}"


def _check_percentile(profile: dict, sch: dict) -> tuple[RequirementResult, str | None]:
    max_pct = sch.get("max_class_percentile")
    if max_pct is None:
        return RequirementResult.NOT_APPLICABLE, None
    rank = profile.get("class_rank")
    size = profile.get("class_size")
    if rank is None or size is None or size <= 0:
        return RequirementResult.UNKNOWN, "Class rank and class size required for percentile"
    pct = (rank / size) * 100.0
    if pct <= max_pct:
        return RequirementResult.MET, f"Percentile {pct:.1f}% ≤ {max_pct}%"
    return RequirementResult.UNMET, f"Percentile {pct:.1f}% > {max_pct}%"


def evaluate_academic(profile: dict, sch: dict) -> RequirementCheck:
    """Academic gate — GWA and/or rank/percentile with optional OR mode."""
    min_gwa = sch.get("min_gwa_normalized")
    max_rank = sch.get("max_class_rank")
    max_pct = sch.get("max_class_percentile")
    if min_gwa is None and max_rank is None and max_pct is None:
        return _na("academic", "Academic requirement")

    use_or = settings.gate_academic_or and (sch.get("academic_gate_mode") or "").strip().lower() == "or"

    gwa_r, gwa_e = _check_gwa(profile, sch)
    rank_r, rank_e = _check_rank(profile, sch)
    pct_r, pct_e = _check_percentile(profile, sch)

    parts = [(gwa_r, gwa_e, "GWA"), (rank_r, rank_e, "rank"), (pct_r, pct_e, "percentile")]
    active = [(r, e, name) for r, e, name in parts if r != RequirementResult.NOT_APPLICABLE]

    if not active:
        return _na("academic", "Academic requirement")

    if not use_or:
        # Legacy: only GWA when gate off; when gate on without or mode, AND all set predicates
        if not settings.gate_academic_or:
            if min_gwa is not None:
                if gwa_r == RequirementResult.UNKNOWN:
                    return _unknown("academic", f"GWA ≥ {min_gwa}%", gwa_e or "GWA not provided")
                if gwa_r == RequirementResult.UNMET:
                    return _unmet("academic", f"GWA ≥ {min_gwa}%", gwa_e or "")
                return _met("academic", f"GWA ≥ {min_gwa}%", gwa_e or "")
            return _na("academic", "Academic requirement")
        for r, e, name in active:
            if r == RequirementResult.UNKNOWN:
                return _unknown("academic", "Academic requirement", e or f"{name} not provided")
            if r == RequirementResult.UNMET:
                return _unmet("academic", "Academic requirement", e or f"{name} not met")
        evidence = "; ".join(e for _, e, _ in active if e)
        return _met("academic", "Academic requirement", evidence)

    # OR mode: any MET satisfies; all UNKNOWN → UNKNOWN; else UNMET
    if any(r == RequirementResult.MET for r, _, _ in active):
        met_evidence = next(e for r, e, _ in active if r == RequirementResult.MET and e)
        return _met("academic", "Academic requirement (any of)", met_evidence or "Requirement met")
    if all(r == RequirementResult.UNKNOWN for r, _, _ in active):
        return _unknown("academic", "Academic requirement (any of)", "Academic credentials not provided")
    evidence = "; ".join(e for _, e, _ in active if e)
    return _unmet("academic", "Academic requirement (any of)", evidence or "No academic path satisfied")


def evaluate_age_as_of(profile: dict, sch: dict, *, as_of: date | None = None) -> RequirementCheck:
    if not settings.gate_age_as_of:
        return _na("age_as_of", "Age as of cutoff date")
    rule = (sch.get("age_as_of_rule") or "").strip()
    cutoff = sch.get("age_as_of_date")
    if not rule or not cutoff:
        return _na("age_as_of", "Age as of cutoff date")

    birthdate = profile.get("birthdate")
    if isinstance(birthdate, str) and birthdate:
        try:
            birthdate = date.fromisoformat(birthdate[:10])
        except ValueError:
            birthdate = None
    if birthdate is None:
        return _unknown("age_as_of", f"Age rule ({rule})", "Birthdate not provided")

    if isinstance(cutoff, str):
        cutoff = date.fromisoformat(cutoff[:10])

    if rule == "born_on_or_after":
        ok = birthdate >= cutoff
        label = f"Born on or after {cutoff.isoformat()}"
    elif rule == "born_on_or_before":
        ok = birthdate <= cutoff
        label = f"Born on or before {cutoff.isoformat()}"
    elif rule in ("age_at_date_lte", "age_at_date_gte"):
        ref = as_of or date.today()
        age = ref.year - birthdate.year
        if (ref.month, ref.day) < (birthdate.month, birthdate.day):
            age -= 1
        min_age = sch.get("min_age")
        max_age = sch.get("max_age")
        if rule == "age_at_date_lte":
            ok = max_age is not None and age <= max_age
            label = f"Age ≤ {max_age} as of {ref.isoformat()}"
        else:
            ok = min_age is not None and age >= min_age
            label = f"Age ≥ {min_age} as of {ref.isoformat()}"
    else:
        return _na("age_as_of", "Age as of cutoff date")

    if ok:
        return _met("age_as_of", label, f"Birthdate: {birthdate.isoformat()}")
    return _unmet("age_as_of", label, f"Birthdate: {birthdate.isoformat()}")


def evaluate_work_experience(profile: dict, sch: dict) -> RequirementCheck:
    if not settings.gate_work_experience:
        return _na("work_experience", "Work experience")
    min_years = sch.get("min_work_experience_years")
    if min_years is None:
        return _na("work_experience", "Work experience")
    years = profile.get("work_experience_years")
    if years is None:
        return _unknown(
            "work_experience",
            f"Work experience (≥ {min_years} years)",
            "Work experience not provided",
        )
    if years >= min_years:
        return _met("work_experience", f"Work experience (≥ {min_years} years)", f"Your experience: {years} years")
    return _unmet(
        "work_experience",
        f"Work experience (≥ {min_years} years)",
        f"Your experience: {years} years",
    )


def evaluate_marital_status(profile: dict, sch: dict) -> RequirementCheck:
    if not settings.gate_marital_status:
        return _na("marital_status", "Marital status")
    required = parse_json_list(sch.get("required_marital_statuses"))
    if not required:
        # Convention: single-only programs may set via type_attributes or explicit list later
        return _na("marital_status", "Marital status")
    status = (profile.get("marital_status") or "").strip().lower()
    if not status:
        return _unknown("marital_status", f"Marital status ({', '.join(required)})", "Marital status not provided")
    req_lower = [str(r).strip().lower() for r in required]
    if status in req_lower:
        return _met("marital_status", f"Marital status ({status})", f"You declared: {status}")
    return _unmet("marital_status", f"Marital status ({', '.join(required)})", f"You declared: {status}")
