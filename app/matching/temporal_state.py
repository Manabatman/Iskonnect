"""Temporal eligibility states for scholarship-student pairs."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any

from app.matching.eligibility_result import QualificationStatus, evaluate_eligibility
from app.matching.hard_filters import _hard_filter_failure_stage, is_application_deadline_passed
from app.matching.profile_completeness import profile_completeness_payload
from app.prediction.cycle_predictor import predict_next_open, _parse_date as parse_cycle_date
from app.utils.application_status import NEEDS_VERIFICATION
from app.utils.json_helpers import parse_json_list
from app.utils.trust_constants import STALE_VERIFICATION_DAYS

# Canonical eligibility states exposed to API/UI
ELIGIBLE_NOW = "eligible_now"
ELIGIBLE_SOON = "eligible_soon"
MISSING_ONE_REQUIREMENT = "missing_one_requirement"
PREPARE_NOW = "prepare_now"
REQUIRES_FUTURE_GRADE = "requires_future_grade_level"
REQUIRES_FUTURE_ENROLLMENT = "requires_future_enrollment"
REQUIRES_BETTER_STANDING = "requires_better_academic_standing"
EXPECTED_NEXT_CYCLE = "expected_next_cycle"
PAST_OPPORTUNITY = "past_opportunity"
POTENTIAL_MATCH = "potential_match"
NOT_ELIGIBLE = "not_eligible"

# Simple four-state UI presentation layer
UI_ELIGIBLE_NOW = "eligible_now"
UI_OPENING_SOON = "opening_soon"
UI_PREPARE_AHEAD = "prepare_ahead"
UI_FUTURE_ELIGIBILITY = "future_eligibility"

UI_STATE_MAP: dict[str, str] = {
    ELIGIBLE_NOW: UI_ELIGIBLE_NOW,
    PREPARE_NOW: UI_PREPARE_AHEAD,
    ELIGIBLE_SOON: UI_OPENING_SOON,
    MISSING_ONE_REQUIREMENT: UI_PREPARE_AHEAD,
    REQUIRES_FUTURE_GRADE: UI_FUTURE_ELIGIBILITY,
    REQUIRES_FUTURE_ENROLLMENT: UI_FUTURE_ELIGIBILITY,
    REQUIRES_BETTER_STANDING: UI_FUTURE_ELIGIBILITY,
    EXPECTED_NEXT_CYCLE: UI_OPENING_SOON,
    PAST_OPPORTUNITY: UI_OPENING_SOON,
    POTENTIAL_MATCH: UI_PREPARE_AHEAD,
    NOT_ELIGIBLE: UI_FUTURE_ELIGIBILITY,
}

SOON_DAYS = 90


def _parse_verified_at(val: Any) -> datetime | None:
    if val is None:
        return None
    if isinstance(val, datetime):
        return val
    if isinstance(val, date):
        return datetime(val.year, val.month, val.day)
    if isinstance(val, str) and val.strip():
        try:
            return datetime.fromisoformat(val.strip().replace("Z", "+00:00")[:19])
        except ValueError:
            return None
    return None


def _null_deadline_stale_verification(sch: dict, today: date | None = None) -> bool:
    """Null deadline with missing or stale verification must not read as actively open."""
    if _parse_open_date(sch.get("application_deadline")) is not None:
        return False
    verified_at = _parse_verified_at(sch.get("last_verified_at"))
    if verified_at is None:
        return True
    age_days = (datetime.utcnow() - verified_at.replace(tzinfo=None)).days
    return age_days > STALE_VERIFICATION_DAYS


def map_to_ui_state(eligibility_state: str) -> str:
    """Map rich internal eligibility state to one of four UI states."""
    return UI_STATE_MAP.get(eligibility_state, UI_FUTURE_ELIGIBILITY)


def _parse_open_date(val: Any) -> date | None:
    if val is None:
        return None
    if isinstance(val, date):
        return val
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, str) and val.strip():
        try:
            return date.fromisoformat(val.strip()[:10])
        except ValueError:
            return None
    return None


def _is_application_open(sch: dict, today: date | None = None) -> bool:
    today = today or date.today()
    open_d = _parse_open_date(sch.get("application_open_date"))
    deadline = _parse_open_date(sch.get("application_deadline"))
    if open_d and open_d > today:
        return False
    if deadline and deadline < today:
        return False
    return True


def _opens_within_days(sch: dict, days: int = SOON_DAYS, today: date | None = None) -> bool:
    today = today or date.today()
    open_d = _parse_open_date(sch.get("application_open_date"))
    if open_d and open_d > today:
        return (open_d - today).days <= days
    predicted = _predicted_open(sch)
    if predicted and predicted > today:
        return (predicted - today).days <= days
    return False


def _predicted_open(sch: dict) -> date | None:
    last_open = parse_cycle_date(sch.get("last_open_date"))
    cycle_type = sch.get("cycle_type")
    if last_open and cycle_type:
        return predict_next_open(last_open, cycle_type)
    return None


def _failure_to_state(stage: str | None) -> str:
    if stage is None:
        return ELIGIBLE_NOW
    if stage == "education_level":
        return REQUIRES_FUTURE_GRADE
    if stage == "gwa":
        return REQUIRES_BETTER_STANDING
    if stage in ("age", "income", "field", "region", "school_type", "members_only"):
        return MISSING_ONE_REQUIREMENT
    return NOT_ELIGIBLE


def _gap_reason(stage: str | None, sch: dict, profile: dict) -> str | None:
    if not stage:
        return None
    labels = {
        "education_level": "You may qualify when you reach the required grade or level—worth planning ahead.",
        "gwa": "Your GWA is below the minimum for now—you can work toward this requirement over time.",
        "income": "Household income is above this program's ceiling based on your profile.",
        "age": "Age requirement isn't met yet based on your profile.",
        "region": "Location or residency requirement doesn't match your profile yet.",
        "school_type": "School type (public/private) requirement doesn't match your profile.",
        "field": "Your field of study doesn't align yet—this may change if you switch courses.",
        "members_only": "This program prioritizes a specific group you haven't declared in your profile.",
    }
    return labels.get(stage, "One or more requirements don't match your profile yet.")


def _next_action(state: str, sch: dict) -> str:
    actions = {
        ELIGIBLE_NOW: "Apply now on the official site",
        ELIGIBLE_SOON: "Save this and prepare your documents",
        PREPARE_NOW: "Start gathering requirements early",
        MISSING_ONE_REQUIREMENT: "See what you need to become eligible",
        REQUIRES_FUTURE_GRADE: "Keep this on your radar for when you advance",
        REQUIRES_BETTER_STANDING: "Focus on raising your GWA to qualify",
        EXPECTED_NEXT_CYCLE: "Save and watch for the next opening",
        PAST_OPPORTUNITY: "Review details to prepare for next cycle",
        POTENTIAL_MATCH: "Complete your profile to unlock better matches",
    }
    base = actions.get(state, "Review scholarship")
    docs = parse_json_list(sch.get("required_documents"))
    if state in (PREPARE_NOW, ELIGIBLE_SOON) and docs:
        return f"{base} — gather: {', '.join(docs[:3])}"
    return base


def _needs_preparation(sch: dict) -> bool:
    docs = parse_json_list(sch.get("required_documents"))
    return bool(
        docs
        or sch.get("has_qualifying_exam")
        or sch.get("has_interview")
        or sch.get("has_essay_requirement")
    )


def classify_scholarship_temporal(
    profile: dict,
    sch: dict,
    *,
    today: date | None = None,
) -> dict[str, Any]:
    """
    Classify one scholarship for a profile into a temporal eligibility state.
    Returns state, gap_reason, predicted_open, next_action, lifecycle_hint.
    """
    today = today or date.today()
    ds = (sch.get("data_status") or "").strip().lower()
    if ds in ("expired", "broken_link", "past_deadline"):
        predicted = _predicted_open(sch)
        if predicted and predicted > today:
            return {
                "eligibility_state": EXPECTED_NEXT_CYCLE,
                "gap_reason": "This cycle has closed, but it may reopen—worth saving for next time.",
                "predicted_open": predicted.isoformat(),
                "next_action": _next_action(EXPECTED_NEXT_CYCLE, sch),
                "lifecycle_hint": "expected_to_reopen",
            }
        return {
            "eligibility_state": PAST_OPPORTUNITY,
            "gap_reason": "This cycle has closed.",
            "predicted_open": None,
            "next_action": _next_action(PAST_OPPORTUNITY, sch),
            "lifecycle_hint": "closed",
        }

    stage = _hard_filter_failure_stage(profile, sch)
    completeness = profile_completeness_payload(profile)
    if completeness.get("low_data_warning") and stage is None:
        state = POTENTIAL_MATCH
        return {
            "eligibility_state": state,
            "gap_reason": "Add a few more profile details for more confident matches.",
            "predicted_open": None,
            "next_action": _next_action(state, sch),
            "lifecycle_hint": "open" if _is_application_open(sch, today) else "upcoming",
        }

    if stage:
        state = _failure_to_state(stage)
        predicted = _predicted_open(sch) if state == EXPECTED_NEXT_CYCLE else None
        return {
            "eligibility_state": state,
            "gap_reason": _gap_reason(stage, sch, profile),
            "predicted_open": predicted.isoformat() if predicted else None,
            "next_action": _next_action(state, sch),
            "lifecycle_hint": "future",
        }

    deadline_passed = is_application_deadline_passed(sch.get("application_deadline"))
    if deadline_passed:
        predicted = _predicted_open(sch)
        if predicted and predicted > today:
            return {
                "eligibility_state": EXPECTED_NEXT_CYCLE,
                "gap_reason": "The deadline passed—this program may open again next cycle.",
                "predicted_open": predicted.isoformat(),
                "next_action": _next_action(EXPECTED_NEXT_CYCLE, sch),
                "lifecycle_hint": "expected_to_reopen",
            }
        return {
            "eligibility_state": PAST_OPPORTUNITY,
            "gap_reason": "The application deadline for this cycle has passed.",
            "predicted_open": None,
            "next_action": _next_action(PAST_OPPORTUNITY, sch),
            "lifecycle_hint": "closed",
        }

    open_now = _is_application_open(sch, today)
    if open_now:
        state = PREPARE_NOW if _needs_preparation(sch) else ELIGIBLE_NOW
        lifecycle_hint = "open"
        gap_reason = None
        if _null_deadline_stale_verification(sch, today):
            lifecycle_hint = "needs_verification"
            gap_reason = "No application deadline is listed and our last verification is outdated — confirm on the official site."
        return {
            "eligibility_state": state,
            "gap_reason": gap_reason,
            "predicted_open": None,
            "next_action": _next_action(state, sch),
            "lifecycle_hint": lifecycle_hint,
        }

    if _opens_within_days(sch, SOON_DAYS, today):
        state = PREPARE_NOW if _needs_preparation(sch) else ELIGIBLE_SOON
        predicted = _parse_open_date(sch.get("application_open_date")) or _predicted_open(sch)
        return {
            "eligibility_state": state,
            "gap_reason": "Applications aren't open yet—good time to prepare documents.",
            "predicted_open": predicted.isoformat() if predicted else None,
            "next_action": _next_action(state, sch),
            "lifecycle_hint": "upcoming",
        }

    predicted = _predicted_open(sch)
    if predicted and predicted > today:
        return {
            "eligibility_state": EXPECTED_NEXT_CYCLE,
            "gap_reason": "Based on past cycles, this scholarship may reopen around a similar time.",
            "predicted_open": predicted.isoformat(),
            "next_action": _next_action(EXPECTED_NEXT_CYCLE, sch),
            "lifecycle_hint": "expected_to_reopen",
        }

    return {
        "eligibility_state": ELIGIBLE_NOW,
        "gap_reason": None,
        "predicted_open": None,
        "next_action": _next_action(ELIGIBLE_NOW, sch),
        "lifecycle_hint": "open",
    }


def attach_temporal_fields(match_row: dict, profile: dict) -> dict:
    """Merge temporal classification into a match result dict."""
    temporal = classify_scholarship_temporal(profile, match_row)
    state = temporal.get("eligibility_state", "")
    out = {**match_row, **temporal, "ui_state": map_to_ui_state(state)}
    if temporal.get("lifecycle_hint") == "needs_verification":
        out["application_status"] = NEEDS_VERIFICATION
    return out
