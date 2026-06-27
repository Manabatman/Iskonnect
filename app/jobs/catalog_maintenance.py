"""
Unified catalog maintenance: deadline expiry + stale verification flags + cache invalidation.

Run: python -m app.jobs.catalog_maintenance

Used by GitHub Actions deadline workflow (via app.scripts.expire_scholarship_deadlines).
"""
from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import or_, update

from app import models
from app.db import SessionLocal
from app.jobs.data_quality import run_data_quality_checks
from app.scrapers.run_logging import log_scraper_run
from app.scholarship_cache import invalidate_scholarship_cache

logger = logging.getLogger(__name__)


def run_catalog_maintenance() -> dict[str, int]:
    """
    - Past application_deadline: set is_active=False and data_status='expired'.
    - Active rows with stale last_verified_at: set data_status='needs_review'.
    - Invalidate scholarship list cache (Redis + in-process).

    Returns counts: expired_rows_updated, needs_review_rows_updated.
    """
    today = date.today()
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    db = SessionLocal()
    expired_count = 0
    review_count = 0
    try:
        # All rows with a past deadline: inactive + expired (handles NULL data_status safely).
        stmt = (
            update(models.Scholarship)
            .where(
                models.Scholarship.application_deadline.isnot(None),
                models.Scholarship.application_deadline < today,
            )
            .values(is_active=False, data_status="expired")
        )
        result = db.execute(stmt)
        expired_count = result.rowcount or 0

        stale = (
            db.query(models.Scholarship)
            .filter(
                models.Scholarship.data_status == "active",
                or_(
                    models.Scholarship.last_verified_at.is_(None),
                    models.Scholarship.last_verified_at < cutoff,
                ),
            )
            .all()
        )
        for s in stale:
            s.data_status = "needs_review"
            review_count += 1

        db.commit()
        logger.info(
            "catalog_maintenance_done deadline_expired_or_synced=%s needs_review=%s",
            expired_count,
            review_count,
        )
        try:
            invalidate_scholarship_cache()
        except Exception as cache_err:
            logger.warning("catalog_maintenance_cache_invalidate_failed: %s", cache_err)

        quality = run_data_quality_checks()

        log_scraper_run(
            "catalog_maintenance",
            "success",
            records_found=expired_count + review_count,
            records_ingested=expired_count + review_count,
            output_path=None,
            error_detail=None,
        )
        return {"expired": expired_count, "needs_review": review_count, "data_quality": quality}
    except Exception:
        db.rollback()
        logger.exception("catalog_maintenance_failed")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    out = run_catalog_maintenance()
    print(
        f"catalog_maintenance: deadline_synced={out['expired']}, "
        f"needs_review={out['needs_review']}"
    )
