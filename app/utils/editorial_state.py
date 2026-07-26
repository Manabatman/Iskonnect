"""Editorial lifecycle shims — editorial_state is primary; is_active/data_status derived for compat."""

from __future__ import annotations

from datetime import date
from typing import Any

PUBLISHED = "published"
ARCHIVED = "archived"
NEEDS_REVIEW = "needs_review"
DRAFT = "draft"
IMPORTED = "imported"
VERIFIED = "verified"


def _get(row: Any, key: str, default=None):
    if isinstance(row, dict):
        return row.get(key, default)
    return getattr(row, key, default)


def derive_is_active(row: Any) -> bool:
    """Whether a row should be treated as student-visible catalog entry."""
    es = (_get(row, "editorial_state") or "").strip().lower()
    if es == ARCHIVED:
        return False
    if es:
        # needs_review and imported rows remain visible; only archived hides.
        return True
    legacy = _get(row, "is_active")
    if legacy is False and (_get(row, "application_status") or "").strip().lower() == "archived":
        return False
    return legacy is not False


def derive_data_status(row: Any, *, today: date | None = None) -> str:
    """Map editorial_state + timeline signals to legacy data_status."""
    es = (_get(row, "editorial_state") or "").strip().lower()
    legacy = (_get(row, "data_status") or "").strip().lower()

    if es == ARCHIVED:
        return "expired"
    if es == NEEDS_REVIEW:
        return "needs_review"
    if es in (DRAFT, IMPORTED):
        return legacy or "needs_review"
    if es == VERIFIED:
        return legacy or "active"

    if es == PUBLISHED or not es:
        deadline = _get(row, "application_deadline")
        if deadline and today and deadline < today:
            return "expired"
        link_status = (_get(row, "link_status") or "").strip().lower()
        if link_status == "broken":
            return "broken_link"
        return legacy or "active"

    return legacy or "active"


def apply_editorial_state(
    row: Any,
    editorial_state: str,
    *,
    today: date | None = None,
) -> None:
    """Set editorial_state and sync derived is_active/data_status for one release."""
    row.editorial_state = editorial_state
    row.is_active = derive_is_active(row)
    row.data_status = derive_data_status(row, today=today)


def sync_legacy_fields_from_editorial(row: Any, *, today: date | None = None) -> None:
    """Recompute is_active/data_status from current editorial_state without changing it."""
    if hasattr(row, "is_active"):
        row.is_active = derive_is_active(row)
    if hasattr(row, "data_status"):
        row.data_status = derive_data_status(row, today=today)
