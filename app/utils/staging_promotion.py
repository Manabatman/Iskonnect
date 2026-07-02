"""Promote scholarship staging rows to the live catalog — all rows require admin approval."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.api.v1.scholarships import persist_scholarship_from_schema

logger = logging.getLogger(__name__)


def verification_source_for(source: str | None) -> str:
    src_lo = (source or "").strip().lower()
    if src_lo in ("philscholar", "scraper"):
        return "team_verified"
    if "csv" in src_lo:
        return "csv_import"
    return "manual"


def promote_staging_row(
    db: Session,
    row: models.ScholarshipStaging,
    *,
    version_changed_by: int | None = None,
) -> models.Scholarship | None:
    """
    Promote a pending staging row to live scholarships.

    Returns the new Scholarship row, or None when skipped due to duplicate.
    Caller must commit the session.
    """
    if row.status != "pending":
        return None
    try:
        data = json.loads(row.payload_json)
        sch = schemas.Scholarship.model_validate(data)
    except Exception as e:
        logger.error("staging_promote_invalid_payload id=%s err=%s", row.id, e)
        raise ValueError(f"Invalid payload_json for staging id={row.id}") from e
    try:
        db_sch = persist_scholarship_from_schema(
            db,
            sch,
            version_changed_by=version_changed_by,
            auto_commit=False,
            verification_source=verification_source_for(row.source),
            allow_upsert=True,
        )
        row.status = "approved"
        row.reviewed_at = datetime.now(timezone.utc)
        return db_sch
    except HTTPException as e:
        if e.status_code == 409:
            row.status = "rejected"
            row.reviewed_at = datetime.now(timezone.utc)
            logger.info("staging_promote_skip_duplicate id=%s title=%r", row.id, row.title[:80])
            return None
        raise
