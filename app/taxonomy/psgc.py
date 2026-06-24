"""
Philippine Standard Geographic Code (PSGC) helpers.

Provides prefix-based matching for region (2-digit), province (4-digit),
municipality (6-digit), and barangay (9-digit) codes. Full PSGC datasets
should be loaded from official PSA releases; this module ships lookup utilities
and a minimal seed map for common NCR entries.
"""

from __future__ import annotations

# Minimal seed: expand via CSV import from https://psa.gov.ph/classification/psgc/
PSGC_SEED: dict[str, dict[str, str]] = {
    "130000000": {"name": "National Capital Region (NCR)", "level": "region"},
    "137400000": {"name": "City of Manila", "level": "city"},
    "137401000": {"name": "Binondo", "level": "barangay"},
    "137402000": {"name": "Ermita", "level": "barangay"},
}


def normalize_psgc_code(code: str | None) -> str | None:
    """Return a 9-digit zero-padded PSGC code or None if invalid."""
    if not code:
        return None
    digits = "".join(ch for ch in str(code).strip() if ch.isdigit())
    if len(digits) < 2 or len(digits) > 9:
        return None
    return digits.ljust(9, "0")


def psgc_prefix_length(level: str) -> int:
    """Return digit prefix length for a geographic level."""
    mapping = {"region": 2, "province": 4, "municipality": 6, "city": 6, "barangay": 9}
    return mapping.get(level.strip().lower(), 9)


def psgc_codes_match(
    student_code: str | None,
    requirement_code: str | None,
    level: str = "region",
) -> bool:
    """Return True when student and requirement PSGC codes share the required prefix."""
    a = normalize_psgc_code(student_code)
    b = normalize_psgc_code(requirement_code)
    if not a or not b:
        return False
    n = psgc_prefix_length(level)
    return a[:n] == b[:n]


def lookup_psgc_name(code: str | None) -> str | None:
    """Resolve a PSGC code to a display name from the seed map."""
    normalized = normalize_psgc_code(code)
    if not normalized:
        return None
    entry = PSGC_SEED.get(normalized)
    return entry["name"] if entry else None
