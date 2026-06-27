"""
Orchestrate registered scraper adapters.

Run: python -m app.scrapers.scrape_runner [--source philscholar]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import sys
from datetime import date, datetime, timezone
from pathlib import Path

from app.scrapers.adapters import SOURCE_REGISTRY
from app.scrapers.adapters.philscholar import PhilScholarAdapter, SITEMAP_INDEX_URL
from app.scrapers.base import fetch_text, save_failure_snapshot
from app.scrapers.run_logging import log_scraper_run

logger = logging.getLogger(__name__)


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _listing_sha256(html: str | None) -> str:
    raw = (html or "").encode("utf-8", errors="replace")
    return hashlib.sha256(raw).hexdigest()


def _last_saved_listing_hash(source: str) -> str | None:
    try:
        from app.db import SessionLocal
        from app import models

        db = SessionLocal()
        try:
            row = (
                db.query(models.ScraperRun)
                .filter(models.ScraperRun.source == source)
                .filter(models.ScraperRun.listing_content_sha256.isnot(None))
                .order_by(models.ScraperRun.id.desc())
                .first()
            )
            return row.listing_content_sha256 if row else None
        finally:
            db.close()
    except Exception:
        logger.warning("last_listing_hash_lookup_failed source=%s", source, exc_info=True)
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


def _collect_philscholar_urls(adapter: PhilScholarAdapter) -> tuple[str | None, list[str]]:
    """Fetch sitemap index + post sitemaps; return combined hash input and post URLs."""
    index_html = fetch_text(SITEMAP_INDEX_URL)
    if not index_html:
        return None, []

    all_locs: list[str] = []
    child_sitemaps = [
        u
        for u in adapter.discover_listing_urls(index_html)
        if "post-sitemap" in u or "sitemap-post" in u
    ]
    if not child_sitemaps:
        child_sitemaps = [u for u in adapter.discover_listing_urls(index_html) if u.endswith(".xml")]

    for sm_url in child_sitemaps[:5]:
        sm_html = fetch_text(sm_url)
        if sm_html:
            all_locs.extend(adapter.discover_listing_urls(sm_html))

    if not all_locs:
        all_locs = adapter.discover_listing_urls(index_html)

    posts = adapter.filter_post_urls(all_locs, limit=50)
    hash_input = index_html + "\n".join(sorted(posts))
    return hash_input, posts


def _enrich_row(adapter, row: dict) -> dict:
    link = (row.get("link") or "").strip()
    if not link:
        return row
    html = fetch_text(link)
    if not html:
        return row
    try:
        extra = adapter.parse_detail_page(html, link)
        return {**row, **{k: v for k, v in extra.items() if v and k != "og_image"}}
    except Exception:
        logger.warning("scrape_detail_parse_failed link=%s", link, exc_info=True)
        save_failure_snapshot(adapter.source, link, html, "parse_failed")
        return row


def run_source(source: str = "philscholar") -> Path:
    if source not in SOURCE_REGISTRY:
        raise SystemExit(f"Unknown source: {source}")

    adapter_cls = SOURCE_REGISTRY[source]
    adapter = adapter_cls()

    root = _project_root()
    raw_dir = root / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    out_path = raw_dir / f"{source}_{today}.json"
    skip_path = raw_dir / f"{source}_{today}.skip"

    if source == "philscholar":
        hash_input, post_urls = _collect_philscholar_urls(adapter)
        content_hash = _listing_sha256(hash_input)
        prev_hash = _last_saved_listing_hash(source)

        if hash_input and prev_hash and content_hash == prev_hash:
            skip_path.write_text("unchanged\n", encoding="utf-8")
            out_path.unlink(missing_ok=True)  # type: ignore[arg-type]
            logger.info("scrape_skip reason=unchanged_listing sha=%s", content_hash[:12])
            log_scraper_run(
                source,
                "no_change",
                records_found=0,
                output_path=str(skip_path),
                listing_content_sha256=content_hash,
            )
            return skip_path

        rows = [adapter.row_from_url(u, adapter.title_from_url(u)) for u in post_urls]
        listing_html_for_snap = hash_input
    else:
        html = fetch_text(adapter.listing_url)
        content_hash = _listing_sha256(html)
        listing_html_for_snap = html
        rows = []
        if html:
            urls = adapter.discover_listing_urls(html)
            rows = [adapter.row_from_url(u) for u in urls[:50]]

    valid_rows = [r for r in rows if _validate_entry(r)]
    enriched: list[dict] = []
    for i, row in enumerate(valid_rows):
        if i < 25:
            enriched.append(_enrich_row(adapter, row))
        else:
            enriched.append(row)

    payload = [
        {
            **r,
            "scraped_at": datetime.now(timezone.utc).isoformat(),
            "scraper_version": "2.0",
        }
        for r in enriched
    ]

    if not payload:
        err = "zero_valid_records"
        snap = save_failure_snapshot(source, adapter.listing_url, listing_html_for_snap, err)
        log_scraper_run(
            source,
            "failed",
            records_found=0,
            output_path=snap,
            error_detail=err,
            listing_content_sha256=content_hash,
        )
        _alert_scraper_failure(source, err)
        raise SystemExit(f"scrape_{source}: zero valid records — failing workflow")

    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    skip_path.unlink(missing_ok=True)  # type: ignore[arg-type]
    logger.info("scrape_wrote path=%s count=%s", out_path, len(payload))

    log_scraper_run(
        source,
        "success" if payload else "failed",
        records_found=len(payload),
        output_path=str(out_path),
        listing_content_sha256=content_hash,
    )
    if not payload:
        _alert_scraper_failure(source, "zero_valid_records")
        raise SystemExit(f"scrape_{source}: zero valid records — failing workflow")
    return out_path


def _alert_scraper_failure(source: str, detail: str) -> None:
    try:
        import sentry_sdk

        if sentry_sdk.Hub.current.client:
            sentry_sdk.capture_message(
                f"Scraper failed: {source} — {detail}",
                level="error",
            )
    except Exception:
        pass


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run scholarship scrapers")
    parser.add_argument("--source", default="philscholar", choices=list(SOURCE_REGISTRY.keys()))
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO)
    path = run_source(args.source)
    print(path)


if __name__ == "__main__":
    main()
