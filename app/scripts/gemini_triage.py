"""
Triage Gemini scholarship CSV rows against the live catalog.

Usage:
  python -m app.scripts.gemini_triage
  python -m app.scripts.gemini_triage --corrected data/scholarships_gemini_corrected.csv --batch2 data/scholarships_gemini_batch2.csv
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlalchemy.orm import Session

from app import models
from app.db import SessionLocal
from app.utils.dedupe import scholarship_dedupe_key
from app.utils.import_contract import CANONICAL_IMPORT_COLUMNS

DEFAULT_CORRECTED = Path("data/scholarships_gemini_corrected.csv")
DEFAULT_BATCH2 = Path("data/scholarships_gemini_batch2.csv")
DEFAULT_TRIAGE = Path("data/gemini_triage.csv")
DEFAULT_STAGING = Path("data/gemini_staging_ready.csv")

TRIAGE_COLUMNS = (
    "source_file",
    "row_index",
    "title",
    "provider",
    "action",
    "matched_id",
    "notes",
)

DATE_COLUMNS = (
    "application_open_date",
    "application_deadline",
    "last_open_date",
    "last_close_date",
)


@dataclass
class CatalogIndex:
    by_dedupe: dict[str, models.Scholarship]
    by_title_provider: dict[tuple[str, str], models.Scholarship]
    scholarships: list[models.Scholarship]


def normalize_text(value: str | None) -> str:
    text = (value or "").strip().lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        raw_header = [h.strip() for h in (reader.fieldnames or [])]
        missing = [c for c in CANONICAL_IMPORT_COLUMNS if c not in raw_header]
        if missing:
            logger_note = f"{path.name}: padding missing columns {missing}"
        else:
            logger_note = ""
        rows: list[dict[str, str]] = []
        for row in reader:
            normalized = {k.strip(): (v or "") for k, v in row.items()}
            for col in CANONICAL_IMPORT_COLUMNS:
                normalized.setdefault(col, "")
            rows.append({col: normalized.get(col, "") for col in CANONICAL_IMPORT_COLUMNS})
        if logger_note:
            print(logger_note)
        return rows


def build_catalog_index(db: Session) -> CatalogIndex:
    scholarships = db.query(models.Scholarship).all()
    by_dedupe: dict[str, models.Scholarship] = {}
    by_title_provider: dict[tuple[str, str], models.Scholarship] = {}
    for sch in scholarships:
        key = scholarship_dedupe_key(sch.title or "", sch.provider, sch.link)
        if key:
            by_dedupe[key] = sch
        tp = (normalize_text(sch.title), normalize_text(sch.provider))
        if tp[0]:
            by_title_provider.setdefault(tp, sch)
    return CatalogIndex(by_dedupe=by_dedupe, by_title_provider=by_title_provider, scholarships=scholarships)


def _find_split_parent(title: str, provider: str, catalog: CatalogIndex) -> models.Scholarship | None:
    gem_title = normalize_text(title)
    gem_provider = normalize_text(provider)
    best: models.Scholarship | None = None
    best_len = 0
    for sch in catalog.scholarships:
        if normalize_text(sch.provider) != gem_provider:
            continue
        cat_title = normalize_text(sch.title)
        if not cat_title or cat_title == gem_title:
            continue
        if gem_title.startswith(cat_title) or cat_title in gem_title:
            if len(cat_title) > best_len and len(gem_title) - len(cat_title) >= 12:
                best = sch
                best_len = len(cat_title)
    return best


def triage_row(row: dict[str, str], catalog: CatalogIndex) -> tuple[str, str, str]:
    title = (row.get("title") or "").strip()
    provider = (row.get("provider") or "").strip()
    link = (row.get("link") or "").strip()
    dedupe = scholarship_dedupe_key(title, provider, link)

    if dedupe in catalog.by_dedupe:
        sch = catalog.by_dedupe[dedupe]
        if normalize_text(sch.title) == normalize_text(title):
            return "skip", str(sch.id), "exact dedupe_key match"
        return "update", str(sch.id), "dedupe_key match with title drift"

    tp = (normalize_text(title), normalize_text(provider))
    if tp[0] and tp in catalog.by_title_provider:
        sch = catalog.by_title_provider[tp]
        if (sch.link or "").strip().lower() == link.lower():
            return "skip", str(sch.id), "title+provider+link match"
        return "update", str(sch.id), "title+provider match; link differs"

    split_parent = _find_split_parent(title, provider, catalog)
    if split_parent is not None:
        return (
            "split",
            str(split_parent.id),
            f"variant of generic parent '{split_parent.title}'",
        )

    for sch in catalog.scholarships:
        if normalize_text(sch.title) == normalize_text(title):
            return "update", str(sch.id), "title match across providers"

    return "new", "", "no catalog match"


def _application_status_from_notes(notes: str) -> str:
    for part in (notes or "").split("|"):
        piece = part.strip()
        if piece.lower().startswith("application_status="):
            return piece.split("=", 1)[1].strip().lower()
    return ""


def strip_unsupported_2026_dates(row: dict[str, str]) -> dict[str, str]:
    """Clear speculative 2026 cycle dates unless research notes mark status=open."""
    if _application_status_from_notes(row.get("research_notes") or "") == "open":
        return row
    cleaned = dict(row)
    for col in DATE_COLUMNS:
        value = (cleaned.get(col) or "").strip()
        if value.startswith("2026-"):
            cleaned[col] = ""
    return cleaned


def triage_files(
    db: Session,
    sources: list[tuple[str, Path]],
) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, int]]:
    catalog = build_catalog_index(db)
    triage_rows: list[dict[str, str]] = []
    staging_rows: list[dict[str, str]] = []
    stats = {"new": 0, "update": 0, "split": 0, "skip": 0, "staging": 0}

    for source_file, path in sources:
        if not path.exists():
            raise FileNotFoundError(path)
        rows = load_csv_rows(path)
        for idx, row in enumerate(rows, start=2):
            action, matched_id, notes = triage_row(row, catalog)
            stats[action] = stats.get(action, 0) + 1
            triage_rows.append(
                {
                    "source_file": source_file,
                    "row_index": str(idx),
                    "title": row.get("title") or "",
                    "provider": row.get("provider") or "",
                    "action": action,
                    "matched_id": matched_id,
                    "notes": notes,
                }
            )
            if action in ("new", "update"):
                staging_rows.append(strip_unsupported_2026_dates(row))
                stats["staging"] += 1

    return triage_rows, staging_rows, stats


def write_csv(path: Path, fieldnames: tuple[str, ...] | list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(fieldnames))
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description="Triage Gemini CSV rows against live catalog")
    parser.add_argument("--corrected", type=Path, default=DEFAULT_CORRECTED)
    parser.add_argument("--batch2", type=Path, default=DEFAULT_BATCH2)
    parser.add_argument("--triage-out", type=Path, default=DEFAULT_TRIAGE)
    parser.add_argument("--staging-out", type=Path, default=DEFAULT_STAGING)
    args = parser.parse_args()

    sources = [
        (args.corrected.name, args.corrected),
        (args.batch2.name, args.batch2),
    ]

    db = SessionLocal()
    try:
        triage_rows, staging_rows, stats = triage_files(db, sources)
    finally:
        db.close()

    write_csv(args.triage_out, TRIAGE_COLUMNS, triage_rows)
    write_csv(args.staging_out, CANONICAL_IMPORT_COLUMNS, staging_rows)

    print(f"gemini_triage -> {args.triage_out} ({len(triage_rows)} rows)")
    print(f"gemini_staging_ready -> {args.staging_out} ({len(staging_rows)} rows)")
    print(f"  new: {stats['new']}")
    print(f"  update: {stats['update']}")
    print(f"  split: {stats['split']}")
    print(f"  skip: {stats['skip']}")
    print(f"  staging: {stats['staging']}")


if __name__ == "__main__":
    main()
