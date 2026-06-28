"""Admin API: scholarship staging queue (CSV import → pending → approve)."""

from __future__ import annotations

from app.utils.dedupe import scholarship_dedupe_key
import json
import logging
from datetime import datetime, timezone
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.api.v1.scholarships import _scholarship_to_response, persist_scholarship_from_schema
from app.scholarship_cache import invalidate_scholarship_cache
from app.auth import require_admin
from app.db import get_db
from app.limiter import limiter
from app.utils.audit import log_action
from app.utils.staging_promotion import verification_source_for

logger = logging.getLogger(__name__)

router = APIRouter(tags=["scholarship-staging"])


def _find_live_duplicate(db: Session, sch: schemas.Scholarship) -> models.Scholarship | None:
    """Return an existing live scholarship with same normalized title + provider."""
    want_t = (sch.title or "").strip().lower()
    want_p = (sch.provider or "").strip().lower()
    if not want_t:
        return None
    candidates = (
        db.query(models.Scholarship)
        .filter(func.lower(func.trim(models.Scholarship.title)) == want_t)
        .all()
    )
    for row in candidates:
        if (row.provider or "").strip().lower() == want_p:
            return row
    return None


def _dedupe_key(title: str, provider: str | None, link: str | None = None) -> str:
    return scholarship_dedupe_key(title, provider, link)


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

    rows: list[dict[str, Any]] = Field(..., min_length=1, max_length=100)


@router.get("/scholarships/staging/pending", response_model=list[StagingRowSummary])
@limiter.limit("60/minute")
def list_staging_pending(
    request: Request,
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
@limiter.limit("30/minute")
def import_staging_rows(
    request: Request,
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
        key = _dedupe_key(sch.title, sch.provider, sch.link)
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
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Duplicate staging row detected")
    return {"created": created, "skipped": skipped}


@router.post("/scholarships/staging/{staging_id}/approve", response_model=schemas.ScholarshipResponse)
@limiter.limit("30/minute")
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
    dup = _find_live_duplicate(db, sch)
    if dup:
        raise HTTPException(
            status_code=409,
            detail=f"A scholarship with this title and provider already exists (id={dup.id}).",
        )
    try:
        db_sch = persist_scholarship_from_schema(
            db,
            sch,
            version_changed_by=_admin.id if _admin else None,
            auto_commit=False,
            verification_source=verification_source_for(row.source),
        )
        row.status = "approved"
        row.reviewed_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_sch)
        invalidate_scholarship_cache()
    except Exception:
        db.rollback()
        raise
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
@limiter.limit("30/minute")
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
