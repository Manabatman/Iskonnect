"""
Weekly digest notifications: reopening opportunities + match highlights.
Run: python -m app.jobs.weekly_digest
"""

from __future__ import annotations

import logging

from app import models
from app.api.v1.profiles import get_profile_dict
from app.api.v1.scholarships import get_cached_scholarship_dicts
from app.config import settings
from app.db import SessionLocal
from app.matching.opportunity_timeline import build_opportunity_timeline
from app.matching.match_service import MatchService
from app.utils.notification_helpers import notification_exists_recently

logger = logging.getLogger(__name__)
DEDUP_DAYS = 7


def run_weekly_digest() -> dict[str, int]:
    if not settings.enable_notifications:
        logger.warning("weekly_digest_skipped enable_notifications=false")
        return {"skipped": True, "created": 0}

    db = SessionLocal()
    created = 0
    try:
        users = db.query(models.User).all()
        scholarships = get_cached_scholarship_dicts(db)
        svc = MatchService()
        for user in users:
            profile_row = db.query(models.Student).filter(models.Student.user_id == user.id).first()
            if not profile_row:
                continue
            profile = get_profile_dict(profile_row.id, db)
            if not profile:
                continue
            results, _ = svc.get_matches(profile, scholarships)
            timeline = build_opportunity_timeline(profile, scholarships, results)
            summary = timeline.get("summary") or {}
            reopening = summary.get("expected_reopening", 0)
            actionable = summary.get("total_actionable", 0)

            if reopening > 0:
                if not notification_exists_recently(
                    db, user.id, "reopening_alert", scholarship_id=None, days=DEDUP_DAYS
                ):
                    db.add(
                        models.Notification(
                            user_id=user.id,
                            type="reopening_alert",
                            title=f"{reopening} scholarship(s) expected to reopen",
                            body=timeline.get("headline"),
                            is_read=False,
                        )
                    )
                    created += 1

            if actionable > 0:
                if not notification_exists_recently(db, user.id, "weekly_digest", scholarship_id=None, days=DEDUP_DAYS):
                    strong = [r for r in results if (r.get("final_score") or 0) >= 70][:3]
                    preview = "; ".join((r.get("title") or "")[:40] for r in strong)
                    db.add(
                        models.Notification(
                            user_id=user.id,
                            type="weekly_digest",
                            title=f"Your week ahead: {actionable} opportunities",
                            body=preview or timeline.get("headline"),
                            is_read=False,
                        )
                    )
                    created += 1

        db.commit()
        logger.info("weekly_digest_done created=%s", created)
        return {"created": created}
    except Exception:
        db.rollback()
        logger.exception("weekly_digest_failed")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(run_weekly_digest())
