"""Admin review queue endpoints for solo-operator scholarship maintenance."""

from __future__ import annotations

from datetime import date, datetime, timedelta
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
from app.utils.data_completeness import (
    PUBLISHABILITY_THRESHOLD,
    completeness_gaps,
    completeness_tier,
    compute_data_completeness_score,
)
from app.utils.editorial_state import PUBLISHED, apply_editorial_state
from app.utils.opportunity_quality import apply_quality_scores, compute_opportunity_quality
from app.utils.quality_score import needs_review_reasons
from app.utils.trust_constants import STALE_VERIFICATION_DAYS, VERIFICATION_FRESH_DAYS
from app.utils.timezone import utc_now_naive

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
    stale_cutoff = utc_now_naive() - timedelta(days=STALE_VERIFICATION_DAYS)

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
        quality = compute_opportunity_quality(s, db)
        payload = _scholarship_to_response(s)
        if hasattr(payload, "model_dump"):
            data = payload.model_dump()
        else:
            data = dict(payload)
        data["confidence_score"] = round(quality.score / 100.0, 3)
        data["quality_score"] = quality.score
        data["review_reasons"] = needs_review_reasons(s)
        if queue_name == "duplicates":
            data["match_type"] = "dedupe_key"
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
    result = apply_quality_scores(s, db)
    db.commit()
    return {
        "id": s.id,
        "confidence_score": s.confidence_score,
        "quality_score": result.score,
        "review_reasons": needs_review_reasons(s),
    }


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
    apply_editorial_state(s, PUBLISHED)
    apply_quality_scores(s, db)
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
    stale_cutoff = utc_now_naive() - timedelta(days=STALE_VERIFICATION_DAYS)
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
    stale_cutoff = utc_now_naive() - timedelta(days=VERIFICATION_FRESH_DAYS)
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
        quality = compute_opportunity_quality(row, db)
        scores.append(int(quality.score))
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
        if int(quality.score) < 70:
            priority_queue.append(
                {
                    "id": row.id,
                    "title": row.title,
                    "completeness_score": int(score),
                    "quality_score": int(quality.score),
                    "gaps": completeness_gaps(row)[:5],
                }
            )

    priority_queue.sort(key=lambda x: x.get("quality_score", x["completeness_score"]))
    avg_completeness = round(sum(compute_data_completeness_score(r) if r.data_completeness_score is None else r.data_completeness_score for r in rows) / len(rows), 1) if rows else 0.0
    avg_quality = round(sum(scores) / len(scores), 1) if scores else 0.0

    return {
        "as_of": today.isoformat(),
        "publishability_threshold": PUBLISHABILITY_THRESHOLD,
        "total_active": len(rows),
        "average_completeness": avg_completeness,
        "average_quality_score": avg_quality,
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


def _verification_age_metrics(db: Session) -> dict:
    """Verification freshness buckets and per-provider SLA breaches (DATA-11)."""
    now = utc_now_naive()
    stale_cutoff = now - timedelta(days=STALE_VERIFICATION_DAYS)
    fresh_cutoff = now - timedelta(days=VERIFICATION_FRESH_DAYS)
    buckets = {"0_30": 0, "31_90": 0, "90_plus": 0, "never": 0}
    provider_breaches: dict[str, int] = {}

    rows = db.query(models.Scholarship).filter(models.Scholarship.is_active == True).all()  # noqa: E712
    for row in rows:
        verified_at = row.last_verified_at
        if verified_at is None:
            buckets["never"] += 1
        elif verified_at >= stale_cutoff:
            buckets["0_30"] += 1
            continue
        elif verified_at >= fresh_cutoff:
            buckets["31_90"] += 1
        else:
            buckets["90_plus"] += 1

        if verified_at is None or verified_at < fresh_cutoff:
            label = (row.provider or "Unknown").strip() or "Unknown"
            provider_breaches[label] = provider_breaches.get(label, 0) + 1

    provider_sla = [
        {"provider": name, "expired_count": count}
        for name, count in sorted(provider_breaches.items(), key=lambda x: (-x[1], x[0]))[:15]
    ]
    return {
        "verification_sla_days": VERIFICATION_FRESH_DAYS,
        "verification_age_distribution": buckets,
        "provider_verification_sla": provider_sla,
    }


@router.get("/admin/dashboard/catalog-health")
@limiter.limit("30/minute")
def admin_catalog_health_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    """Consolidated catalog health: health, import, and data-quality metrics."""
    health = admin_scholarship_health_dashboard(request, db, _admin)
    import_stats = admin_import_dashboard(request, db, _admin)
    quality = admin_data_quality_dashboard(request, db, _admin)

    today = date.today()
    month_start = today.replace(day=1)
    institution_specific_count = (
        db.query(func.count(models.Scholarship.id))
        .filter(
            models.Scholarship.is_active == True,  # noqa: E712
            models.Scholarship.provider_type == "Institutional",
        )
        .scalar()
        or 0
    )
    deadline_unknown_count = (
        db.query(func.count(models.Scholarship.id))
        .filter(
            models.Scholarship.is_active == True,  # noqa: E712
            models.Scholarship.application_deadline.is_(None),
        )
        .scalar()
        or 0
    )
    month_start_dt = datetime.combine(month_start, datetime.min.time())
    verified_this_month = (
        db.query(func.count(models.Scholarship.id))
        .filter(
            models.Scholarship.last_verified_at.isnot(None),
            models.Scholarship.last_verified_at >= month_start_dt,
        )
        .scalar()
        or 0
    )
    verification_metrics = _verification_age_metrics(db)

    return {
        "as_of": today.isoformat(),
        "health": health,
        "import": import_stats,
        "data_quality": quality,
        "institution_specific_count": int(institution_specific_count),
        "deadline_unknown_count": int(deadline_unknown_count),
        "avg_quality_score": quality.get("average_quality_score", 0),
        "verified_this_month": int(verified_this_month),
        **verification_metrics,
    }
