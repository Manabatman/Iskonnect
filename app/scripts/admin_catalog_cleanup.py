"""
Admin catalog cleanup: merge-and-delete verified duplicate pairs and obsolete rows.

Usage:
  python -m app.scripts.admin_catalog_cleanup
  python -m app.scripts.admin_catalog_cleanup --apply
  python -m app.scripts.admin_catalog_cleanup --audit-only
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlalchemy import func

from app import models
from app.db import SessionLocal
from app.services.duplicate_detection import count_dedupe_key_collisions, find_duplicate_pairs
from app.services.scholarship_catalog_admin import (
    CatalogAdminError,
    deactivate_scholarship,
    merge_before_delete,
    permanently_delete_scholarship,
)

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = ROOT / "data" / "admin_catalog_cleanup_report.json"

# canonical_id -> duplicate_id (delete duplicate, keep canonical)
MERGE_PAIRS: dict[int, int] = {
    1: 114,
    10: 115,
    61: 116,
    75: 126,
    124: 110,
    88: 22,
    66: 6,
    73: 2,
    72: 12,
    25: 21,
}

STANDALONE_DELETE = [79, 19]

JLSS_TRACK_IDS = [121, 122, 123]


@dataclass
class CleanupOutcome:
    action: str
    scholarship_id: int
    detail: str = ""


@dataclass
class CleanupReport:
    dry_run: bool = True
    audit_only: bool = False
    merge_outcomes: list[CleanupOutcome] = field(default_factory=list)
    standalone_outcomes: list[CleanupOutcome] = field(default_factory=list)
    audit: dict = field(default_factory=dict)


def _audit_catalog(db) -> dict:
    total = db.query(func.count(models.Scholarship.id)).scalar() or 0
    active = (
        db.query(func.count(models.Scholarship.id))
        .filter(models.Scholarship.is_active == True)  # noqa: E712
        .scalar()
        or 0
    )
    inactive = total - active
    fuzzy_pairs = len(find_duplicate_pairs(db, min_confidence=0.85, include_inactive=True))
    dedupe_collisions = count_dedupe_key_collisions(db)
    broken = (
        db.query(func.count(models.Scholarship.id))
        .filter(models.Scholarship.link_status == "broken")
        .scalar()
        or 0
    )

    orphan_saved = 0
    orphan_apps = 0
    sch_ids = {r[0] for r in db.query(models.Scholarship.id).all()}
    for row in db.query(models.SavedScholarship.scholarship_id).distinct():
        if row[0] not in sch_ids:
            orphan_saved += 1
    for row in db.query(models.Application.scholarship_id).distinct():
        if row[0] not in sch_ids:
            orphan_apps += 1

    return {
        "total": int(total),
        "active": int(active),
        "inactive": int(inactive),
        "dedupe_key_collision_groups": dedupe_collisions,
        "fuzzy_duplicate_pairs": fuzzy_pairs,
        "broken_links": int(broken),
        "orphan_saved_scholarships": orphan_saved,
        "orphan_applications": orphan_apps,
    }


def run(*, apply: bool = False, audit_only: bool = False) -> CleanupReport:
    db = SessionLocal()
    report = CleanupReport(dry_run=not apply, audit_only=audit_only)
    try:
        if not audit_only:
            for canonical_id, duplicate_id in MERGE_PAIRS.items():
                try:
                    if apply:
                        result = merge_before_delete(db, canonical_id, duplicate_id, dry_run=False)
                        db.commit()
                        detail = f"merged fields={result.fields_merged}, deleted={result.deleted}"
                    else:
                        result = merge_before_delete(db, canonical_id, duplicate_id, dry_run=True)
                        detail = f"would merge fields={result.fields_merged}"
                    report.merge_outcomes.append(
                        CleanupOutcome("merged", duplicate_id, f"keep {canonical_id}: {detail}")
                    )
                except CatalogAdminError as exc:
                    db.rollback()
                    report.merge_outcomes.append(
                        CleanupOutcome("skipped", duplicate_id, f"keep {canonical_id}: {exc.message}")
                    )

            for sid in STANDALONE_DELETE:
                row = db.query(models.Scholarship).filter(models.Scholarship.id == sid).first()
                if not row:
                    report.standalone_outcomes.append(CleanupOutcome("skipped", sid, "not found"))
                    continue
                if sid == 79:
                    tracks = (
                        db.query(models.Scholarship)
                        .filter(models.Scholarship.id.in_(JLSS_TRACK_IDS))
                        .count()
                    )
                    if tracks < len(JLSS_TRACK_IDS):
                        report.standalone_outcomes.append(
                            CleanupOutcome("skipped", sid, f"JLSS tracks missing ({tracks}/3)")
                        )
                        continue
                try:
                    if row.is_active is not False:
                        if apply:
                            deactivate_scholarship(db, row)
                            db.flush()
                        else:
                            report.standalone_outcomes.append(
                                CleanupOutcome("deactivate", sid, "would deactivate before delete")
                            )
                    if apply:
                        permanently_delete_scholarship(db, sid, skip_inactive_guard=True)
                        db.commit()
                        report.standalone_outcomes.append(CleanupOutcome("deleted", sid, "permanent delete"))
                    else:
                        report.standalone_outcomes.append(
                            CleanupOutcome("delete", sid, "would permanently delete")
                        )
                except CatalogAdminError as exc:
                    db.rollback()
                    report.standalone_outcomes.append(CleanupOutcome("skipped", sid, exc.message))

        report.audit = _audit_catalog(db)
        return report
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Admin catalog duplicate cleanup")
    parser.add_argument("--apply", action="store_true", help="Apply changes to database")
    parser.add_argument("--audit-only", action="store_true", help="Only emit audit metrics")
    args = parser.parse_args()

    report = run(apply=args.apply, audit_only=args.audit_only)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": report.dry_run,
        "audit_only": report.audit_only,
        "merge_outcomes": [asdict(o) for o in report.merge_outcomes],
        "standalone_outcomes": [asdict(o) for o in report.standalone_outcomes],
        "audit": report.audit,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"\nWrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
