"""Public landing statistics (LAND-03a) — cached, no auth, no PII."""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.limiter import limiter
from app.public_stats_cache import get_cached_public_stats
from app.schemas import PublicStatsResponse
from app.services.public_stats import compute_public_stats, static_fallback_stats

logger = logging.getLogger(__name__)

router = APIRouter(tags=["public"])


@router.get("/public/stats", response_model=PublicStatsResponse)
@limiter.limit("60/minute")
def get_public_stats(
    request: Request,
    db: Session = Depends(get_db),
):
    """Substantiated catalog signals for the landing page (1-hour cache)."""

    def _build() -> dict:
        stats = compute_public_stats(db)
        return stats.model_dump(mode="json")

    try:
        payload = get_cached_public_stats(_build)
        return PublicStatsResponse.model_validate(payload)
    except Exception:
        logger.exception("public_stats_compute_failed")
        return static_fallback_stats()
