"""
Append-only audit logging. Failures never block the request path.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from sqlalchemy.orm import Session

from app import models

logger = logging.getLogger(__name__)


def log_action(
    db: Session,
    *,
    actor_id: int | None,
    actor_type: str,
    action: str,
    resource_type: str | None = None,
    resource_id: int | None = None,
    details: dict[str, Any] | None = None,
    ip_address: str | None = None,
) -> None:
    """Insert one audit log row. Swallows all exceptions."""
    try:
        row = models.AuditLog(
            actor_id=actor_id,
            actor_type=actor_type,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=json.dumps(details) if details is not None else None,
            ip_address=ip_address,
        )
        db.add(row)
        db.commit()
    except Exception as e:
        try:
            db.rollback()
        except Exception:
            pass
        logger.warning("audit_log_failed action=%s error=%s", action, e)
