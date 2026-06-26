"""Admin analytics overview."""

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models
from app.auth import get_current_user_id, require_admin
from app.db import get_db
from app.limiter import limiter

router = APIRouter(tags=["analytics"])


@router.get("/admin/analytics/overview")
@limiter.limit("60/minute")
def analytics_overview(
    request: Request,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    total_scholarships = db.query(func.count(models.Scholarship.id)).scalar() or 0
    total_profiles = db.query(func.count(models.Student.id)).scalar() or 0
    total_match_runs = db.query(func.count(models.MatchRun.id)).scalar() or 0

    avg_score = db.query(func.avg(models.MatchResult.final_score)).scalar()
    avg_match_score = float(avg_score) if avg_score is not None else None

    since = datetime.now(timezone.utc) - timedelta(days=30)
    match_runs_last_30 = (
        db.query(func.count(models.MatchRun.id)).filter(models.MatchRun.created_at >= since).scalar() or 0
    )

    # Scholarships by data_status (nullable treated as active for display)
    status_rows = db.query(models.Scholarship.data_status, func.count(models.Scholarship.id)).group_by(
        models.Scholarship.data_status
    ).all()
    scholarships_by_status = {str(s or "unknown"): c for s, c in status_rows}

    region_rows = db.query(models.Student.region, func.count(models.Student.id)).group_by(models.Student.region).all()
    profiles_by_region = {str(r or "unknown"): c for r, c in region_rows if r}

    sch_region_rows = (
        db.query(models.Scholarship.eligible_regions, func.count(models.Scholarship.id))
        .group_by(models.Scholarship.eligible_regions)
        .limit(50)
        .all()
    )
    scholarships_by_region = {str(r or "mixed")[:80]: c for r, c in sch_region_rows}

    total_users = db.query(func.count(models.User.id)).scalar() or 0
    total_applications = db.query(func.count(models.Application.id)).scalar() or 0
    app_status_rows = (
        db.query(models.Application.status, func.count(models.Application.id)).group_by(models.Application.status).all()
    )
    applications_by_status = {str(s): c for s, c in app_status_rows}
    pending_staging = (
        db.query(func.count(models.ScholarshipStaging.id))
        .filter(models.ScholarshipStaging.status == "pending")
        .scalar()
        or 0
    )
    pending_verifications = (
        db.query(func.count(models.VerificationRequest.id))
        .filter(models.VerificationRequest.status == "pending")
        .scalar()
        or 0
    )

    return {
        "total_scholarships": total_scholarships,
        "total_profiles": total_profiles,
        "total_users": total_users,
        "total_match_runs": total_match_runs,
        "total_applications": total_applications,
        "applications_by_status": applications_by_status,
        "pending_staging_rows": pending_staging,
        "pending_verifications": pending_verifications,
        "avg_match_score": avg_match_score,
        "scholarships_by_status": scholarships_by_status,
        "scholarships_by_region": scholarships_by_region,
        "profiles_by_region": profiles_by_region,
        "match_runs_last_30_days": match_runs_last_30,
    }


@router.get("/analytics/student-summary")
@limiter.limit("30/minute")
def student_analytics_summary(
    request: Request,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    """Lightweight funnel-style counts for the signed-in student (non-admin)."""
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    app_rows = db.query(models.Application.status, func.count(models.Application.id)).filter(
        models.Application.user_id == user_id
    ).group_by(models.Application.status).all()
    applications_by_status = {str(s): c for s, c in app_rows}

    saved_count = (
        db.query(func.count(models.SavedScholarship.id))
        .filter(models.SavedScholarship.user_id == user_id)
        .scalar()
        or 0
    )
    profile_count = db.query(func.count(models.Student.id)).filter(models.Student.user_id == user_id).scalar() or 0
    match_runs = db.query(func.count(models.MatchRun.id)).filter(models.MatchRun.user_id == user_id).scalar() or 0

    return {
        "applications_by_status": applications_by_status,
        "saved_scholarships_count": saved_count,
        "has_profile": profile_count > 0,
        "match_runs_count": match_runs,
    }
