"""
Authoritative scholarship application lifecycle status.

Stored on Scholarship.application_status and synced at write time (import, maintenance,
admin actions). UI and search read this field — they do not re-derive lifecycle from
scattered flags.

Architecture target:
  Scholarship identity → cycle fields → application_status (single student-facing state)
"""

from __future__ import annotations

from datetime import date
from typing import Any

# Canonical values (match frontend LIFECYCLE_STATUS_GUIDE keys)
OPEN = "open"
CLOSED = "closed"
PREVIOUS_CYCLE = "previous_cycle"
EXPECTED_REOPEN = "expected_reopen"
ARCHIVED = "archived"
NEEDS_VERIFICATION = "needs_verification"

APPLICATION_STATUSES: frozenset[str] = frozenset(
    {OPEN, CLOSED, PREVIOUS_CYCLE, EXPECTED_REOPEN, ARCHIVED, NEEDS_VERIFICATION}
)

# Search / filter timing buckets map to application_status sets
TIMING_FILTER_MAP: dict[str, frozenset[str]] = {
    "open_now": frozenset({OPEN}),
    "opening_soon": frozenset({OPEN}),  # future open_date still stored as open until window ends
    "closed": frozenset({CLOSED, PREVIOUS_CYCLE}),
    "expected_reopen": frozenset({EXPECTED_REOPEN}),
    "previous_cycle": frozenset({PREVIOUS_CYCLE}),
    "archived": frozenset({ARCHIVED}),
    "needs_verification": frozenset({NEEDS_VERIFICATION}),
}


def _get(row: Any, name: str, default: Any = None) -> Any:
    if isinstance(row, dict):
        return row.get(name, default)
    return getattr(row, name, default)


def _parse_date(val: Any) -> date | None:
    if val is None:
        return None
    if isinstance(val, date):
        return val
    if isinstance(val, str) and val.strip():
        try:
            return date.fromisoformat(val.strip()[:10])
        except ValueError:
            return None
    return None


def _has_reopen_prediction(row: Any) -> bool:
    cycle_type = (_get(row, "cycle_type") or "").strip().lower()
    last_open = _parse_date(_get(row, "last_open_date"))
    if not cycle_type or not last_open or cycle_type == "rolling":
        return False
    return True


def _has_historical_cycle(row: Any) -> bool:
    return bool(
        _parse_date(_get(row, "last_close_date"))
        or (_get(row, "academic_year_target") or "").strip()
        or _parse_date(_get(row, "last_open_date"))
    )


def _window_has_ended(row: Any, today: date) -> bool:
    ds = (_get(row, "data_status") or "").strip().lower()
    if ds in ("expired", "past_deadline"):
        return True
    deadline = _parse_date(_get(row, "application_deadline"))
    return bool(deadline and deadline < today)


def _window_not_yet_open(row: Any, today: date) -> bool:
    open_d = _parse_date(_get(row, "application_open_date"))
    return bool(open_d and open_d > today)


def compute_application_status(row: Any, today: date | None = None) -> str:
    """
    Derive application_status from stored scholarship fields.
    Called at write time only (persist, maintenance, admin) — not on every API read.
    """
    today = today or date.today()

    if _get(row, "is_active") is False:
        return ARCHIVED

    ds = (_get(row, "data_status") or "").strip().lower()
    if ds == "needs_review":
        return NEEDS_VERIFICATION

    if _window_has_ended(row, today):
        if _has_reopen_prediction(row):
            return EXPECTED_REOPEN
        if _has_historical_cycle(row):
            return PREVIOUS_CYCLE
        return CLOSED

    if _window_not_yet_open(row, today):
        return OPEN

    return OPEN


def sync_application_status(row: Any, today: date | None = None) -> str:
    """Compute and assign application_status on an ORM Scholarship row."""
    status = compute_application_status(row, today=today)
    row.application_status = status
    return status


def application_status_label(status: str | None) -> str:
    """Student-facing labels (keep in sync with frontend scholarshipStatus.ts)."""
    labels = {
        OPEN: "Open now",
        CLOSED: "Closed",
        PREVIOUS_CYCLE: "Past cycle",
        EXPECTED_REOPEN: "Expected to reopen",
        ARCHIVED: "No longer offered",
        NEEDS_VERIFICATION: "Needs verification",
    }
    return labels.get((status or "").strip().lower(), status or "")


def humanize_verification_source(source: str | None) -> str | None:
    if not source or not str(source).strip():
        return None
    mapping = {
        "manual": "Verified by ISKONNECT team",
        "scraper": "Official website",
        "partner": "Partner organization",
        "csv_import": "Imported record",
    }
    key = str(source).strip().lower()
    return mapping.get(key, source.replace("_", " ").title())
