"""Public landing stats cache — 1-hour TTL, Redis with in-process fallback."""

from __future__ import annotations

import json
import logging
import time
from typing import Callable

from app.config import settings

logger = logging.getLogger(__name__)

REDIS_KEY = "iskonnect:public_stats:v1"
TTL_SECONDS = 3600

_process_cache: dict | None = None
_process_cache_time: float = 0.0
_redis_client = None


def _get_redis():
    global _redis_client
    if not settings.redis_url:
        return None
    if _redis_client is None:
        try:
            import redis

            _redis_client = redis.from_url(settings.redis_url, decode_responses=True)
        except Exception as e:
            logger.warning("public_stats_cache_redis_connect_failed: %s", e)
            return None
    return _redis_client


def invalidate_public_stats_cache() -> None:
    global _process_cache, _process_cache_time
    _process_cache = None
    _process_cache_time = 0.0
    r = _get_redis()
    if r:
        try:
            r.delete(REDIS_KEY)
        except Exception as e:
            logger.warning("public_stats_cache_redis_invalidate_failed: %s", e)


def get_cached_public_stats(build_stats: Callable[[], dict]) -> dict:
    global _process_cache, _process_cache_time

    r = _get_redis()
    if r:
        try:
            raw = r.get(REDIS_KEY)
            if raw:
                return json.loads(raw)
        except Exception as e:
            logger.warning("public_stats_cache_redis_read_failed: %s", e)

    now = time.monotonic()
    if _process_cache is not None and (now - _process_cache_time) < TTL_SECONDS:
        return _process_cache

    data = build_stats()
    _process_cache = data
    _process_cache_time = now

    if r:
        try:
            r.setex(REDIS_KEY, TTL_SECONDS, json.dumps(data, default=str))
        except Exception as e:
            logger.warning("public_stats_cache_redis_write_failed: %s", e)

    return data
