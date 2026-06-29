"""Automated catalog data-quality checks (read-only counts)."""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import func, or_

from app import models
from app.db import SessionLocal

logger = logging.getLogger(__name__)


def run_data_quality_checks() -> dict[str, int]:
    """
    Return counts of common catalog issues for admin monitoring.
    Does not mutate rows.
    """
    db = SessionLocal()
    today = date.today()
    stale_cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    orphan_cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    try:
        duplicate_rows = (
            db.query(models.Scholarship.dedupe_key)
            .filter(models.Scholarship.dedupe_key.isnot(None))
            .group_by(models.Scholarship.dedupe_key)
            .having(func.count(models.Scholarship.id) > 1)
            .all()
        )
        duplicate_dedupe = len(duplicate_rows)

        missing_deadline = (
            db.query(func.count(models.Scholarship.id))
            .filter(
                models.Scholarship.is_active == True,  # noqa: E712
                models.Scholarship.application_deadline.is_(None),
            )
            .scalar()
            or 0
        )

        broken_links = (
            db.query(func.count(models.Scholarship.id))
            .filter(models.Scholarship.link_status == "broken")
            .scalar()
            or 0
        )

        missing_provider = (
            db.query(func.count(models.Scholarship.id))
            .filter(
                models.Scholarship.is_active == True,  # noqa: E712
                or_(models.Scholarship.provider.is_(None), models.Scholarship.provider == ""),
            )
            .scalar()
            or 0
        )

        missing_regions = (
            db.query(func.count(models.Scholarship.id))
            .filter(
                models.Scholarship.is_active == True,  # noqa: E712
                or_(models.Scholarship.regions.is_(None), models.Scholarship.regions == ""),
                or_(models.Scholarship.eligible_regions.is_(None), models.Scholarship.eligible_regions == ""),
            )
            .scalar()
            or 0
        )

        stale_scholarships = (
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

        orphan_staging = (
            db.query(func.count(models.ScholarshipStaging.id))
            .filter(
                models.ScholarshipStaging.status == "pending",
                models.ScholarshipStaging.created_at < orphan_cutoff,
            )
            .scalar()
            or 0
        )

        expired_active = (
            db.query(func.count(models.Scholarship.id))
            .filter(
                models.Scholarship.is_active == True,  # noqa: E712
                models.Scholarship.application_deadline.isnot(None),
                models.Scholarship.application_deadline < today,
            )
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

        low_quality = (
            db.query(func.count(models.Scholarship.id))
            .filter(
                models.Scholarship.is_active == True,  # noqa: E712
                or_(
                    models.Scholarship.confidence_score.is_(None),
                    models.Scholarship.confidence_score < 0.5,
                ),
            )
            .scalar()
            or 0
        )

        result = {
            "duplicate_dedupe_keys": int(duplicate_dedupe),
            "missing_deadline_active": int(missing_deadline),
            "broken_links": int(broken_links),
            "missing_provider_active": int(missing_provider),
            "missing_regions_active": int(missing_regions),
            "stale_verification_active": int(stale_scholarships),
            "orphan_staging_pending_30d": int(orphan_staging),
            "expired_deadline_still_active": int(expired_active),
            "missing_image_active": int(missing_image),
            "low_quality_active": int(low_quality),
        }
        logger.info("data_quality_checks %s", result)
        return result
    finally:
        db.close()
