"""
Notify users about upcoming deadlines for saved scholarships (ENABLE_NOTIFICATIONS).
Run: python -m app.jobs.deadline_reminders
"""

from __future__ import annotations

import logging
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.config import settings
from app.db import SessionLocal
from app import models

logger = logging.getLogger(__name__)

HORIZON_DAYS = 7


def run_deadline_reminders() -> dict[str, int]:
    if not settings.enable_notifications:
        logger.warning("deadline_reminders_skipped enable_notifications=false")
        return {"skipped": True, "created": 0}

    db = SessionLocal()
    created = 0
    try:
        today = date.today()
        horizon = today + timedelta(days=HORIZON_DAYS)
        saved = db.query(models.SavedScholarship).all()
        for s in saved:
            sch = db.query(models.Scholarship).filter(models.Scholarship.id == s.scholarship_id).first()
            if not sch or not sch.application_deadline:
                continue
            d = sch.application_deadline
            if isinstance(d, str):
                continue
            if d < today or d > horizon:
                continue
            exists = (
                db.query(models.Notification)
                .filter(
                    models.Notification.user_id == s.user_id,
                    models.Notification.scholarship_id == s.scholarship_id,
                    models.Notification.type == "deadline_approaching",
                )
                .first()
            )
            if exists:
                continue
            db.add(
                models.Notification(
                    user_id=s.user_id,
                    type="deadline_approaching",
                    title=f"Deadline soon: {(sch.title or '')[:100]}",
                    body=f"Application deadline is {d.isoformat()}.",
                    scholarship_id=s.scholarship_id,
                    is_read=False,
                )
            )
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
