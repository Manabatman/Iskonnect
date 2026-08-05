"""Regression tests for browse search filters (nationwide geo + combined filters)."""

import json
from datetime import date, timedelta

from app import models
from app.api.v1.scholarship_search import (
    _apply_search_ordering,
    apply_education_level_browse_filter,
    apply_region_browse_filter,
)


def _sch(
    title: str,
    *,
    eligible_regions=None,
    regions_legacy=None,
    eligible_cities=None,
    eligible_levels=None,
):
    return models.Scholarship(
        title=title,
        provider="Test",
        is_active=True,
        eligible_regions=json.dumps(eligible_regions) if eligible_regions is not None else None,
        regions=regions_legacy,
        eligible_cities=json.dumps(eligible_cities) if eligible_cities is not None else None,
        eligible_levels=json.dumps(eligible_levels) if eligible_levels is not None else None,
    )


def _base_query(db_session):
    return db_session.query(models.Scholarship).filter(models.Scholarship.is_active != False)  # noqa: E712


def test_region_filter_includes_nationwide_and_matching_rows(db_session):
    db_session.add_all(
        [
            _sch("Nationwide TVET", eligible_levels=["TVET"]),
            _sch("Region V College", eligible_regions=["Region V"], eligible_levels=["College"]),
            _sch("Region V TVET", eligible_regions=["Region V"], eligible_levels=["TVET"]),
            _sch("Nationwide College", eligible_levels=["College"]),
        ]
    )
    db_session.commit()

    q = apply_region_browse_filter(_base_query(db_session), "Region V")
    titles = {r.title for r in q.all()}
    assert titles == {
        "Nationwide TVET",
        "Nationwide College",
        "Region V College",
        "Region V TVET",
    }


def test_region_v_and_education_tvet_intersection(db_session):
    db_session.add_all(
        [
            _sch("Nationwide TVET", eligible_levels=["TVET"]),
            _sch("Nationwide College", eligible_levels=["College"]),
            _sch("Region V TVET", eligible_regions=["Region V"], eligible_levels=["TVET"]),
            _sch("Region V College", eligible_regions=["Region V"], eligible_levels=["College"]),
        ]
    )
    db_session.commit()

    q = _base_query(db_session)
    q = apply_region_browse_filter(q, "Region V")
    q = apply_education_level_browse_filter(q, "TVET")
    titles = {r.title for r in q.all()}
    assert titles == {"Nationwide TVET", "Region V TVET"}


def test_base_query_returns_active_rows(db_session):
    db_session.add(_sch("Open to all"))
    db_session.commit()
    assert _base_query(db_session).count() >= 1


def test_search_ordering_prioritizes_open_then_deadline_then_title(db_session):
    today = date.today()
    db_session.add_all(
        [
            models.Scholarship(
                title="Zeta Closed",
                provider="Test",
                is_active=True,
                application_status="closed",
            ),
            models.Scholarship(
                title="Alpha Open",
                provider="Test",
                is_active=True,
                application_status="open",
                application_deadline=today + timedelta(days=30),
            ),
            models.Scholarship(
                title="Beta Open",
                provider="Test",
                is_active=True,
                application_status="open",
                application_deadline=today + timedelta(days=5),
            ),
        ]
    )
    db_session.commit()

    rows = _apply_search_ordering(_base_query(db_session), today=today).all()
    titles = [r.title for r in rows]
    assert titles.index("Beta Open") < titles.index("Alpha Open")
    assert titles.index("Alpha Open") < titles.index("Zeta Closed")


def test_search_ordering_deadline_sort(db_session):
    today = date.today()
    db_session.add_all(
        [
            models.Scholarship(
                title="No deadline",
                provider="Test",
                is_active=True,
                application_status="open",
            ),
            models.Scholarship(
                title="Later",
                provider="Test",
                is_active=True,
                application_status="open",
                application_deadline=today + timedelta(days=30),
            ),
            models.Scholarship(
                title="Sooner",
                provider="Test",
                is_active=True,
                application_status="open",
                application_deadline=today + timedelta(days=3),
            ),
        ]
    )
    db_session.commit()

    rows = _apply_search_ordering(_base_query(db_session), sort="deadline", today=today).all()
    titles = [r.title for r in rows]
    assert titles.index("Sooner") < titles.index("Later")
    assert titles.index("Later") < titles.index("No deadline")


def test_search_ordering_title_sort(db_session):
    db_session.add_all(
        [
            _sch("Zebra Grant"),
            _sch("Alpha Grant"),
            _sch("Mango Grant"),
        ]
    )
    db_session.commit()

    rows = _apply_search_ordering(_base_query(db_session), sort="title").all()
    assert [r.title for r in rows] == ["Alpha Grant", "Mango Grant", "Zebra Grant"]


def test_search_ordering_verified_sort(db_session):
    today = date.today()
    db_session.add_all(
        [
            models.Scholarship(
                title="Never verified",
                provider="Test",
                is_active=True,
                last_verified_at=None,
            ),
            models.Scholarship(
                title="Verified recently",
                provider="Test",
                is_active=True,
                last_verified_at=today,
            ),
            models.Scholarship(
                title="Verified older",
                provider="Test",
                is_active=True,
                last_verified_at=today - timedelta(days=30),
            ),
        ]
    )
    db_session.commit()

    rows = _apply_search_ordering(_base_query(db_session), sort="verified", today=today).all()
    titles = [r.title for r in rows]
    assert titles.index("Verified recently") < titles.index("Verified older")
    assert titles.index("Verified older") < titles.index("Never verified")


def test_search_ordering_unknown_sort_falls_back_to_relevance(db_session):
    today = date.today()
    db_session.add_all(
        [
            models.Scholarship(
                title="Closed row",
                provider="Test",
                is_active=True,
                application_status="closed",
            ),
            models.Scholarship(
                title="Open row",
                provider="Test",
                is_active=True,
                application_status="open",
                application_deadline=today + timedelta(days=10),
            ),
        ]
    )
    db_session.commit()

    relevance_rows = _apply_search_ordering(_base_query(db_session), sort="relevance", today=today).all()
    unknown_rows = _apply_search_ordering(_base_query(db_session), sort="not-a-sort", today=today).all()
    assert [r.title for r in relevance_rows] == [r.title for r in unknown_rows]
