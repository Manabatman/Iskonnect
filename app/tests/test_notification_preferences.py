"""Notification preference API."""

from app import models
from app.auth import create_access_token


def _auth_headers(client, Session):
    db = Session()
    try:
        user = models.User(
            email="notify_prefs@example.com",
            password_hash="x",
            role="student",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        token = create_access_token(user.id, role="student")
        return {"Authorization": f"Bearer {token}"}, user.id
    finally:
        db.close()


def test_notification_preferences_roundtrip(api_with_db):
    client, Session = api_with_db
    headers, _user_id = _auth_headers(client, Session)

    r = client.get("/api/v1/settings/notifications", headers=headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["notify_deadline_reminders"] is True
    assert data["notify_new_matches"] is True

    r2 = client.patch(
        "/api/v1/settings/notifications",
        headers=headers,
        json={"notify_deadline_reminders": False, "notify_new_matches": False},
    )
    assert r2.status_code == 200, r2.text
    updated = r2.json()
    assert updated["notify_deadline_reminders"] is False
    assert updated["notify_new_matches"] is False
