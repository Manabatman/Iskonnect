"""Snapshot and version records for scholarship rows."""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models


def _serialize_val(v: Any) -> Any:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    return v


def snapshot_scholarship_row(s: models.Scholarship) -> dict[str, Any]:
    """Comparable dict of main scholarship columns for diffs."""
    keys = [
        "title",
        "provider",
        "source",
        "link",
        "description",
        "min_age",
        "max_age",
        "application_deadline",
        "application_open_date",
        "is_active",
        "data_status",
        "eligible_levels",
        "eligible_regions",
        "eligible_cities",
        "max_income_threshold",
        "min_gwa_normalized",
    ]
    out: dict[str, Any] = {}
    for k in keys:
        out[k] = _serialize_val(getattr(s, k, None))
    return out


def diff_snapshots(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    changes: dict[str, Any] = {}
    for k in set(before) | set(after):
        if before.get(k) != after.get(k):
            changes[k] = {"from": before.get(k), "to": after.get(k)}
    return changes


def next_version_number(db: Session, scholarship_id: int) -> int:
    m = (
        db.query(func.max(models.ScholarshipVersion.version_number))
        .filter(models.ScholarshipVersion.scholarship_id == scholarship_id)
        .scalar()
    )
    return (m or 0) + 1


def record_scholarship_version(
    db: Session,
    *,
    scholarship_id: int,
    changes: dict[str, Any],
    changed_by: int | None,
) -> None:
    vn = next_version_number(db, scholarship_id)
    row = models.ScholarshipVersion(
        scholarship_id=scholarship_id,
        version_number=vn,
        changes=json.dumps(changes, default=str),
        changed_by=changed_by,
    )
    db.add(row)
