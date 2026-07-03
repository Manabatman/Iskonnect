"""Build opportunity timeline buckets for a student profile."""

from __future__ import annotations

from datetime import date
from typing import Any

from app.matching.eligibility_result import QualificationStatus, evaluate_eligibility
from app.matching.temporal_state import (
    ELIGIBLE_NOW,
    ELIGIBLE_SOON,
    EXPECTED_NEXT_CYCLE,
    MISSING_ONE_REQUIREMENT,
    PAST_OPPORTUNITY,
    PREPARE_NOW,
    REQUIRES_BETTER_STANDING,
    REQUIRES_FUTURE_GRADE,
    attach_temporal_fields,
    classify_scholarship_temporal,
    map_to_ui_state,
)
from app.serialization.scholarship import scholarship_to_catalog_dict


def _slim_card(sch: dict, temporal: dict) -> dict:
    state = temporal.get("eligibility_state", "")
    return {
        "id": sch.get("id"),
        "title": sch.get("title"),
        "provider": sch.get("provider"),
        "link": sch.get("link"),
        "image_url": sch.get("image_url"),
        "image_alt": sch.get("image_alt"),
        "application_deadline": sch.get("application_deadline"),
        "application_open_date": sch.get("application_open_date"),
        "eligibility_state": temporal.get("eligibility_state"),
        "ui_state": map_to_ui_state(state),
        "gap_reason": temporal.get("gap_reason"),
        "predicted_open": temporal.get("predicted_open"),
        "next_action": temporal.get("next_action"),
        "lifecycle_hint": temporal.get("lifecycle_hint"),
        "data_status": sch.get("data_status"),
        "verification_source": sch.get("verification_source"),
        "last_verified_at": sch.get("last_verified_at"),
    }


def _bucket_card(lanes: dict[str, list[dict]], state: str, card: dict) -> None:
    if state == ELIGIBLE_NOW:
        lanes["available_now"].append(card)
    elif state == ELIGIBLE_SOON:
        lanes["opening_soon"].append(card)
    elif state in (PREPARE_NOW, MISSING_ONE_REQUIREMENT):
        lanes["prepare_for"].append(card)
    elif state == EXPECTED_NEXT_CYCLE:
        lanes["expected_reopening"].append(card)
    elif state in (REQUIRES_FUTURE_GRADE, REQUIRES_BETTER_STANDING):
        lanes["future_eligibility"].append(card)
    elif state == PAST_OPPORTUNITY:
        lanes["past_reference"].append(card)


def build_opportunity_timeline(
    profile: dict,
    scholarships: list[dict],
    scored_matches: list[dict],
    *,
    max_per_lane: int = 12,
) -> dict[str, Any]:
    """
    Bucket scholarships into timeline lanes using a single pre-scored match pass.
    Only non-scoring scholarships are classified temporally without scoring.
    """
    today = date.today()
    scored_by_id = {m.get("id"): m for m in scored_matches if m.get("id") is not None}

    lanes: dict[str, list[dict]] = {
        "available_now": [],
        "opening_soon": [],
        "prepare_for": [],
        "expected_reopening": [],
        "future_eligibility": [],
        "past_reference": [],
    }

    seen_ids: set[int] = set()
    for match in scored_matches:
        sid = match.get("id")
        if sid is None:
            continue
        seen_ids.add(int(sid))
        state = match.get("eligibility_state")
        if not state:
            temporal = classify_scholarship_temporal(profile, match, today=today)
            card = {**match, **temporal, "ui_state": map_to_ui_state(temporal["eligibility_state"])}
            state = temporal["eligibility_state"]
        else:
            card = match
        _bucket_card(lanes, state, card)

    for sch in scholarships:
        sid = sch.get("id")
        if sid is not None and int(sid) in seen_ids:
            continue
        elig = evaluate_eligibility(profile, sch)
        # Hard-ineligible scholarships must not appear in actionable timeline lanes
        if elig.status == QualificationStatus.NOT_ELIGIBLE:
            continue
        temporal = classify_scholarship_temporal(profile, sch, today=today)
        state = temporal["eligibility_state"]
        card = {**scholarship_to_catalog_dict(sch), **_slim_card(sch, temporal)}
        card["eligibility"] = elig.to_dict()
        _bucket_card(lanes, state, card)

    for key in ("available_now", "opening_soon", "prepare_for"):
        lanes[key].sort(
            key=lambda x: (
                -(x.get("final_score") or x.get("score") or 0),
                x.get("id") or 0,
                (x.get("title") or "").lower(),
            )
        )
    lanes["expected_reopening"].sort(key=lambda x: x.get("predicted_open") or "")
    lanes["future_eligibility"].sort(key=lambda x: x.get("title") or "")

    counts = {k: len(v) for k, v in lanes.items()}
    summary = {
        "available_now": counts["available_now"],
        "opening_soon": counts["opening_soon"],
        "prepare_for": counts["prepare_for"],
        "expected_reopening": counts["expected_reopening"],
        "future_eligibility": counts["future_eligibility"],
        "past_reference": counts["past_reference"],
        "total_actionable": counts["available_now"] + counts["opening_soon"] + counts["prepare_for"],
    }

    trimmed = {k: v[:max_per_lane] for k, v in lanes.items()}
    return {
        "summary": summary,
        "lanes": trimmed,
        "headline": _headline(summary),
    }


def _headline(summary: dict[str, int]) -> str:
    parts = []
    if summary["available_now"]:
        parts.append(f"{summary['available_now']} available today")
    if summary["opening_soon"]:
        parts.append(f"{summary['opening_soon']} opening soon")
    if summary["prepare_for"]:
        parts.append(f"{summary['prepare_for']} to prepare for")
    if summary["expected_reopening"]:
        parts.append(f"{summary['expected_reopening']} expected to reopen")
    if not parts:
        return "Build your profile to unlock more opportunities along your journey."
    return " · ".join(parts)
