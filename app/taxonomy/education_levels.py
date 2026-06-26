"""
Education level normalization for scholarship matching.

Maps profile and scholarship level labels (including Senior High synonyms) to
canonical buckets so hard filters and SQL prefilters stay aligned.
"""

from __future__ import annotations

SENIOR_HIGH_BUCKET = "senior_high"
COLLEGE_BUCKET = "college"
TVET_BUCKET = "tvet"
GRADUATE_BUCKET = "graduate"

SENIOR_HIGH_VARIANTS: frozenset[str] = frozenset({
    "senior high",
    "senior high school",
    "high school",
    "grade 11",
    "grade 12",
})

COLLEGE_VARIANTS: frozenset[str] = frozenset({
    "college",
    "college 1st year",
    "college 2nd year",
    "college 3rd year",
    "college 4th year",
})

TVET_VARIANTS: frozenset[str] = frozenset({
    "tvet",
    "vocational",
})

GRADUATE_VARIANTS: frozenset[str] = frozenset({
    "graduate",
    "master's",
    "masters",
    "phd",
    "doctoral",
})

LEVEL_BUCKETS: dict[str, frozenset[str]] = {
    SENIOR_HIGH_BUCKET: SENIOR_HIGH_VARIANTS,
    COLLEGE_BUCKET: COLLEGE_VARIANTS,
    TVET_BUCKET: TVET_VARIANTS,
    GRADUATE_BUCKET: GRADUATE_VARIANTS,
}

# flat lookup: label -> bucket key
_LABEL_TO_BUCKET: dict[str, str] = {}
for _bucket, _variants in LEVEL_BUCKETS.items():
    for _v in _variants:
        _LABEL_TO_BUCKET[_v] = _bucket


def normalize_education_level(level: str | None) -> str | None:
    """Return canonical bucket key (e.g. senior_high) or None if unknown."""
    if not level or not str(level).strip():
        return None
    return _LABEL_TO_BUCKET.get(str(level).strip().lower())


def education_levels_compatible(profile_level: str, scholarship_level: str) -> bool:
    """True when profile and scholarship education labels refer to the same bucket."""
    p = str(profile_level).strip().lower()
    s = str(scholarship_level).strip().lower()
    if p == s:
        return True
    pb = normalize_education_level(p)
    sb = normalize_education_level(s)
    if pb and sb:
        return pb == sb
    return False


def level_search_literals(profile_level: str) -> list[str]:
    """
    All level strings to search in eligible_levels JSON for SQL ILIKE prefilter.
    Includes the profile's literal label and every synonym in its bucket.
    """
    raw = str(profile_level).strip()
    if not raw:
        return []
    literals = {raw}
    bucket = normalize_education_level(raw)
    if bucket and bucket in LEVEL_BUCKETS:
        literals.update(LEVEL_BUCKETS[bucket])
    return sorted(literals)
