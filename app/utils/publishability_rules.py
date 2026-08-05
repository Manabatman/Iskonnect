"""
SPEC-13 — Publishability rule validation for scholarship catalog rows.

Rejects publish when structured rule data is incomplete or inconsistent.
"""

from __future__ import annotations

from typing import Any

from app.config import settings
from app.utils.json_helpers import parse_json_list


def _get(row: Any, key: str, default=None):
    if isinstance(row, dict):
        return row.get(key, default)
    return getattr(row, key, default)


def _academic_predicate_count(row: Any) -> int:
    count = 0
    if _get(row, "min_gwa_normalized") is not None:
        count += 1
    if _get(row, "max_class_rank") is not None:
        count += 1
    if _get(row, "max_class_percentile") is not None:
        count += 1
    return count


def _has_consortium_lock(row: Any) -> bool:
    title = (_get(row, "title") or "").lower()
    desc = (_get(row, "description") or "").lower()
    markers = ("consortium", "erdt", "asthrdp", "cbpsme", "partner school", "partner universities")
    if any(m in title or m in desc for m in markers):
        return True
    systems = parse_json_list(_get(row, "eligible_school_systems"))
    return bool(systems)


def validate_scholarship_publish_rules(
    row: Any,
    *,
    required_affiliation_codes: list[str] | None = None,
    conflict_scope_codes: list[str] | None = None,
) -> list[str]:
    """
    Return human-readable validation errors. Empty list means rule data is publishable.
    """
    if not settings.publishability_rule_validation:
        return []

    errors: list[str] = []
    sid = _get(row, "id")

    mode = (_get(row, "academic_gate_mode") or "").strip().lower()
    if mode and mode not in ("and", "or"):
        errors.append(f"scholarship {sid}: academic_gate_mode must be 'and' or 'or'")
    if mode == "or" and _academic_predicate_count(row) < 2:
        errors.append(
            f"scholarship {sid}: academic_gate_mode='or' requires at least two academic predicates "
            "(min_gwa_normalized, max_class_rank, max_class_percentile)"
        )

    max_units = _get(row, "max_prior_tertiary_units")
    enrollment = parse_json_list(_get(row, "eligible_enrollment_status"))
    if max_units == 0 and "incoming_freshman" not in enrollment:
        errors.append(
            f"scholarship {sid}: zero-unit programs should include incoming_freshman in eligible_enrollment_status"
        )

    schools = parse_json_list(_get(row, "eligible_schools"))
    if _has_consortium_lock(row) and not schools:
        errors.append(f"scholarship {sid}: consortium/partner program requires non-empty eligible_schools")

    aff_codes = required_affiliation_codes if required_affiliation_codes is not None else _get(
        row, "required_affiliation_codes"
    )
    if aff_codes is not None and len(aff_codes) == 0 and _get(row, "members_only"):
        errors.append(
            f"scholarship {sid}: members_only scholarships with registry gates need required_affiliation_codes"
        )

    scope_codes = conflict_scope_codes if conflict_scope_codes is not None else _get(row, "conflict_scope_codes")
    if scope_codes is not None and len(scope_codes) == 0:
        errors.append(f"scholarship {sid}: conflict-scoped scholarship must have at least one conflict scope")

    age_rule = (_get(row, "age_as_of_rule") or "").strip()
    if age_rule and not _get(row, "age_as_of_date"):
        errors.append(f"scholarship {sid}: age_as_of_rule set without age_as_of_date")

    parent_id = _get(row, "parent_program_id")
    if parent_id is not None and parent_id == sid:
        errors.append(f"scholarship {sid}: parent_program_id cannot reference self")

    return errors


def is_rule_publishable(row: Any, **kwargs: Any) -> bool:
    return len(validate_scholarship_publish_rules(row, **kwargs)) == 0
