"""
Top 25 scholarships × 10 canonical personas — provider acceptance matrix.

Usage:
  python -m app.scripts.provider_acceptance_matrix
  python -m app.scripts.provider_acceptance_matrix --write
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.db import SessionLocal
from app import models
from app.serialization.scholarship import scholarship_to_catalog_dict
from app.matching.scholarship_enrichment import attach_scholarship_join_fields
from app.matching.eligibility_result import evaluate_eligibility, QualificationStatus

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "verification" / "reports" / "provider_acceptance"

TOP25_IDS = [
    73, 66, 76, 10, 130, 84, 81, 65, 16, 14, 72, 117, 61, 54, 3, 66, 73, 10, 76, 130, 84, 81, 65, 16, 14,
]
TOP25_IDS = list(dict.fromkeys(TOP25_IDS))[:25]

PERSONAS: list[dict] = [
    {
        "id": "grade12_compeng_ph",
        "label": "Grade 12 CompEng PH-only",
        "profile": {
            "education_level": "Grade 12",
            "enrollment_status": "incoming_freshman",
            "prior_tertiary_units": 0,
            "gwa_normalized": 93,
            "region": "Metro Manila",
            "field_of_study_broad": "Engineering",
            "preferred_courses": ["BS Computer Engineering"],
            "study_destination_preference": "PHILIPPINES_ONLY",
            "citizenship": "Filipino",
            "age": 18,
        },
    },
    {
        "id": "incoming_stem_ncr",
        "label": "Incoming STEM NCR",
        "profile": {
            "education_level": "College",
            "enrollment_status": "incoming_freshman",
            "prior_tertiary_units": 0,
            "gwa_normalized": 92,
            "region": "Metro Manila",
            "field_of_study_broad": "STEM",
            "study_destination_preference": "PHILIPPINES_ONLY",
        },
    },
    {
        "id": "gsis_dependent",
        "label": "GSIS dependent",
        "profile": {
            "education_level": "College",
            "enrollment_status": "incoming_freshman",
            "gwa_normalized": 88,
            "region": "Metro Manila",
            "is_gsis_dependent": True,
            "study_destination_preference": "PHILIPPINES_ONLY",
        },
    },
    {
        "id": "frontliner_dependent",
        "label": "Medical frontliner dependent",
        "profile": {
            "education_level": "Grade 12",
            "enrollment_status": "incoming_freshman",
            "gwa_normalized": 90,
            "region": "Metro Manila",
            "is_medical_frontliner_dependent": True,
            "study_destination_preference": "PHILIPPINES_ONLY",
        },
    },
    {
        "id": "abroad_only",
        "label": "Abroad-only preference",
        "profile": {
            "education_level": "College",
            "enrollment_status": "incoming_freshman",
            "gwa_normalized": 95,
            "region": "Metro Manila",
            "field_of_study_broad": "Engineering",
            "study_destination_preference": "ABROAD_ONLY",
        },
    },
    {
        "id": "both_destinations",
        "label": "PH + abroad preference",
        "profile": {
            "education_level": "College",
            "enrollment_status": "incoming_freshman",
            "gwa_normalized": 94,
            "region": "Metro Manila",
            "study_destination_preference": "BOTH",
        },
    },
    {
        "id": "education_major",
        "label": "Education major intent",
        "profile": {
            "education_level": "Grade 12",
            "enrollment_status": "incoming_freshman",
            "gwa_normalized": 91,
            "region": "Metro Manila",
            "field_of_study_broad": "Education",
            "preferred_courses": ["Bachelor of Elementary Education"],
            "study_destination_preference": "PHILIPPINES_ONLY",
        },
    },
    {
        "id": "enrolled_with_units",
        "label": "Enrolled with prior units",
        "profile": {
            "education_level": "College",
            "enrollment_status": "enrolled",
            "prior_tertiary_units": 24,
            "gwa_normalized": 90,
            "region": "Metro Manila",
            "study_destination_preference": "PHILIPPINES_ONLY",
        },
    },
    {
        "id": "4ps_ncfrs",
        "label": "4Ps + NCFRS",
        "profile": {
            "education_level": "College",
            "gwa_normalized": 85,
            "region": "Metro Manila",
            "is_4ps_listahanan": True,
            "affiliation_codes": ["ncfrs"],
            "study_destination_preference": "PHILIPPINES_ONLY",
        },
    },
    {
        "id": "minimal_profile",
        "label": "Minimal profile",
        "profile": {
            "education_level": "College",
            "region": "Metro Manila",
            "study_destination_preference": "PHILIPPINES_ONLY",
        },
    },
]


def _status_symbol(status: QualificationStatus) -> str:
    if status == QualificationStatus.QUALIFIED:
        return "Q"
    if status == QualificationStatus.PROVISIONALLY_QUALIFIED:
        return "P"
    if status == QualificationStatus.ALMOST_QUALIFIED:
        return "A"
    return "X"


def build_matrix(*, write: bool = False) -> dict:
    db = SessionLocal()
    rows: list[dict] = []
    try:
        for sid in TOP25_IDS:
            row = db.query(models.Scholarship).filter(models.Scholarship.id == sid).first()
            if not row:
                continue
            sch = attach_scholarship_join_fields(db, scholarship_to_catalog_dict(row))
            cells: dict[str, str] = {}
            for persona in PERSONAS:
                result = evaluate_eligibility(persona["profile"], sch)
                cells[persona["id"]] = _status_symbol(result.status)
            rows.append(
                {
                    "scholarship_id": sid,
                    "title": row.title,
                    "provider": row.provider,
                    "cells": cells,
                }
            )
    finally:
        db.close()

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "legend": {"Q": "qualified", "P": "provisionally_qualified", "A": "almost_qualified", "X": "not_eligible"},
        "personas": [{"id": p["id"], "label": p["label"]} for p in PERSONAS],
        "rows": rows,
    }

    if write:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        (OUT_DIR / "matrix.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
        lines = [
            "# Provider acceptance matrix (Top 25 × 10 personas)",
            "",
            f"Generated: {payload['generated_at']}",
            "",
            "Legend: Q=qualified, P=provisional, A=almost, X=not eligible",
            "",
        ]
        header = "| Scholarship | " + " | ".join(p["id"] for p in PERSONAS) + " |"
        sep = "|---|" + "|".join(["---"] * len(PERSONAS)) + "|"
        lines.extend([header, sep])
        for row in rows:
            title = (row["title"] or "")[:40].replace("|", "/")
            cells = " | ".join(row["cells"].get(p["id"], "-") for p in PERSONAS)
            lines.append(f"| {row['scholarship_id']} {title} | {cells} |")
        (OUT_DIR / "matrix.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate provider acceptance matrix")
    parser.add_argument("--write", action="store_true", help="Write matrix.json and matrix.md")
    args = parser.parse_args()
    payload = build_matrix(write=args.write)
    print(json.dumps({"rows": len(payload["rows"]), "personas": len(payload["personas"])}, indent=2))


if __name__ == "__main__":
    main()
