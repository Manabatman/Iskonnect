"""Progressive login lockout via Redis (optional — no-op when Redis unavailable in dev)."""

from __future__ import annotations

import hashlib
import logging

from app.config import settings

logger = logging.getLogger(__name__)

MAX_FAILURES = 5
LOCKOUT_SECONDS = 900  # 15 minutes
FAILURE_WINDOW_SECONDS = 900


def _get_redis():
    if not settings.redis_url:
        return None
    try:
        import redis

        return redis.from_url(settings.redis_url, decode_responses=True)
    except Exception as exc:
        logger.warning("login_lockout_redis_connect_failed: %s", exc)
        return None


def _email_key(email: str) -> str:
    normalized = email.strip().lower()
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:24]
    return f"auth:login_fail:{digest}"


def is_login_locked(email: str) -> bool:
    r = _get_redis()
    if r is None:
        return False
    try:
        count = int(r.get(_email_key(email)) or 0)
        return count >= MAX_FAILURES
    except Exception as exc:
        logger.warning("login_lockout_read_failed: %s", exc)
        return False


def record_failed_login(email: str) -> int:
    r = _get_redis()
    if r is None:
        return 0
    key = _email_key(email)
    try:
        pipe = r.pipeline()
        pipe.incr(key)
        pipe.expire(key, FAILURE_WINDOW_SECONDS)
        count, _ = pipe.execute()
        return int(count)
    except Exception as exc:
        logger.warning("login_lockout_write_failed: %s", exc)
        return 0


def clear_failed_logins(email: str) -> None:
    r = _get_redis()
    if r is None:
        return
    try:
        r.delete(_email_key(email))
    except Exception as exc:
        logger.warning("login_lockout_clear_failed: %s", exc)
