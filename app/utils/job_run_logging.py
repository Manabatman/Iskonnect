"""Log background job runs to the scraper_runs table (legacy name; used for all maintenance jobs)."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from app import models
from app.db import SessionLocal

logger = logging.getLogger(__name__)


def log_job_run(
    source: str,
    status: str,
    *,
    records_found: int = 0,
    records_ingested: int = 0,
    output_path: str | None = None,
    error_detail: str | None = None,
) -> None:
    db = SessionLocal()
    try:
        row = models.ScraperRun(
            source=source,
            status=status,
            records_found=records_found,
            records_ingested=records_ingested,
            output_path=output_path,
            error_detail=error_detail,
            started_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc),
        )
        db.add(row)
        db.commit()
    except Exception as e:
        logger.warning("job_run_log_failed source=%s err=%s", source, e)
        db.rollback()
    finally:
        db.close()
