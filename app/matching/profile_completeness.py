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
    filled, total = count_hard_filter_fields_populated(profile)
    return {
        "filled_fields": filled,
        "total_fields": total,
        "low_data_warning": filled < 3,
    }
