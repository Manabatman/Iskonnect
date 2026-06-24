"""
GWA (General Weighted Average) normalization utility.

Converts Philippine grading scales to a 0–100 percentage baseline for uniform
comparison across institutions. Does not define scoring math — normalization only.
"""

GWA_SCALE_5_0 = "5.0_scale"  # 1.00 highest, 3.00 passing (SUCs, UP, PUP)
GWA_SCALE_4_0 = "4.0_scale"  # 4.00 highest, 1.00 passing (DLSU, Ateneo, UST)
GWA_SCALE_PERCENTAGE = "percentage"  # 100 highest, 75 passing (K-12, many foundations)

GWA_SCALE_ALIASES: dict[str, str] = {
    "numeric_1_to_5": GWA_SCALE_5_0,
    "numeric_4_scale": GWA_SCALE_4_0,
    "percentage_75_to_100": GWA_SCALE_PERCENTAGE,
    "1.0_scale": GWA_SCALE_5_0,
    "5.0": GWA_SCALE_5_0,
    "4.0": GWA_SCALE_4_0,
    "percent": GWA_SCALE_PERCENTAGE,
    "pct": GWA_SCALE_PERCENTAGE,
}


def resolve_gwa_scale(scale: str | None) -> str | None:
    """Map client scale identifiers to canonical scale keys."""
    if scale is None:
        return None
    key = str(scale).strip().lower()
    if not key:
        return None
    if key in GWA_SCALE_ALIASES:
        return GWA_SCALE_ALIASES[key]
    if key in (GWA_SCALE_5_0, GWA_SCALE_4_0, GWA_SCALE_PERCENTAGE):
        return key
    return None


def _parse_numeric(value: str | float | int) -> float | None:
    """Parse input to float, handling commas and whitespace."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip().replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def _is_ambiguous_without_scale(val: float) -> bool:
    """Values in (1, 5) could be 5.0-scale grades misread as percentages."""
    return 1.0 < val < 5.0


def normalize_gwa(
    gwa_raw: str | float | int | None,
    scale: str | None = None,
) -> float | None:
    """Convert GWA to 0–100 normalized percentage.

    Returns ``None`` when input is invalid or when the scale is unknown and the
    numeric value is ambiguous (would silently mis-score as a percentage).

    Scale mapping (linear; used consistently for matching vs min_gwa_normalized):
    - ``5.0_scale``: 1.00 = 100%, 2.00 = 75%, 3.00 = 50%, 4.00 = 25%, 5.00 = 0%
    - ``4.0_scale``: 0.00 = 0%, 4.00 = 100%
    - ``percentage``: pass-through clamped to [0, 100]
    """
    val = _parse_numeric(gwa_raw)
    if val is None:
        return None

    scale_key = resolve_gwa_scale(scale)
    if scale_key is None and scale not in (None, ""):
        # Explicit but unrecognized scale — fail soft rather than assume percentage.
        if _is_ambiguous_without_scale(val):
            return None
        return max(0.0, min(100.0, val))

    if scale_key is None or scale_key == GWA_SCALE_PERCENTAGE:
        return max(0.0, min(100.0, val))

    if scale_key == GWA_SCALE_5_0:
        if val < 1.0:
            return 100.0
        if val > 5.0:
            return 0.0
        return 100.0 - (val - 1.0) * 25.0

    if scale_key == GWA_SCALE_4_0:
        if val >= 4.0:
            return 100.0
        if val <= 0.0:
            return 0.0
        return (val / 4.0) * 100.0

    return None
