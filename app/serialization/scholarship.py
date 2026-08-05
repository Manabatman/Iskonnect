"""
Canonical scholarship serialization for API, matching, and cache layers.

All endpoints that return scholarship data for cards or detail views should use
these helpers so image_url and related display fields cannot drift.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Mapping

from app.utils.application_status import compute_application_status
from app.utils.json_helpers import parse_json
# provider_logo reserved for future column; always None until modeled.
SCHOLARSHIP_CARD_DISPLAY_KEYS: tuple[str, ...] = (
    "id",
    "title",
    "provider",
    "link",
    "description",
    "image_url",
    "image_alt",
    "provider_logo",
    "regions",
    "min_age",
    "max_age",
    "level",
    "provider_type",
    "scholarship_type",
    "needs_tags",
    "benefit_tuition",
    "benefit_allowance_monthly",
    "benefit_books",
    "benefit_total_value",
    "application_deadline",
    "application_open_date",
    "required_documents",
    "data_status",
    "application_status",
    "verification_source",
    "link_status",
)

# Extra catalog fields for matching / admin (not always on match rows).
SCHOLARSHIP_CATALOG_EXTRA_KEYS: tuple[str, ...] = (
    "source",
    "countries",
    "eligible_levels",
    "eligible_regions",
    "eligible_cities",
    "residency_required",
    "eligible_school_types",
    "eligible_schools",
    "eligible_school_systems",
    "eligible_school_categories",
    "eligible_year_levels",
    "eligible_enrollment_status",
    "eligible_courses_psced",
    "eligible_courses_specific",
    "preferred_extracurriculars",
    "preferred_awards",
    "max_income_threshold",
    "min_gwa_normalized",
    "priority_groups",
    "members_only",
    "has_qualifying_exam",
    "has_interview",
    "has_essay_requirement",
    "has_return_service",
    "academic_year_target",
    "is_active",
    "last_verified_at",
    "confidence_score",
    "link_last_checked_at",
    "link_failure_count",
    "last_open_date",
    "last_close_date",
    "cycle_type",
    "deadline_precision",
    "deadline_note",
    "deadline_source_url",
    "citizenship_required",
    "next_review_date",
    "opportunity_type",
    "type_attributes",
    "organization_id",
    "editorial_state",
    "max_prior_tertiary_units",
    "min_work_experience_years",
    "max_class_rank",
    "max_class_percentile",
    "academic_gate_mode",
    "allow_transferee",
    "allow_shiftee",
    "first_undergraduate_only",
    "min_residency_years",
    "age_as_of_date",
    "age_as_of_rule",
    "max_parent_salary_grade",
    "parent_program_id",
    "required_affiliation_codes",
    "conflict_scope_codes",
)

MATCH_SCORING_KEYS: tuple[str, ...] = (
    "score",
    "final_score",
    "eligibility_status",
    "deadline_passed",
    "readiness_score",
    "explanation",
    "breakdown",
    "confidence",
    "suggestions",
    "why_not_higher",
    "scoring_policy_version",
    "qualification_status",
    "qualifying_requirements",
    "missing_requirements",
    "eligibility_confidence",
    "requirements",
    "unverified_requirements",
    "provisional_reason",
)

MATCH_MINIMAL_EXTRA_KEYS: tuple[str, ...] = (
    "score",
    "final_score",
    "eligibility_status",
    "confidence",
    "application_deadline",
)


def _get_attr(row: Any, name: str, default: Any = None) -> Any:
    if isinstance(row, Mapping):
        return row.get(name, default)
    return getattr(row, name, default)


def format_field_value(val: Any, *, dates_as_iso: bool) -> Any:
    """Normalize date/datetime fields for JSON or Pydantic responses."""
    if val is None:
        return None
    if dates_as_iso and isinstance(val, (date, datetime)):
        return val.isoformat()
    return val


def _resolved_regions(row: Any) -> list:
    regions = parse_json(_get_attr(row, "regions"))
    if not regions and _get_attr(row, "eligible_regions"):
        regions = parse_json(_get_attr(row, "eligible_regions"))
    return regions or []


def _resolve_provider_display(row: Any) -> str | None:
    """Canonical provider label from linked organization when available."""
    org = _get_attr(row, "organization")
    if org is not None:
        return getattr(org, "canonical_name", None) or _get_attr(row, "provider")
    display = _get_attr(row, "provider_display") or _get_attr(row, "provider_canonical_name")
    if display:
        return display
    return _get_attr(row, "provider")


def _resolve_provider_logo(row: Any) -> str | None:
    """Wire provider_logo from organization.logo_url when linked."""
    explicit = _get_attr(row, "provider_logo")
    if explicit:
        return explicit
    org = _get_attr(row, "organization")
    if org is not None:
        return getattr(org, "logo_url", None)
    return None


def scholarship_row_to_payload(row: Any, *, dates_as_iso: bool = False) -> dict[str, Any]:
    """Full scholarship dict from an ORM row or catalog/match dict."""
    ad = _get_attr(row, "application_deadline")
    aod = _get_attr(row, "application_open_date")
    lod = _get_attr(row, "last_open_date")
    lcd = _get_attr(row, "last_close_date")
    lva = _get_attr(row, "last_verified_at")
    llc = _get_attr(row, "link_last_checked_at")
    attrs_raw = parse_json(_get_attr(row, "type_attributes"))
    type_attributes = attrs_raw if isinstance(attrs_raw, dict) else None

    return {
        "id": _get_attr(row, "id"),
        "title": _get_attr(row, "title"),
        "provider": _get_attr(row, "provider"),
        "provider_display": _resolve_provider_display(row),
        "source": _get_attr(row, "source"),
        "countries": parse_json(_get_attr(row, "countries")),
        "regions": _resolved_regions(row),
        "min_age": _get_attr(row, "min_age"),
        "max_age": _get_attr(row, "max_age"),
        "needs_tags": parse_json(_get_attr(row, "needs_tags")),
        "level": _get_attr(row, "level"),
        "link": _get_attr(row, "link"),
        "description": _get_attr(row, "description"),
        "image_url": _get_attr(row, "image_url"),
        "image_alt": _get_attr(row, "image_alt"),
        "provider_logo": _resolve_provider_logo(row),
        "provider_type": _get_attr(row, "provider_type"),
        "scholarship_type": _get_attr(row, "scholarship_type"),
        "eligible_levels": parse_json(_get_attr(row, "eligible_levels")),
        "eligible_regions": parse_json(_get_attr(row, "eligible_regions")),
        "eligible_cities": parse_json(_get_attr(row, "eligible_cities")),
        "residency_required": bool(_get_attr(row, "residency_required", False)),
        "eligible_school_types": parse_json(_get_attr(row, "eligible_school_types")),
        "eligible_schools": parse_json(_get_attr(row, "eligible_schools")),
        "eligible_school_systems": parse_json(_get_attr(row, "eligible_school_systems")),
        "eligible_school_categories": parse_json(_get_attr(row, "eligible_school_categories")),
        "eligible_year_levels": parse_json(_get_attr(row, "eligible_year_levels")),
        "eligible_enrollment_status": parse_json(_get_attr(row, "eligible_enrollment_status")),
        "citizenship_required": _get_attr(row, "citizenship_required"),
        "eligible_courses_psced": parse_json(_get_attr(row, "eligible_courses_psced")),
        "eligible_courses_specific": parse_json(_get_attr(row, "eligible_courses_specific")),
        "preferred_extracurriculars": parse_json(_get_attr(row, "preferred_extracurriculars")),
        "preferred_awards": parse_json(_get_attr(row, "preferred_awards")),
        "max_income_threshold": _get_attr(row, "max_income_threshold"),
        "min_gwa_normalized": _get_attr(row, "min_gwa_normalized"),
        "priority_groups": parse_json(_get_attr(row, "priority_groups")),
        "members_only": bool(_get_attr(row, "members_only", False)),
        "benefit_tuition": bool(_get_attr(row, "benefit_tuition", False)),
        "benefit_allowance_monthly": _get_attr(row, "benefit_allowance_monthly"),
        "benefit_books": bool(_get_attr(row, "benefit_books", False)),
        "benefit_total_value": _get_attr(row, "benefit_total_value"),
        "required_documents": parse_json(_get_attr(row, "required_documents")),
        "has_qualifying_exam": bool(_get_attr(row, "has_qualifying_exam", False)),
        "has_interview": bool(_get_attr(row, "has_interview", False)),
        "has_essay_requirement": bool(_get_attr(row, "has_essay_requirement", False)),
        "has_return_service": bool(_get_attr(row, "has_return_service", False)),
        "application_deadline": format_field_value(ad, dates_as_iso=dates_as_iso),
        "deadline_precision": _get_attr(row, "deadline_precision"),
        "deadline_note": _get_attr(row, "deadline_note"),
        "deadline_source_url": _get_attr(row, "deadline_source_url"),
        "application_open_date": format_field_value(aod, dates_as_iso=dates_as_iso),
        "academic_year_target": _get_attr(row, "academic_year_target"),
        "is_active": _get_attr(row, "is_active", True),
        "last_verified_at": format_field_value(lva, dates_as_iso=dates_as_iso),
        "verification_source": _get_attr(row, "verification_source"),
        "data_completeness_score": _get_attr(row, "data_completeness_score"),
        "confidence_score": _get_attr(row, "confidence_score"),
        "data_status": _get_attr(row, "data_status"),
        "application_status": _get_attr(row, "application_status")
        or compute_application_status(row),
        "link_status": _get_attr(row, "link_status"),
        "link_last_checked_at": format_field_value(llc, dates_as_iso=dates_as_iso),
        "link_failure_count": _get_attr(row, "link_failure_count"),
        "last_open_date": format_field_value(lod, dates_as_iso=dates_as_iso),
        "last_close_date": format_field_value(lcd, dates_as_iso=dates_as_iso),
        "cycle_type": _get_attr(row, "cycle_type"),
        "next_review_date": format_field_value(_get_attr(row, "next_review_date"), dates_as_iso=dates_as_iso),
        "opportunity_type": _get_attr(row, "opportunity_type") or "scholarship",
        "type_attributes": type_attributes,
        "organization_id": _get_attr(row, "organization_id"),
        "editorial_state": _get_attr(row, "editorial_state"),
        "max_prior_tertiary_units": _get_attr(row, "max_prior_tertiary_units"),
        "min_work_experience_years": _get_attr(row, "min_work_experience_years"),
        "max_class_rank": _get_attr(row, "max_class_rank"),
        "max_class_percentile": _get_attr(row, "max_class_percentile"),
        "academic_gate_mode": _get_attr(row, "academic_gate_mode"),
        "allow_transferee": _get_attr(row, "allow_transferee"),
        "allow_shiftee": _get_attr(row, "allow_shiftee"),
        "first_undergraduate_only": bool(_get_attr(row, "first_undergraduate_only", False)),
        "min_residency_years": _get_attr(row, "min_residency_years"),
        "age_as_of_date": format_field_value(_get_attr(row, "age_as_of_date"), dates_as_iso=dates_as_iso),
        "age_as_of_rule": _get_attr(row, "age_as_of_rule"),
        "max_parent_salary_grade": _get_attr(row, "max_parent_salary_grade"),
        "parent_program_id": _get_attr(row, "parent_program_id"),
        "required_affiliation_codes": _get_attr(row, "required_affiliation_codes"),
        "conflict_scope_codes": _get_attr(row, "conflict_scope_codes"),
    }


def scholarship_to_api_payload(row: Any) -> dict[str, Any]:
    """API responses (ScholarshipResponse) — dates as date objects for Pydantic."""
    return scholarship_row_to_payload(row, dates_as_iso=False)


def scholarship_to_catalog_dict(row: Any) -> dict[str, Any]:
    """Matching cache / JSON-safe catalog entries — dates as ISO strings."""
    return scholarship_row_to_payload(row, dates_as_iso=True)


def scholarship_card_fields(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Subset required for scholarship cards; missing keys default to None/false."""
    out: dict[str, Any] = {}
    for key in SCHOLARSHIP_CARD_DISPLAY_KEYS:
        if key == "provider_logo":
            out[key] = payload.get("provider_logo")
            continue
        if key in (
            "benefit_tuition",
            "benefit_books",
        ):
            out[key] = bool(payload.get(key, False))
            continue
        if key in ("regions", "needs_tags", "required_documents"):
            val = payload.get(key)
            out[key] = val if isinstance(val, list) else parse_json(val) or []
            continue
        out[key] = payload.get(key)
    return out


def missing_card_display_keys(payload: Mapping[str, Any]) -> list[str]:
    """Return card display keys absent from payload (for regression tests)."""
    return [k for k in SCHOLARSHIP_CARD_DISPLAY_KEYS if k not in payload]


def build_match_result_payload(
    scholarship: Mapping[str, Any],
    *,
    scoring: Mapping[str, Any],
) -> dict[str, Any]:
    """Merge catalog scholarship display fields with live or stored match scoring."""
    base = scholarship_card_fields(scholarship)
    for key in MATCH_SCORING_KEYS:
        if key in scoring:
            base[key] = scoring[key]
    return base


def build_stored_match_scoring(
    match_result_row: Any,
    *,
    explanation: list | None = None,
    breakdown: dict | None = None,
    suggestions: list | None = None,
    why_not_higher: list | None = None,
) -> dict[str, Any]:
    """Scoring slice from a persisted MatchResult ORM row."""
    score = (
        match_result_row.final_score
        if match_result_row.final_score is not None
        else match_result_row.score
    )
    return {
        "score": score,
        "final_score": score,
        "explanation": explanation or [],
        "breakdown": breakdown,
        "confidence": match_result_row.confidence,
        "suggestions": suggestions or [],
        "why_not_higher": why_not_higher or [],
        "scoring_policy_version": match_result_row.scoring_policy_version,
        "eligibility_status": getattr(match_result_row, "eligibility_status", None),
    }


def build_upcoming_scholarship_payload(scholarship: Mapping[str, Any], *, cycle: Mapping[str, Any]) -> dict[str, Any]:
    """Upcoming (cycle prediction) row with card display fields."""
    card = scholarship_card_fields(scholarship)
    card.update(
        {
            "cycle_type": cycle.get("cycle_type"),
            "last_open_date": cycle.get("last_open_date"),
            "last_close_date": cycle.get("last_close_date"),
            "predicted_next_open": cycle.get("predicted_next_open"),
        }
    )
    return card
