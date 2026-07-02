"""Regression tests aligned with audit plan (deadlines, dedupe)."""

from datetime import date, timedelta

from sqlalchemy import and_

from app import models
from app.utils.dedupe import scholarship_dedupe_key


def test_dedupe_key_stable():
    link = "https://example.com/same-program"
    a = scholarship_dedupe_key("  ABC Scholarship ", "DOST ", link)
    b = scholarship_dedupe_key("abc scholarship", "dost", link)
    assert a == b
    c = scholarship_dedupe_key("abc scholarship", "dost", "https://example.com/other")
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
