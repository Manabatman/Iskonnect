"""In-app notifications (feature-flagged)."""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.schemas import NotificationResponse
from app.auth import get_current_user_id
from app.config import settings
from app.db import get_db

logger = logging.getLogger(__name__)

router = APIRouter(tags=["notifications"])


def _require_notifications_enabled():
    if not settings.enable_notifications:
        raise HTTPException(status_code=404, detail="Notifications are disabled")


@router.get("/notifications", response_model=list[NotificationResponse])
def list_notifications(
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
    limit: int = 50,
    offset: int = 0,
):
    _require_notifications_enabled()
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    rows = (
        db.query(models.Notification)
        .filter(models.Notification.user_id == user_id)
        .order_by(models.Notification.created_at.desc())
        .offset(offset)
        .limit(min(limit, 200))
        .all()
    )
    return rows


@router.get("/notifications/unread-count")
def unread_count(
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    _require_notifications_enabled()
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    n = (
        db.query(models.Notification)
        .filter(models.Notification.user_id == user_id, models.Notification.is_read == False)  # noqa: E712
        .count()
    )
    return {"unread": n}


@router.post("/notifications/{notification_id}/read")
def mark_read(
    notification_id: int,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    _require_notifications_enabled()
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    row = (
        db.query(models.Notification)
        .filter(models.Notification.id == notification_id, models.Notification.user_id == user_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Notification not found")
    row.is_read = True
    db.commit()
    return {"status": "read", "id": notification_id}
