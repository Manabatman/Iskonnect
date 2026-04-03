"""
GWA (General Weighted Average) normalization utility.
Converts Philippine grading scales to 0-100 percentage for uniform comparison.
Does NOT define scoring math - only normalization.
"""

GWA_SCALE_5_0 = "5.0_scale"  # 1.00 highest, 3.00 passing (SUCs, UP, PUP)
GWA_SCALE_4_0 = "4.0_scale"  # 4.00 highest, 1.00 passing (DLSU, Ateneo, UST)
GWA_SCALE_PERCENTAGE = "percentage"  # 100 highest, 75 passing (K-12, many foundations)


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


def normalize_gwa(
    gwa_raw: str | float | int | None,
    scale: str | None = None,
) -> float | None:
    """
    Convert GWA to 0-100 normalized percentage.
    Returns None if input is invalid.

    Scale mapping (linear; used consistently for matching vs min_gwa_normalized):
    - 5.0_scale: 1.00 = 100%, 2.00 = 75%, 3.00 = 50%, 4.00 = 25%, 5.00 = 0%
      (values below 1.0 map to 100%; above 5.0 to 0%)
    - 4.0_scale: 0.00 = 0%, 1.00 = 25%, 2.00 = 50%, 3.00 = 75%, 4.00 = 100%
    - percentage: pass-through clamped to [0, 100]
    """
    val = _parse_numeric(gwa_raw)
    if val is None:
        return None

    scale_key = (scale or "").strip().lower()

    if scale_key in ("percentage", "percent", "pct", ""):
        # Assume already percentage
        return max(0.0, min(100.0, val))

    if scale_key in ("5.0_scale", "5.0", "1.0_scale"):
        # Linear from 1 (best) to 5 (worst): pct = 100 - (val - 1) * 25
        if val < 1.0:
            return 100.0
        if val > 5.0:
            return 0.0
        return 100.0 - (val - 1.0) * 25.0  # 1->100, 2->75, 3->50, 4->25, 5->0

    if scale_key in ("4.0_scale", "4.0"):
        # Linear from 0 to 4: pct = (val / 4) * 100
        if val >= 4.0:
            return 100.0
        if val <= 0.0:
            return 0.0
        return (val / 4.0) * 100.0

    # Default: treat as percentage
    return max(0.0, min(100.0, val))
