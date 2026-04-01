"""Admin API: scholarship staging queue (CSV import → pending → approve)."""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import datetime, timezone
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app import models, schemas
from app.api.v1.scholarships import _scholarship_to_response, persist_scholarship_from_schema
from app.auth import require_admin
from app.db import get_db
from app.utils.audit import log_action

logger = logging.getLogger(__name__)

router = APIRouter(tags=["scholarship-staging"])


def _dedupe_key(title: str, provider: str | None) -> str:
    raw = f"{(title or '').strip().lower()}|{(provider or '').strip().lower()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:64]


class StagingRowSummary(BaseModel):
    id: int
    title: str
    provider: str | None
    source: str | None
    status: str
    dedupe_key: str | None
    created_at: datetime


class StagingImportRequest(BaseModel):
    """JSON body matching schemas.Scholarship fields (stored as payload_json)."""

    rows: list[dict[str, Any]] = Field(..., min_length=1)


@router.get("/scholarships/staging/pending", response_model=list[StagingRowSummary])
def list_staging_pending(
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    rows = (
        db.query(models.ScholarshipStaging)
        .filter(models.ScholarshipStaging.status == "pending")
        .order_by(models.ScholarshipStaging.created_at.asc())
        .all()
    )
    return [
        StagingRowSummary(
            id=r.id,
            title=r.title,
            provider=r.provider,
            source=r.source,
            status=r.status,
            dedupe_key=r.dedupe_key,
            created_at=r.created_at,
        )
        for r in rows
    ]


@router.post("/scholarships/staging/import")
def import_staging_rows(
    body: StagingImportRequest,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    """Batch insert rows into staging. Each row must be a JSON object compatible with Scholarship schema."""
    created = 0
    skipped = 0
    for row in body.rows:
        try:
            sch = schemas.Scholarship.model_validate(row)
        except Exception as e:
            logger.warning("staging_import_invalid_row: %s", e)
            skipped += 1
            continue
        key = _dedupe_key(sch.title, sch.provider)
        existing = (
            db.query(models.ScholarshipStaging)
            .filter(models.ScholarshipStaging.dedupe_key == key, models.ScholarshipStaging.status == "pending")
            .first()
        )
        if existing:
            skipped += 1
            continue
        st = models.ScholarshipStaging(
            title=sch.title,
            provider=sch.provider,
            source=sch.source,
            payload_json=json.dumps(row),
            status="pending",
            dedupe_key=key,
        )
        db.add(st)
        created += 1
    db.commit()
    return {"created": created, "skipped": skipped}


@router.post("/scholarships/staging/{staging_id}/approve", response_model=schemas.ScholarshipResponse)
def approve_staging(
    request: Request,
    staging_id: int,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    row = (
        db.query(models.ScholarshipStaging)
        .filter(models.ScholarshipStaging.id == staging_id, models.ScholarshipStaging.status == "pending")
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Staging row not found or already processed")
    try:
        data = json.loads(row.payload_json)
        sch = schemas.Scholarship.model_validate(data)
    except Exception as e:
        logger.error("staging_approve_invalid_payload id=%s err=%s", staging_id, e)
        raise HTTPException(status_code=400, detail="Invalid payload_json for scholarship schema")
    db_sch = persist_scholarship_from_schema(
        db,
        sch,
        version_changed_by=_admin.id if _admin else None,
    )
    sid = row.id
    row = db.query(models.ScholarshipStaging).filter(models.ScholarshipStaging.id == sid).first()
    if row:
        row.status = "approved"
        row.reviewed_at = datetime.now(timezone.utc)
        db.commit()
    log_action(
        db,
        actor_id=_admin.id if _admin else None,
        actor_type="admin",
        action="staging.approve",
        resource_type="scholarship_staging",
        resource_id=staging_id,
        details={"scholarship_id": db_sch.id},
        ip_address=request.client.host if request.client else None,
    )
    return _scholarship_to_response(db_sch)


@router.post("/scholarships/staging/{staging_id}/reject")
def reject_staging(
    request: Request,
    staging_id: int,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    row = db.query(models.ScholarshipStaging).filter(models.ScholarshipStaging.id == staging_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Staging row not found")
    row.status = "rejected"
    row.reviewed_at = datetime.now(timezone.utc)
    db.commit()
    log_action(
        db,
        actor_id=_admin.id if _admin else None,
        actor_type="admin",
        action="staging.reject",
        resource_type="scholarship_staging",
        resource_id=staging_id,
        details={},
        ip_address=request.client.host if request.client else None,
    )
    return {"status": "rejected", "id": staging_id}
