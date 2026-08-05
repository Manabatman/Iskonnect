"""
Canonical priority group labels and alias normalization for scholarship matching.
"""

from __future__ import annotations

# Map CSV/import variants to canonical EQUITY_GROUPS keys (or affiliation labels).
PRIORITY_GROUP_ALIASES: dict[str, str] = {
    "4Ps": "4Ps/Listahanan",
    "Listahanan": "4Ps/Listahanan",
    "Solo Parent Dependents": "Solo Parent Dependent",
    "Farmers and Fishers Dependents": "Farmer/Fisher Dependent",
    "Indigenous Peoples (Lumad)": "IP",
    "Indigenous Peoples (IP)": "IP",
    "IP Academic Achievers": "IP",
    "CAR Indigenous Youth": "IP",
    "working student": "Working Student",
    "working students": "Working Student",
    "employed student": "Working Student",
    "student athlete": "Student Athlete",
    "student athletes": "Student Athlete",
    "athlete": "Student Athlete",
    "athletes": "Student Athlete",
    "varsity": "Student Athlete",
    "varsity athlete": "Student Athlete",
}


def resolve_priority_group(label: str) -> str:
    """Return canonical priority group label for matching and storage."""
    raw = (label or "").strip()
    if not raw:
        return raw
    return PRIORITY_GROUP_ALIASES.get(raw, raw)


def normalize_priority_groups(groups: list[str] | None) -> list[str]:
    """Deduplicate and canonicalize priority group labels."""
    if not groups:
        return []
    seen: set[str] = set()
    out: list[str] = []
    for g in groups:
        canon = resolve_priority_group(str(g))
        if canon and canon not in seen:
            seen.add(canon)
            out.append(canon)
    return out
