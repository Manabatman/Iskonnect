"""
Import a CSV of scholarship rows into the staging table (pending admin approval).

Each row should use column headers that map to Scholarship API fields (see schemas.Scholarship).
Requires admin auth in production; for local dev with AUTH_DISABLED=true, staging import is open.

Usage:
  python -m app.scripts.csv_to_staging --csv path/to/file.csv

With DATABASE_URL set and migrations applied.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Project root
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.db import SessionLocal
from app import models
from app.scripts.import_scholarships import load_csv  # reuse normalized CSV loader
from app.utils.dedupe import scholarship_dedupe_key


def _dedupe_key(title: str, provider: str | None, link: str | None = None) -> str:
    return scholarship_dedupe_key(title, provider, link)


def main() -> None:
    parser = argparse.ArgumentParser(description="Import scholarships CSV into staging queue")
    parser.add_argument("--csv", required=True, help="Path to CSV file")
    args = parser.parse_args()

    rows = load_csv(args.csv)
    db = SessionLocal()
    created = 0
    skipped = 0
    try:
        for row in rows:
            title = (row.get("title") or "").strip()
            if not title:
                skipped += 1
                continue
            provider = row.get("provider")
            link = row.get("link")
            key = _dedupe_key(title, provider, link)
            if (
                db.query(models.ScholarshipStaging)
                .filter(models.ScholarshipStaging.dedupe_key == key, models.ScholarshipStaging.status == "pending")
                .first()
            ):
                skipped += 1
                continue
            st = models.ScholarshipStaging(
                title=title,
                provider=provider,
                source=row.get("source") or "csv_import",
                payload_json=json.dumps(row),
                status="pending",
                dedupe_key=key,
            )
            db.add(st)
            created += 1
        db.commit()
        print(f"Staging import complete: created={created}, skipped={skipped}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
