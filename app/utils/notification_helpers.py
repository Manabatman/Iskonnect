"""Create in-app notifications after match runs (guarded by ENABLE_NOTIFICATIONS)."""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from app import models
from app.config import settings

logger = logging.getLogger(__name__)

NEW_MATCH_SCORE_THRESHOLD = 70.0
DEADLINE_REMINDER_DAYS = 7


def _parse_deadline(val: Any) -> date | None:
    if val is None:
        return None
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, date):
        return val
    if isinstance(val, str):
        s = val.strip()
        if not s:
            return None
        try:
            if "T" in s:
                return datetime.fromisoformat(s.replace("Z", "+00:00")).date()
            return date.fromisoformat(s[:10])
        except (ValueError, TypeError):
            return None
    return None


def _score_of(r: dict) -> float:
    v = r.get("final_score")
    if v is None:
        v = r.get("score")
    try:
        return float(v) if v is not None else 0.0
    except (TypeError, ValueError):
        return 0.0


def create_notifications_for_match_results(db: Session, user_id: int, results: list[dict]) -> None:
    """
    Insert Notification rows for strong matches and upcoming deadlines.
    Does nothing when ENABLE_NOTIFICATIONS is false.
    Commits on success; logs and rolls back only the notification inserts on failure.
    """
    if not settings.enable_notifications or not results:
        return

    try:
        today = date.today()
        horizon = today + timedelta(days=DEADLINE_REMINDER_DAYS)

        strong = [r for r in results if _score_of(r) >= NEW_MATCH_SCORE_THRESHOLD]
        if strong:
            preview = "; ".join((r.get("title") or "")[:48] for r in strong[:3])
            if len(strong) > 3:
                preview += f" (+{len(strong) - 3} more)"
            db.add(
                models.Notification(
                    user_id=user_id,
                    type="new_match",
                    title=f"You have {len(strong)} strong match(es)",
                    body=preview or None,
                    scholarship_id=strong[0].get("id"),
                    is_read=False,
                )
            )

        seen_deadline_scholarships: set[int] = set()
        for r in results:
            sid = r.get("id")
            if not sid or sid in seen_deadline_scholarships:
                continue
            d = _parse_deadline(r.get("application_deadline"))
            if d is None or d < today or d > horizon:
                continue
            seen_deadline_scholarships.add(int(sid))
            db.add(
                models.Notification(
                    user_id=user_id,
                    type="deadline_reminder",
                    title=f"Deadline soon: {(r.get('title') or 'Scholarship')[:100]}",
                    body=f"Application deadline is {d.isoformat()}.",
                    scholarship_id=int(sid),
                    is_read=False,
                )
            )

        db.commit()
    except Exception:
        logger.exception("create_notifications_for_match_results failed user_id=%s", user_id)
        db.rollback()
