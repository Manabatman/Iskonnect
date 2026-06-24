"""Shared HTTP helpers for scrapers."""

from __future__ import annotations

import logging
import time
from typing import Any

import httpx

logger = logging.getLogger(__name__)

DEFAULT_UA = "Iskonnect-ScholarshipBot/1.0 (+https://iskonnect.example)"
REQUEST_GAP_SEC = 1.0


def fetch_text(url: str, timeout: float = 15.0, retries: int = 2) -> str | None:
    """GET URL and return response text; None on failure."""
    last_err: Exception | None = None
    for attempt in range(retries + 1):
        try:
            time.sleep(REQUEST_GAP_SEC)
            with httpx.Client(timeout=timeout, headers={"User-Agent": DEFAULT_UA}) as client:
                r = client.get(url, follow_redirects=True)
                if 200 <= r.status_code < 400:
                    return r.text
                logger.warning("scrape_http_status url=%s code=%s", url, r.status_code)
        except Exception as e:
            last_err = e
            logger.warning("scrape_fetch_attempt url=%s err=%s", url, e)
            time.sleep(3.0)
    if last_err:
        logger.error("scrape_fetch_failed url=%s", url)
    return None
