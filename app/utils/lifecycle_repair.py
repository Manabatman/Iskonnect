"""Shared helpers for deadline-driven lifecycle — cycle closed ≠ program discontinued."""

from __future__ import annotations

from datetime import date
from typing import Any

from app.utils.application_status import sync_application_status
from app.utils.editorial_state import PUBLISHED, apply_editorial_state

PERMANENTLY_DISCONTINUED = "permanently_discontinued"


def _get(row: Any, key: str, default=None):
    if isinstance(row, dict):
        return row.get(key, default)
    return getattr(row, key, default)


def is_permanently_discontinued(row: Any) -> bool:
    status = (_get(row, "application_status") or "").strip().lower()
    return status == PERMANENTLY_DISCONTINUED


def sync_past_deadline_cycle(row: Any, today: date | None = None) -> bool:
    """
    When a cycle deadline has passed, move dates into last_* fields and keep the row active.

    Returns True if the row was updated.
    """
    today = today or date.today()
    if is_permanently_discontinued(row):
        return False

    deadline = _get(row, "application_deadline")
    if deadline is None:
        return False
    if isinstance(deadline, str):
        try:
            deadline = date.fromisoformat(deadline.strip()[:10])
        except ValueError:
            return False
    if deadline >= today:
        return False

    open_date = _get(row, "application_open_date")
    if open_date and isinstance(open_date, str):
        try:
            open_date = date.fromisoformat(open_date.strip()[:10])
        except ValueError:
            open_date = None

    if not _get(row, "last_close_date") or _get(row, "last_close_date") < deadline:
        row.last_close_date = deadline

    if open_date and (not _get(row, "last_open_date") or _get(row, "last_open_date") > open_date):
        row.last_open_date = open_date

    row.application_deadline = None
    if open_date and open_date <= today:
        row.application_open_date = None

    apply_editorial_state(row, PUBLISHED, today=today)
    sync_application_status(row, today=today)
    # After clearing stale deadline, re-derive cycle-closed status explicitly.
    if _get(row, "application_deadline") is None and _get(row, "last_close_date"):
        cycle_type = (_get(row, "cycle_type") or "").strip().lower()
        if cycle_type and cycle_type != "rolling":
            row.application_status = "expected_reopen"
        else:
            row.application_status = "previous_cycle"
    return True
