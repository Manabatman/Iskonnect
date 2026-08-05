"""Cloudflare Turnstile server-side verification (optional — no-op when secret unset)."""

from __future__ import annotations

import logging

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

SITEVERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


def turnstile_enabled() -> bool:
    return bool(settings.turnstile_secret_key)


def verify_turnstile(token: str | None, remote_ip: str | None = None) -> bool:
    """Return True if Turnstile is disabled or verification succeeds."""
    if not turnstile_enabled():
        return True
    if not token or not token.strip():
        return False
    payload: dict[str, str] = {
        "secret": settings.turnstile_secret_key or "",
        "response": token.strip(),
    }
    if remote_ip:
        payload["remoteip"] = remote_ip
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(SITEVERIFY_URL, data=payload)
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        logger.warning("turnstile_verify_failed: %s", exc)
        return False
    if not data.get("success"):
        logger.info("turnstile_rejected error_codes=%s", data.get("error-codes"))
        return False
    return True


def require_turnstile_or_400(token: str | None, remote_ip: str | None = None) -> None:
    from fastapi import HTTPException, status

    if not turnstile_enabled():
        return
    if not verify_turnstile(token, remote_ip):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Security check failed. Please complete the verification and try again.",
        )
