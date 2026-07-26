"""
Count populated hard-filter-related profile fields for low-data warnings.
Aligned with fields used in app.matching.hard_filters.
"""

from __future__ import annotations

import json
from typing import Any


def _parse_preferred_courses(val: Any) -> list:
    if val is None:
        return []
    if isinstance(val, list):
        return [str(x).strip() for x in val if x and str(x).strip()]
    if isinstance(val, str):
        try:
            p = json.loads(val)
            return [str(x).strip() for x in p if x and str(x).strip()] if isinstance(p, list) else []
        except (json.JSONDecodeError, TypeError):
            return []
    return []


def count_hard_filter_fields_populated(profile: dict) -> tuple[int, int]:
    """
    Return (filled_count, total) for seven hard-filter-related signals.
    """
    total = 7
    filled = 0

    if profile.get("age") is not None:
        filled += 1

    level = (profile.get("education_level") or profile.get("current_academic_stage") or "").strip()
    if level:
        filled += 1

    if (profile.get("region") or "").strip():
        filled += 1

    if (profile.get("school_type") or "").strip():
        filled += 1

    if profile.get("household_income_annual") is not None or (profile.get("income_bracket") or "").strip():
        filled += 1

    if profile.get("gwa_normalized") is not None:
        filled += 1

    if (profile.get("field_of_study_broad") or "").strip() or _parse_preferred_courses(profile.get("preferred_courses")):
        filled += 1

    return filled, total


def profile_completeness_payload(profile: dict) -> dict:
    """Profile quality for matching — counts hard-filter fields and lists gaps."""
    field_defs = [
        ("age", "Age", "profile-builder?step=personal"),
        ("education_level", "Education level", "profile-builder?step=education"),
        ("region", "Region", "profile-builder?step=location"),
        ("school_type", "School type (public/private)", "profile-builder?step=education"),
        ("income", "Household income or bracket", "profile-builder?step=location"),
        ("gwa", "GWA / grades", "profile-builder?step=education"),
        ("field_of_study", "Field of study or courses", "profile-builder?step=field"),
        ("school", "Current school", "profile-builder?step=education"),
        ("current_year_level", "Current year level", "profile-builder?step=education"),
        ("enrollment_status", "Enrollment status", "profile-builder?step=education"),
    ]

    def _filled(key: str) -> bool:
        if key == "age":
            return profile.get("age") is not None
        if key == "education_level":
            return bool((profile.get("education_level") or profile.get("current_academic_stage") or "").strip())
        if key == "region":
            return bool((profile.get("region") or "").strip())
        if key == "school_type":
            return bool((profile.get("school_type") or "").strip())
        if key == "income":
            return profile.get("household_income_annual") is not None or bool(
                (profile.get("income_bracket") or "").strip()
            )
        if key == "gwa":
            return profile.get("gwa_normalized") is not None
        if key == "field_of_study":
            return bool((profile.get("field_of_study_broad") or "").strip()) or bool(
                _parse_preferred_courses(profile.get("preferred_courses"))
            )
        if key == "school":
            return bool((profile.get("school") or profile.get("school_id") or "").strip())
        if key == "current_year_level":
            return profile.get("current_year_level") is not None
        if key == "enrollment_status":
            return bool((profile.get("enrollment_status") or "").strip())
        return False

    missing: list[dict[str, str]] = []
    filled_count = 0
    for key, label, link in field_defs:
        if _filled(key):
            filled_count += 1
        else:
            missing.append({"key": key, "label": label, "profile_link": link})

    total = len(field_defs)
    percent = round(100 * filled_count / total) if total else 0
    legacy_filled, legacy_total = count_hard_filter_fields_populated(profile)

    hints: list[str] = []
    if not _filled("school"):
        hints.append("Adding your school lets us check institution-specific programs.")
    if not _filled("current_year_level"):
        hints.append("Year level helps filter scholarships for your standing (e.g. incoming 3rd year).")
    if not _filled("income"):
        hints.append("Income data unlocks need-based scholarship filters.")

    return {
        "filled_fields": legacy_filled,
        "total_fields": legacy_total,
        "quality_percent": percent,
        "quality_filled": filled_count,
        "quality_total": total,
        "missing_fields": missing,
        "improvement_hints": hints,
        "low_data_warning": legacy_filled < 3,
    }
