"""Trust/freshness chip labels from scholarship metadata (transparent, no opaque scores)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


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
    ds = (scholarship.get("data_status") or "").strip().lower()
    if ds == "needs_review":
        chips.append({"label": "Needs verification", "tone": "warning"})
    elif ds in ("expired", "past_deadline"):
        chips.append({"label": "Closed cycle", "tone": "neutral"})
    elif ds == "broken_link":
        chips.append({"label": "Link issue", "tone": "danger"})

    verified_label = _format_verified_date(scholarship.get("last_verified_at"))
    if verified_label:
        chips.append({"label": f"Verified {verified_label}", "tone": "success"})
    else:
        chips.append({"label": "Not yet verified", "tone": "warning"})

    source = (scholarship.get("verification_source") or "").strip()
    if source:
        chips.append({"label": f"Source: {source[:32]}", "tone": "neutral"})

    return chips


def attach_freshness_fields(row: dict) -> dict:
    out = {**row, "freshness_chips": build_freshness_chips(row)}
    out.pop("confidence_score", None)
    return out
