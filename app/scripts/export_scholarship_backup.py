"""
Export scholarship-related tables to a timestamped SQL backup file.

Usage:
  python -m app.scripts.export_scholarship_backup
  python -m app.scripts.export_scholarship_backup --output data/backups/pre_remediation_20260803.sql
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlalchemy import inspect, text

from app.config import settings
from app.db import SessionLocal, engine

BACKUP_TABLES: tuple[str, ...] = (
    "scholarships",
    "field_evidence",
    "scholarship_versions",
    "scholarships_staging",
    "match_results",
    "saved_scholarships",
    "applications",
    "scholarship_reports",
    "notifications",
    "referral_click_daily",
)

ROOT = Path(__file__).resolve().parents[2]


def _sql_literal(value) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        return str(value)
    escaped = str(value).replace("'", "''")
    return f"'{escaped}'"


def export_backup(output_path: Path) -> dict:
    if not settings.database_url:
        raise SystemError("DATABASE_URL is not configured")

    inspector = inspect(engine)
    existing = set(inspector.get_table_names())
    missing = [t for t in BACKUP_TABLES if t not in existing]
    if missing:
        raise SystemError(f"Missing tables: {missing}")

    counts: dict[str, int] = {}
    lines: list[str] = [
        "-- ISKONNECT scholarship remediation backup",
        f"-- Generated: {datetime.now(timezone.utc).isoformat()}",
        f"-- Source: {settings.database_url.split('@')[-1] if '@' in settings.database_url else 'configured'}",
        "BEGIN;",
    ]

    db = SessionLocal()
    try:
        for table in BACKUP_TABLES:
            columns = [c["name"] for c in inspector.get_columns(table)]
            col_list = ", ".join(columns)
            rows = db.execute(text(f'SELECT * FROM "{table}" ORDER BY 1')).mappings().all()
            counts[table] = len(rows)
            lines.append(f"\n-- Table: {table} ({len(rows)} rows)")
            if not rows:
                continue
            for row in rows:
                values = ", ".join(_sql_literal(row[c]) for c in columns)
                lines.append(f'INSERT INTO "{table}" ({col_list}) VALUES ({values});')
    finally:
        db.close()

    lines.append("COMMIT;")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "output_path": str(output_path),
        "table_counts": counts,
        "total_rows": sum(counts.values()),
    }
    manifest_path = output_path.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Export scholarship-related tables to SQL backup")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "backups" / f"pre_remediation_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.sql",
    )
    args = parser.parse_args()
    manifest = export_backup(args.output)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
