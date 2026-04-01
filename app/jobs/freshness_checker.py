"""
Mark scholarships expired by deadline; flag stale verification (>30 days) as needs_review.
Run: python -m app.jobs.freshness_checker
"""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import or_

from app.db import SessionLocal
from app import models

logger = logging.getLogger(__name__)


def run_freshness_check() -> tuple[int, int]:
    """
    Returns (expired_count, needs_review_count).
    """
    db = SessionLocal()
    expired_count = 0
    review_count = 0
    try:
        today = date.today()
        cutoff = datetime.now(timezone.utc) - timedelta(days=30)

        # Expired by deadline
        expired_rows = (
            db.query(models.Scholarship)
            .filter(
                models.Scholarship.application_deadline.isnot(None),
                models.Scholarship.application_deadline < today,
                models.Scholarship.data_status != "expired",
            )
            .all()
        )
        for s in expired_rows:
            s.data_status = "expired"
            expired_count += 1

        # Stale verification: active rows with no recent verification
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
            "freshness_checker_done expired=%s needs_review=%s",
            expired_count,
            review_count,
        )
        return expired_count, review_count
    except Exception:
        db.rollback()
        logger.exception("freshness_checker_failed")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    e, r = run_freshness_check()
    print(f"expired={e} needs_review={r}")
