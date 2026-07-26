"""
Unified catalog maintenance: deadline expiry + stale verification flags + cache invalidation.

Run: python -m app.jobs.catalog_maintenance

Used by GitHub Actions deadline workflow (via app.scripts.expire_scholarship_deadlines).
"""
from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import and_, or_, update

from app import models
from app.db import SessionLocal
from app.jobs.data_quality import run_data_quality_checks
from app.utils.job_run_logging import log_job_run
from app.scholarship_cache import invalidate_scholarship_cache
from app.utils.application_status import sync_application_status
from app.utils.editorial_state import NEEDS_REVIEW, apply_editorial_state, sync_legacy_fields_from_editorial
from app.utils.trust_constants import STALE_VERIFICATION_DAYS

logger = logging.getLogger(__name__)


def run_catalog_maintenance() -> dict[str, int]:
    """
    - Past application_deadline: set data_status='expired' and sync application_status (keep searchable).
    - Active rows with stale last_verified_at: set data_status='needs_review' and sync application_status.
    - Invalidate scholarship list cache (Redis + in-process).

    Returns counts: expired_rows_updated, needs_review_rows_updated.
    """
    today = date.today()
    stale_cutoff = datetime.now(timezone.utc) - timedelta(days=STALE_VERIFICATION_DAYS)
    db = SessionLocal()
    expired_count = 0
    review_count = 0
    try:
        stmt = (
            update(models.Scholarship)
            .where(
                models.Scholarship.application_deadline.isnot(None),
                models.Scholarship.application_deadline < today,
            )
            .values(data_status="expired", editorial_state="archived", is_active=False)
        )
        result = db.execute(stmt)
        expired_count = result.rowcount or 0

        legacy = (
            db.query(models.Scholarship)
            .filter(models.Scholarship.data_status == "past_deadline")
            .all()
        )
        for s in legacy:
            apply_editorial_state(s, "archived", today=today)
            sync_application_status(s, today=today)
            expired_count += 1

        stale = (
            db.query(models.Scholarship)
            .filter(
                models.Scholarship.data_status == "active",
                or_(
                    models.Scholarship.last_verified_at.is_(None),
                    models.Scholarship.last_verified_at < stale_cutoff,
                ),
            )
            .all()
        )
        for s in stale:
            apply_editorial_state(s, NEEDS_REVIEW, today=today)
            sync_application_status(s, today=today)
            review_count += 1

        broken_open = (
            db.query(models.Scholarship)
            .filter(
                models.Scholarship.data_status == "broken_link",
                models.Scholarship.application_status == "open",
            )
            .all()
        )
        broken_link_demoted = 0
        for s in broken_open:
            apply_editorial_state(s, NEEDS_REVIEW, today=today)
            sync_application_status(s, today=today)
            broken_link_demoted += 1
            review_count += 1

        # Sync application_status for deadline-expired rows and any stale values
        expired_rows = (
            db.query(models.Scholarship)
            .filter(
                or_(
                    models.Scholarship.data_status.in_(["expired", "past_deadline"]),
                    and_(
                        models.Scholarship.application_deadline.isnot(None),
                        models.Scholarship.application_deadline < today,
                    ),
                )
            )
            .all()
        )
        for s in expired_rows:
            sync_legacy_fields_from_editorial(s, today=today)
            sync_application_status(s, today=today)

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
        from app.jobs.data_quality import recompute_completeness_scores, count_structured_eligibility_gaps
        from app.utils.opportunity_quality import apply_quality_scores

        completeness_updated = recompute_completeness_scores()
        for row in db.query(models.Scholarship).filter(models.Scholarship.is_active == True).all():  # noqa: E712
            apply_quality_scores(row, db)
        db.commit()
        structured_gaps = count_structured_eligibility_gaps()

        log_job_run(
            "catalog_maintenance",
            "success",
            records_found=expired_count + review_count,
            records_ingested=expired_count + review_count,
            output_path=None,
            error_detail=None,
        )
        return {
            "expired": expired_count,
            "needs_review": review_count,
            "data_quality": quality,
            "completeness_updated": completeness_updated,
            "structured_eligibility_gaps": structured_gaps,
        }
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
