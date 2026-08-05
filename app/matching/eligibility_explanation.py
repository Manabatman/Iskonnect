"""Backend-authored eligibility explanation — single source of truth for UI surfaces."""

from __future__ import annotations

from typing import Any

from app.matching.eligibility_result import EligibilityResult, RequirementResult
from app.matching.temporal_state import classify_scholarship_temporal
from app.utils.data_completeness import is_publishable

CATALOG_INCLUDED = "included_in_recommendations"
CATALOG_PENDING = "recommendation_pending"
CATALOG_UNAVAILABLE = "listing_unavailable"

CATALOG_MESSAGES: dict[str, str] = {
    CATALOG_PENDING: (
        "This scholarship is not yet included in automated recommendations "
        "while we complete and validate its catalog information."
    ),
    CATALOG_UNAVAILABLE: (
        "This listing is no longer active in our catalog for automated recommendations."
    ),
}


def _derive_catalog_visibility(sch: dict) -> tuple[str, str | None]:
    ds = (sch.get("data_status") or "").strip().lower()
    if ds in ("expired", "broken_link", "past_deadline"):
        return CATALOG_UNAVAILABLE, CATALOG_MESSAGES[CATALOG_UNAVAILABLE]
    if is_publishable(sch):
        return CATALOG_INCLUDED, None
    return CATALOG_PENDING, CATALOG_MESSAGES[CATALOG_PENDING]


STATUS_ELIGIBLE_NOW = "eligible_now"
STATUS_NOT_ELIGIBLE_YET = "not_eligible_yet"
STATUS_CURRENTLY_NOT_ELIGIBLE = "currently_not_eligible"

STATUS_LABELS: dict[str, str] = {
    STATUS_ELIGIBLE_NOW: "Eligible Now",
    STATUS_NOT_ELIGIBLE_YET: "Not Eligible Yet",
    STATUS_CURRENTLY_NOT_ELIGIBLE: "Currently Not Eligible",
}

_FIXED_BLOCKER_PRIORITY = ("citizenship", "age", "age_as_of", "data_status", "conflict_scope")
_CHANGEABLE_BLOCKER_PRIORITY = (
    "year_level",
    "education_level",
    "gwa",
    "academic",
    "enrollment_status",
    "income",
    "prior_units",
    "work_experience",
    "residency_years",
)
_SITUATIONAL_BLOCKER_PRIORITY = (
    "field",
    "region",
    "school_type",
    "school",
    "school_category",
    "members_only",
    "required_affiliation",
    "marital_status",
    "parent_salary_grade",
    "entry_path",
)


def _derive_application_window(sch: dict, temporal: dict[str, Any]) -> str:
    deadline_precision = (sch.get("deadline_precision") or "").strip().lower()
    cycle_type = (sch.get("cycle_type") or "").strip().lower()
    if deadline_precision == "rolling" or cycle_type == "rolling":
        return "rolling"
    if deadline_precision == "not_announced":
        return "not_announced"
    open_date = sch.get("application_open_date")
    deadline = sch.get("application_deadline")
    if not open_date and not deadline and deadline_precision in ("", "not_announced"):
        return "not_announced"
    lifecycle = (temporal.get("lifecycle_hint") or "").strip().lower()
    mapping = {
        "open": "open",
        "upcoming": "opens_later",
        "expected_to_reopen": "opens_later",
        "closed": "closed",
        "needs_verification": "unconfirmed",
        "future": "opens_later",
    }
    return mapping.get(lifecycle, "unconfirmed")


def _unmet_requirements(elig: EligibilityResult) -> list:
    return [r for r in elig.requirements if r.result == RequirementResult.UNMET]


def _pick_primary_blocker(elig: EligibilityResult) -> dict[str, Any] | None:
    unmet = [r for r in elig.requirements if r.result == RequirementResult.UNMET]
    if not unmet:
        return None

    def _first_in_priority(keys: tuple[str, ...]) -> dict[str, Any] | None:
        for key in keys:
            for req in unmet:
                if req.key == key:
                    return {
                        "key": req.key,
                        "title": req.label.split(" (")[0] if " (" in req.label else req.label,
                        "changeable": req.changeable or "fixed",
                    }
        return None

    fixed = [r for r in unmet if r.changeable == "fixed"]
    if fixed:
        picked = _first_in_priority(_FIXED_BLOCKER_PRIORITY)
        if picked:
            return picked
        req = fixed[0]
        return {"key": req.key, "title": req.label.split(" (")[0], "changeable": "fixed"}

    changeable = [r for r in unmet if r.changeable == "changeable"]
    if changeable:
        picked = _first_in_priority(_CHANGEABLE_BLOCKER_PRIORITY)
        if picked:
            return picked

    situational = [r for r in unmet if r.changeable == "situational"]
    if situational:
        picked = _first_in_priority(_SITUATIONAL_BLOCKER_PRIORITY)
        if picked:
            return picked

    req = unmet[0]
    return {
        "key": req.key,
        "title": req.label.split(" (")[0] if " (" in req.label else req.label,
        "changeable": req.changeable or "fixed",
    }


def _has_fixed_unmet(elig: EligibilityResult) -> bool:
    return any(
        r.result == RequirementResult.UNMET and r.changeable == "fixed"
        for r in elig.requirements
    )


def _build_summary_and_reason(
    status: str,
    elig: EligibilityResult,
    application_window: str,
    temporal: dict[str, Any],
) -> tuple[str, str | None]:
    if status == STATUS_ELIGIBLE_NOW:
        return "You currently meet the requirements and applications are open.", None

    if status == STATUS_CURRENTLY_NOT_ELIGIBLE:
        return "One or more permanent eligibility requirements are not met.", None

    # not_eligible_yet
    if elig.passes_for_matching and application_window in ("closed", "opens_later"):
        return (
            "You meet the eligibility requirements, but applications are currently closed.",
            "Check back when applications reopen, or save this scholarship to track it.",
        )

    gap = temporal.get("gap_reason")
    if gap:
        return (
            "You could become eligible after reaching your next year level or when applications reopen.",
            gap,
        )

    unmet = _unmet_requirements(elig)
    if unmet:
        hints = [r.change_hint for r in unmet if r.change_hint]
        reason = hints[0] if hints else None
        return (
            "You could become eligible after reaching your next year level or when applications reopen.",
            reason,
        )

    return (
        "You could become eligible after reaching your next year level or when applications reopen.",
        None,
    )


def build_eligibility_explanation(
    profile: dict,
    sch: dict,
    elig: EligibilityResult,
) -> dict[str, Any]:
    """Return the definitive explanation object for frontend rendering."""
    temporal = classify_scholarship_temporal(profile, sch)
    application_window = _derive_application_window(sch, temporal)

    if _has_fixed_unmet(elig):
        status = STATUS_CURRENTLY_NOT_ELIGIBLE
    elif elig.passes_for_matching and application_window in ("open", "rolling"):
        status = STATUS_ELIGIBLE_NOW
    else:
        status = STATUS_NOT_ELIGIBLE_YET

    summary, reason = _build_summary_and_reason(status, elig, application_window, temporal)
    primary_blocker = _pick_primary_blocker(elig)
    if status == STATUS_ELIGIBLE_NOW:
        primary_blocker = None

    next_action = temporal.get("next_action") or "Review scholarship details"
    if status == STATUS_CURRENTLY_NOT_ELIGIBLE:
        next_action = "Review requirements below"
    elif status == STATUS_NOT_ELIGIBLE_YET and elig.passes_for_matching and application_window == "closed":
        next_action = "Save this scholarship and check back when applications reopen"

    catalog_status, catalog_message = _derive_catalog_visibility(sch)

    return {
        "status": status,
        "status_label": STATUS_LABELS[status],
        "summary": summary,
        "reason": reason,
        "application_window": application_window,
        "next_action": next_action,
        "primary_blocker": primary_blocker,
        "catalog_status": catalog_status,
        "catalog_message": catalog_message,
        "requirements": [r.to_dict() for r in elig.requirements],
        "qualification_status": elig.status.value,
        "passes_for_matching": elig.passes_for_matching,
        "missing_requirements": elig.missing_requirements,
        "qualifying_requirements": elig.qualifying_requirements,
        "eligibility_confidence": elig.confidence,
    }
