"""SEC-06 / SEC-08: account deletion rate limit and erasure completeness."""

import json

from app import models
from app.auth import create_access_token, hash_password


def _auth_headers(user_id: int) -> dict[str, str]:
    return {"Authorization": f"Bearer {create_access_token(user_id)}"}


def test_delete_profile_rate_limited(api_with_db):
    client, Session = api_with_db
    headers_list: list[dict[str, str]] = []
    db = Session()
    try:
        for i in range(4):
            user = models.User(
                email=f"delete_rate_{i}@example.com",
                password_hash=hash_password("password1234"),
                email_verified=True,
            )
            db.add(user)
            db.flush()
            headers_list.append(_auth_headers(user.id))
        db.commit()
    finally:
        db.close()

    statuses = [client.delete("/api/v1/profiles/me", headers=h).status_code for h in headers_list[:3]]
    assert all(code in (200, 404) for code in statuses)

    r = client.delete("/api/v1/profiles/me", headers=headers_list[3])
    assert r.status_code == 429


def test_account_deletion_anonymizes_feedback_and_redacts_audit(api_with_db):
    client, Session = api_with_db
    db = Session()
    try:
        user = models.User(
            email="erase_user@example.com",
            password_hash=hash_password("password1234"),
            email_verified=True,
        )
        db.add(user)
        db.flush()
        db.add(
            models.ProductFeedback(
                user_id=user.id,
                category="bug",
                message="Something broke",
                contact_email="erase_user@example.com",
            )
        )
        db.add(
            models.AuditLog(
                actor_id=user.id,
                actor_type="user",
                action="profile.update",
                resource_type="student",
                resource_id=1,
                details=json.dumps({"email": "erase_user@example.com", "user_id": user.id}),
            )
        )
        db.commit()
        user_id = user.id
    finally:
        db.close()

    r = client.delete("/api/v1/profiles/me", headers=_auth_headers(user_id))
    assert r.status_code == 200

    db = Session()
    try:
        feedback = db.query(models.ProductFeedback).filter(
            models.ProductFeedback.message == "Something broke"
        ).first()
        assert feedback is not None
        assert feedback.user_id is None
        assert feedback.contact_email is None

        audit = db.query(models.AuditLog).filter(models.AuditLog.actor_id == user_id).first()
        assert audit is not None
        details = json.loads(audit.details)
        assert "email" not in details
        assert details.get("user_id") == user_id

        assert db.query(models.User).filter(models.User.id == user_id).first() is None
    finally:
        db.close()
