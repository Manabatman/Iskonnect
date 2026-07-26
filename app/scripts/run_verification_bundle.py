"""
Automated link-audit pass for pending verification bundles.

Generates the five-file deliverable scaffold under verification/reports/{bundle_id}/:
  - human_report.md (automated link audit summary)
  - field_changes.csv (link_status confirm/update rows)
  - new_scholarships.json, schema_candidates.json, important_notes.json (templates)

Full field verification still requires a ChatGPT session with the bundle prompt.
This script unblocks link_status corrections and documents bundle progress.

Usage:
  python -m app.scripts.run_verification_bundle --bundle tesda
  python -m app.scripts.run_verification_bundle --all-pending
  python -m app.scripts.run_verification_bundle --all-pending --apply-links
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
import time
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlalchemy.orm import Session

from app import models
from app.db import SessionLocal
from app.jobs.link_checker import _head_status
from app.scripts.apply_field_changes import apply_field_changes

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]
EXPORT_DIR = ROOT / "verification" / "export" / "bundles"
REPORTS_DIR = ROOT / "verification" / "reports"
MASTER_INDEX = ROOT / "verification" / "export" / "master_index.json"
COMPLETE_BUNDLES = frozenset({"ched_unifast", "dost"})
FIELD_COLUMNS = (
    "id,field,iskconnect_value,official_value,action,change_reason,closure_type,"
    "confidence,source_url,evidence_snippet,official_last_updated,announcement_date,verified_at"
).split(",")


def _load_pending_bundle_ids() -> list[str]:
    data = json.loads(MASTER_INDEX.read_text(encoding="utf-8"))
    return [bid for bid in data.get("bundles", {}) if bid not in COMPLETE_BUNDLES]


def _bundle_scholarship_ids(bundle_id: str) -> list[int]:
    path = EXPORT_DIR / f"{bundle_id}.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    ids: list[int] = []
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            sid = (row.get("id") or "").strip()
            if sid.isdigit():
                ids.append(int(sid))
    return ids


def _audit_bundle(db: Session, bundle_id: str) -> tuple[list[dict[str, str]], dict]:
    today = date.today().isoformat()
    ids = _bundle_scholarship_ids(bundle_id)
    rows: list[dict[str, str]] = []
    stats = {"checked": 0, "ok": 0, "broken": 0, "unchanged": 0, "updates": 0}

    scholarships = (
        db.query(models.Scholarship).filter(models.Scholarship.id.in_(ids)).order_by(models.Scholarship.id).all()
        if ids
        else []
    )
    by_id = {s.id: s for s in scholarships}

    for sid in ids:
        sch = by_id.get(sid)
        if not sch:
            logger.warning("bundle=%s missing scholarship id=%s", bundle_id, sid)
            continue
        url = (sch.link or "").strip()
        if not url.startswith(("http://", "https://")):
            continue
        time.sleep(1.0)
        ok, tag = _head_status(url)
        stats["checked"] += 1
        new_status = "ok" if ok else "broken"
        current = (sch.link_status or "").strip().lower()
        if new_status == "ok":
            stats["ok"] += 1
        else:
            stats["broken"] += 1

        action = "confirm_unchanged" if current == new_status else "update"
        if action == "confirm_unchanged":
            stats["unchanged"] += 1
        else:
            stats["updates"] += 1

        rows.append(
            {
                "id": str(sid),
                "field": "link_status",
                "iskconnect_value": sch.link_status or "",
                "official_value": new_status,
                "action": action,
                "change_reason": "automated_head_check" if action == "update" else "",
                "closure_type": "",
                "confidence": "partially_verified",
                "source_url": url,
                "evidence_snippet": f"HEAD check {'passed' if ok else f'failed ({tag})'} on {today}",
                "official_last_updated": "",
                "announcement_date": "",
                "verified_at": today,
            }
        )

    return rows, stats


def _write_bundle_reports(bundle_id: str, field_rows: list[dict[str, str]], stats: dict) -> Path:
    out_dir = REPORTS_DIR / bundle_id
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = out_dir / "field_changes.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_COLUMNS)
        writer.writeheader()
        writer.writerows(field_rows)

    report_path = out_dir / "human_report.md"
    report_path.write_text(
        "\n".join(
            [
                f"# {bundle_id} — automated link audit",
                "",
                f"**Generated:** {date.today().isoformat()}",
                "",
                "This bundle received an automated HTTP HEAD link audit only.",
                "Full provider verification (eligibility, dates, benefits) still requires",
                f"a ChatGPT session with `verification/prompts/{bundle_id}_prompt.md`.",
                "",
                "## Link audit summary",
                "",
                f"- Scholarships checked: {stats.get('checked', 0)}",
                f"- Links OK: {stats.get('ok', 0)}",
                f"- Links broken: {stats.get('broken', 0)}",
                f"- link_status updates proposed: {stats.get('updates', 0)}",
                "",
                "## Next steps",
                "",
                "1. Run the bundle ChatGPT prompt for full field verification.",
                "2. Merge human field_changes.csv with this automated file if needed.",
                "3. Apply: `python -m app.scripts.apply_field_changes --csv "
                f"verification/reports/{bundle_id}/field_changes.csv --apply`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    for name, template in (
        ("new_scholarships.json", ROOT / "verification" / "templates" / "new_scholarships.template.json"),
        ("schema_candidates.json", ROOT / "verification" / "templates" / "schema_candidates.template.json"),
        ("important_notes.json", ROOT / "verification" / "templates" / "important_notes.template.json"),
    ):
        dest = out_dir / name
        if not dest.exists():
            dest.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")

    return out_dir


def process_bundle(bundle_id: str, *, apply_links: bool = False) -> dict:
    db = SessionLocal()
    try:
        field_rows, stats = _audit_bundle(db, bundle_id)
        out_dir = _write_bundle_reports(bundle_id, field_rows, stats)
        apply_summary = None
        if apply_links and field_rows:
            apply_summary = apply_field_changes(db, field_rows, dry_run=False)
            db.commit()
            apply_summary = {
                "applied": apply_summary.applied,
                "skipped_drift": apply_summary.skipped_drift,
                "skipped_confirm_unchanged": apply_summary.skipped_confirm_unchanged,
            }
        return {"bundle_id": bundle_id, "stats": stats, "report_dir": str(out_dir), "apply": apply_summary}
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run automated link audit for verification bundles")
    parser.add_argument("--bundle", action="append", default=[], help="Bundle id (repeatable)")
    parser.add_argument("--all-pending", action="store_true", help="Process all bundles except ched_unifast and dost")
    parser.add_argument("--apply-links", action="store_true", help="Apply link_status updates via apply_field_changes")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    bundles = list(args.bundle)
    if args.all_pending:
        bundles = _load_pending_bundle_ids()
    if not bundles:
        parser.error("Specify --bundle ID or --all-pending")

    results = []
    for bundle_id in bundles:
        logger.info("Processing bundle %s", bundle_id)
        results.append(process_bundle(bundle_id, apply_links=args.apply_links))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
