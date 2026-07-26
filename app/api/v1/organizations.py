"""Public organization profile and aggregate catalog stats."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models
from app.db import get_db
from app.limiter import limiter
from app.schemas import OrganizationResponse
from app.utils.timezone import utc_now_naive

router = APIRouter(tags=["organizations"])


@router.get("/organizations/{slug}", response_model=OrganizationResponse)
@limiter.limit("60/minute")
def get_organization(
    request: Request,
    slug: str,
    db: Session = Depends(get_db),
):
    """Public organization profile with aggregate opportunity stats."""
    org = db.query(models.Organization).filter(models.Organization.slug == slug).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    opportunity_count = (
        db.query(func.count(models.Scholarship.id))
        .filter(
            models.Scholarship.organization_id == org.id,
            models.Scholarship.is_active == True,  # noqa: E712
        )
        .scalar()
        or 0
    )

    report_count = (
        db.query(func.count(models.ScholarshipReport.id))
        .join(models.Scholarship, models.ScholarshipReport.scholarship_id == models.Scholarship.id)
        .filter(models.Scholarship.organization_id == org.id)
        .scalar()
        or 0
    )

    verified_rows = (
        db.query(models.Scholarship.last_verified_at)
        .filter(
            models.Scholarship.organization_id == org.id,
            models.Scholarship.last_verified_at.isnot(None),
        )
        .all()
    )
    avg_freshness_days: float | None = None
    if verified_rows:
        now = utc_now_naive()
        ages: list[float] = []
        for (verified_at,) in verified_rows:
            if verified_at is None:
                continue
            if isinstance(verified_at, datetime):
                delta = now - verified_at.replace(tzinfo=None) if verified_at.tzinfo else now - verified_at
                ages.append(delta.total_seconds() / 86400.0)
        if ages:
            avg_freshness_days = round(sum(ages) / len(ages), 1)

    return OrganizationResponse(
        slug=org.slug,
        canonical_name=org.canonical_name,
        org_type=org.org_type,
        logo_url=org.logo_url,
        website=org.website,
        verification_status=org.verification_status,
        opportunity_count=int(opportunity_count),
        avg_freshness_days=avg_freshness_days,
        report_count=int(report_count),
    )
