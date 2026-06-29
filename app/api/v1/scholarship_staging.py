"""Admin API: scholarship staging queue (CSV import → pending → approve)."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Annotated, Any, Literal

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.api.v1.scholarships import _scholarship_to_response, persist_scholarship_from_schema
from app.auth import require_admin
from app.db import get_db
from app.limiter import limiter
from app.scholarship_cache import invalidate_scholarship_cache
from app.utils.audit import log_action
from app.utils.dedupe import scholarship_dedupe_key
from app.utils.duplicate_candidates import find_duplicate_candidates, merge_confidence
from app.utils.import_validation import summarize_import_report, validate_import_row
from app.utils.scholarship_persist import find_existing_scholarship
from app.utils.scholarship_versioning import diff_snapshots, snapshot_scholarship_row
from app.utils.staging_promotion import verification_source_for

logger = logging.getLogger(__name__)

router = APIRouter(tags=["scholarship-staging"])


def _dedupe_key(title: str, provider: str | None, link: str | None = None) -> str:
    return scholarship_dedupe_key(title, provider, link)


def _live_catalog_index(db: Session) -> list[dict]:
    rows = db.query(models.Scholarship).all()
    return [
        {
            "id": r.id,
            "title": r.title,
            "provider": r.provider,
            "link": r.link,
            "dedupe_key": r.dedupe_key,
        }
        for r in rows
    ]


def _pending_dedupe_keys(db: Session) -> set[str]:
    keys = (
        db.query(models.ScholarshipStaging.dedupe_key)
        .filter(models.ScholarshipStaging.status == "pending")
        .all()
    )
    return {k[0] for k in keys if k[0]}


def _live_dedupe_keys(db: Session) -> set[str]:
    keys = db.query(models.Scholarship.dedupe_key).filter(models.Scholarship.dedupe_key.isnot(None)).all()
    return {k[0] for k in keys}


class StagingRowSummary(BaseModel):
    id: int
    title: str
    provider: str | None
    source: str | None
    status: str
    dedupe_key: str | None
    created_at: datetime
    duplicate_candidates: list[dict] = []


class StagingImportRequest(BaseModel):
    """JSON body matching schemas.Scholarship fields (stored as payload_json)."""

    rows: list[dict[str, Any]] = Field(..., min_length=1, max_length=100)


class StagingApproveRequest(BaseModel):
    """How to promote a staging row to the live catalog."""

    action: Literal["create", "update", "merge", "ignore"] = "create"
    target_scholarship_id: int | None = None


@router.get("/scholarships/staging/pending", response_model=list[StagingRowSummary])
@limiter.limit("60/minute")
def list_staging_pending(
    request: Request,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    catalog = _live_catalog_index(db)
    rows = (
        db.query(models.ScholarshipStaging)
        .filter(models.ScholarshipStaging.status == "pending")
        .order_by(models.ScholarshipStaging.created_at.asc())
        .all()
    )
    out: list[StagingRowSummary] = []
    for r in rows:
        try:
            data = json.loads(r.payload_json)
            title = data.get("title") or r.title
            provider = data.get("provider") or r.provider
            link = data.get("link")
        except Exception:
            title, provider, link = r.title, r.provider, None
        candidates = find_duplicate_candidates(title, provider, link, known=catalog)
        out.append(
            StagingRowSummary(
                id=r.id,
                title=r.title,
                provider=r.provider,
                source=r.source,
                status=r.status,
                dedupe_key=r.dedupe_key,
                created_at=r.created_at,
                duplicate_candidates=candidates,
            )
        )
    return out


@router.post("/scholarships/staging/import")
@limiter.limit("30/minute")
def import_staging_rows(
    request: Request,
    body: StagingImportRequest,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    """Batch insert rows into staging with per-row validation report."""
    live_keys = _live_dedupe_keys(db)
    pending_keys = _pending_dedupe_keys(db)
    catalog = _live_catalog_index(db)
    report_rows: list[dict[str, Any]] = []
    created = 0
    skipped = 0
    invalid = 0

    for row in body.rows:
        result = validate_import_row(row, live_dedupe_keys=live_keys, pending_dedupe_keys=pending_keys)
        if result.get("status") == "invalid":
            invalid += 1
            report_rows.append(result)
            continue
        if result.get("status") == "skipped":
            skipped += 1
            report_rows.append(result)
            continue

        try:
            sch = schemas.Scholarship.model_validate(row)
        except Exception as e:
            invalid += 1
            report_rows.append(
                {"status": "invalid", "title": row.get("title"), "error": str(e), "warnings": []}
            )
            continue

        key = _dedupe_key(sch.title, sch.provider, sch.link)
        candidates = find_duplicate_candidates(sch.title, sch.provider, sch.link, known=catalog)
        result["duplicate_candidates"] = candidates

        st = models.ScholarshipStaging(
            title=sch.title,
            provider=sch.provider,
            source=sch.source,
            payload_json=json.dumps(row),
            status="pending",
            dedupe_key=key,
        )
        db.add(st)
        pending_keys.add(key)
        created += 1
        result["status"] = "created"
        report_rows.append(result)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Duplicate staging row detected")

    report = summarize_import_report(report_rows)
    report["created"] = created
    report["skipped"] = skipped
    report["invalid"] = invalid
    return report


@router.get("/scholarships/staging/{staging_id}/diff")
@limiter.limit("60/minute")
def staging_diff(
    request: Request,
    staging_id: int,
    target_scholarship_id: int | None = None,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    """Preview field diff between staging payload and a live scholarship."""
    row = db.query(models.ScholarshipStaging).filter(models.ScholarshipStaging.id == staging_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Staging row not found")
    data = json.loads(row.payload_json)
    sch = schemas.Scholarship.model_validate(data)
    live = None
    if target_scholarship_id:
        live = db.query(models.Scholarship).filter(models.Scholarship.id == target_scholarship_id).first()
    if not live:
        live = find_existing_scholarship(db, sch)
    if not live:
        return {"has_live_match": False, "diff": {}, "duplicate_candidates": []}
    catalog = _live_catalog_index(db)
    candidates = find_duplicate_candidates(sch.title, sch.provider, sch.link, known=catalog)
    return {
        "has_live_match": True,
        "live_scholarship_id": live.id,
        "diff": diff_snapshots(snapshot_scholarship_row(live), {
            **snapshot_scholarship_row(live),
            **{k: getattr(sch, k, None) for k in snapshot_scholarship_row(live).keys()},
        }),
        "duplicate_candidates": candidates,
    }


@router.post("/scholarships/staging/{staging_id}/approve", response_model=schemas.ScholarshipResponse)
@limiter.limit("30/minute")
def approve_staging(
    request: Request,
    staging_id: int,
    body: StagingApproveRequest | None = None,
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
    action = (body.action if body else "create")
    try:
        data = json.loads(row.payload_json)
        sch = schemas.Scholarship.model_validate(data)
    except Exception as e:
        logger.error("staging_approve_invalid_payload id=%s err=%s", staging_id, e)
        raise HTTPException(status_code=400, detail="Invalid payload_json for scholarship schema")

    if action == "ignore":
        row.status = "rejected"
        row.reviewed_at = datetime.now(timezone.utc)
        db.commit()
        return {"status": "ignored", "id": staging_id}

    existing = find_existing_scholarship(db, sch)
    catalog = _live_catalog_index(db)
    candidates = find_duplicate_candidates(sch.title, sch.provider, sch.link, known=catalog)

    if action == "merge" and body and body.target_scholarship_id:
        existing = db.query(models.Scholarship).filter(models.Scholarship.id == body.target_scholarship_id).first()
        if not existing:
            raise HTTPException(status_code=404, detail="Target scholarship not found")
        top = candidates[0] if candidates else None
        if top and merge_confidence(top["confidence"]) == "low":
            raise HTTPException(
                status_code=409,
                detail="Merge confidence too low; use update with explicit target or create new",
            )

    allow_upsert = action in ("update", "merge") or (action == "create" and existing is not None)
    if action == "create" and existing and not allow_upsert:
        raise HTTPException(
            status_code=409,
            detail=f"A scholarship with this title and provider already exists (id={existing.id}). "
            "Use action=update to refresh the existing row.",
        )

    try:
        db_sch = persist_scholarship_from_schema(
            db,
            sch,
            version_changed_by=_admin.id if _admin else None,
            auto_commit=False,
            verification_source=verification_source_for(row.source),
            allow_upsert=allow_upsert,
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
        details={"scholarship_id": db_sch.id, "action": action},
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
