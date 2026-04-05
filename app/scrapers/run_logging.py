"""Persist scraper execution summary to scraper_runs (optional; fails quietly if DB unavailable)."""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


def log_scraper_run(
    source: str,
    status: str,
    *,
    records_found: int | None = None,
    records_ingested: int | None = None,
    output_path: str | None = None,
    error_detail: str | None = None,
) -> None:
    try:
        from app.db import SessionLocal
        from app import models
        from app.utils.timezone import utc_now_naive

        db = SessionLocal()
        try:
            row = models.ScraperRun(
                source=source,
                status=status,
                records_found=records_found,
                records_ingested=records_ingested,
                output_path=output_path,
                error_detail=error_detail,
                completed_at=utc_now_naive(),
            )
            db.add(row)
            db.commit()
        finally:
            db.close()
    except Exception as e:
        logger.warning("scraper_run_log_failed source=%s err=%s", source, e)
