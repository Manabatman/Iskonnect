"""Admin analytics overview."""

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models
from app.auth import require_admin
from app.db import get_db

router = APIRouter(tags=["analytics"])


@router.get("/admin/analytics/overview")
def analytics_overview(
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

    return {
        "total_scholarships": total_scholarships,
        "total_profiles": total_profiles,
        "total_match_runs": total_match_runs,
        "avg_match_score": avg_match_score,
        "scholarships_by_status": scholarships_by_status,
        "scholarships_by_region_sample": scholarships_by_region,
        "profiles_by_region": profiles_by_region,
        "match_runs_last_30_days": match_runs_last_30,
    }
