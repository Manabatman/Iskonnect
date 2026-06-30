"""Trust/freshness chip labels from scholarship metadata (transparent, no opaque scores)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.utils.application_status import (
    NEEDS_VERIFICATION,
    application_status_label,
    humanize_verification_source,
)


def _parse_dt(val: Any) -> datetime | None:
    if val is None:
        return None
    if isinstance(val, datetime):
        return val
    if isinstance(val, str) and val.strip():
        try:
            return datetime.fromisoformat(val.replace("Z", "+00:00"))
        except ValueError:
            return None
    return None


def _format_verified_date(val: Any) -> str | None:
    dt = _parse_dt(val)
    if not dt:
        return None
    return dt.strftime("%b %d, %Y")


def build_freshness_chips(scholarship: dict) -> list[dict[str, str]]:
    """Return UI chips from verifiable facts only (no completeness/confidence score)."""
    chips: list[dict[str, str]] = []
    app_status = (scholarship.get("application_status") or "").strip().lower()
    ds = (scholarship.get("data_status") or "").strip().lower()

    if app_status == NEEDS_VERIFICATION or ds == "needs_review":
        chips.append({"label": "Needs verification", "tone": "warning"})
    elif ds == "broken_link" or (scholarship.get("link_status") or "").strip().lower() == "broken":
        chips.append({"label": "Link issue", "tone": "danger"})

    verified_label = _format_verified_date(scholarship.get("last_verified_at"))
    if verified_label and app_status != NEEDS_VERIFICATION and ds != "needs_review":
        chips.append({"label": f"Last verified {verified_label}", "tone": "success"})
    elif app_status != NEEDS_VERIFICATION and ds != "needs_review":
        chips.append({"label": "Not yet verified", "tone": "warning"})

    source = humanize_verification_source(scholarship.get("verification_source"))
    if source:
        chips.append({"label": source, "tone": "neutral"})

    return chips


def attach_freshness_fields(row: dict) -> dict:
    out = {**row, "freshness_chips": build_freshness_chips(row)}
    out.pop("confidence_score", None)
    return out
