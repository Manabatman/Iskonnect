"""Additional read-only admin list endpoints for the admin dashboard UI."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app import models
from app.auth import require_admin
from app.db import get_db
from app.limiter import limiter
from app.utils.timezone import to_philippine_iso

router = APIRouter(tags=["admin-extended"])


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
    out = []
    for r in runs:
        cnt = db.query(models.MatchResult).filter(models.MatchResult.run_id == r.id).count()
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
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "ph_created_at": to_philippine_iso(r.created_at) if r.created_at else None,
        }
        for r in rows
    ]


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
            "error_detail": (r.error_detail[:500] + "…") if r.error_detail and len(r.error_detail) > 500 else r.error_detail,
        }
        for r in rows
    ]
