"""
Merge confirmed semantic duplicate scholarship pairs.

Policy: keep canonical row, archive loser with application_status=archived,
migrate saved_scholarship references, write field_evidence + versions. No hard deletes.

Usage:
  python -m app.scripts.merge_catalog_duplicates
  python -m app.scripts.merge_catalog_duplicates --apply
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlalchemy.orm import Session

from app import models
from app.db import SessionLocal
from app.utils.application_status import sync_application_status
from app.utils.editorial_state import ARCHIVED, apply_editorial_state
from app.utils.field_evidence import create_field_evidence
from app.utils.scholarship_versioning import diff_snapshots, record_scholarship_version, snapshot_scholarship_row

logger = logging.getLogger(__name__)

# canonical_id -> duplicate_id
MERGE_PAIRS: dict[int, int] = {
    1: 114,   # CHED Merit
    10: 115,  # SM Foundation
    61: 116,  # Megaworld
    75: 126,  # Aboitiz
    124: 110,  # OWWA ELAP (keep 124)
}

UMBRELLA_UPDATES: dict[int, dict] = {
    4: {
        "title": "TESDA Scholarship Programs (umbrella)",
        "description": (
            "Umbrella entry for TESDA-funded scholarship and training programs. "
            "See linked tracks: Training for Work Scholarship Program (TWSP) and "
            "Special Training for Employment Program (STEP)."
        ),
    },
    79: {
        "title": "DOST-SEI Junior Level Science Scholarship (JLSS) — umbrella",
        "description": (
            "Umbrella for DOST-SEI JLSS merit, RA 7687, and RA 10612 tracks. "
            "Each track has its own listing for eligibility-specific matching."
        ),
    },
}


@dataclass
class MergeOutcome:
    action: str
    canonical_id: int
    duplicate_id: int
    detail: str = ""


@dataclass
class MergeSummary:
    merged: int = 0
    umbrella_updated: int = 0
    dry_run: bool = True
    outcomes: list[MergeOutcome] = field(default_factory=list)


def _migrate_saved_references(db: Session, *, from_id: int, to_id: int, dry_run: bool) -> int:
    rows = db.query(models.SavedScholarship).filter(models.SavedScholarship.scholarship_id == from_id).all()
    count = 0
    for row in rows:
        exists = (
            db.query(models.SavedScholarship)
            .filter(
                models.SavedScholarship.user_id == row.user_id,
                models.SavedScholarship.scholarship_id == to_id,
            )
            .first()
        )
        if exists:
            if not dry_run:
                db.delete(row)
        else:
            if not dry_run:
                row.scholarship_id = to_id
        count += 1
    return count


def merge_pair(db: Session, canonical_id: int, duplicate_id: int, *, dry_run: bool) -> MergeOutcome:
    canonical = db.query(models.Scholarship).filter(models.Scholarship.id == canonical_id).first()
    duplicate = db.query(models.Scholarship).filter(models.Scholarship.id == duplicate_id).first()
    if not canonical or not duplicate:
        return MergeOutcome("skipped", canonical_id, duplicate_id, "missing row")

    before = snapshot_scholarship_row(duplicate)
    migrated = _migrate_saved_references(db, from_id=duplicate_id, to_id=canonical_id, dry_run=dry_run)

    if not dry_run:
        apply_editorial_state(duplicate, ARCHIVED)
        duplicate.is_active = False
        duplicate.application_status = "archived"
        duplicate.data_status = "expired"
        note = f"Merged into scholarship id={canonical_id} ({canonical.title})"
        duplicate.description = ((duplicate.description or "").strip() + f"\n\n{note}").strip()
        sync_application_status(duplicate)
        create_field_evidence(
            db,
            scholarship_id=duplicate_id,
            field_key="merge",
            value_snapshot=str(canonical_id),
            source_url=canonical.link,
            source_type="duplicate_merge",
            evidence_snippet=note,
            confidence=1.0,
        )
        after = snapshot_scholarship_row(duplicate)
        changes = diff_snapshots(before, after)
        if changes:
            record_scholarship_version(db, scholarship_id=duplicate_id, changes=changes, changed_by=None)

    return MergeOutcome(
        "merged",
        canonical_id,
        duplicate_id,
        f"saved_refs_migrated={migrated}",
    )


def apply_umbrella(db: Session, sid: int, updates: dict, *, dry_run: bool) -> bool:
    row = db.query(models.Scholarship).filter(models.Scholarship.id == sid).first()
    if not row:
        return False
    before = snapshot_scholarship_row(row)
    for key, val in updates.items():
        setattr(row, key, val)
    if not dry_run:
        after = snapshot_scholarship_row(row)
        changes = diff_snapshots(before, after)
        if changes:
            record_scholarship_version(db, scholarship_id=sid, changes=changes, changed_by=None)
    return True


def run(*, apply: bool = False) -> MergeSummary:
    db = SessionLocal()
    summary = MergeSummary(dry_run=not apply)
    try:
        for canonical_id, duplicate_id in MERGE_PAIRS.items():
            outcome = merge_pair(db, canonical_id, duplicate_id, dry_run=not apply)
            summary.outcomes.append(outcome)
            if outcome.action == "merged":
                summary.merged += 1

        for sid, updates in UMBRELLA_UPDATES.items():
            if apply_umbrella(db, sid, updates, dry_run=not apply):
                summary.umbrella_updated += 1

        if apply:
            db.commit()
        else:
            db.rollback()
        return summary
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    summary = run(apply=args.apply)
    print(json.dumps({"merged": summary.merged, "umbrella_updated": summary.umbrella_updated, "outcomes": [o.__dict__ for o in summary.outcomes]}, indent=2))


if __name__ == "__main__":
    main()
