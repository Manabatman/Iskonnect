"""Editorial state must not hide needs_review rows from browse."""

from app.utils.editorial_state import NEEDS_REVIEW, PUBLISHED, apply_editorial_state, derive_is_active


def test_needs_review_stays_active():
    row = type("Row", (), {"editorial_state": None, "is_active": True, "data_status": "active", "application_deadline": None, "link_status": None})()
    apply_editorial_state(row, NEEDS_REVIEW)
    assert derive_is_active(row) is True
    assert row.is_active is True


def test_archived_is_inactive():
    row = type("Row", (), {"editorial_state": None, "is_active": True, "data_status": "active", "application_deadline": None, "link_status": None})()
    from app.utils.editorial_state import ARCHIVED

    apply_editorial_state(row, ARCHIVED)
    assert derive_is_active(row) is False
