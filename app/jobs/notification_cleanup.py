"""Delete read notifications older than retention window."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from app.db import SessionLocal
from app import models

logger = logging.getLogger(__name__)

RETENTION_DAYS = 90


def run_notification_cleanup(retention_days: int = RETENTION_DAYS) -> dict[str, int]:
    cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=retention_days)
    db = SessionLocal()
    try:
        deleted = (
            db.query(models.Notification)
            .filter(
                models.Notification.is_read == True,  # noqa: E712
                models.Notification.created_at < cutoff,
            )
            .delete(synchronize_session=False)
        )
        db.commit()
        logger.info("notification_cleanup_deleted=%s cutoff=%s", deleted, cutoff.isoformat())
        return {"deleted": deleted, "retention_days": retention_days}
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(run_notification_cleanup())
