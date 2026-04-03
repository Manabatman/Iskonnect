"""
PhilScholar scraper (MVP skeleton).

Fetches the public listing page and attempts to parse cards. If HTML structure
changes or the site blocks the request, writes an empty list and logs warnings.

Run: python -m app.scrapers.scrape_philscholar
Output: data/raw/philscholar_YYYY-MM-DD.json
"""
from __future__ import annotations

import json
import logging
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup

from app.scrapers.base import fetch_text

logger = logging.getLogger(__name__)

# Public scholarship listing — adjust path if the site changes.
LIST_URL = "https://philscholar.com/scholarships/"


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _parse_listing(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    out: list[dict] = []
    # Generic article/card pattern — tune selectors after inspecting live HTML.
    for art in soup.select("article")[:50]:
        title_el = art.select_one("h2 a, h3 a, .entry-title a, a")
        if not title_el:
            continue
        title = title_el.get_text(strip=True)
        link = title_el.get("href") or ""
        if not title or not link.startswith("http"):
            continue
        out.append(
            {
                "title": title,
                "link": link,
                "provider": None,
                "description": None,
                "source": "philscholar",
            }
        )
    return out


def run_scrape() -> Path:
    root = _project_root()
    raw_dir = root / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    out_path = raw_dir / f"philscholar_{date.today().isoformat()}.json"

    html = fetch_text(LIST_URL)
    rows: list[dict] = []
    if html:
        try:
            rows = _parse_listing(html)
        except Exception:
            logger.exception("scrape_philscholar_parse_failed")
    else:
        logger.warning("scrape_philscholar_no_html")

    from datetime import datetime, timezone

    payload = [
        {
            **r,
            "scraped_at": datetime.now(timezone.utc).isoformat(),
            "scraper_version": "1.0",
        }
        for r in rows
    ]
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("scrape_philscholar_wrote path=%s count=%s", out_path, len(payload))
    return out_path


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(run_scrape())
