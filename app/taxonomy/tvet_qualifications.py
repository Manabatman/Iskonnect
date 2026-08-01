"""
TESDA / TVET qualification taxonomy (DATA-06).

Qualifications are separate from degree fields and are offered only when the
student's academic stage is TVET.
"""

from __future__ import annotations

# qualification name -> broad discipline used for upward matching
TVET_QUALIFICATIONS: dict[str, str] = {
    "Automotive Servicing NC II": "Engineering",
    "Shielded Metal Arc Welding NC II": "Engineering",
    "Electrical Installation and Maintenance NC II": "Engineering",
    "Electronics Servicing NC II": "IT",
    "Computer Systems Servicing NC II": "IT",
    "Refrigeration and Air-Conditioning Servicing NC II": "Engineering",
    "Plumbing NC II": "Engineering",
    "Carpentry NC II": "Engineering",
    "Masonry NC II": "Engineering",
    "Heavy Equipment Operation NC II": "Engineering",
    "Machining NC II": "Engineering",
    "Dressmaking NC II": "Business",
    "Tailoring NC II": "Business",
    "Cookery NC II": "Tourism & Hospitality",
    "Bread and Pastry Production NC II": "Tourism & Hospitality",
    "Housekeeping NC II": "Tourism & Hospitality",
    "Caregiving NC II": "Medical",
    "Beauty Care NC II": "Business",
    "Bookkeeping NC II": "Business",
}

_TVET_STAGE_ALIASES = frozenset({"tvet", "vocational", "tesda"})


def is_tvet_stage(academic_stage: str | None) -> bool:
    if not academic_stage:
        return False
    return academic_stage.strip().lower() in _TVET_STAGE_ALIASES


def tvet_qualifications_for_stage(academic_stage: str | None) -> list[str]:
    """Return TVET qualifications only when the profile stage is TVET."""
    if not is_tvet_stage(academic_stage):
        return []
    return sorted(TVET_QUALIFICATIONS.keys())


def tvet_broad_discipline(qualification: str) -> str | None:
    return TVET_QUALIFICATIONS.get(qualification)
