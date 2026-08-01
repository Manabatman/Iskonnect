"""Public catalog trust signals (no auth)."""

from __future__ import annotations

from datetime import timedelta

from fastapi import APIRouter, Depends, Request
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models
from app.db import get_db
from app.limiter import limiter
from app.schemas import CatalogTrustResponse
from app.utils.timezone import utc_now_naive
from app.utils.trust_constants import VERIFICATION_FRESH_DAYS

router = APIRouter(tags=["public"])


@router.get("/public/catalog-trust", response_model=CatalogTrustResponse)
@limiter.limit("60/minute")
def get_catalog_trust(
    request: Request,
    db: Session = Depends(get_db),
):
    """Aggregate verification posture for the active catalog (public, no PII)."""
    active = models.Scholarship.is_active == True  # noqa: E712
    now = utc_now_naive()
    fresh_cutoff = now - timedelta(days=VERIFICATION_FRESH_DAYS)

    published_count = db.query(func.count(models.Scholarship.id)).filter(active).scalar() or 0
    last_catalog_verification_at = (
        db.query(func.max(models.Scholarship.last_verified_at))
        .filter(active, models.Scholarship.last_verified_at.isnot(None))
        .scalar()
    )
    verified_within_90d_count = (
        db.query(func.count(models.Scholarship.id))
        .filter(active, models.Scholarship.last_verified_at >= fresh_cutoff)
        .scalar()
        or 0
    )

    return CatalogTrustResponse(
        published_count=int(published_count),
        last_catalog_verification_at=last_catalog_verification_at,
        verified_within_90d_count=int(verified_within_90d_count),
        verification_fresh_days=VERIFICATION_FRESH_DAYS,
    )
