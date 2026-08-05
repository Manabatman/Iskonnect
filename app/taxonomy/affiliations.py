"""Affiliation code catalog helpers — equity flag sync and profile checks."""

from __future__ import annotations

from typing import Any

# Maps equity profile boolean fields to affiliation codes (kind=equity).
EQUITY_FLAG_TO_AFFILIATION: dict[str, str] = {
    "is_pwd": "pwd",
    "is_indigenous_people": "ip",
    "is_solo_parent_dependent": "solo_parent_dependent",
    "is_ofw_dependent": "ofw_dependent",
    "is_military_dependent": "military_dependent",
    "is_uniformed_service_dependent": "uniformed_service_dependent",
    "is_farmer_fisher_dependent": "farmer_fisher_dependent",
    "is_4ps_listahanan": "4ps_listahanan",
    "is_gsis_dependent": "gsis_member",
    "is_sss_dependent": "sss_member",
    "is_medical_frontliner_dependent": "medical_frontliner_dependent",
}

EMPLOYMENT_AFFILIATIONS: dict[str, str] = {
    "is_hei_faculty_or_staff": "hei_faculty",
}


def profile_affiliation_codes(profile: dict[str, Any]) -> set[str]:
    """Derive attested affiliation codes from profile fields (no DB join required)."""
    codes: set[str] = set()
    explicit = profile.get("affiliation_codes") or profile.get("student_affiliation_codes") or []
    for c in explicit:
        if c:
            codes.add(str(c).strip().lower())
    for flag, code in EQUITY_FLAG_TO_AFFILIATION.items():
        if profile.get(flag):
            codes.add(code)
    for flag, code in EMPLOYMENT_AFFILIATIONS.items():
        if profile.get(flag):
            codes.add(code)
    return codes


def profile_has_affiliation(profile: dict[str, Any], code: str) -> bool:
    return code.strip().lower() in profile_affiliation_codes(profile)
