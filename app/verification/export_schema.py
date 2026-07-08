"""Field list and serialization for external verification exports."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from app.serialization.scholarship import scholarship_to_catalog_dict
from app.utils.json_helpers import parse_json

# Columns written to CSV/JSON for ChatGPT verification (ordered).
VERIFICATION_EXPORT_COLUMNS: tuple[str, ...] = (
    "id",
    "verification_bundle",
    "verification_priority",
    "title",
    "provider",
    "provider_type",
    "scholarship_type",
    "primary_link",
    "link_status",
    "data_status",
    "description",
    "eligible_levels",
    "eligible_regions",
    "eligible_cities",
    "residency_required",
    "eligible_school_types",
    "eligible_courses_psced",
    "eligible_courses_specific",
    "citizenship_required",
    "max_income_threshold",
    "min_gwa_normalized",
    "min_age",
    "max_age",
    "priority_groups",
    "members_only",
    "benefit_tuition",
    "benefit_allowance_monthly",
    "benefit_books",
    "benefit_miscellaneous",
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
    "application_status",
    "last_verified_at",
    "verification_source",
    "is_active",
)

_LIST_FIELDS = frozenset(
    {
        "eligible_levels",
        "eligible_regions",
        "eligible_cities",
        "eligible_school_types",
        "eligible_courses_psced",
        "eligible_courses_specific",
        "priority_groups",
        "required_documents",
    }
)

_BOOL_FIELDS = frozenset(
    {
        "residency_required",
        "members_only",
        "benefit_tuition",
        "benefit_books",
        "has_qualifying_exam",
        "has_interview",
        "has_essay_requirement",
        "has_return_service",
        "is_active",
    }
)

_DATE_FIELDS = frozenset(
    {
        "application_open_date",
        "application_deadline",
        "last_open_date",
        "last_close_date",
    }
)


def _format_date(val: Any) -> str | None:
    if val is None:
        return None
    if isinstance(val, datetime):
        return val.date().isoformat()
    if isinstance(val, date):
        return val.isoformat()
    if isinstance(val, str) and val.strip():
        return val.strip()[:10]
    return None


def _format_datetime(val: Any) -> str | None:
    if val is None:
        return None
    if isinstance(val, datetime):
        return val.isoformat(sep=" ", timespec="seconds")
    if isinstance(val, str) and val.strip():
        return val.strip()
    return None


def _list_to_pipe(val: Any) -> str:
    if val is None:
        return ""
    if isinstance(val, list):
        return "|".join(str(x).strip() for x in val if x is not None and str(x).strip())
    parsed = parse_json(val, default=[])
    if isinstance(parsed, list):
        return "|".join(str(x).strip() for x in parsed if x is not None and str(x).strip())
    return str(val)


def _bool_str(val: Any) -> str:
    if val is None:
        return ""
    return "true" if bool(val) else "false"


def compute_verification_priority(row: dict[str, Any]) -> str:
    link_status = (row.get("link_status") or "").strip().lower()
    data_status = (row.get("data_status") or "").strip().lower()
    if link_status == "broken" or data_status in ("broken_link", "needs_review"):
        return "high"
    return "normal"


def row_to_verification_export(
    row: Any,
    *,
    verification_bundle: str,
) -> dict[str, Any]:
    """Build one verification export record from an ORM Scholarship row."""
    catalog = scholarship_to_catalog_dict(row)
    out: dict[str, Any] = {
        "id": catalog.get("id"),
        "verification_bundle": verification_bundle,
        "title": catalog.get("title"),
        "provider": catalog.get("provider"),
        "provider_type": catalog.get("provider_type"),
        "scholarship_type": catalog.get("scholarship_type"),
        "primary_link": catalog.get("link"),
        "link_status": catalog.get("link_status"),
        "data_status": catalog.get("data_status"),
        "description": catalog.get("description"),
        "eligible_levels": parse_json(catalog.get("eligible_levels"), default=[]),
        "eligible_regions": parse_json(catalog.get("eligible_regions"), default=[]),
        "eligible_cities": parse_json(catalog.get("eligible_cities"), default=[]),
        "residency_required": catalog.get("residency_required"),
        "eligible_school_types": parse_json(catalog.get("eligible_school_types"), default=[]),
        "eligible_courses_psced": parse_json(catalog.get("eligible_courses_psced"), default=[]),
        "eligible_courses_specific": parse_json(catalog.get("eligible_courses_specific"), default=[]),
        "citizenship_required": catalog.get("citizenship_required"),
        "max_income_threshold": catalog.get("max_income_threshold"),
        "min_gwa_normalized": catalog.get("min_gwa_normalized"),
        "min_age": catalog.get("min_age"),
        "max_age": catalog.get("max_age"),
        "priority_groups": parse_json(catalog.get("priority_groups"), default=[]),
        "members_only": catalog.get("members_only"),
        "benefit_tuition": catalog.get("benefit_tuition"),
        "benefit_allowance_monthly": catalog.get("benefit_allowance_monthly"),
        "benefit_books": catalog.get("benefit_books"),
        "benefit_miscellaneous": catalog.get("benefit_miscellaneous"),
        "benefit_total_value": catalog.get("benefit_total_value"),
        "required_documents": parse_json(catalog.get("required_documents"), default=[]),
        "has_qualifying_exam": catalog.get("has_qualifying_exam"),
        "has_interview": catalog.get("has_interview"),
        "has_essay_requirement": catalog.get("has_essay_requirement"),
        "has_return_service": catalog.get("has_return_service"),
        "application_open_date": catalog.get("application_open_date"),
        "application_deadline": catalog.get("application_deadline"),
        "academic_year_target": catalog.get("academic_year_target"),
        "cycle_type": catalog.get("cycle_type"),
        "last_open_date": catalog.get("last_open_date"),
        "last_close_date": catalog.get("last_close_date"),
        "application_status": catalog.get("application_status"),
        "last_verified_at": catalog.get("last_verified_at"),
        "verification_source": catalog.get("verification_source"),
        "is_active": catalog.get("is_active"),
    }
    out["verification_priority"] = compute_verification_priority(out)
    return out


def verification_record_to_csv_row(record: dict[str, Any]) -> dict[str, str]:
    """Flatten export record for CSV writing."""
    row: dict[str, str] = {}
    for col in VERIFICATION_EXPORT_COLUMNS:
        val = record.get(col)
        if col in _LIST_FIELDS:
            row[col] = _list_to_pipe(val)
        elif col in _BOOL_FIELDS:
            row[col] = _bool_str(val)
        elif col in _DATE_FIELDS:
            row[col] = _format_date(val) or ""
        elif col == "last_verified_at":
            row[col] = _format_datetime(val) or ""
        elif val is None:
            row[col] = ""
        else:
            row[col] = str(val)
    return row
