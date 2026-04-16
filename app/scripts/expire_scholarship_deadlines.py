"""
Mark scholarships with application_deadline in the past as inactive (no scraping required).
Also runs stale-verification flags and clears the scholarship list cache.

Usage:
  python -m app.scripts.expire_scholarship_deadlines
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings
from app.jobs.catalog_maintenance import run_catalog_maintenance

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    db_url = (settings.database_url or "").strip()
    if not db_url:
        raise SystemExit("DATABASE_URL is not configured.")

    from datetime import date

    today = date.today()
    out = run_catalog_maintenance()
    exp = out.get("expired", 0)
    rev = out.get("needs_review", 0)
    logger.info(
        "expire_scholarship_deadlines (catalog_maintenance) deadline_synced=%s needs_review=%s as_of=%s",
        exp,
        rev,
        today.isoformat(),
    )
    print(
        f"Catalog maintenance as of {today.isoformat()}: "
        f"deadline rows updated={exp}, flagged needs_review={rev}."
    )


if __name__ == "__main__":
    main()
