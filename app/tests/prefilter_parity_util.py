"""Shared helpers for MATCH-08 plan prefilter parity (SQLite + Postgres)."""

from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app import models
from app.api.v1.matches import _prefilter_scholarships_query
from app.api.v1.scholarships import _scholarship_to_response
from app.db import Base
from app.matching.match_service import MatchService

_JSON_LIST_FIELDS = frozenset(
    {
        "eligible_levels",
        "eligible_regions",
        "eligible_cities",
        "eligible_school_types",
        "eligible_schools",
        "eligible_school_systems",
        "eligible_school_categories",
        "eligible_year_levels",
        "eligible_enrollment_status",
        "eligible_courses_psced",
        "eligible_courses_specific",
        "priority_groups",
        "needs_tags",
        "required_documents",
        "preferred_extracurriculars",
        "preferred_awards",
    }
)

_DATE_FIELDS = frozenset(
    {
        "application_deadline",
        "application_open_date",
        "last_open_date",
        "last_close_date",
    }
)

PERSONA_FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "persona_catalog.json"


def postgres_parity_database_url() -> str | None:
    url = os.environ.get("DATABASE_URL", "").strip()
    return url if url.startswith("postgresql") else None


def _scholarship_row(s: dict) -> dict:
    row: dict = {}
    for k, v in s.items():
        if k.startswith("gt_") or k.startswith("_"):
            continue
        if k in _JSON_LIST_FIELDS:
            row[k] = json.dumps(v) if v is not None else "[]"
        elif k in _DATE_FIELDS:
            row[k] = date.fromisoformat(v) if isinstance(v, str) else v
        else:
            row[k] = v
    if row.get("is_active") is None:
        row["is_active"] = True
    return row


def build_sqlite_parity_db(scholarships: list[dict]) -> Session:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    for s in scholarships:
        db.add(models.Scholarship(**_scholarship_row(s)))
    db.commit()
    return db


def build_postgres_parity_db(scholarships: list[dict], database_url: str) -> Session:
    engine = create_engine(database_url)
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    db.query(models.Scholarship).delete()
    db.commit()
    for s in scholarships:
        row = _scholarship_row(s)
        cols = list(row.keys())
        placeholders = []
        params: dict = {}
        for col in cols:
            if col in _JSON_LIST_FIELDS:
                placeholders.append(f"CAST(:{col} AS jsonb)")
            else:
                placeholders.append(f":{col}")
            params[col] = row[col]
        sql = f"INSERT INTO scholarships ({', '.join(cols)}) VALUES ({', '.join(placeholders)})"
        db.execute(text(sql), params)
    db.commit()
    return db


def ordered_match_tuples(profile: dict, scholarships: list[dict], db: Session | None = None) -> list[tuple[int, float]]:
    svc = MatchService()
    if db is None:
        results, _ = svc.get_matches(profile, scholarships)
    else:
        rows = _prefilter_scholarships_query(db, profile).all()
        dicts = [_scholarship_to_response(r) for r in rows]
        results, _ = svc.get_matches(profile, dicts)
    return [
        (
            int(r["id"]),
            float(r.get("final_score") if r.get("final_score") is not None else r.get("score", 0)),
        )
        for r in results
    ]


def assert_prefilter_parity(profile: dict, scholarships: list[dict], db: Session) -> None:
    off = ordered_match_tuples(profile, scholarships)
    on = ordered_match_tuples(profile, scholarships, db)
    assert on == off, (
        f"Prefilter changed match order or scores.\n"
        f"  off (first 5): {off[:5]}\n"
        f"  on  (first 5): {on[:5]}"
    )
