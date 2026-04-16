"""
Load raw JSON from scrapers into scholarships_staging (pending admin approval).

Usage:
  python -m app.scripts.ingest_scraped --source data/raw/philscholar_2026-04-03.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings
from app.db import SessionLocal
from app import models
from app.schemas import Scholarship

logger = logging.getLogger(__name__)


def _dedupe_key(title: str, provider: str | None, link: str | None) -> str:
    raw = (
        f"{(title or '').strip().lower()}|{(provider or '').strip().lower()}"
        f"|{(link or '').strip().lower()}"
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:64]


def _find_live_duplicate(db, title: str, provider: str | None, link: str | None) -> bool:
    from sqlalchemy import func

    want_t = (title or "").strip().lower()
    want_p = (provider or "").strip().lower()
    want_l = (link or "").strip().lower()
    if not want_t:
        return False
    if want_l:
        by_link = (
            db.query(models.Scholarship)
            .filter(
                func.lower(func.trim(func.coalesce(models.Scholarship.link, ""))) == want_l
            )
            .first()
        )
        if by_link is not None:
            return True
    candidates = (
        db.query(models.Scholarship)
        .filter(func.lower(func.trim(models.Scholarship.title)) == want_t)
        .all()
    )
    for row in candidates:
        if (row.provider or "").strip().lower() == want_p:
            return True
    return False


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    db_url = (settings.database_url or "").strip()
    if not db_url:
        logger.error("ingest_scraped DATABASE_URL is empty — set it in .env or the environment.")
        raise SystemExit("DATABASE_URL is not configured.")
    if os.environ.get("GITHUB_ACTIONS") == "true" and not db_url.lower().startswith("postgres"):
        logger.error(
            "ingest_scraped In GitHub Actions, DATABASE_URL must be your Supabase/Postgres URI "
            "(repository secret)."
        )
        raise SystemExit("DATABASE_URL must be a postgresql:// URI in GitHub Actions.")

    parser = argparse.ArgumentParser(description="Ingest scraped JSON into staging")
    parser.add_argument("--source", required=True, help="Path to raw JSON file (array of objects)")
    args = parser.parse_args()
    path = Path(args.source)
    if not path.exists():
        raise SystemExit(f"File not found: {path}")
    raw = path.read_text(encoding="utf-8").strip()
    if len(raw) < 3:
        raise SystemExit(f"Scrape output file is empty or too small: {path}")
    data = json.loads(raw)
    if not isinstance(data, list):
        raise SystemExit("JSON root must be an array")

    db = SessionLocal()
    created = skipped_dup = skipped_inv = skipped_live = 0
    try:
        for i, row in enumerate(data):
            if not isinstance(row, dict):
                skipped_inv += 1
                continue
            title = (row.get("title") or "").strip()
            link = (row.get("link") or "").strip()
            if not title or not link:
                logger.warning("ingest_scraped skip row=%s reason=missing_title_or_link", i)
                skipped_inv += 1
                continue
            provider = row.get("provider")
            source = row.get("source") or "scraper"
            key = _dedupe_key(title, provider, link)
            if (
                db.query(models.ScholarshipStaging)
                .filter(models.ScholarshipStaging.dedupe_key == key, models.ScholarshipStaging.status == "pending")
                .first()
            ):
                skipped_dup += 1
                continue
            if _find_live_duplicate(db, title, provider, link):
                logger.info(
                    "ingest_scraped skip row=%s reason=already_live title=%r",
                    i,
                    title[:80],
                )
                skipped_live += 1
                continue
            try:
                sch = Scholarship(
                    title=title,
                    provider=provider,
                    source=source,
                    link=link,
                    description=row.get("description"),
                )
                payload = sch.model_dump(mode="json", exclude_none=True)
            except Exception as e:
                logger.warning("ingest_scraped skip row=%s reason=validation err=%s", i, e)
                skipped_inv += 1
                continue
            st = models.ScholarshipStaging(
                title=title,
                provider=provider,
                source=source,
                payload_json=json.dumps(payload),
                status="pending",
                dedupe_key=key,
            )
            db.add(st)
            created += 1
        db.commit()
        print(
            f"Ingest complete: created={created}, skipped_duplicate={skipped_dup}, "
            f"skipped_invalid={skipped_inv}, skipped_already_live={skipped_live}"
        )
        try:
            from app.scrapers.run_logging import log_scraper_run

            log_scraper_run(
                "philscholar_ingest",
                "success",
                records_found=len(data),
                records_ingested=created,
                output_path=str(path),
            )
        except Exception as log_err:
            logger.warning("ingest_scraper_log_failed err=%s", log_err)
    finally:
        db.close()


if __name__ == "__main__":
    main()
