"""
Migration v1 catalog backfill — sparse columns, join tables, consortium schools.

Idempotent; safe to dry-run.

Usage:
  python -m app.scripts.migration_v1_backfill
  python -m app.scripts.migration_v1_backfill --apply
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlalchemy.orm import Session

from app import models
from app.db import SessionLocal
from app.scholarship_cache import invalidate_scholarship_cache
from app.utils.field_evidence import create_field_evidence
from app.utils.json_helpers import parse_json

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "verification" / "export" / "migration_v1_backfill_manifest.json"


@dataclass
class BackfillReport:
    dry_run: bool = True
    field_updates: list[dict[str, Any]] = field(default_factory=list)
    consortium_updates: list[dict[str, Any]] = field(default_factory=list)
    conflict_links: list[dict[str, Any]] = field(default_factory=list)
    affiliation_links: list[dict[str, Any]] = field(default_factory=list)
    skipped: list[dict[str, Any]] = field(default_factory=list)
    errors: list[dict[str, Any]] = field(default_factory=list)


def _load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _merge_json_list(existing: Any, new_values: list[str]) -> str:
    current = parse_json(existing) or []
    merged = list(dict.fromkeys([*(str(x) for x in current if x), *new_values]))
    return json.dumps(merged)


def _apply_field_update(db: Session, row: models.Scholarship, fields: dict[str, Any], *, dry_run: bool) -> list[str]:
    changed: list[str] = []
    for key, val in fields.items():
        if key == "eligible_enrollment_status" and isinstance(val, list):
            new_val = _merge_json_list(getattr(row, key, None), val)
            if getattr(row, key, None) != new_val:
                if not dry_run:
                    setattr(row, key, new_val)
                    create_field_evidence(
                        db,
                        scholarship_id=row.id,
                        field_key=key,
                        value_snapshot=new_val,
                        source_type="migration_v1_backfill",
                    )
                changed.append(key)
            continue
        if key == "eligible_schools" and isinstance(val, list):
            new_val = json.dumps(val)
            if getattr(row, key, None) != new_val:
                if not dry_run:
                    setattr(row, key, new_val)
                    create_field_evidence(
                        db,
                        scholarship_id=row.id,
                        field_key=key,
                        value_snapshot=new_val,
                        source_type="migration_v1_backfill",
                    )
                changed.append(key)
            continue
        if getattr(row, key, None) != val:
            if not dry_run:
                setattr(row, key, val)
                create_field_evidence(
                    db,
                    scholarship_id=row.id,
                    field_key=key,
                    value_snapshot=str(val),
                    source_type="migration_v1_backfill",
                )
            changed.append(key)
    return changed


def _link_scope(db: Session, sid: int, scope_code: str, *, dry_run: bool) -> bool:
    scope = db.query(models.ConflictScope).filter(models.ConflictScope.code == scope_code).first()
    if not scope:
        return False
    exists = (
        db.query(models.ScholarshipConflictScope)
        .filter(
            models.ScholarshipConflictScope.scholarship_id == sid,
            models.ScholarshipConflictScope.scope_id == scope.id,
        )
        .first()
    )
    if exists:
        return False
    if not dry_run:
        db.add(models.ScholarshipConflictScope(scholarship_id=sid, scope_id=scope.id))
    return True


def _link_affiliation(db: Session, sid: int, aff_code: str, *, dry_run: bool) -> bool:
    aff = db.query(models.AffiliationCode).filter(models.AffiliationCode.code == aff_code).first()
    if not aff:
        return False
    exists = (
        db.query(models.ScholarshipRequiredAffiliation)
        .filter(
            models.ScholarshipRequiredAffiliation.scholarship_id == sid,
            models.ScholarshipRequiredAffiliation.affiliation_id == aff.id,
        )
        .first()
    )
    if exists:
        return False
    if not dry_run:
        db.add(models.ScholarshipRequiredAffiliation(scholarship_id=sid, affiliation_id=aff.id))
    return True


def run_backfill(*, apply: bool = False, db: Session | None = None) -> BackfillReport:
    manifest = _load_manifest()
    report = BackfillReport(dry_run=not apply)
    owns_session = db is None
    if owns_session:
        db = SessionLocal()
    assert db is not None
    try:
        for entry in manifest.get("scholarship_field_updates") or []:
            sid = entry.get("id")
            row = db.query(models.Scholarship).filter(models.Scholarship.id == sid).first()
            if not row:
                report.skipped.append({"id": sid, "reason": "not found"})
                continue
            fields = entry.get("fields") or {}
            changed = _apply_field_update(db, row, fields, dry_run=not apply)
            if changed:
                report.field_updates.append({"id": sid, "fields_changed": changed, "reason": entry.get("reason")})

        for entry in manifest.get("consortium_school_updates") or []:
            needle = (entry.get("title_contains") or "").lower()
            schools = entry.get("eligible_schools") or []
            rows = db.query(models.Scholarship).filter(models.Scholarship.is_active != False).all()  # noqa: E712
            for row in rows:
                title_lower = (row.title or "").lower()
                if needle and needle not in title_lower:
                    continue
                # Skip umbrella rows that bundle multiple graduate consortium programs.
                if needle == "asthrdp" and "erdt" in title_lower and "/" in title_lower:
                    continue
                if needle == "erdt" and "asthrdp" in title_lower and "/" in title_lower:
                    continue
                changed = _apply_field_update(db, row, {"eligible_schools": schools}, dry_run=not apply)
                if changed:
                    report.consortium_updates.append({"id": row.id, "title": row.title})

        for entry in manifest.get("conflict_scope_assignments") or []:
            code = entry.get("scope_code")
            for sid in entry.get("scholarship_ids") or []:
                if _link_scope(db, int(sid), str(code), dry_run=not apply):
                    report.conflict_links.append({"scholarship_id": sid, "scope_code": code})

        for entry in manifest.get("required_affiliation_assignments") or []:
            code = entry.get("affiliation_code")
            for sid in entry.get("scholarship_ids") or []:
                if _link_affiliation(db, int(sid), str(code), dry_run=not apply):
                    report.affiliation_links.append({"scholarship_id": sid, "affiliation_code": code})

        for entry in manifest.get("age_as_of_updates") or []:
            fields = {
                "age_as_of_date": date.fromisoformat(str(entry["age_as_of_date"])),
                "age_as_of_rule": entry.get("age_as_of_rule"),
            }
            for sid in entry.get("scholarship_ids") or []:
                row = db.query(models.Scholarship).filter(models.Scholarship.id == sid).first()
                if not row:
                    report.skipped.append({"id": sid, "reason": "not found for age_as_of"})
                    continue
                changed = _apply_field_update(db, row, fields, dry_run=not apply)
                if changed:
                    report.field_updates.append({"id": sid, "fields_changed": changed, "reason": entry.get("reason")})

        if apply and owns_session:
            db.commit()
            invalidate_scholarship_cache()
        elif owns_session:
            db.rollback()
    except Exception as exc:
        if owns_session:
            db.rollback()
        report.errors.append({"error": str(exc)})
        raise
    finally:
        if owns_session:
            db.close()
    return report


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Migration v1 eligibility backfill")
    parser.add_argument("--apply", action="store_true", help="Persist changes (default: dry run)")
    args = parser.parse_args()
    report = run_backfill(apply=args.apply)
    logger.info(
        "migration_v1_backfill complete dry_run=%s fields=%s consortium=%s conflicts=%s affiliations=%s",
        report.dry_run,
        len(report.field_updates),
        len(report.consortium_updates),
        len(report.conflict_links),
        len(report.affiliation_links),
    )


if __name__ == "__main__":
    main()
