"""Resolve free-text school names to canonical registry IDs."""

from __future__ import annotations

import re

from app.taxonomy.schools import SCHOOL_REGISTRY


def _normalize(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = s.replace("university of the philippines", "up")
    return s


def resolve_school_id(name: str | None) -> str | None:
    """
    Map a user-typed or imported school name to a canonical registry id.

    Returns None when no match is found (caller may treat as unknown).
    """
    if not name or not str(name).strip():
        return None
    raw = str(name).strip()
    norm = _normalize(raw)

    if raw in SCHOOL_REGISTRY:
        return raw

    for sid, entry in SCHOOL_REGISTRY.items():
        if _normalize(entry["canonical_name"]) == norm:
            return sid
        for alias in entry.get("aliases") or []:
            if _normalize(alias) == norm:
                return sid

    # Abbreviation / substring heuristics for major HEIs
    shortcuts = {
        "pup": "polytechnic-university-of-the-philippines",
        "ust": "university-of-santo-tomas",
        "dlsu": "de-la-salle-university",
        "ateneo": "ateneo-de-manila-university",
        "up diliman": "university-of-the-philippines-diliman",
        "up manila": "university-of-the-philippines-manila",
        "up los baños": "university-of-the-philippines-los-banos",
        "uplb": "university-of-the-philippines-los-banos",
        "upd": "university-of-the-philippines-diliman",
        "plm": "pamantasan-ng-lungsod-ng-maynila",
    }
    key = norm.replace(".", "")
    if key in shortcuts and shortcuts[key] in SCHOOL_REGISTRY:
        return shortcuts[key]

    return None


def resolve_school_ids(names: list[str]) -> list[str]:
    """Resolve a list of names/ids; preserve order, skip unresolved."""
    out: list[str] = []
    seen: set[str] = set()
    for name in names:
        if not name:
            continue
        sid = name if name in SCHOOL_REGISTRY else resolve_school_id(name)
        if sid and sid not in seen:
            seen.add(sid)
            out.append(sid)
    return out
