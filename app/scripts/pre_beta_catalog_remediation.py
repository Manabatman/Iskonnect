"""
Pre-beta catalog remediation — Gabay Guro, Pagpupugay, MEXT/GKS destination data.

Field evidence only; does not bump last_verified_at.

Usage:
  python -m app.scripts.pre_beta_catalog_remediation
  python -m app.scripts.pre_beta_catalog_remediation --apply
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlalchemy.orm import Session

from app import models
from app.db import SessionLocal
from app.scholarship_cache import invalidate_scholarship_cache
from app.scripts.migration_v1_backfill import BackfillReport, _apply_field_update, _link_affiliation
from app.utils.field_evidence import create_field_evidence

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "verification" / "export" / "pre_beta_remediation_manifest.json"

_JSON_LIST_FIELDS = frozenset({"eligible_courses_psced", "eligible_courses_specific", "eligible_levels"})


def _load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _normalize_fields(fields: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, val in fields.items():
        if key in _JSON_LIST_FIELDS and isinstance(val, list):
            out[key] = json.dumps(val)
        else:
            out[key] = val
    return out


def _ensure_affiliation_seed(db: Session, code: str, *, dry_run: bool) -> bool:
    row = db.query(models.AffiliationCode).filter(models.AffiliationCode.code == code).first()
    if row:
        return False
    if dry_run:
        return True
    db.add(
        models.AffiliationCode(
            code=code,
            kind="equity",
            label="Medical frontliner dependent",
        )
    )
    return True


def run_remediation(*, apply: bool = False, db: Session | None = None) -> BackfillReport:
    manifest = _load_manifest()
    report = BackfillReport(dry_run=not apply)
    owns_session = db is None
    if owns_session:
        db = SessionLocal()
    assert db is not None
    try:
        for entry in manifest.get("required_affiliation_assignments") or []:
            code = str(entry.get("affiliation_code") or "")
            if code == "medical_frontliner_dependent":
                if _ensure_affiliation_seed(db, code, dry_run=not apply):
                    report.affiliation_links.append({"seeded": code})

        for entry in manifest.get("scholarship_field_updates") or []:
            sid = entry.get("id")
            row = db.query(models.Scholarship).filter(models.Scholarship.id == sid).first()
            if not row:
                report.skipped.append({"id": sid, "reason": "not found"})
                continue
            fields = _normalize_fields(entry.get("fields") or {})
            changed = _apply_field_update(db, row, fields, dry_run=not apply)
            if changed:
                report.field_updates.append({"id": sid, "fields_changed": changed, "reason": entry.get("reason")})

        for entry in manifest.get("required_affiliation_assignments") or []:
            code = entry.get("affiliation_code")
            for sid in entry.get("scholarship_ids") or []:
                if _link_affiliation(db, int(sid), str(code), dry_run=not apply):
                    report.affiliation_links.append({"scholarship_id": sid, "affiliation_code": code})
                    if apply:
                        create_field_evidence(
                            db,
                            scholarship_id=int(sid),
                            field_key="required_affiliation_codes",
                            value_snapshot=str(code),
                            source_type="pre_beta_remediation",
                        )

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
    parser = argparse.ArgumentParser(description="Pre-beta catalog remediation")
    parser.add_argument("--apply", action="store_true", help="Persist changes (default: dry run)")
    args = parser.parse_args()
    report = run_remediation(apply=args.apply)
    logger.info(
        "pre_beta_remediation complete dry_run=%s fields=%s affiliations=%s skipped=%s",
        report.dry_run,
        len(report.field_updates),
        len(report.affiliation_links),
        len(report.skipped),
    )


if __name__ == "__main__":
    main()
