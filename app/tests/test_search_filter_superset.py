"""Search filter superset and timing regression tests."""

from __future__ import annotations

import json
from datetime import date, timedelta

from app import models
from app.api.v1.scholarship_search import (
    _base_search_query,
    apply_education_level_browse_filter,
    apply_field_browse_filter,
    apply_life_stage_filter,
    apply_region_browse_filter,
    apply_timing_filter,
)


def _add(db, **kwargs):
    row = models.Scholarship(provider="Test", is_active=True, **kwargs)
    db.add(row)
    db.commit()
    return row


def test_timing_any_is_superset_of_archived(db_session):
    db_session.add_all(
        [
            models.Scholarship(title="Active Open", provider="T", is_active=True, application_status="open"),
            models.Scholarship(title="Archived Row", provider="T", is_active=False, application_status="archived"),
        ]
    )
    db_session.commit()

    base = _base_search_query(db_session)
    any_count = base.count()
    archived_count = apply_timing_filter(base, "archived").count()
    assert any_count >= archived_count


def test_open_now_excludes_future_open_date(db_session):
    today = date.today()
    future = today + timedelta(days=14)
    db_session.add_all(
        [
            models.Scholarship(
                title="Open today",
                provider="T",
                is_active=True,
                application_status="open",
                application_open_date=today - timedelta(days=1),
            ),
            models.Scholarship(
                title="Opening soon",
                provider="T",
                is_active=True,
                application_status="open",
                application_open_date=future,
            ),
        ]
    )
    db_session.commit()
    q = apply_timing_filter(_base_search_query(db_session), "open_now", today=today)
    titles = {r.title for r in q.all()}
    assert "Open today" in titles
    assert "Opening soon" not in titles


def test_life_stage_includes_empty_levels(db_session):
    db_session.add_all(
        [
            models.Scholarship(title="Any level", provider="T", is_active=True, eligible_levels=None),
            models.Scholarship(
                title="College only",
                provider="T",
                is_active=True,
                eligible_levels=json.dumps(["Graduate"]),
            ),
        ]
    )
    db_session.commit()
    q = apply_life_stage_filter(_base_search_query(db_session), "college")
    titles = {r.title for r in q.all()}
    assert "Any level" in titles
    assert "College only" not in titles


def test_field_filter_includes_empty_courses(db_session):
    db_session.add_all(
        [
            models.Scholarship(title="All courses", provider="T", is_active=True, eligible_courses_psced=None),
            models.Scholarship(
                title="STEM only",
                provider="T",
                is_active=True,
                eligible_courses_psced=json.dumps(["Engineering"]),
            ),
        ]
    )
    db_session.commit()
    q = apply_field_browse_filter(_base_search_query(db_session), "Engineering")
    titles = {r.title for r in q.all()}
    assert "All courses" in titles
    assert "STEM only" in titles
