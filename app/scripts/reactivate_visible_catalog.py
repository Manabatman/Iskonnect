"""Re-activate rows wrongly hidden by needs_review editorial_state mapping."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app import models
from app.db import SessionLocal
from app.utils.application_status import sync_application_status
from app.utils.editorial_state import sync_legacy_fields_from_editorial


def run(*, apply: bool = False) -> int:
    db = SessionLocal()
    fixed = 0
    try:
        rows = (
            db.query(models.Scholarship)
            .filter(
                models.Scholarship.is_active == False,  # noqa: E712
                models.Scholarship.editorial_state == "needs_review",
            )
            .all()
        )
        for r in rows:
            status = (r.application_status or "").strip().lower()
            if status in ("permanently_discontinued",):
                continue
            r.is_active = True
            sync_legacy_fields_from_editorial(r)
            sync_application_status(r)
            fixed += 1
        archived_wrong = (
            db.query(models.Scholarship)
            .filter(
                models.Scholarship.is_active == False,  # noqa: E712
                models.Scholarship.editorial_state != "archived",
                models.Scholarship.application_status != "permanently_discontinued",
            )
            .all()
        )
        for r in archived_wrong:
            if r in rows:
                continue
            status = (r.application_status or "").strip().lower()
            if status in ("permanently_discontinued", "archived") and r.editorial_state == "archived":
                continue
            r.is_active = True
            sync_legacy_fields_from_editorial(r)
            sync_application_status(r)
            fixed += 1
        if apply:
            db.commit()
        else:
            db.rollback()
        return fixed
    finally:
        db.close()


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    n = run(apply=args.apply)
    print({"reactivated": n, "dry_run": not args.apply})
