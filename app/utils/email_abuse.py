"""Outbound email abuse controls (per-email cooldown, daily caps) via Redis."""

from __future__ import annotations

import hashlib
import logging
from datetime import date

from app.config import settings

logger = logging.getLogger(__name__)

# Per-email: 1 send per purpose per 5 minutes; max 5 per purpose per day
EMAIL_COOLDOWN_SECONDS = 300
EMAIL_DAILY_CAP = 5
# Global platform cap (all purposes)
GLOBAL_DAILY_CAP = 2000

_redis_client = None


def _redis():
    global _redis_client
    if not settings.redis_url:
        return None
    if _redis_client is None:
        try:
            import redis

            _redis_client = redis.from_url(settings.redis_url, decode_responses=True)
        except Exception as e:
            logger.warning("email_abuse_redis_connect_failed: %s", e)
            return None
    return _redis_client


def _email_hash(email: str) -> str:
    return hashlib.sha256(email.strip().lower().encode()).hexdigest()[:32]


def can_send_transactional_email(purpose: str, to_email: str) -> bool:
    """
    Return True if an outbound email to to_email for purpose may be sent.

    When Redis is unavailable (local dev), allows sends.
    """
    r = _redis()
    if r is None:
        return True
    eh = _email_hash(to_email)
    purpose_key = purpose.strip().lower()
    cooldown_key = f"email:cooldown:{purpose_key}:{eh}"
    daily_key = f"email:daily:{purpose_key}:{eh}:{date.today().isoformat()}"
    global_key = f"email:global:daily:{date.today().isoformat()}"
    try:
        if r.exists(cooldown_key):
            return False
        daily_count = int(r.get(daily_key) or 0)
        if daily_count >= EMAIL_DAILY_CAP:
            return False
        global_count = int(r.get(global_key) or 0)
        if global_count >= GLOBAL_DAILY_CAP:
            return False
    except Exception as e:
        logger.warning("email_abuse_check_failed: %s", e)
        return True
    return True


def record_transactional_email_sent(purpose: str, to_email: str) -> None:
    """Record a successful outbound email send for rate-limit accounting."""
    r = _redis()
    if r is None:
        return
    eh = _email_hash(to_email)
    purpose_key = purpose.strip().lower()
    cooldown_key = f"email:cooldown:{purpose_key}:{eh}"
    daily_key = f"email:daily:{purpose_key}:{eh}:{date.today().isoformat()}"
    global_key = f"email:global:daily:{date.today().isoformat()}"
    try:
        pipe = r.pipeline()
        pipe.setex(cooldown_key, EMAIL_COOLDOWN_SECONDS, "1")
        pipe.incr(daily_key)
        pipe.expire(daily_key, 86400)
        pipe.incr(global_key)
        pipe.expire(global_key, 86400)
        pipe.execute()
    except Exception as e:
        logger.warning("email_abuse_record_failed: %s", e)
