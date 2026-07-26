"""
Backfill trust labels for research-imported rows that were wrongly marked manual/verified.

Usage:
  python -m app.scripts.backfill_import_trust --apply
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app import models
from app.db import SessionLocal


def run(*, apply: bool = False, min_id: int = 92) -> dict:
    db = SessionLocal()
    updated = 0
    try:
        rows = (
            db.query(models.Scholarship)
            .filter(
                models.Scholarship.id >= min_id,
                models.Scholarship.verification_source.in_(("manual", None, "")),
            )
            .all()
        )
        for r in rows:
            r.verification_source = "csv_import"
            r.last_verified_at = None
            r.confidence_score = None
            if r.editorial_state in (None, "", "verified"):
                r.editorial_state = "imported"
            updated += 1
        if apply:
            db.commit()
        else:
            db.rollback()
        return {"updated": updated, "dry_run": not apply}
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--min-id", type=int, default=92)
    args = parser.parse_args()
    print(run(apply=args.apply, min_id=args.min_id))


if __name__ == "__main__":
    main()
