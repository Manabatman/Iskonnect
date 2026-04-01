"""Admin audit log query API."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import models
from app.schemas import AuditLogResponse
from app.auth import require_admin
from app.db import get_db

router = APIRouter(tags=["audit"])


@router.get("/admin/audit/logs", response_model=list[AuditLogResponse])
def list_audit_logs(
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
    action: str | None = Query(None),
    resource_type: str | None = Query(None),
    actor_id: int | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    q = db.query(models.AuditLog).order_by(models.AuditLog.created_at.desc())
    if action:
        q = q.filter(models.AuditLog.action == action)
    if resource_type:
        q = q.filter(models.AuditLog.resource_type == resource_type)
    if actor_id is not None:
        q = q.filter(models.AuditLog.actor_id == actor_id)
    rows = q.offset(offset).limit(limit).all()
    return rows
