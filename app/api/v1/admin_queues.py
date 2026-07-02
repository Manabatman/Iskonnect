"""Admin review queue endpoints for solo-operator scholarship maintenance."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app import models
from app.api.v1.scholarships import _scholarship_to_response
from app.auth import require_admin
from app.db import get_db
from app.limiter import limiter
from app.utils.application_status import sync_application_status
from app.utils.quality_score import compute_confidence_score, needs_review_reasons
from app.utils.data_completeness import (
    PUBLISHABILITY_THRESHOLD,
    completeness_gaps,
    completeness_tier,
    compute_data_completeness_score,
)
from app.utils.scholarship_persist import utc_now_naive

router = APIRouter(tags=["admin-queues"])

QueueName = Literal[
    "needs_review",
    "stale",
    "low_quality",
    "missing_image",
    "duplicates",
    "reports",
]


@router.get("/admin/queues/{queue_name}")
@limiter.limit("60/minute")
def admin_review_queue(
    request: Request,
    queue_name: QueueName,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
):
    """Paginated admin review queues for scholarship maintenance."""
    offset = (page - 1) * limit
    today = date.today()
    stale_cutoff = datetime.now(timezone.utc) - timedelta(days=30)

    if queue_name == "needs_review":
        q = db.query(models.Scholarship).filter(models.Scholarship.data_status == "needs_review")
    elif queue_name == "stale":
        q = db.query(models.Scholarship).filter(
            models.Scholarship.is_active == True,  # noqa: E712
            or_(
                models.Scholarship.last_verified_at.is_(None),
                models.Scholarship.last_verified_at < stale_cutoff,
            ),
        )
    elif queue_name == "missing_image":
        q = db.query(models.Scholarship).filter(
            models.Scholarship.is_active == True,  # noqa: E712
            or_(models.Scholarship.image_url.is_(None), models.Scholarship.image_url == ""),
        )
    elif queue_name == "low_quality":
        q = db.query(models.Scholarship).filter(
            models.Scholarship.is_active == True,  # noqa: E712
            or_(
                models.Scholarship.confidence_score.is_(None),
                models.Scholarship.confidence_score < 0.5,
            ),
        )
    elif queue_name == "duplicates":
        dup_keys = (
            db.query(models.Scholarship.dedupe_key)
            .filter(models.Scholarship.dedupe_key.isnot(None))
            .group_by(models.Scholarship.dedupe_key)
            .having(func.count(models.Scholarship.id) > 1)
            .all()
        )
        keys = [k[0] for k in dup_keys]
        if not keys:
            return {"queue": queue_name, "total": 0, "page": page, "limit": limit, "items": []}
        q = db.query(models.Scholarship).filter(models.Scholarship.dedupe_key.in_(keys))
    elif queue_name == "reports":
        rows = (
            db.query(models.ScholarshipReport)
            .filter(models.ScholarshipReport.status == "pending")
            .order_by(models.ScholarshipReport.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        total = (
            db.query(func.count(models.ScholarshipReport.id))
            .filter(models.ScholarshipReport.status == "pending")
            .scalar()
            or 0
        )
        return {
            "queue": queue_name,
            "total": int(total),
            "page": page,
            "limit": limit,
            "items": [
                {
                    "id": r.id,
                    "scholarship_id": r.scholarship_id,
                    "issue_type": r.issue_type,
                    "description": r.description,
                    "status": r.status,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                }
                for r in rows
            ],
        }
    else:
        q = db.query(models.Scholarship).filter(False)

    rows = q.order_by(models.Scholarship.id.desc()).offset(offset).limit(limit).all()
    items = []
    for s in rows:
        score = compute_confidence_score(s)
        payload = _scholarship_to_response(s)
        if hasattr(payload, "model_dump"):
            data = payload.model_dump()
        else:
            data = dict(payload)
        data["confidence_score"] = score
        data["review_reasons"] = needs_review_reasons(s)
        items.append(data)

    total = q.count()

    return {
        "queue": queue_name,
        "total": int(total),
        "page": page,
        "limit": limit,
        "items": items,
    }


@router.post("/admin/scholarships/{scholarship_id}/recompute-quality")
@limiter.limit("60/minute")
def recompute_scholarship_quality(
    request: Request,
    scholarship_id: int,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    s = db.query(models.Scholarship).filter(models.Scholarship.id == scholarship_id).first()
    if not s:
        return {"detail": "not found"}
    s.confidence_score = compute_confidence_score(s)
    db.commit()
    return {"id": s.id, "confidence_score": s.confidence_score, "review_reasons": needs_review_reasons(s)}


@router.post("/admin/scholarships/{scholarship_id}/verify-refresh")
@limiter.limit("60/minute")
def verify_refresh_scholarship(
    request: Request,
    scholarship_id: int,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    """One-click verification refresh for scholarship health ops."""
    s = db.query(models.Scholarship).filter(models.Scholarship.id == scholarship_id).first()
    if not s:
        return {"detail": "not found"}
    s.last_verified_at = utc_now_naive()
    if s.data_status in (None, "", "needs_review"):
        s.data_status = "active"
    s.confidence_score = compute_confidence_score(s)
    sync_application_status(s)
    db.commit()
    from app.scholarship_cache import invalidate_scholarship_cache

    invalidate_scholarship_cache()
    return {
        "id": s.id,
        "last_verified_at": s.last_verified_at.isoformat() if s.last_verified_at else None,
        "confidence_score": s.confidence_score,
        "data_status": s.data_status,
        "application_status": s.application_status,
    }


@router.get("/admin/dashboard/health")
@limiter.limit("30/minute")
def admin_scholarship_health_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    """Scholarship catalog health summary for admin dashboard."""
    today = date.today()
    stale_cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    total = db.query(func.count(models.Scholarship.id)).scalar() or 0
    active = (
        db.query(func.count(models.Scholarship.id))
        .filter(models.Scholarship.is_active == True)  # noqa: E712
        .scalar()
        or 0
    )
    needs_review = (
        db.query(func.count(models.Scholarship.id))
        .filter(models.Scholarship.data_status == "needs_review")
        .scalar()
        or 0
    )
    stale = (
        db.query(func.count(models.Scholarship.id))
        .filter(
            models.Scholarship.is_active == True,  # noqa: E712
            or_(
                models.Scholarship.last_verified_at.is_(None),
                models.Scholarship.last_verified_at < stale_cutoff,
            ),
        )
        .scalar()
        or 0
    )
    expired = (
        db.query(func.count(models.Scholarship.id))
        .filter(models.Scholarship.data_status.in_(["expired", "past_deadline"]))
        .scalar()
        or 0
    )
    missing_image = (
        db.query(func.count(models.Scholarship.id))
        .filter(
            models.Scholarship.is_active == True,  # noqa: E712
            or_(models.Scholarship.image_url.is_(None), models.Scholarship.image_url == ""),
        )
        .scalar()
        or 0
    )
    pending_reports = (
        db.query(func.count(models.ScholarshipReport.id))
        .filter(models.ScholarshipReport.status == "pending")
        .scalar()
        or 0
    )
    return {
        "as_of": today.isoformat(),
        "total": int(total),
        "active": int(active),
        "needs_review": int(needs_review),
        "stale_verification": int(stale),
        "expired_or_closed": int(expired),
        "missing_image": int(missing_image),
        "pending_reports": int(pending_reports),
    }


@router.get("/admin/dashboard/import")
@limiter.limit("30/minute")
def admin_import_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    """Import pipeline summary: staging queue and recent maintenance job runs."""
    staging_pending = (
        db.query(func.count(models.ScholarshipStaging.id))
        .filter(models.ScholarshipStaging.status == "pending")
        .scalar()
        or 0
    )
    staging_total = db.query(func.count(models.ScholarshipStaging.id)).scalar() or 0
    recent_runs = (
        db.query(models.ScraperRun)
        .order_by(models.ScraperRun.started_at.desc())
        .limit(10)
        .all()
    )
    return {
        "staging_pending": int(staging_pending),
        "staging_total": int(staging_total),
        "recent_maintenance_runs": [
            {
                "id": r.id,
                "source": r.source,
                "status": r.status,
                "records_found": r.records_found,
                "records_ingested": r.records_ingested,
                "started_at": r.started_at.isoformat() if r.started_at else None,
                "completed_at": r.completed_at.isoformat() if r.completed_at else None,
                "error_detail": r.error_detail,
            }
            for r in recent_runs
        ],
    }


@router.get("/admin/data-quality")
@limiter.limit("30/minute")
def admin_data_quality_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    """Scholarship data quality health metrics for admin operations."""
    today = date.today()
    stale_cutoff = datetime.now(timezone.utc) - timedelta(days=90)
    rows = db.query(models.Scholarship).filter(models.Scholarship.is_active == True).all()  # noqa: E712

    scores: list[int] = []
    tier_counts = {"verified_ready": 0, "usable": 0, "needs_work": 0}
    gap_counts: dict[str, int] = {}
    missing_residency = 0
    missing_income = 0
    missing_courses = 0
    expired_verification = 0
    below_publishable = 0
    priority_queue: list[dict] = []

    for row in rows:
        score = row.data_completeness_score
        if score is None:
            score = compute_data_completeness_score(row)
        scores.append(int(score))
        tier = completeness_tier(int(score))
        tier_counts[tier] = tier_counts.get(tier, 0) + 1
        if int(score) < PUBLISHABILITY_THRESHOLD:
            below_publishable += 1
        for gap in completeness_gaps(row):
            gap_counts[gap] = gap_counts.get(gap, 0) + 1
            if gap == "missing_residency_rules":
                missing_residency += 1
            elif gap == "missing_income_rules":
                missing_income += 1
            elif gap == "missing_course_restrictions":
                missing_courses += 1
        if row.last_verified_at is None or row.last_verified_at < stale_cutoff:
            expired_verification += 1
        if int(score) < 70:
            priority_queue.append(
                {
                    "id": row.id,
                    "title": row.title,
                    "completeness_score": int(score),
                    "gaps": completeness_gaps(row)[:5],
                }
            )

    priority_queue.sort(key=lambda x: x["completeness_score"])
    avg = round(sum(scores) / len(scores), 1) if scores else 0.0

    return {
        "as_of": today.isoformat(),
        "publishability_threshold": PUBLISHABILITY_THRESHOLD,
        "total_active": len(rows),
        "average_completeness": avg,
        "tier_distribution": tier_counts,
        "below_publishable_threshold": below_publishable,
        "needs_review": sum(1 for r in rows if r.data_status == "needs_review"),
        "missing_residency_rules": missing_residency,
        "missing_income_rules": missing_income,
        "missing_course_restrictions": missing_courses,
        "expired_verification": expired_verification,
        "gap_counts": gap_counts,
        "high_priority_records": priority_queue[:25],
    }
