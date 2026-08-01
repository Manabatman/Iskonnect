"""
Cached /plan responses: optional Redis (shared) with in-process fallback.

Keyed by profile fingerprint + scoring policy version. TTL 10 minutes.
Invalidated on profile update and catalog mutation.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from typing import Any

from app.config import settings

logger = logging.getLogger(__name__)

PLAN_CACHE_TTL = 600
PLAN_KEY_PREFIX = "iskonnect:plan:v1"

_process_plan_cache: dict[str, tuple[float, dict[str, Any]]] = {}
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
            logger.warning("plan_cache_redis_connect_failed: %s", e)
            return None
    return _redis_client


def _policy_version() -> str:
    return "db_weights" if settings.db_driven_weights else "default"


def profile_fingerprint(profile: dict) -> str:
    """Stable hash of profile fields that influence matching."""
    relevant = {k: profile.get(k) for k in sorted(profile.keys())}
    raw = json.dumps(relevant, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def plan_cache_key(profile_id: int, profile: dict, *, limit: int, offset: int) -> str:
    return f"{PLAN_KEY_PREFIX}:{profile_id}:{profile_fingerprint(profile)}:{_policy_version()}:{limit}:{offset}"


def get_cached_plan(key: str) -> dict[str, Any] | None:
    r = _get_redis()
    if r:
        try:
            raw = r.get(key)
            if raw:
                return json.loads(raw)
        except Exception as e:
            logger.warning("plan_cache_redis_read_failed: %s", e)

    entry = _process_plan_cache.get(key)
    if entry and (time.monotonic() - entry[0]) < PLAN_CACHE_TTL:
        return entry[1]
    return None


def set_cached_plan(key: str, payload: dict[str, Any]) -> None:
    now = time.monotonic()
    _process_plan_cache[key] = (now, payload)

    r = _get_redis()
    if r:
        try:
            r.setex(key, PLAN_CACHE_TTL, json.dumps(payload))
        except Exception as e:
            logger.warning("plan_cache_redis_write_failed: %s", e)


def invalidate_plan_cache(profile_id: int | None = None) -> None:
    """Drop cached plan entries for one profile or all profiles."""
    global _process_plan_cache

    if profile_id is None:
        _process_plan_cache = {}
    else:
        prefix = f"{PLAN_KEY_PREFIX}:{profile_id}:"
        _process_plan_cache = {k: v for k, v in _process_plan_cache.items() if not k.startswith(prefix)}

    r = _get_redis()
    if not r:
        return
    try:
        if profile_id is None:
            for key in r.scan_iter(match=f"{PLAN_KEY_PREFIX}:*"):
                r.delete(key)
        else:
            for key in r.scan_iter(match=f"{PLAN_KEY_PREFIX}:{profile_id}:*"):
                r.delete(key)
    except Exception as e:
        logger.warning("plan_cache_redis_invalidate_failed: %s", e)
