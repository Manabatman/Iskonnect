"""Admin analytics overview and aggregate referral clicks (C9)."""

from datetime import date, datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from pydantic import BaseModel, Field, model_validator
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models
from app.auth import get_current_user_id, require_admin
from app.db import get_db
from app.limiter import limiter
from app.utils.timezone import today_manila

router = APIRouter(tags=["analytics"])

ALLOWED_SURFACES = frozenset({"card", "detail_page", "detail_panel", "trust_source"})
ALLOWED_LINK_KINDS = frozenset({"apply_official", "check_official", "view_source"})


class ReferralClickCreate(BaseModel):
    scholarship_id: int = Field(..., gt=0)
    surface: str = Field(..., min_length=1, max_length=32)
    link_kind: str = Field(..., min_length=1, max_length=32)

    @model_validator(mode="after")
    def validate_enums(self):
        if self.surface not in ALLOWED_SURFACES:
            raise ValueError("invalid surface")
        if self.link_kind not in ALLOWED_LINK_KINDS:
            raise ValueError("invalid link_kind")
        return self


class ReferralClickResponse(BaseModel):
    recorded: bool = True


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

    active_count = (
        db.query(func.count(models.Scholarship.id)).filter(models.Scholarship.is_active != False).scalar() or 0  # noqa: E712
    )
    broken_links = (
        db.query(func.count(models.Scholarship.id))
        .filter(models.Scholarship.is_active != False, models.Scholarship.link_status == "broken")  # noqa: E712
        .scalar()
        or 0
    )
    with_evidence = (
        db.query(func.count(func.distinct(models.FieldEvidence.scholarship_id)))
        .join(models.Scholarship, models.Scholarship.id == models.FieldEvidence.scholarship_id)
        .filter(
            models.Scholarship.is_active != False,  # noqa: E712
            models.FieldEvidence.superseded_at.is_(None),
        )
        .scalar()
        or 0
    )
    missing_precision = (
        db.query(func.count(models.Scholarship.id))
        .filter(models.Scholarship.is_active != False, models.Scholarship.deadline_precision.is_(None))  # noqa: E712
        .scalar()
        or 0
    )

    catalog_quality = {
        "active_scholarships": active_count,
        "broken_links": broken_links,
        "broken_link_pct": round(100.0 * broken_links / active_count, 1) if active_count else 0.0,
        "with_field_evidence": with_evidence,
        "evidence_pct": round(100.0 * with_evidence / active_count, 1) if active_count else 0.0,
        "missing_deadline_precision": missing_precision,
    }

    referral_since = today_manila() - timedelta(days=30)
    referral_clicks_last_30 = (
        db.query(func.coalesce(func.sum(models.ReferralClickDaily.click_count), 0))
        .filter(models.ReferralClickDaily.day >= referral_since)
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
        "catalog_quality": catalog_quality,
        "referral_clicks_last_30_days": int(referral_clicks_last_30),
    }


@router.post("/analytics/referral-clicks", response_model=ReferralClickResponse)
@limiter.limit("120/minute")
def record_referral_click(
    request: Request,
    body: Annotated[ReferralClickCreate, Body()],
    db: Session = Depends(get_db),
):
    """Aggregate-only outbound click counter — no user id, no PII (C9)."""
    day = today_manila()
    exists = (
        db.query(models.Scholarship.id)
        .filter(models.Scholarship.id == body.scholarship_id, models.Scholarship.is_active != False)  # noqa: E712
        .first()
    )
    if not exists:
        raise HTTPException(status_code=404, detail="Scholarship not found")

    row = (
        db.query(models.ReferralClickDaily)
        .filter(
            models.ReferralClickDaily.day == day,
            models.ReferralClickDaily.scholarship_id == body.scholarship_id,
            models.ReferralClickDaily.surface == body.surface,
            models.ReferralClickDaily.link_kind == body.link_kind,
        )
        .first()
    )
    if row:
        row.click_count = (row.click_count or 0) + 1
    else:
        db.add(
            models.ReferralClickDaily(
                day=day,
                scholarship_id=body.scholarship_id,
                surface=body.surface,
                link_kind=body.link_kind,
                click_count=1,
            )
        )
    db.commit()
    return ReferralClickResponse()


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
