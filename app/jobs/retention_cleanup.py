"""
Flag user accounts with no recent match activity for admin review (does not delete).
Run: python -m app.jobs.retention_cleanup
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import func

from app.config import settings
from app.db import SessionLocal
from app import models
from app.utils.audit import log_action

logger = logging.getLogger(__name__)


def run_retention_scan() -> dict:
    """
    Users linked to a profile who have zero match_runs in the last RETENTION_INACTIVE_DAYS
    get an audit log entry (candidate for review).
    """
    db = SessionLocal()
    stats = {"candidates": 0, "error": None}
    try:
        cutoff = datetime.now(timezone.utc) - timedelta(days=settings.retention_inactive_days)
        user_ids = [
            r[0]
            for r in db.query(models.Student.user_id).filter(models.Student.user_id.isnot(None)).distinct().all()
        ]
        stale: list[int] = []
        for uid in user_ids:
            last_run = (
                db.query(func.max(models.MatchRun.created_at)).filter(models.MatchRun.user_id == uid).scalar()
            )
            if last_run is None or last_run < cutoff:
                stale.append(uid)
                stats["candidates"] += 1
        if stale:
            try:
                log_action(
                    db,
                    actor_id=None,
                    actor_type="system",
                    action="retention.scan",
                    resource_type="users",
                    resource_id=None,
                    details={
                        "reason": "no_recent_match_activity",
                        "inactive_days_threshold": settings.retention_inactive_days,
                        "user_ids": stale[:100],
                        "total": len(stale),
                    },
                    ip_address=None,
                )
                db.commit()
            except Exception as audit_err:
                db.rollback()
                logger.exception("retention_audit_failed: %s", audit_err)
                stats["error"] = str(audit_err)
        logger.info("retention_scan_done %s", stats)
        return stats
    except Exception as e:
        logger.exception("retention_scan_failed: %s", e)
        stats["error"] = str(e)
        return stats
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(run_retention_scan())
