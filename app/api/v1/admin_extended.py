"""Additional read-only admin list endpoints for the admin dashboard UI."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models
from app.auth import require_admin
from app.db import get_db
from app.limiter import limiter
from app.utils.timezone import to_philippine_iso

router = APIRouter(tags=["admin-extended"])

FEEDBACK_TRIAGE_STATUSES = frozenset({"new", "triaged", "planned", "in_progress", "shipped", "declined"})


class FeedbackTriageUpdate(BaseModel):
    triage_status: str = Field(..., min_length=1, max_length=32)
    triage_note: str | None = Field(default=None, max_length=4000)


@router.get("/admin/users")
@limiter.limit("60/minute")
def admin_list_users(
    request: Request,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
    limit: int = Query(200, ge=1, le=500),
):
    rows = db.query(models.User).order_by(models.User.id.desc()).limit(limit).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "role": getattr(u, "role", "student"),
            "email_verified": bool(getattr(u, "email_verified", False)),
        }
        for u in rows
    ]


@router.get("/admin/match-runs/recent")
@limiter.limit("60/minute")
def admin_recent_match_runs(
    request: Request,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
    limit: int = Query(50, ge=1, le=200),
):
    runs = db.query(models.MatchRun).order_by(models.MatchRun.created_at.desc()).limit(limit).all()
    if not runs:
        return []
    run_ids = [r.id for r in runs]
    counts = dict(
        db.query(models.MatchResult.run_id, func.count(models.MatchResult.id))
        .filter(models.MatchResult.run_id.in_(run_ids))
        .group_by(models.MatchResult.run_id)
        .all()
    )
    out = []
    for r in runs:
        cnt = int(counts.get(r.id, 0))
        out.append(
            {
                "id": r.id,
                "user_id": r.user_id,
                "profile_id": r.profile_id,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "ph_created_at": to_philippine_iso(r.created_at) if r.created_at else None,
                "result_count": cnt,
            }
        )
    return out


@router.get("/admin/feedback/list")
@limiter.limit("60/minute")
def admin_list_feedback(
    request: Request,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
    limit: int = Query(100, ge=1, le=500),
):
    rows = (
        db.query(models.ProductFeedback)
        .order_by(models.ProductFeedback.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": r.id,
            "user_id": r.user_id,
            "category": r.category,
            "message": r.message,
            "contact_email": r.contact_email,
            "triage_status": getattr(r, "triage_status", "new"),
            "triage_note": getattr(r, "triage_note", None),
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "ph_created_at": to_philippine_iso(r.created_at) if r.created_at else None,
        }
        for r in rows
    ]


@router.patch("/admin/feedback/{feedback_id}")
@limiter.limit("60/minute")
def admin_update_feedback_triage(
    feedback_id: int,
    request: Request,
    body: Annotated[FeedbackTriageUpdate, Body()],
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    if body.triage_status not in FEEDBACK_TRIAGE_STATUSES:
        raise HTTPException(status_code=422, detail="Invalid triage status")
    row = db.query(models.ProductFeedback).filter(models.ProductFeedback.id == feedback_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Feedback not found")
    row.triage_status = body.triage_status
    row.triage_note = body.triage_note.strip() if body.triage_note else None
    db.commit()
    db.refresh(row)
    return {
        "id": row.id,
        "triage_status": row.triage_status,
        "triage_note": row.triage_note,
    }


@router.delete("/admin/feedback/{feedback_id}")
@limiter.limit("60/minute")
def admin_delete_feedback(
    feedback_id: int,
    request: Request,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    row = db.query(models.ProductFeedback).filter(models.ProductFeedback.id == feedback_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Feedback not found")
    db.delete(row)
    db.commit()
    return {"deleted": True, "id": feedback_id}


@router.get("/admin/staging/stats")
@limiter.limit("60/minute")
def admin_staging_stats(
    request: Request,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    """Counts of staging rows by status for admin dashboard / monitoring."""
    from sqlalchemy import func

    rows = (
        db.query(models.ScholarshipStaging.status, func.count(models.ScholarshipStaging.id))
        .group_by(models.ScholarshipStaging.status)
        .all()
    )
    counts = {status: int(n) for status, n in rows}
    return {
        "pending": counts.get("pending", 0),
        "approved": counts.get("approved", 0),
        "rejected": counts.get("rejected", 0),
        "total": sum(counts.values()),
    }


@router.get("/admin/scraper-runs/latest")
@limiter.limit("60/minute")
def admin_latest_scraper_runs(
    request: Request,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
    limit: int = Query(20, ge=1, le=100),
):
    rows = (
        db.query(models.ScraperRun)
        .order_by(models.ScraperRun.started_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": r.id,
            "source": r.source,
            "started_at": r.started_at.isoformat() if r.started_at else None,
            "completed_at": r.completed_at.isoformat() if r.completed_at else None,
            "status": r.status,
            "records_found": r.records_found,
            "records_ingested": r.records_ingested,
            "output_path": r.output_path,
            "listing_content_sha256": getattr(r, "listing_content_sha256", None),
            "error_detail": (r.error_detail[:500] + "…") if r.error_detail and len(r.error_detail) > 500 else r.error_detail,
        }
        for r in rows
    ]

