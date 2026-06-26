"""Client IP extraction for rate limiting behind reverse proxies (Render, Railway)."""

from __future__ import annotations

from starlette.requests import Request

from app.config import settings


def get_client_ip(request: Request) -> str:
    """
    Return the client IP for rate-limit keying.

    When TRUST_PROXY_HEADERS is true (production behind Render/Railway), the left-most
    X-Forwarded-For address is the original client. Otherwise use the direct peer IP
    to prevent XFF spoofing on local/dev.
    """
    if settings.trust_proxy_headers:
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            first = forwarded.split(",")[0].strip()
            if first:
                return first
    if request.client and request.client.host:
        return request.client.host
    return "127.0.0.1"
