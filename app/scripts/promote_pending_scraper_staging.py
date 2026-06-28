"""
One-off / maintenance: promote pending staging rows from trusted scraper sources to live scholarships.

Usage:
  python -m app.scripts.promote_pending_scraper_staging
  python -m app.scripts.promote_pending_scraper_staging --dry-run
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.db import SessionLocal
from app import models
from app.scholarship_cache import invalidate_scholarship_cache
from app.utils.staging_promotion import is_trusted_scraper_source, promote_staging_row

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Promote pending scraper staging rows to live catalog")
    parser.add_argument("--dry-run", action="store_true", help="List pending rows without promoting")
    args = parser.parse_args()

    db = SessionLocal()
    promoted = skipped = failed = 0
    try:
        rows = (
            db.query(models.ScholarshipStaging)
            .filter(models.ScholarshipStaging.status == "pending")
            .order_by(models.ScholarshipStaging.created_at.asc())
            .all()
        )
        trusted = [r for r in rows if is_trusted_scraper_source(r.source)]
        if args.dry_run:
            print(f"Would promote {len(trusted)} trusted pending row(s) (of {len(rows)} total pending)")
            for r in trusted:
                print(f"  id={r.id} source={r.source!r} title={r.title[:60]!r}")
            return

        for row in trusted:
            try:
                out = promote_staging_row(db, row)
                if out is None:
                    skipped += 1
                else:
                    promoted += 1
            except Exception as e:
                failed += 1
                logger.exception("promote_failed id=%s err=%s", row.id, e)

        if promoted > 0:
            db.commit()
            invalidate_scholarship_cache()
        else:
            db.rollback()

        print(
            f"Promote complete: promoted={promoted}, skipped_duplicate={skipped}, failed={failed}, "
            f"trusted_pending={len(trusted)}"
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
