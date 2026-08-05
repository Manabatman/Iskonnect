"""CRUD helpers for scholarship field evidence records."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from app import models


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def supersede_active_evidence(
    db: Session,
    scholarship_id: int,
    field_key: str,
    *,
    auto_flush: bool = False,
) -> None:
    """Mark existing active evidence rows for a field as superseded."""
    rows = (
        db.query(models.FieldEvidence)
        .filter(
            models.FieldEvidence.scholarship_id == scholarship_id,
            models.FieldEvidence.field_key == field_key,
            models.FieldEvidence.superseded_at.is_(None),
        )
        .all()
    )
    now = _utcnow()
    for row in rows:
        row.superseded_at = now
    if auto_flush:
        db.flush()


def create_field_evidence(
    db: Session,
    *,
    scholarship_id: int,
    field_key: str,
    value_snapshot: Any,
    source_url: str | None = None,
    source_type: str | None = None,
    evidence_snippet: str | None = None,
    confidence: float | None = None,
    reviewer_id: int | None = None,
    supersede_existing: bool = True,
    auto_flush: bool = False,
) -> models.FieldEvidence:
    if supersede_existing:
        supersede_active_evidence(db, scholarship_id, field_key, auto_flush=auto_flush)
    if value_snapshot is not None and not isinstance(value_snapshot, str):
        value_snapshot = json.dumps(value_snapshot, default=str)
    row = models.FieldEvidence(
        scholarship_id=scholarship_id,
        field_key=field_key,
        value_snapshot=value_snapshot,
        source_url=source_url,
        source_type=source_type or ("staging_import" if source_url else "manual"),
        evidence_snippet=evidence_snippet,
        confidence=confidence,
        retrieved_at=_utcnow(),
        reviewer_id=reviewer_id,
    )
    db.add(row)
    if auto_flush:
        db.flush()
    return row


_INTERNAL_SNIPPET_MARKERS = (
    "iskonnect id",
    "migration_v1",
    "gemini",
    "notebooklm",
    "cursor remediation",
    "field_changes",
)


def _is_internal_snippet(text: str | None) -> bool:
    if not text:
        return False
    lower = text.lower()
    return any(m in lower for m in _INTERNAL_SNIPPET_MARKERS)


def _evidence_to_dict(row: models.FieldEvidence, *, include_internal: bool = False) -> dict[str, Any]:
    snippet = row.evidence_snippet
    if not include_internal and _is_internal_snippet(snippet):
        snippet = None
    return {
        "id": row.id,
        "field_key": row.field_key,
        "value_snapshot": row.value_snapshot,
        "source_url": row.source_url,
        "source_type": row.source_type,
        "evidence_snippet": snippet,
        "confidence": row.confidence,
        "retrieved_at": row.retrieved_at.isoformat() if row.retrieved_at else None,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }


def list_admin_field_evidence(db: Session, scholarship_id: int) -> list[dict[str, Any]]:
    """Full evidence trail for admin/reviewer surfaces."""
    rows = (
        db.query(models.FieldEvidence)
        .filter(
            models.FieldEvidence.scholarship_id == scholarship_id,
            models.FieldEvidence.superseded_at.is_(None),
        )
        .order_by(models.FieldEvidence.field_key, models.FieldEvidence.created_at.desc())
        .all()
    )
    return [_evidence_to_dict(row, include_internal=True) for row in rows]


def list_public_field_evidence(db: Session, scholarship_id: int) -> list[dict[str, Any]]:
    """Deprecated for student detail — use admin endpoint. Kept for backwards compatibility."""
    return list_admin_field_evidence(db, scholarship_id)


def promote_evidence_from_staging_payload(
    db: Session,
    scholarship: models.Scholarship,
    raw_payload: dict[str, Any],
    *,
    reviewer_id: int | None = None,
    verification_source: str | None = None,
) -> None:
    """
    Create field_evidence rows from staging import metadata (source_urls) and core fields.
    Sets verified_by on the scholarship when reviewer_id is provided.
    """
    source_urls_raw = raw_payload.get("source_urls") or ""
    if isinstance(source_urls_raw, list):
        urls = [u for u in source_urls_raw if u]
    elif isinstance(source_urls_raw, str) and source_urls_raw.strip():
        urls = [u.strip() for u in source_urls_raw.split("|") if u.strip()]
    else:
        urls = []
    primary_url = urls[0] if urls else (scholarship.link or None)

    tracked_fields: list[tuple[str, Any]] = [
        ("link", scholarship.link),
        ("application_deadline", scholarship.application_deadline.isoformat() if scholarship.application_deadline else None),
        ("application_open_date", scholarship.application_open_date.isoformat() if scholarship.application_open_date else None),
        ("max_income_threshold", scholarship.max_income_threshold),
        ("min_gwa_normalized", scholarship.min_gwa_normalized),
        ("eligible_levels", scholarship.eligible_levels),
        ("eligible_regions", scholarship.eligible_regions),
        ("eligible_schools", scholarship.eligible_schools),
    ]
    for field_key, value in tracked_fields:
        if value is None or value == "" or value == "[]":
            continue
        create_field_evidence(
            db,
            scholarship_id=scholarship.id,
            field_key=field_key,
            value_snapshot=value,
            source_url=primary_url,
            source_type=verification_source or "staging_import",
            reviewer_id=reviewer_id,
            auto_flush=True,
        )

    if reviewer_id is not None:
        scholarship.verified_by = reviewer_id
    scholarship.last_verified_at = _utcnow()
