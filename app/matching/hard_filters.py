"""
Hard filter service - deal-breakers that exclude scholarships before scoring.

Uses EligibilityResult as the single eligibility authority. Scholarships with
status not_eligible are excluded from scored matches; others may be scored and ranked.
"""

import logging
from datetime import date, datetime

from app.matching.eligibility_result import (
    EligibilityResult,
    QualificationStatus,
    RequirementResult,
    cities_match,
    evaluate_eligibility,
    normalize_city,
)
from app.utils.json_helpers import parse_json_list
from app.utils.timezone import today_manila

logger = logging.getLogger(__name__)

DEADLINE_PASSED_MESSAGE = (
    "You satisfy the eligibility requirements but the application deadline has already passed."
)


def is_application_deadline_passed(application_deadline) -> bool:
    """True when the scholarship application deadline is before today (Asia/Manila calendar day)."""
    if application_deadline is None:
        return False
    if isinstance(application_deadline, datetime):
        deadline_day = application_deadline.date()
    elif isinstance(application_deadline, date):
        deadline_day = application_deadline
    elif isinstance(application_deadline, str) and application_deadline.strip():
        try:
            deadline_day = date.fromisoformat(application_deadline.strip()[:10])
        except ValueError:
            return False
    else:
        return False
    return deadline_day < today_manila()


# Re-export for backward compatibility in tests and temporal_state
__all__ = [
    "DEADLINE_PASSED_MESSAGE",
    "cities_match",
    "evaluate_eligibility",
    "filter_scholarships",
    "is_application_deadline_passed",
    "normalize_city",
    "_hard_filter_failure_stage",
]


def _hard_filter_failure_stage(profile: dict, sch: dict) -> str | None:
    """Return the first failed filter name, or None if passes. Uses EligibilityResult."""
    result = evaluate_eligibility(profile, sch)
    if result.status != QualificationStatus.NOT_ELIGIBLE:
        return None
    for req in result.requirements:
        if req.result == RequirementResult.UNMET:
            return req.key
    return "unknown"


def _missing_profile_fields(profile: dict) -> list[str]:
    missing: list[str] = []
    if profile.get("age") is None:
        missing.append("age")
    pl = profile.get("education_level") or profile.get("current_academic_stage")
    if not pl or not str(pl).strip():
        missing.append("education_level")
    has_region = profile.get("region") and str(profile.get("region")).strip()
    has_city = profile.get("city_municipality") and str(profile.get("city_municipality")).strip()
    if not has_region and not has_city:
        missing.append("region_or_city")
    st = profile.get("school_type")
    if not st or not str(st).strip():
        missing.append("school_type")
    if profile.get("household_income_annual") is None and not profile.get("income_bracket"):
        missing.append("income")
    if profile.get("gwa_normalized") is None and not (
        profile.get("gwa_raw") and str(profile.get("gwa_raw")).strip()
    ):
        missing.append("gwa")
    broad = profile.get("field_of_study_broad")
    prefs = parse_json_list(profile.get("preferred_courses"))
    if not (broad and str(broad).strip()) and not any(prefs):
        missing.append("field_of_study")
    return missing


def _top_blockers(eliminated: dict[str, int], missing: list[str]) -> list[str]:
    blockers: list[str] = []
    if "gwa" in missing:
        blockers.append("Your profile is missing GWA; merit thresholds could not be evaluated strictly.")
    if "income" in missing:
        blockers.append("Household income or bracket is missing; income ceilings may not filter accurately.")
    if "field_of_study" in missing:
        blockers.append("Add your field of study or preferred courses to match course-specific scholarships.")
    if "region_or_city" in missing:
        blockers.append("Region or city helps LGU and location-restricted scholarships match accurately.")
    labels = {
        "data_status": "expired or broken-link data status",
        "age": "age requirements",
        "education_level": "education level",
        "region": "region or city location",
        "school_type": "school type (public/private)",
        "income": "household income limits",
        "gwa": "GWA / academic minimums",
        "field": "field of study or course alignment",
        "members_only": "members-only priority group",
    }
    for key, count in sorted(eliminated.items(), key=lambda x: -x[1]):
        if count <= 0:
            continue
        blockers.append(f"{count} scholarship(s) excluded by {labels.get(key, key)}.")
        if len(blockers) >= 6:
            break
    return blockers[:6]


def filter_scholarships(profile: dict, scholarships: list) -> tuple[list, dict]:
    """
    Return scholarships that pass eligibility (not not_eligible) and diagnostics.
    Each candidate dict is annotated with _eligibility_result.
    """
    result: list = []
    eliminated: dict[str, int] = {
        "data_status": 0,
        "age": 0,
        "education_level": 0,
        "region": 0,
        "school_type": 0,
        "income": 0,
        "gwa": 0,
        "field": 0,
        "members_only": 0,
    }
    eliminated_scholarships: list[dict] = []
    eligibility_by_id: dict[int, dict] = {}
    filter_labels = {
        "data_status": "expired or broken-link data status",
        "age": "age requirements",
        "education_level": "education level",
        "region": "region or city location",
        "school_type": "school type (public/private)",
        "income": "household income limits",
        "gwa": "GWA / academic minimums",
        "field": "field of study or course alignment",
        "members_only": "members-only priority group",
        "unknown": "eligibility requirements",
    }

    for sch in scholarships:
        elig: EligibilityResult = evaluate_eligibility(profile, sch)
        sid = sch.get("id")
        if sid is not None:
            eligibility_by_id[int(sid)] = elig.to_dict()

        if not elig.passes_for_matching:
            stage = None
            for req in elig.requirements:
                if req.result == RequirementResult.UNMET:
                    stage = req.key
                    break
            stage = stage or "unknown"
            eliminated[stage] = eliminated.get(stage, 0) + 1
            if len(eliminated_scholarships) < 50:
                eliminated_scholarships.append(
                    {
                        "scholarship_id": sch.get("id"),
                        "title": sch.get("title"),
                        "filter": stage,
                        "reason": filter_labels.get(stage, stage),
                        "eligibility": elig.to_dict(),
                    }
                )
            continue

        annotated = {**sch, "_eligibility_result": elig.to_dict()}
        result.append(annotated)

    missing = _missing_profile_fields(profile)
    diagnostics = {
        "total_checked": len(scholarships),
        "passed_hard_filters": len(result),
        "eliminated_by_filter": {k: v for k, v in eliminated.items() if v},
        "eliminated_scholarships": eliminated_scholarships,
        "hard_exclusions": eliminated_scholarships,
        "missing_profile_fields": missing,
        "top_blockers": _top_blockers(eliminated, missing),
        "deadline_passed_count": sum(
            1 for sch in result if is_application_deadline_passed(sch.get("application_deadline"))
        ),
        "eligibility_by_scholarship_id": eligibility_by_id,
    }
    return result, diagnostics
