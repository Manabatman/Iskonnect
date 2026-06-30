"""
Import a CSV of scholarship rows into the staging table (pending admin approval).

Each row should use column headers that map to Scholarship API fields (see schemas.Scholarship).
Requires admin auth in production; staging import API uses require_admin.

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
from app.scripts.import_scholarships import load_csv_strict
from app.utils.dedupe import scholarship_dedupe_key
from app.utils.import_validation import summarize_import_report, validate_import_row


def _dedupe_key(title: str, provider: str | None, link: str | None = None) -> str:
    return scholarship_dedupe_key(title, provider, link)


def _live_dedupe_keys(db) -> set[str]:
    keys = db.query(models.Scholarship.dedupe_key).filter(models.Scholarship.dedupe_key.isnot(None)).all()
    return {k[0] for k in keys}


def _pending_dedupe_keys(db) -> set[str]:
    keys = (
        db.query(models.ScholarshipStaging.dedupe_key)
        .filter(models.ScholarshipStaging.status == "pending")
        .all()
    )
    return {k[0] for k in keys if k[0]}


def main() -> None:
    parser = argparse.ArgumentParser(description="Import scholarships CSV into staging queue")
    parser.add_argument("--csv", required=True, help="Path to CSV file")
    parser.add_argument("--report", default=None, help="Optional path to write JSON import report")
    args = parser.parse_args()

    rows, structural = load_csv_strict(args.csv)
    report_rows: list[dict] = []

    if not structural.get("header_valid", True):
        report = summarize_import_report(report_rows, structural=structural)
        report["created"] = 0
        report["skipped"] = 0
        report["invalid"] = 0
        report["aborted"] = True
        report["abort_reason"] = "; ".join(structural.get("header_errors") or ["invalid_header"])
        print(json.dumps(report, indent=2, default=str))
        if args.report:
            Path(args.report).write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
        sys.exit(1)

    for rejection in structural.get("rejected_rows") or []:
        report_rows.append(rejection)

    db = SessionLocal()
    created = 0
    skipped = 0
    invalid = 0
    try:
        live_keys = _live_dedupe_keys(db)
        pending_keys = _pending_dedupe_keys(db)
        for row in rows:
            result = validate_import_row(row, live_dedupe_keys=live_keys, pending_dedupe_keys=pending_keys)
            if result.get("status") == "invalid":
                invalid += 1
                report_rows.append(result)
                continue
            if result.get("status") == "skipped":
                skipped += 1
                report_rows.append(result)
                continue
            title = (row.get("title") or "").strip()
            if not title:
                invalid += 1
                report_rows.append({"status": "invalid", "warnings": ["missing_title"]})
                continue
            provider = row.get("provider")
            link = row.get("link")
            key = _dedupe_key(title, provider, link)
            st = models.ScholarshipStaging(
                title=title,
                provider=provider,
                source=row.get("source") or "csv_import",
                payload_json=json.dumps(row),
                status="pending",
                dedupe_key=key,
            )
            db.add(st)
            pending_keys.add(key)
            created += 1
            result["status"] = "created"
            report_rows.append(result)
        db.commit()
        report = summarize_import_report(report_rows, structural=structural)
        report["created"] = created
        report["skipped"] = skipped
        report["invalid"] = invalid
        print(json.dumps(report, indent=2, default=str))
        if args.report:
            Path(args.report).write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    finally:
        db.close()


if __name__ == "__main__":
    main()
