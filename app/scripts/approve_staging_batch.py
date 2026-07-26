"""
Bulk-approve pending scholarship staging rows into the live catalog.

Uses the same promotion path as POST /api/v1/scholarships/staging/{id}/approve.

Usage:
  python -m app.scripts.approve_staging_batch
  python -m app.scripts.approve_staging_batch --apply
  python -m app.scripts.approve_staging_batch --apply --source discovery_import
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app import models
from app.db import SessionLocal
from app.utils.staging_promotion import promote_staging_row

logger = logging.getLogger(__name__)


def run(*, apply: bool = False, source_filter: str | None = None) -> dict:
    db = SessionLocal()
    summary = {"pending": 0, "approved": 0, "rejected": 0, "errors": 0, "rows": []}
    try:
        q = db.query(models.ScholarshipStaging).filter(models.ScholarshipStaging.status == "pending")
        if source_filter:
            q = q.filter(models.ScholarshipStaging.source.ilike(f"%{source_filter}%"))
        rows = q.order_by(models.ScholarshipStaging.id).all()
        summary["pending"] = len(rows)

        for row in rows:
            entry = {"id": row.id, "title": row.title, "source": row.source, "status": "dry_run"}
            if not apply:
                summary["rows"].append(entry)
                continue
            try:
                promoted = promote_staging_row(db, row, version_changed_by=None)
                if promoted:
                    db.commit()
                    entry["status"] = "approved"
                    entry["scholarship_id"] = promoted.id
                    summary["approved"] += 1
                else:
                    db.commit()
                    entry["status"] = "rejected_duplicate"
                    summary["rejected"] += 1
            except Exception as exc:
                db.rollback()
                entry["status"] = "error"
                entry["error"] = str(exc)
                summary["errors"] += 1
                logger.exception("staging_approve_failed id=%s", row.id)
            summary["rows"].append(entry)
        return summary
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Bulk approve pending scholarship staging rows")
    parser.add_argument("--apply", action="store_true", help="Persist approvals (default is dry-run)")
    parser.add_argument("--source", default=None, help="Optional source substring filter")
    parser.add_argument("--report", default=None, help="Write JSON summary to this path")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    summary = run(apply=args.apply, source_filter=args.source)
    print(json.dumps(summary, indent=2))
    if args.report:
        Path(args.report).write_text(json.dumps(summary, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
