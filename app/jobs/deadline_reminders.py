"""
Notify users about upcoming deadlines for saved scholarships (ENABLE_NOTIFICATIONS).
Run: python -m app.jobs.deadline_reminders
"""

from __future__ import annotations

import logging

from app.config import settings
from app.db import SessionLocal
from app import models
from app.utils.notification_helpers import maybe_notify_deadline_from_row

logger = logging.getLogger(__name__)

HORIZON_DAYS = 7


def run_deadline_reminders() -> dict[str, int]:
    if not settings.enable_notifications:
        logger.warning("deadline_reminders_skipped enable_notifications=false")
        return {"skipped": True, "created": 0}

    db = SessionLocal()
    created = 0
    try:
        saved = db.query(models.SavedScholarship).all()
        for s in saved:
            sch = db.query(models.Scholarship).filter(models.Scholarship.id == s.scholarship_id).first()
            if not sch:
                continue
            if maybe_notify_deadline_from_row(db, s.user_id, sch, horizon_days=HORIZON_DAYS):
                created += 1
        db.commit()
        logger.info("deadline_reminders_done created=%s", created)
        return {"created": created}
    except Exception:
        db.rollback()
        logger.exception("deadline_reminders_failed")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(run_deadline_reminders())
