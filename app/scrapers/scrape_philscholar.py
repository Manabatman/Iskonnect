"""
PhilScholar scraper (MVP skeleton).

Fetches the public listing page and attempts to parse cards. Uses SHA-256 of raw HTML
to skip re-parsing/ingest when the listing page has not changed since the last run.

Run: python -m app.scrapers.scrape_philscholar
Output: data/raw/philscholar_YYYY-MM-DD.json (or philscholar_YYYY-MM-DD.skip when unchanged).
"""
from __future__ import annotations

import hashlib
import json
import logging
from datetime import date, datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup

from app.scrapers.base import fetch_text

logger = logging.getLogger(__name__)

LIST_URL = "https://philscholar.com/scholarships/"


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _listing_sha256(html: str | None) -> str:
    raw = (html or "").encode("utf-8", errors="replace")
    return hashlib.sha256(raw).hexdigest()


def _last_saved_listing_hash() -> str | None:
    try:
        from app.db import SessionLocal
        from app import models

        db = SessionLocal()
        try:
            row = (
                db.query(models.ScraperRun)
                .filter(models.ScraperRun.source == "philscholar")
                .filter(models.ScraperRun.listing_content_sha256.isnot(None))
                .order_by(models.ScraperRun.id.desc())
                .first()
            )
            return row.listing_content_sha256 if row else None
        finally:
            db.close()
    except Exception:
        logger.warning("last_listing_hash_lookup_failed", exc_info=True)
        return None


def _validate_entry(row: dict) -> bool:
    title = (row.get("title") or "").strip()
    link = (row.get("link") or "").strip()
    if not title or len(title) < 3:
        return False
    if not link.startswith("https://") and not link.startswith("http://"):
        return False
    if len(link) > 2048:
        return False
    return True


def _parse_detail_page(html: str) -> dict:
    """Extract description and provider hints from a scholarship detail page."""
    soup = BeautifulSoup(html, "lxml")
    out: dict = {}
    content = soup.select_one(".entry-content, article .post-content, .post-content, article")
    if content:
        text = content.get_text(" ", strip=True)
        if text:
            out["description"] = text[:8000]
    provider_el = soup.select_one(".author a, .posted-by a, .provider, meta[property='og:site_name']")
    if provider_el:
        if provider_el.name == "meta":
            out["provider"] = (provider_el.get("content") or "").strip() or None
        else:
            out["provider"] = provider_el.get_text(strip=True) or None
    return out


def _enrich_row_from_detail(row: dict) -> dict:
    """Fetch detail page for description/provider (rate-limited via base.fetch_text)."""
    link = (row.get("link") or "").strip()
    if not link:
        return row
    html = fetch_text(link)
    if not html:
        return row
    try:
        extra = _parse_detail_page(html)
        return {**row, **{k: v for k, v in extra.items() if v}}
    except Exception:
        logger.warning("scrape_philscholar_detail_parse_failed link=%s", link, exc_info=True)
        return row


def _parse_listing(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    out: list[dict] = []
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
    """Write JSON path, or a `.skip` marker path when listing HTML unchanged."""
    root = _project_root()
    raw_dir = root / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    out_path = raw_dir / f"philscholar_{today}.json"
    skip_path = raw_dir / f"philscholar_{today}.skip"

    html = fetch_text(LIST_URL)
    content_hash = _listing_sha256(html)
    prev_hash = _last_saved_listing_hash()

    from app.scrapers.run_logging import log_scraper_run

    if html and prev_hash and content_hash == prev_hash:
        skip_path.write_text("unchanged\n", encoding="utf-8")
        if out_path.exists():
            out_path.unlink(missing_ok=True)  # type: ignore[arg-type]
        logger.info("scrape_philscholar_skip reason=unchanged_listing sha=%s", content_hash[:12])
        log_scraper_run(
            "philscholar",
            "no_change",
            records_found=0,
            output_path=str(skip_path),
            error_detail=None,
            listing_content_sha256=content_hash,
        )
        return skip_path

    rows: list[dict] = []
    if html:
        try:
            rows = _parse_listing(html)
        except Exception:
            logger.exception("scrape_philscholar_parse_failed")
    else:
        logger.warning("scrape_philscholar_no_html")

    valid_rows = [r for r in rows if _validate_entry(r)]
    if len(valid_rows) < len(rows):
        logger.info("scrape_philscholar_filtered invalid=%s valid=%s", len(rows) - len(valid_rows), len(valid_rows))

    enriched_rows: list[dict] = []
    for i, row in enumerate(valid_rows):
        if i < 25:
            enriched_rows.append(_enrich_row_from_detail(row))
        else:
            enriched_rows.append(row)

    payload = [
        {
            **r,
            "scraped_at": datetime.now(timezone.utc).isoformat(),
            "scraper_version": "1.2",
        }
        for r in enriched_rows
    ]
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    skip_path.unlink(missing_ok=True)  # type: ignore[arg-type]
    logger.info("scrape_philscholar_wrote path=%s count=%s", out_path, len(payload))

    status = "success" if payload else ("partial" if html else "failed")
    err = None if html else "no_html_response"
    if html and not payload:
        status = "failed"
        err = "zero_valid_records"
    log_scraper_run(
        "philscholar",
        status,
        records_found=len(payload),
        output_path=str(out_path),
        error_detail=err,
        listing_content_sha256=content_hash if html else None,
    )
    if not payload and html:
        raise SystemExit("scrape_philscholar: zero valid records — failing workflow")
    return out_path


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(run_scrape())
