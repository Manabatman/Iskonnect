"""
Automated validation for non-tier-1 catalog rows.

Link health, status recompute, unsupported deadline detection, structural flags.

Usage:
  python -m app.scripts.automated_catalog_validation --apply
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app import models
from app.db import SessionLocal
from app.jobs.link_checker import _head_status
from app.utils.application_status import sync_application_status
from app.utils.lifecycle_repair import sync_past_deadline_cycle

logger = logging.getLogger(__name__)

TIER1_PROVIDER_KEYWORDS = (
    "commission on higher education",
    "ched",
    "unifast",
    "dost",
    "science education institute",
    "tesda",
    "owwa",
    "dswd",
    "gsis",
    "sss",
    "department of health",
    "ncip",
    "sm foundation",
    "megaworld",
    "aboitiz",
    "ayala",
    "metrobank",
    "bpi",
    "pldt",
    "security bank",
    "ateneo",
    "de la salle",
    "santo tomas",
    "university of the philippines",
    "university of makati",
)


def _is_tier1(row: models.Scholarship) -> bool:
    blob = f"{row.provider or ''} {row.title or ''}".lower()
    return any(k in blob for k in TIER1_PROVIDER_KEYWORDS)


def run(*, apply: bool = False) -> dict:
    today = date.today()
    db = SessionLocal()
    stats = {"checked": 0, "link_updates": 0, "cycle_rolls": 0, "labeled_import": 0}
    queue: list[dict] = []
    try:
        rows = db.query(models.Scholarship).filter(models.Scholarship.is_active != False).all()  # noqa: E712
        for r in rows:
            if _is_tier1(r):
                continue
            stats["checked"] += 1
            url = (r.link or "").strip()
            if url.startswith(("http://", "https://")):
                time.sleep(0.5)
                ok, tag = _head_status(url)
                new_status = "ok" if ok else "broken"
                if (r.link_status or "") != new_status:
                    stats["link_updates"] += 1
                    if apply:
                        r.link_status = new_status
                        r.link_last_checked_at = datetime_now()

            if r.application_deadline and r.application_deadline < today:
                if apply and sync_past_deadline_cycle(r, today=today):
                    stats["cycle_rolls"] += 1
                elif not apply:
                    stats["cycle_rolls"] += 1

            if apply:
                if not r.verification_source or r.verification_source == "manual":
                    if not (
                        db.query(models.FieldEvidence)
                        .filter(
                            models.FieldEvidence.scholarship_id == r.id,
                            models.FieldEvidence.superseded_at.is_(None),
                        )
                        .first()
                    ):
                        r.verification_source = "csv_import"
                        r.last_verified_at = None
                        stats["labeled_import"] += 1
                sync_application_status(r, today=today)

            if (r.link_status or "") == "broken" or not r.deadline_precision:
                queue.append(
                    {
                        "id": r.id,
                        "title": r.title,
                        "provider": r.provider,
                        "link_status": r.link_status,
                        "deadline_precision": r.deadline_precision,
                    }
                )

        if apply:
            db.commit()
        else:
            db.rollback()

        out_path = Path("verification/reports/automated_validation_queue.json")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(queue, indent=2), encoding="utf-8")
        stats["queue_path"] = str(out_path)
        stats["queue_size"] = len(queue)
        return stats
    finally:
        db.close()


def datetime_now():
    from datetime import datetime, timezone

    return datetime.now(timezone.utc)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    print(json.dumps(run(apply=args.apply), indent=2))


if __name__ == "__main__":
    main()
