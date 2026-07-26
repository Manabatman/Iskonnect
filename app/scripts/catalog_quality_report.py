"""
Emit catalog quality metrics and provider coverage report.

Usage:
  python -m app.scripts.catalog_quality_report
  python -m app.scripts.catalog_quality_report --output data/catalog_quality_report.md
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import func

from app import models
from app.db import SessionLocal
from app.utils.verification_display import verification_badge_for_row

ROOT = Path(__file__).resolve().parents[2]


def _pct(num: int, denom: int) -> str:
    if denom == 0:
        return "0%"
    return f"{100.0 * num / denom:.1f}%"


def build_report() -> str:
    db = SessionLocal()
    try:
        rows = db.query(models.Scholarship).all()
        active = [r for r in rows if r.is_active is not False]
        archived = [r for r in rows if r.is_active is False]

        badge_counts: dict[str, int] = {}
        broken = 0
        no_precision = 0
        unsupported_deadline = 0
        with_evidence = 0

        for r in active:
            badge = verification_badge_for_row(r, db)
            badge_counts[badge] = badge_counts.get(badge, 0) + 1
            if (r.link_status or "").lower() == "broken":
                broken += 1
            if not r.deadline_precision:
                no_precision += 1
            if r.application_deadline and not r.deadline_precision:
                unsupported_deadline += 1
            if (
                db.query(models.FieldEvidence)
                .filter(
                    models.FieldEvidence.scholarship_id == r.id,
                    models.FieldEvidence.superseded_at.is_(None),
                )
                .first()
            ):
                with_evidence += 1

        provider_rows = (
            db.query(models.Scholarship.provider_type, func.count(models.Scholarship.id))
            .filter(models.Scholarship.is_active != False)  # noqa: E712
            .group_by(models.Scholarship.provider_type)
            .all()
        )

        lines = [
            "# ISKONNECT Catalog Quality Report",
            "",
            f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
            "",
            "## Summary",
            "",
            f"| Metric | Value |",
            f"|--------|------:|",
            f"| Total scholarships | {len(rows)} |",
            f"| Active | {len(active)} |",
            f"| Archived / inactive | {len(archived)} |",
            f"| With field evidence | {with_evidence} ({_pct(with_evidence, len(active))} of active) |",
            f"| Broken links (active) | {broken} ({_pct(broken, len(active))}) |",
            f"| Missing deadline precision | {no_precision} |",
            f"| Exact deadline without precision | {unsupported_deadline} |",
            "",
            "## Verification badges (active)",
            "",
            "| Badge | Count |",
            "|-------|------:|",
        ]
        for badge, count in sorted(badge_counts.items(), key=lambda x: -x[1]):
            lines.append(f"| {badge} | {count} |")

        lines.extend(
            [
                "",
                "## Coverage by provider type (active)",
                "",
                "| Provider type | Count |",
                "|---------------|------:|",
            ]
        )
        for ptype, count in provider_rows:
            lines.append(f"| {ptype or 'unknown'} | {count} |")

        lines.extend(
            [
                "",
                "## Quality targets (public beta)",
                "",
                "| Metric | Target | Current |",
                "|--------|--------|---------|",
                f"| Verified active scholarships | 100% | {_pct(badge_counts.get('verified', 0), len(active))} |",
                f"| Broken links | <1% | {_pct(broken, len(active))} |",
                f"| Scholarships with official sources (field evidence) | 100% | {_pct(with_evidence, len(active))} |",
                f"| Unsupported deadlines | 0 | {unsupported_deadline} |",
                "",
                "## Recommended next research",
                "",
                "1. Complete full ChatGPT verification for LGU NCR bundle",
                "2. Web-verify remaining university rows (Ateneo, DLSU, UST tracks)",
                "3. Resolve broken_link rows flagged by link checker",
                "4. Continue tier-1 government provider reverification every 90 days",
                "",
            ]
        )
        return "\n".join(lines)
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(ROOT / "data" / "catalog_quality_report.md"))
    args = parser.parse_args()
    report = build_report()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(report)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
