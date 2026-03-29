"""
Scholarship list cache: optional Redis (shared across workers) with in-process fallback.

Set REDIS_URL (e.g. redis://localhost:6379/0) for multi-worker deployments.
Without Redis, cache is per-process only — use a single worker or accept up to TTL staleness.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Callable

from sqlalchemy.orm import Session

from app.config import settings

logger = logging.getLogger(__name__)

REDIS_KEY = "iskonnect:scholarships_json:v1"
TTL_SECONDS = 300

_process_cache: list | None = None
_process_cache_time: float = 0.0


def invalidate_scholarship_cache() -> None:
    """Clear scholarship list cache (call after scholarship mutations)."""
    global _process_cache, _process_cache_time
    _process_cache = None
    _process_cache_time = 0.0
    if settings.redis_url:
        try:
            import redis

            redis.from_url(settings.redis_url).delete(REDIS_KEY)
        except Exception as e:
            logger.warning("scholarship_cache_redis_invalidate_failed: %s", e)


def get_cached_scholarship_dicts(
    db: Session,
    build_all_dicts: Callable[[Session], list[dict]],
) -> list[dict]:
    """Load scholarship dicts from Redis, process cache, or DB."""
    global _process_cache, _process_cache_time

    if settings.redis_url:
        try:
            import redis

            r = redis.from_url(settings.redis_url, decode_responses=True)
            raw = r.get(REDIS_KEY)
            if raw:
                return json.loads(raw)
        except Exception as e:
            logger.warning("scholarship_cache_redis_read_failed: %s", e)

    now = time.monotonic()
    if _process_cache is not None and (now - _process_cache_time) < TTL_SECONDS:
        return _process_cache

    data = build_all_dicts(db)
    _process_cache = data
    _process_cache_time = now

    if settings.redis_url:
        try:
            import redis

            redis.from_url(settings.redis_url, decode_responses=True).setex(
                REDIS_KEY, TTL_SECONDS, json.dumps(data)
            )
        except Exception as e:
            logger.warning("scholarship_cache_redis_write_failed: %s", e)

    return data
