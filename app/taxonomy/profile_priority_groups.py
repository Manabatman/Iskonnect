"""Profile-derived priority group labels (DATA-08).

These are separate from the 11 equity groups in ``equity_groups.py`` — they are
computed from explicit profile fields and used for scholarship ``priority_groups`` matching.
"""

from __future__ import annotations

from typing import Any

WORKING_STUDENT = "Working Student"
STUDENT_ATHLETE = "Student Athlete"

_EMPLOYED_STATUSES = frozenset(
    {
        "employed",
        "part-time",
        "part time",
        "full-time",
        "full time",
        "self-employed",
        "self employed",
    }
)

_ATHLETE_LEVELS = frozenset(
    {
        "varsity",
        "club",
        "regional",
        "national",
    }
)


def _norm(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def profile_working_student(profile: dict[str, Any]) -> bool:
    """True when student is employed or enrolled in an evening/weekend program."""
    status = _norm(profile.get("employment_status"))
    if status in _EMPLOYED_STATUSES:
        return True
    evening = profile.get("evening_weekend_program")
    if evening is True or _norm(evening) in {"true", "yes", "1", "on"}:
        return True
    return False


def profile_student_athlete(profile: dict[str, Any]) -> bool:
    """True when athlete_level is set to a recognized competitive level."""
    return _norm(profile.get("athlete_level")) in _ATHLETE_LEVELS


def profile_priority_groups(profile: dict[str, Any]) -> list[str]:
    """Ordered list of profile-derived priority group labels."""
    out: list[str] = []
    if profile_working_student(profile):
        out.append(WORKING_STUDENT)
    if profile_student_athlete(profile):
        out.append(STUDENT_ATHLETE)
    return out
