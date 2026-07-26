"""Regression: deadline expiry must not deactivate scholarships."""

from __future__ import annotations

from datetime import date, timedelta

from app import models
from app.jobs.catalog_maintenance import run_catalog_maintenance
from app.utils.lifecycle_repair import sync_past_deadline_cycle


def test_sync_past_deadline_keeps_active_and_rolls_dates(db_session):
    today = date.today()
    past = today - timedelta(days=30)
    s = models.Scholarship(
        title="Annual Grant",
        provider="Test Agency",
        is_active=True,
        editorial_state="published",
        data_status="active",
        application_status="open",
        application_deadline=past,
        application_open_date=past - timedelta(days=60),
        cycle_type="annual",
    )
    db_session.add(s)
    db_session.commit()

    assert sync_past_deadline_cycle(s, today=today) is True
    assert s.is_active is True
    assert s.application_deadline is None
    assert s.last_close_date == past
    assert s.application_status in ("expected_reopen", "previous_cycle", "closed")


def test_catalog_maintenance_does_not_deactivate_on_deadline(db_session):
    today = date.today()
    past = today - timedelta(days=10)
    s = models.Scholarship(
        title="Cycle Closed Program",
        provider="Test",
        is_active=True,
        editorial_state="published",
        data_status="active",
        application_deadline=past,
        cycle_type="annual",
    )
    db_session.add(s)
    db_session.commit()
    sid = s.id

    run_catalog_maintenance()

    row = db_session.query(models.Scholarship).filter(models.Scholarship.id == sid).one()
    assert row.is_active is True
    assert row.application_status != "archived"


def test_permanently_discontinued_not_repaired(db_session):
    today = date.today()
    past = today - timedelta(days=5)
    s = models.Scholarship(
        title="Dead Program",
        provider="Test",
        is_active=False,
        editorial_state="archived",
        data_status="expired",
        application_status="permanently_discontinued",
        application_deadline=past,
    )
    db_session.add(s)
    db_session.commit()

    assert sync_past_deadline_cycle(s, today=today) is False
    assert s.is_active is False
