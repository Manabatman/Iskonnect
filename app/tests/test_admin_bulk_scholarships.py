"""Tests for admin bulk scholarship actions."""

from app import models
from app.auth import create_access_token
from app.utils.dedupe import scholarship_dedupe_key


def _admin_headers(client, Session):
    db = Session()
    try:
        user = models.User(email="admin_bulk@example.com", password_hash="x", role="admin")
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"Authorization": f"Bearer {create_access_token(user.id, role='admin')}"}
    finally:
        db.close()


def test_bulk_deactivate_and_restore(api_with_db):
    client, Session = api_with_db
    headers = _admin_headers(client, Session)
    db = Session()
    try:
        s = models.Scholarship(
            title="Bulk Target",
            provider="Gov",
            link="https://example.com/bulk",
            dedupe_key=scholarship_dedupe_key("Bulk Target", "Gov", "https://example.com/bulk"),
            is_active=True,
        )
        db.add(s)
        db.commit()
        db.refresh(s)
        sid = s.id
    finally:
        db.close()

    r = client.post(
        "/api/v1/admin/scholarships/bulk",
        headers=headers,
        json={"ids": [sid], "action": "deactivate"},
    )
    assert r.status_code == 200
    assert sid in r.json()["succeeded"]

    r2 = client.post(
        "/api/v1/admin/scholarships/bulk",
        headers=headers,
        json={"ids": [sid], "action": "restore"},
    )
    assert r2.status_code == 200
    assert sid in r2.json()["succeeded"]


def test_bulk_permanent_delete_skips_active(api_with_db):
    client, Session = api_with_db
    headers = _admin_headers(client, Session)
    db = Session()
    try:
        s = models.Scholarship(
            title="Still Active",
            provider="Gov",
            link="https://example.com/active-bulk",
            dedupe_key=scholarship_dedupe_key("Still Active", "Gov", "https://example.com/active-bulk"),
            is_active=True,
        )
        db.add(s)
        db.commit()
        db.refresh(s)
        sid = s.id
    finally:
        db.close()

    r = client.post(
        "/api/v1/admin/scholarships/bulk",
        headers=headers,
        json={"ids": [sid], "action": "permanent_delete"},
    )
    assert r.status_code == 200
    body = r.json()
    assert sid not in body["succeeded"]
    assert any(f["id"] == sid for f in body["failed"])
