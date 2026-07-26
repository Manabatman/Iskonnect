"""In-app notifications (feature-flagged)."""

import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models
from app.schemas import NotificationResponse
from app.auth import get_current_user, get_current_user_id
from app.config import settings
from app.db import get_db
from app.limiter import limiter

logger = logging.getLogger(__name__)

router = APIRouter(tags=["notifications"])


class NotificationPreferencesResponse(BaseModel):
    notify_deadline_reminders: bool
    notify_new_matches: bool
    notifications_globally_enabled: bool


class NotificationPreferencesUpdate(BaseModel):
    notify_deadline_reminders: bool | None = None
    notify_new_matches: bool | None = None


def _require_notifications_enabled():
    if not settings.enable_notifications:
        raise HTTPException(status_code=404, detail="Notifications are disabled")


@router.get("/settings/notifications", response_model=NotificationPreferencesResponse)
@limiter.limit("60/minute")
def get_notification_preferences(
    request: Request,
    user: Annotated[models.User | None, Depends(get_current_user)] = None,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return NotificationPreferencesResponse(
        notify_deadline_reminders=bool(getattr(user, "notify_deadline_reminders", True)),
        notify_new_matches=bool(getattr(user, "notify_new_matches", True)),
        notifications_globally_enabled=settings.enable_notifications,
    )


@router.patch("/settings/notifications", response_model=NotificationPreferencesResponse)
@limiter.limit("30/minute")
def update_notification_preferences(
    request: Request,
    body: Annotated[NotificationPreferencesUpdate, Body()],
    db: Session = Depends(get_db),
    user: Annotated[models.User | None, Depends(get_current_user)] = None,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if body.notify_deadline_reminders is not None:
        user.notify_deadline_reminders = body.notify_deadline_reminders
    if body.notify_new_matches is not None:
        user.notify_new_matches = body.notify_new_matches
    db.commit()
    db.refresh(user)
    return NotificationPreferencesResponse(
        notify_deadline_reminders=bool(user.notify_deadline_reminders),
        notify_new_matches=bool(user.notify_new_matches),
        notifications_globally_enabled=settings.enable_notifications,
    )


@router.get("/notifications", response_model=list[NotificationResponse])
@limiter.limit("60/minute")
def list_notifications(
    request: Request,
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
@limiter.limit("60/minute")
def unread_count(
    request: Request,
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
@limiter.limit("120/minute")
def mark_read(
    request: Request,
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


@router.post("/notifications/read-all")
@limiter.limit("30/minute")
def mark_all_read(
    request: Request,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    _require_notifications_enabled()
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    updated = (
        db.query(models.Notification)
        .filter(models.Notification.user_id == user_id, models.Notification.is_read == False)  # noqa: E712
        .update({"is_read": True}, synchronize_session=False)
    )
    db.commit()
    return {"status": "read_all", "updated": updated}


@router.delete("/notifications/{notification_id}")
@limiter.limit("60/minute")
def delete_notification(
    request: Request,
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
    db.delete(row)
    db.commit()
    return {"status": "deleted", "id": notification_id}


@router.delete("/notifications")
@limiter.limit("30/minute")
def clear_all_notifications(
    request: Request,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    _require_notifications_enabled()
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    deleted = (
        db.query(models.Notification)
        .filter(models.Notification.user_id == user_id)
        .delete(synchronize_session=False)
    )
    db.commit()
    return {"status": "cleared", "deleted": deleted}
