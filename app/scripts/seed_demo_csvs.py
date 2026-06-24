"""
Import scraped scholarship CSVs for local demo (merges with existing seed data).

Usage:
    python -m app.scripts.seed_demo_csvs
    python -m app.scripts.seed_demo_csvs --csv path/to/custom.csv
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.db import SessionLocal
from app import models
from app.scholarship_cache import invalidate_scholarship_cache
from app.scripts.import_scholarships import run_import


def _default_csv_paths() -> list[Path]:
    """Default CSV locations: .cursor/plans/data/, legacy .cursor/plans/, then data/raw/."""
    project_root = Path(__file__).resolve().parents[2]
    workspace_plans = project_root.parent / ".cursor" / "plans"
    names = ["philscholar.csv", "sikap.csv", "scholarships.csv"]
    for subdir in ("data", ""):
        search_dir = workspace_plans / subdir if subdir else workspace_plans
        paths = [search_dir / name for name in names if (search_dir / name).exists()]
        if paths:
            return paths
    raw_dir = project_root / "data" / "raw"
    return [raw_dir / name for name in names if (raw_dir / name).exists()]


def _print_db_summary() -> None:
    db = SessionLocal()
    try:
        total = db.query(models.Scholarship).count()
        print(f"\nScholarships in DB: {total}")
        rows = (
            db.query(models.Scholarship.source, models.Scholarship.id)
            .all()
        )
        by_source: dict[str, int] = {}
        for source, _ in rows:
            key = source or "(seed)"
            by_source[key] = by_source.get(key, 0) + 1
        for src, count in sorted(by_source.items(), key=lambda x: (-x[1], x[0])):
            print(f"  {src}: {count}")
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed demo scholarships from scraped CSVs")
    parser.add_argument(
        "--csv",
        action="append",
        dest="csv_paths",
        help="Path to a CSV file (repeat for multiple). Defaults to .cursor/plans/*.csv",
    )
    parser.add_argument("--batch-size", type=int, default=50)
    args = parser.parse_args()

    paths = [Path(p) for p in args.csv_paths] if args.csv_paths else _default_csv_paths()
    if not paths:
        plans_dir = Path(__file__).resolve().parents[2].parent / ".cursor" / "plans" / "data"
        print(
            "No CSV files found. Place philscholar.csv, sikap.csv, and scholarships.csv in "
            f"{plans_dir} or pass --csv paths explicitly.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    grand_inserted = 0
    for path in paths:
        if not path.exists():
            print(f"Skipping missing file: {path}", file=sys.stderr)
            continue
        print(f"\n=== Importing {path.name} ===")
        summary = run_import(str(path), batch_size=args.batch_size)
        print(f"  Rows in file:  {summary['total']}")
        print(f"  Inserted:      {summary['inserted']}")
        print(f"  Skipped:       {summary['skipped']}")
        print(f"  Errors:        {summary['errors']}")
        grand_inserted += summary["inserted"]

    invalidate_scholarship_cache()
    print(f"\nCache invalidated. Total new rows inserted: {grand_inserted}")
    _print_db_summary()


if __name__ == "__main__":
    main()
