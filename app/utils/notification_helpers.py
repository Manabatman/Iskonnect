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
DEADLINE_HORIZON_DAYS = 7
URGENT_DEADLINE_DAYS = 3
DEDUP_DAYS = 3
DEADLINE_NOTIFICATION_TYPE = "deadline_approaching"
STALE_DATA_STATUSES = frozenset({"needs_review", "broken_link", "expired", "past_deadline"})


def is_trustworthy_scholarship(scholarship: dict) -> bool:
    """Skip notifications for unreliable catalog rows."""
    ds = (scholarship.get("data_status") or "").strip().lower()
    if ds in STALE_DATA_STATUSES:
        return False
    return True


def notification_exists_recently(
    db: Session,
    user_id: int,
    ntype: str,
    *,
    scholarship_id: int | None = None,
    days: int = DEDUP_DAYS,
) -> bool:
    cutoff = datetime.utcnow() - timedelta(days=days)
    q = db.query(models.Notification).filter(
        models.Notification.user_id == user_id,
        models.Notification.type == ntype,
        models.Notification.created_at >= cutoff,
    )
    if scholarship_id is not None:
        q = q.filter(models.Notification.scholarship_id == scholarship_id)
    return q.first() is not None


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


def upsert_deadline_notification(
    db: Session,
    user_id: int,
    *,
    scholarship_id: int,
    title: str,
    deadline: date,
    dedup_days: int = DEDUP_DAYS,
) -> bool:
    """
    Create a deadline_approaching notification if none exists recently.
    Returns True if a notification was added (not yet committed).
    """
    if notification_exists_recently(
        db,
        user_id,
        DEADLINE_NOTIFICATION_TYPE,
        scholarship_id=scholarship_id,
        days=dedup_days,
    ):
        return False

    today = date.today()
    urgent = (deadline - today).days <= URGENT_DEADLINE_DAYS
    prefix = "Urgent: " if urgent else ""
    db.add(
        models.Notification(
            user_id=user_id,
            type=DEADLINE_NOTIFICATION_TYPE,
            title=f"{prefix}Deadline soon: {title[:100]}",
            body=f"Application deadline is {deadline.isoformat()}.",
            scholarship_id=scholarship_id,
            is_read=False,
        )
    )
    return True


def maybe_notify_deadline_from_dict(
    db: Session,
    user_id: int,
    scholarship: dict,
    *,
    horizon_days: int = DEADLINE_HORIZON_DAYS,
) -> bool:
    """Notify if scholarship dict has a deadline within horizon. Returns True if queued."""
    if not is_trustworthy_scholarship(scholarship):
        return False
    sid = scholarship.get("id")
    if not sid:
        return False
    today = date.today()
    d = _parse_deadline(scholarship.get("application_deadline"))
    if d is None or d < today or d > today + timedelta(days=horizon_days):
        return False
    return upsert_deadline_notification(
        db,
        user_id,
        scholarship_id=int(sid),
        title=(scholarship.get("title") or "Scholarship"),
        deadline=d,
    )


def maybe_notify_deadline_from_row(
    db: Session,
    user_id: int,
    scholarship_row: models.Scholarship,
    *,
    horizon_days: int = DEADLINE_HORIZON_DAYS,
) -> bool:
    """Notify from ORM scholarship row (saved-scholarship batch job)."""
    if not scholarship_row.application_deadline:
        return False
    d = scholarship_row.application_deadline
    if isinstance(d, str):
        return False
    sch_dict = {
        "id": scholarship_row.id,
        "title": scholarship_row.title,
        "application_deadline": d,
        "data_status": scholarship_row.data_status,
    }
    return maybe_notify_deadline_from_dict(db, user_id, sch_dict, horizon_days=horizon_days)


def create_notifications_for_match_results(db: Session, user_id: int, results: list[dict]) -> None:
    """
    Insert Notification rows for strong matches and upcoming deadlines.
    Does nothing when ENABLE_NOTIFICATIONS is false.
    """
    if not settings.enable_notifications or not results:
        return

    try:
        strong = [r for r in results if _score_of(r) >= NEW_MATCH_SCORE_THRESHOLD and is_trustworthy_scholarship(r)]
        if strong and not notification_exists_recently(db, user_id, "new_match", scholarship_id=strong[0].get("id")):
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
            if not sid or int(sid) in seen_deadline_scholarships:
                continue
            if maybe_notify_deadline_from_dict(db, user_id, r):
                seen_deadline_scholarships.add(int(sid))

        db.commit()
    except Exception:
        logger.exception("create_notifications_for_match_results failed user_id=%s", user_id)
        db.rollback()
