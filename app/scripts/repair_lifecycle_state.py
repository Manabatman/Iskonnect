"""
Repair scholarships wrongly archived by deadline-expiry maintenance.

Dry-run by default. Restores is_active, rolls past deadlines into last_close_date,
and writes scholarship_versions for each repair.

Usage:
  python -m app.scripts.repair_lifecycle_state
  python -m app.scripts.repair_lifecycle_state --apply
  python -m app.scripts.repair_lifecycle_state --apply --report data/repair_lifecycle.json
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlalchemy.orm import Session

from app import models
from app.db import SessionLocal
from app.utils.application_status import sync_application_status
from app.utils.editorial_state import PUBLISHED, apply_editorial_state
from app.utils.lifecycle_repair import is_permanently_discontinued, sync_past_deadline_cycle
from app.utils.scholarship_versioning import diff_snapshots, record_scholarship_version, snapshot_scholarship_row

logger = logging.getLogger(__name__)


@dataclass
class RepairOutcome:
    scholarship_id: int
    title: str
    action: str
    detail: str = ""


@dataclass
class RepairSummary:
    candidates: int = 0
    repaired: int = 0
    skipped: int = 0
    dry_run: bool = True
    outcomes: list[RepairOutcome] = field(default_factory=list)


def _needs_repair(s: models.Scholarship, today: date) -> tuple[bool, str]:
    if is_permanently_discontinued(s):
        return False, "permanently_discontinued"

    if s.is_active is False or (s.application_status or "").lower() == "archived":
        if s.editorial_state == "archived" or s.data_status in ("expired", "past_deadline"):
            return True, "wrongly_archived_by_deadline"

    if s.application_deadline and s.application_deadline < today and s.is_active is not False:
        return True, "stale_deadline_needs_cycle_roll"

    if s.data_status in ("expired", "past_deadline") and not is_permanently_discontinued(s):
        return True, "legacy_expired_status"

    return False, ""


def repair_row(db: Session, s: models.Scholarship, *, today: date, dry_run: bool) -> RepairOutcome | None:
    needs, reason = _needs_repair(s, today)
    if not needs:
        return None

    before = snapshot_scholarship_row(s)

    if s.is_active is False or s.editorial_state == "archived":
        apply_editorial_state(s, PUBLISHED, today=today)

    sync_past_deadline_cycle(s, today=today)
    sync_application_status(s, today=today)

    if s.data_status in ("expired", "past_deadline"):
        s.data_status = "active"

    after = snapshot_scholarship_row(s)
    changes = diff_snapshots(before, after)
    if not changes:
        return RepairOutcome(s.id, s.title[:80], "skipped", "no effective change")

    if not dry_run:
        record_scholarship_version(db, scholarship_id=s.id, changes=changes, changed_by=None)

    return RepairOutcome(s.id, s.title[:80], "repaired", reason)


def run(*, apply: bool = False) -> RepairSummary:
    today = date.today()
    db = SessionLocal()
    summary = RepairSummary(dry_run=not apply)
    try:
        rows = db.query(models.Scholarship).order_by(models.Scholarship.id).all()
        for s in rows:
            outcome = repair_row(db, s, today=today, dry_run=not apply)
            if outcome is None:
                continue
            summary.candidates += 1
            summary.outcomes.append(outcome)
            if outcome.action == "repaired":
                summary.repaired += 1
            else:
                summary.skipped += 1

        if apply:
            db.commit()
        else:
            db.rollback()
        return summary
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Repair deadline-wrong archival state")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--report", default=None)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    summary = run(apply=args.apply)
    payload = {
        "dry_run": summary.dry_run,
        "candidates": summary.candidates,
        "repaired": summary.repaired,
        "skipped": summary.skipped,
        "outcomes": [o.__dict__ for o in summary.outcomes],
    }
    print(json.dumps(payload, indent=2))
    if args.report:
        Path(args.report).write_text(json.dumps(payload, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
