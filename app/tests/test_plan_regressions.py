"""Regression tests aligned with audit plan (ingest, deadlines, dedupe)."""

import sys
from datetime import date, timedelta

import pytest
from sqlalchemy import and_

from app import models
from app.scripts import ingest_scraped as ingest_mod


def test_dedupe_key_stable():
    link = "https://example.com/same-program"
    a = ingest_mod._dedupe_key("  ABC Scholarship ", "DOST ", link)
    b = ingest_mod._dedupe_key("abc scholarship", "dost", link)
    assert a == b
    # Same title/provider but different URL → different key
    c = ingest_mod._dedupe_key("abc scholarship", "dost", "https://example.com/other")
    assert c != a


def test_expire_deadline_deactivates_scholarship(db_session):
    past = date.today() - timedelta(days=10)
    s = models.Scholarship(
        title="Expired Test",
        provider="Test",
        link="https://example.com/expired-test",
        source="test",
        is_active=True,
        application_deadline=past,
    )
    db_session.add(s)
    db_session.commit()

    q = db_session.query(models.Scholarship).filter(
        and_(
            models.Scholarship.is_active.is_(True),
            models.Scholarship.application_deadline.isnot(None),
            models.Scholarship.application_deadline < date.today(),
        )
    )
    n = q.update({models.Scholarship.is_active: False}, synchronize_session=False)
    db_session.commit()
    assert n == 1
    db_session.refresh(s)
    assert s.is_active is False


def test_future_deadline_not_matched_by_expiry_query(db_session):
    fut = date.today() + timedelta(days=30)
    s = models.Scholarship(
        title="Future Test",
        provider="Test",
        link="https://example.com/future-test",
        source="test",
        is_active=True,
        application_deadline=fut,
    )
    db_session.add(s)
    db_session.commit()
    q = db_session.query(models.Scholarship).filter(
        and_(
            models.Scholarship.is_active.is_(True),
            models.Scholarship.application_deadline.isnot(None),
            models.Scholarship.application_deadline < date.today(),
        )
    )
    assert q.count() == 0


def test_ingest_requires_non_empty_database_url(monkeypatch):
    import app.config as cfg

    monkeypatch.setattr(cfg.settings, "database_url", "")
    monkeypatch.setattr(sys, "argv", ["ingest_scraped", "--source", "data/raw/x.json"])
    with pytest.raises(SystemExit, match="DATABASE_URL"):
        ingest_mod.main()


def test_ingest_rejects_non_postgres_on_github_actions(monkeypatch):
    import app.config as cfg

    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setattr(cfg.settings, "database_url", "sqlite:///./x.db")
    monkeypatch.setattr(sys, "argv", ["ingest_scraped", "--source", "data/raw/x.json"])
    with pytest.raises(SystemExit, match="postgresql"):
        ingest_mod.main()
