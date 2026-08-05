"""MATCH-08: SQL prefilter must return identical ordered match results (prefilter on vs off)."""

from __future__ import annotations

import json

import pytest
from sqlalchemy.dialects import postgresql

from app.api.v1.matches import _prefilter_scholarships_query
from eval.generate_data import generate_profiles, generate_scholarships

from .prefilter_parity_util import (
    PERSONA_FIXTURE_PATH,
    assert_prefilter_parity,
    build_postgres_parity_db,
    build_sqlite_parity_db,
    postgres_parity_database_url,
)


def test_prefilter_query_compiles_with_postgres_jsonb_cast():
    """Postgres must cast jsonb eligible_levels before ILIKE (migration 029)."""
    db = build_sqlite_parity_db([])
    try:
        q = _prefilter_scholarships_query(db, {"education_level": "College"})
        sql = str(q.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
    finally:
        db.close()
    upper = sql.upper()
    assert "CAST" in upper
    assert "AS TEXT" in upper
    assert "ILIKE" in upper


@pytest.fixture(scope="module")
def eval_db():
    scholarships = generate_scholarships()
    db = build_sqlite_parity_db(scholarships)
    try:
        yield db, scholarships
    finally:
        db.close()


@pytest.fixture(scope="module")
def persona_db():
    with PERSONA_FIXTURE_PATH.open(encoding="utf-8") as f:
        catalog = json.load(f)
    scholarships = catalog["scholarships"]
    db = build_sqlite_parity_db(scholarships)
    try:
        yield db, scholarships, catalog["personas"]
    finally:
        db.close()


@pytest.fixture(scope="module")
def eval_db_postgres():
    url = postgres_parity_database_url()
    if not url:
        pytest.skip("Postgres DATABASE_URL required for MATCH-08 Postgres parity")
    scholarships = generate_scholarships()
    db = build_postgres_parity_db(scholarships, url)
    try:
        yield db, scholarships
    finally:
        db.close()


@pytest.fixture(scope="module")
def persona_db_postgres():
    url = postgres_parity_database_url()
    if not url:
        pytest.skip("Postgres DATABASE_URL required for MATCH-08 Postgres parity")
    with PERSONA_FIXTURE_PATH.open(encoding="utf-8") as f:
        catalog = json.load(f)
    scholarships = catalog["scholarships"]
    db = build_postgres_parity_db(scholarships, url)
    try:
        yield db, scholarships, catalog["personas"]
    finally:
        db.close()


def test_prefilter_parity_eval_profiles(eval_db):
    db, scholarships = eval_db
    for profile in generate_profiles():
        assert_prefilter_parity(profile, scholarships, db)


def test_prefilter_parity_personas(persona_db):
    db, scholarships, personas = persona_db
    for persona in personas:
        assert_prefilter_parity(persona["profile"], scholarships, db)


def test_prefilter_parity_eval_profiles_postgres(eval_db_postgres):
    db, scholarships = eval_db_postgres
    for profile in generate_profiles():
        assert_prefilter_parity(profile, scholarships, db)


def test_prefilter_parity_personas_postgres(persona_db_postgres):
    db, scholarships, personas = persona_db_postgres
    for persona in personas:
        assert_prefilter_parity(persona["profile"], scholarships, db)
