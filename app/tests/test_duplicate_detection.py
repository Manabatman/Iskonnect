"""Tests for duplicate pair detection."""

from app import models
from app.auth import create_access_token
from app.services.duplicate_detection import find_duplicate_pairs
from app.utils.dedupe import scholarship_dedupe_key


def _admin_headers(client, Session):
    db = Session()
    try:
        user = models.User(email="admin_dup@example.com", password_hash="x", role="admin")
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"Authorization": f"Bearer {create_access_token(user.id, role='admin')}"}
    finally:
        db.close()


def test_find_duplicate_pairs_fuzzy_title(db_session):
    a = models.Scholarship(
        title="Quezon City Scholarship Program",
        provider="Quezon City",
        link="https://example.com/qc",
        dedupe_key=scholarship_dedupe_key("Quezon City Scholarship Program", "Quezon City", "https://example.com/qc"),
        is_active=True,
    )
    b = models.Scholarship(
        title="Quezon City Scholarship Program QCSP",
        provider="Quezon City",
        link="https://example.com/qc",
        dedupe_key=scholarship_dedupe_key(
            "Quezon City Scholarship Program QCSP", "Quezon City", "https://example.com/qc"
        ),
        is_active=False,
    )
    db_session.add_all([a, b])
    db_session.commit()

    pairs = find_duplicate_pairs(db_session, min_confidence=0.85)
    assert len(pairs) >= 1
    assert pairs[0]["match_reason"] in ("exact_link", "title_provider", "similar_title")


def test_duplicate_candidates_api(api_with_db):
    client, Session = api_with_db
    headers = _admin_headers(client, Session)
    db = Session()
    try:
        db.add(
            models.Scholarship(
                title="SM Foundation College Scholarship",
                provider="SM Foundation",
                link="https://example.com/sm",
                dedupe_key=scholarship_dedupe_key(
                    "SM Foundation College Scholarship", "SM Foundation", "https://example.com/sm"
                ),
            )
        )
        db.add(
            models.Scholarship(
                title="SM Foundation College Scholarship Program",
                provider="SM Foundation",
                link="https://example.com/sm",
                dedupe_key=scholarship_dedupe_key(
                    "SM Foundation College Scholarship Program",
                    "SM Foundation",
                    "https://example.com/sm",
                ),
                is_active=False,
            )
        )
        db.commit()
    finally:
        db.close()

    r = client.get("/api/v1/admin/duplicates/candidates", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] >= 1
