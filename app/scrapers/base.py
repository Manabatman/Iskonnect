"""Shared HTTP helpers for scrapers."""

from __future__ import annotations

import logging
import random
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import httpx

logger = logging.getLogger(__name__)

DEFAULT_UA = "Iskonnect-ScholarshipBot/1.0 (+https://iskonnect.example)"
REQUEST_GAP_SEC = 1.0
_robots_cache: dict[str, RobotFileParser] = {}


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def save_failure_snapshot(source: str, url: str, html: str | None, reason: str) -> str | None:
    """Persist HTML (or reason) for post-mortem debugging."""
    try:
        snap_dir = _project_root() / "data" / "snapshots"
        snap_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        safe = urlparse(url).netloc.replace(".", "_")[:40]
        path = snap_dir / f"{source}_{safe}_{ts}.html"
        body = html if html else f"<!-- no html: {reason} -->"
        path.write_text(body[:500_000], encoding="utf-8", errors="replace")
        return str(path)
    except Exception:
        logger.warning("snapshot_save_failed source=%s url=%s", source, url, exc_info=True)
        return None


def robots_allowed(url: str, user_agent: str = DEFAULT_UA) -> bool:
    """Best-effort robots.txt check for the URL origin."""
    try:
        parsed = urlparse(url)
        origin = f"{parsed.scheme}://{parsed.netloc}"
        if origin not in _robots_cache:
            rp = RobotFileParser()
            rp.set_url(f"{origin}/robots.txt")
            try:
                rp.read()
            except Exception:
                return True
            _robots_cache[origin] = rp
        return _robots_cache[origin].can_fetch(user_agent, url)
    except Exception:
        return True


def fetch_text(
    url: str,
    timeout: float = 15.0,
    retries: int = 2,
    *,
    check_robots: bool = True,
) -> str | None:
    """GET URL with backoff; None on failure."""
    if check_robots and not robots_allowed(url):
        logger.warning("scrape_robots_disallow url=%s", url)
        return None

    last_err: Exception | None = None
    for attempt in range(retries + 1):
        try:
            gap = REQUEST_GAP_SEC + random.uniform(0, 0.5)
            time.sleep(gap)
            with httpx.Client(timeout=timeout, headers={"User-Agent": DEFAULT_UA}) as client:
                r = client.get(url, follow_redirects=True)
                if 200 <= r.status_code < 400:
                    return r.text
                logger.warning("scrape_http_status url=%s code=%s", url, r.status_code)
        except Exception as e:
            last_err = e
            backoff = 3.0 * (2**attempt) + random.uniform(0, 1)
            logger.warning("scrape_fetch_attempt url=%s err=%s backoff=%.1fs", url, e, backoff)
            time.sleep(backoff)
    if last_err:
        logger.error("scrape_fetch_failed url=%s", url)
    return None
