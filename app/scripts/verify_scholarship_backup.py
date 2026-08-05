"""Verify scholarship backup manifest matches expected production row counts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlalchemy import func

from app import models
from app.db import SessionLocal

from app.scripts.export_scholarship_backup import BACKUP_TABLES

ROOT = Path(__file__).resolve().parents[2]

TABLE_MODELS = {
    "scholarships": models.Scholarship,
    "field_evidence": models.FieldEvidence,
    "scholarship_versions": models.ScholarshipVersion,
    "scholarships_staging": models.ScholarshipStaging,
    "match_results": models.MatchResult,
    "saved_scholarships": models.SavedScholarship,
    "applications": models.Application,
    "scholarship_reports": models.ScholarshipReport,
    "notifications": models.Notification,
    "referral_click_daily": models.ReferralClickDaily,
}


def verify_manifest(manifest_path: Path) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    backup_counts = manifest.get("table_counts") or {}
    db = SessionLocal()
    try:
        live_counts: dict[str, int] = {}
        for table in BACKUP_TABLES:
            model = TABLE_MODELS[table]
            live_counts[table] = db.query(func.count()).select_from(model).scalar() or 0
    finally:
        db.close()

    mismatches = {
        table: {"backup": backup_counts.get(table), "live": live_counts.get(table)}
        for table in BACKUP_TABLES
        if backup_counts.get(table) != live_counts.get(table)
    }
    ok = not mismatches
    return {"ok": ok, "backup_counts": backup_counts, "live_counts": live_counts, "mismatches": mismatches}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=ROOT / "data" / "backups" / "pre_remediation_20260803.manifest.json",
    )
    args = parser.parse_args()
    result = verify_manifest(args.manifest)
    print(json.dumps(result, indent=2))
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
