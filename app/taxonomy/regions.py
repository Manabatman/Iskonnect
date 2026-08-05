"""
Philippine region constants and normalization.
Expanded from original REGION_ALIASES for LGU and geographic matching.
"""

# Region aliases: map common user inputs to canonical names for exact matching.
# Full PHILIPPINE_REGIONS names map to themselves (lowercase) for consistency.
REGION_ALIASES = {
    "ncr": "ncr",
    "national capital region": "ncr",
    "metro manila": "ncr",
    "ncr - metro manila": "ncr",
    "region i - ilocos": "region i - ilocos",
    "region ii - cagayan valley": "region ii - cagayan valley",
    "region iii - central luzon": "region iii - central luzon",
    "region iv-a - calabarzon": "region iv-a - calabarzon",
    "region iv-b - mimaropa": "region iv-b - mimaropa",
    "region v - bicol": "region v - bicol",
    "region vi - western visayas": "region vi - western visayas",
    "region vii - central visayas": "region vii - central visayas",
    "region viii - eastern visayas": "region viii - eastern visayas",
    "region ix - zamboanga peninsula": "region ix - zamboanga peninsula",
    "region x - northern mindanao": "region x - northern mindanao",
    "region xi - davao": "region xi - davao",
    "region xii - soccsksargen": "region xii - soccsksargen",
    "region xiii - caraga": "region xiii - caraga",
    "barmm": "barmm",
    "car": "car",
    "calabarzon": "region iv-a - calabarzon",
    "region 4a": "region iv-a - calabarzon",
    "region 4a - calabarzon": "region iv-a - calabarzon",
    "region iv-a": "region iv-a - calabarzon",
    "central luzon": "region iii - central luzon",
    "ilocos": "region i - ilocos",
    "ilocos region": "region i - ilocos",
    "bicol": "region v - bicol",
    "bicol region": "region v - bicol",
    "cordillera": "car",
    "mimaropa": "region iv-b - mimaropa",
    "cagayan valley": "region ii - cagayan valley",
    "luzon": "luzon",
    "western visayas": "region vi - western visayas",
    "central visayas": "region vii - central visayas",
    "eastern visayas": "region viii - eastern visayas",
    "visayas": "visayas",
    "region vi": "region vi - western visayas",
    "region vii": "region vii - central visayas",
    "region viii": "region viii - eastern visayas",
    "zamboanga": "region ix - zamboanga peninsula",
    "zamboanga peninsula": "region ix - zamboanga peninsula",
    "northern mindanao": "region x - northern mindanao",
    "davao region": "region xi - davao",
    "davao": "region xi - davao",
    "region xi": "region xi - davao",
    "soccsksargen": "region xii - soccsksargen",
    "caraga": "region xiii - caraga",
    "bangsamoro": "barmm",
    "mindanao": "mindanao",
}


# Canonical Philippine regions (17 regions)
PHILIPPINE_REGIONS = [
    "NCR",
    "CAR",
    "Region I - Ilocos",
    "Region II - Cagayan Valley",
    "Region III - Central Luzon",
    "Region IV-A - Calabarzon",
    "Region IV-B - Mimaropa",
    "Region V - Bicol",
    "Region VI - Western Visayas",
    "Region VII - Central Visayas",
    "Region VIII - Eastern Visayas",
    "Region IX - Zamboanga Peninsula",
    "Region X - Northern Mindanao",
    "Region XI - Davao",
    "Region XII - Soccsksargen",
    "Region XIII - Caraga",
    "BARMM",
]

# Island groups for coarse matching
ISLAND_GROUPS = {
    "metro manila": "luzon",
    "luzon": "luzon",
    "visayas": "visayas",
    "mindanao": "mindanao",
}


def normalize_region(region: str | None) -> str:
    """Normalize region for matching (e.g. NCR, Metro Manila -> ``ncr``)."""
    if not region or not str(region).strip():
        return ""
    key = str(region).strip().lower()
    return REGION_ALIASES.get(key, key)


# Preferred storage labels keyed by normalized region token.
_CANONICAL_REGION_LABELS: dict[str, str] = {
    normalize_region(r): r for r in PHILIPPINE_REGIONS
}
_CANONICAL_REGION_LABELS["ncr"] = "NCR"
_CANONICAL_REGION_LABELS["luzon"] = "Luzon"
_CANONICAL_REGION_LABELS["visayas"] = "Visayas"
_CANONICAL_REGION_LABELS["mindanao"] = "Mindanao"


def canonical_region_label(region: str | None) -> str:
    """Return preferred catalog label for a region (e.g. Metro Manila -> NCR)."""
    if not region or not str(region).strip():
        return ""
    norm = normalize_region(region)
    return _CANONICAL_REGION_LABELS.get(norm, str(region).strip())


def region_search_literals(region: str) -> list[str]:
    """All stored labels that should match a browse filter for ``region``."""
    val = (region or "").strip()
    if not val:
        return []
    norm = normalize_region(val)
    literals: set[str] = {val}
    if norm:
        literals.add(canonical_region_label(val))
        for alias, key in REGION_ALIASES.items():
            if key == norm:
                literals.add(alias.title() if alias.islower() else alias)
                # preserve common uppercase forms
                if alias == "metro manila":
                    literals.add("Metro Manila")
                if alias == "national capital region":
                    literals.add("National Capital Region")
        for r in PHILIPPINE_REGIONS:
            if normalize_region(r) == norm:
                literals.add(r)
    return sorted(x for x in literals if x)
