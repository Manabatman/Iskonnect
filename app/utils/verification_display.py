"""User-facing verification badges and trust signals derived from scholarship data."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any

from app.utils.application_status import humanize_verification_source
from app.utils.data_completeness import (
    completeness_tier,
    compute_data_completeness_score,
    public_completeness_label,
)


def _parse_dt(val: Any) -> datetime | None:
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


def verification_badge(row: Any) -> str:
    """
    User-facing badge: verified | partially_verified | needs_review
    """
    ds = (_get(row, "data_status") or "").strip().lower()
    if ds == "needs_review":
        return "needs_review"
    score = _completeness(row)
    verified_at = _parse_dt(_get(row, "last_verified_at"))
    vsource = (_get(row, "verification_source") or "").strip().lower()
    if verified_at and vsource in ("manual", "team_verified", "partner", "csv_import"):
        age_days = (datetime.utcnow() - verified_at.replace(tzinfo=None)).days
        if age_days <= 90 and score >= 60:
            return "verified"
        if age_days <= 180:
            return "partially_verified"
    if score >= 85:
        return "partially_verified"
    return "needs_review"


def verification_badge_label(badge: str) -> str:
    return {
        "verified": "Verified",
        "partially_verified": "Partially verified",
        "needs_review": "Needs review",
    }.get(badge, "Needs review")


def _get(row: Any, key: str, default=None):
    if isinstance(row, dict):
        return row.get(key, default)
    return getattr(row, key, default)


def _completeness(row: Any) -> int:
    score = _get(row, "data_completeness_score")
    if score is not None:
        return int(score)
    return compute_data_completeness_score(row)


def attach_verification_fields(payload: dict[str, Any]) -> dict[str, Any]:
    """Add user-facing verification/trust fields to a scholarship payload."""
    badge = verification_badge(payload)
    score = _completeness(payload)
    verified_at = _get(payload, "last_verified_at")
    vsource = _get(payload, "verification_source")
    payload["verification_badge"] = badge
    payload["verification_badge_label"] = verification_badge_label(badge)
    payload["verification_source_label"] = humanize_verification_source(vsource)
    payload["completeness_label"] = public_completeness_label(score)
    payload["completeness_tier"] = completeness_tier(score)
    if verified_at:
        dt = _parse_dt(verified_at)
        if dt:
            days = (datetime.utcnow() - dt.replace(tzinfo=None)).days
            if days == 0:
                payload["last_reviewed_label"] = "Verified today"
            elif days == 1:
                payload["last_reviewed_label"] = "Verified yesterday"
            elif days < 30:
                payload["last_reviewed_label"] = f"Verified {days} days ago"
            else:
                payload["last_reviewed_label"] = f"Last reviewed {days} days ago"
    return payload
