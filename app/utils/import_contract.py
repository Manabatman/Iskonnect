"""Canonical CSV import contract for scholarship staging imports."""

from __future__ import annotations

from app import schemas

# Schema-importable columns used by the Gemini → Cursor CSV workflow (ordered).
CANONICAL_SCHEMA_COLUMNS: tuple[str, ...] = (
    "title",
    "provider",
    "source",
    "link",
    "description",
    "provider_type",
    "scholarship_type",
    "eligible_levels",
    "eligible_regions",
    "eligible_cities",
    "residency_required",
    "eligible_school_types",
    "eligible_courses_psced",
    "eligible_courses_specific",
    "max_income_threshold",
    "min_gwa_normalized",
    "min_age",
    "max_age",
    "priority_groups",
    "members_only",
    "benefit_tuition",
    "benefit_allowance_monthly",
    "benefit_books",
    "benefit_total_value",
    "required_documents",
    "has_qualifying_exam",
    "has_interview",
    "has_essay_requirement",
    "has_return_service",
    "application_open_date",
    "application_deadline",
    "academic_year_target",
    "cycle_type",
    "last_open_date",
    "last_close_date",
    "is_active",
)

KNOWN_METADATA_COLUMNS: tuple[str, ...] = (
    "source_slug",
    "research_notes",
    "source_urls",
    "dedupe_rationale",
)

CANONICAL_IMPORT_COLUMNS: tuple[str, ...] = CANONICAL_SCHEMA_COLUMNS + KNOWN_METADATA_COLUMNS

KNOWN_COLUMNS: frozenset[str] = frozenset(CANONICAL_IMPORT_COLUMNS)

REQUIRED_COLUMNS: frozenset[str] = frozenset({"title"})

RECOMMENDED_COLUMNS: frozenset[str] = frozenset(
    {"provider", "link", "scholarship_type", "provider_type", "eligible_levels"}
)

# Fail fast at import if contract columns are not defined on the Pydantic schema.
_missing_schema = [c for c in CANONICAL_SCHEMA_COLUMNS if c not in schemas.Scholarship.model_fields]
if _missing_schema:
    raise RuntimeError(
        f"Import contract columns missing from schemas.Scholarship: {_missing_schema}"
    )


def normalize_header(name: str) -> str:
    """Normalize a CSV header to a canonical column key (mirrors load_csv)."""
    key = (name or "").strip().lower().replace(" ", "_")
    if key == "url":
        return "link"
    return key


def validate_header(fieldnames: list[str]) -> dict[str, list[str]]:
    """
    Validate normalized CSV headers against the import contract.

    Returns:
        unknown: headers not in KNOWN_COLUMNS
        missing_required: REQUIRED_COLUMNS absent from header
        missing_recommended: RECOMMENDED_COLUMNS absent from header
        duplicate: normalized keys that appear more than once
    """
    normalized = [normalize_header(fn) for fn in fieldnames]
    seen: dict[str, int] = {}
    for key in normalized:
        seen[key] = seen.get(key, 0) + 1
    duplicate = sorted(k for k, count in seen.items() if count > 1)
    present = set(normalized)
    return {
        "unknown": sorted(k for k in normalized if k not in KNOWN_COLUMNS),
        "missing_required": sorted(REQUIRED_COLUMNS - present),
        "missing_recommended": sorted(RECOMMENDED_COLUMNS - present),
        "duplicate": duplicate,
    }
