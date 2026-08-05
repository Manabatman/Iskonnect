"""Automated catalog data-quality checks (read-only counts)."""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import and_, cast, func, or_, String

from app import models
from app.db import SessionLocal

logger = logging.getLogger(__name__)


def _empty_json_list_col(col):
    """NULL, blank, or JSON empty list — works on SQLite text and Postgres jsonb."""
    as_text = func.trim(func.coalesce(cast(col, String), ""))
    return or_(col.is_(None), as_text == "", as_text == "[]")


def _empty_text_col(col):
    return or_(col.is_(None), func.trim(func.coalesce(col, "")) == "")


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
                _empty_text_col(models.Scholarship.regions),
                _empty_json_list_col(models.Scholarship.eligible_regions),
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


def recompute_completeness_scores() -> int:
    """Recompute data_completeness_score for all active scholarships. Returns rows updated."""
    from app.utils.data_completeness import compute_data_completeness_score
    from app.scholarship_cache import invalidate_scholarship_cache

    db = SessionLocal()
    updated = 0
    try:
        rows = db.query(models.Scholarship).filter(models.Scholarship.is_active == True).all()  # noqa: E712
        for row in rows:
            score = compute_data_completeness_score(row)
            if row.data_completeness_score != score:
                row.data_completeness_score = score
                updated += 1
        db.commit()
        if updated:
            invalidate_scholarship_cache()
        logger.info("recompute_completeness_scores updated=%s", updated)
        return updated
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def count_structured_eligibility_gaps() -> int:
    """
    Count active scholarships with no structured eligibility dimensions encoded.
    Used to size the structured-eligibility backfill program.
    """
    db = SessionLocal()
    try:
        rows = (
            db.query(func.count(models.Scholarship.id))
            .filter(
                models.Scholarship.is_active == True,  # noqa: E712
                _empty_json_list_col(models.Scholarship.eligible_levels),
                _empty_json_list_col(models.Scholarship.eligible_regions),
                _empty_json_list_col(models.Scholarship.eligible_cities),
                models.Scholarship.max_income_threshold.is_(None),
                models.Scholarship.min_gwa_normalized.is_(None),
                _empty_json_list_col(models.Scholarship.eligible_courses_psced),
                _empty_json_list_col(models.Scholarship.eligible_courses_specific),
            )
            .scalar()
            or 0
        )
        return int(rows)
    finally:
        db.close()
