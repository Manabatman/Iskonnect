"""Admin API for DB-driven scoring weights."""

import logging
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app import models
from app.schemas import ScoringWeightItem, ScoringWeightResponse, ScoringWeightsUpdateRequest
from app.auth import require_admin
from app.db import get_db
from app.limiter import limiter
from app.utils.audit import log_action

logger = logging.getLogger(__name__)

router = APIRouter(tags=["scoring-admin"])

_EXPECTED = {"academic", "income", "field_alignment", "geographic", "equity_priority"}


@router.get("/admin/scoring/weights", response_model=ScoringWeightResponse)
@limiter.limit("60/minute")
def get_scoring_weights(
    request: Request,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    rows = db.query(models.ScoringWeight).order_by(models.ScoringWeight.id.asc()).all()
    return ScoringWeightResponse(
        weights=[ScoringWeightItem(component=r.component, weight=float(r.weight)) for r in rows]
    )


@router.put("/admin/scoring/weights", response_model=ScoringWeightResponse)
@limiter.limit("30/minute")
def put_scoring_weights(
    request: Request,
    body: ScoringWeightsUpdateRequest,
    db: Session = Depends(get_db),
    admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    comps = {w.component for w in body.weights}
    if comps != _EXPECTED:
        raise HTTPException(
            status_code=400,
            detail=f"Must supply exactly these components: {sorted(_EXPECTED)}",
        )
    total = sum(w.weight for w in body.weights)
    if abs(total - 1.0) > 0.001:
        raise HTTPException(status_code=400, detail=f"Weights must sum to 1.0 (got {total})")

    now = datetime.now(timezone.utc)
    for w in body.weights:
        row = db.query(models.ScoringWeight).filter(models.ScoringWeight.component == w.component).first()
        if row:
            row.weight = w.weight
            row.updated_at = now
            row.updated_by = admin.id if admin else None
        else:
            db.add(
                models.ScoringWeight(
                    component=w.component,
                    weight=w.weight,
                    updated_at=now,
                    updated_by=admin.id if admin else None,
                )
            )
    db.commit()

    client = request.client.host if request.client else None
    log_action(
        db,
        actor_id=admin.id if admin else None,
        actor_type="admin",
        action="scoring_weights.update",
        resource_type="scoring_weights",
        resource_id=None,
        details={"weights": [w.model_dump() for w in body.weights]},
        ip_address=client,
    )

    rows = db.query(models.ScoringWeight).order_by(models.ScoringWeight.id.asc()).all()
    return ScoringWeightResponse(
        weights=[ScoringWeightItem(component=r.component, weight=float(r.weight)) for r in rows]
    )
