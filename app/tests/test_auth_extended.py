"""Auth flow tests: password reset, email verify, non-enumerating register."""

from datetime import timedelta

from app import models
from app.auth import (
    create_email_verification_token,
    hash_password,
    hash_refresh_token,
    issue_refresh_token,
    new_refresh_token_plain,
)
from app.utils.timezone import utc_now_naive


def _create_user(Session, email: str, password: str = "password1") -> models.User:
    db = Session()
    try:
        user = models.User(email=email, password_hash=hash_password(password), email_verified=False)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()


def test_register_non_enumerating_duplicate(api_with_db):
    client, Session = api_with_db
    _create_user(Session, "dup_user@example.com")
    r = client.post(
        "/api/v1/auth/register",
        json={"email": "dup_user@example.com", "password": "password2"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data.get("access_token") is None
    assert "detail" in data


def test_password_reset_revokes_refresh_tokens(api_with_db):
    client, Session = api_with_db
    user = _create_user(Session, "reset_user@example.com")
    db = Session()
    try:
        rt = issue_refresh_token(db, user.id)
        db.commit()
    finally:
        db.close()

    client.post("/api/v1/auth/forgot-password", json={"email": "reset_user@example.com"})

    db = Session()
    try:
        user = db.query(models.User).filter(models.User.id == user.id).first()
        raw = new_refresh_token_plain()
        user.password_reset_token_hash = hash_refresh_token(raw)
        user.password_reset_expires_at = utc_now_naive() + timedelta(hours=1)
        db.commit()
        token = raw
    finally:
        db.close()

    r = client.post(
        "/api/v1/auth/reset-password",
        json={"token": token, "new_password": "newpassword1"},
    )
    assert r.status_code == 200

    r_old = client.post("/api/v1/auth/refresh", json={"refresh_token": rt})
    assert r_old.status_code == 401


def test_verify_email(api_with_db):
    client, Session = api_with_db
    user = _create_user(Session, "verify_user@example.com")
    token = create_email_verification_token(user.id)
    r = client.post("/api/v1/auth/verify-email", json={"token": token})
    assert r.status_code == 200

    db = Session()
    try:
        row = db.query(models.User).filter(models.User.id == user.id).first()
        assert row.email_verified is True
    finally:
        db.close()


def test_login_unverified_blocked_when_verification_required(api_with_db, monkeypatch):
    client, Session = api_with_db
    monkeypatch.setattr("app.config.settings.require_email_verification", True)
    monkeypatch.setattr("app.config.settings.smtp_host", "smtp.example.com")
    monkeypatch.setattr("app.config.settings.email_from", "noreply@example.com")
    _create_user(Session, "unverified@example.com", "password1")
    r = client.post(
        "/api/v1/auth/login",
        json={"email": "unverified@example.com", "password": "password1"},
    )
    assert r.status_code == 403


def test_login_unverified_allowed_when_verification_disabled(api_with_db, monkeypatch):
    client, Session = api_with_db
    monkeypatch.setattr("app.config.settings.require_email_verification", False)
    _create_user(Session, "beta_user@example.com", "password1")
    r = client.post(
        "/api/v1/auth/login",
        json={"email": "beta_user@example.com", "password": "password1"},
    )
    assert r.status_code == 200
    assert r.json().get("access_token")


def test_register_auto_verifies_when_verification_disabled(api_with_db, monkeypatch):
    client, Session = api_with_db
    monkeypatch.setattr("app.config.settings.require_email_verification", False)
    r = client.post(
        "/api/v1/auth/register",
        json={"email": "auto_verify@example.com", "password": "password1"},
    )
    assert r.status_code == 200
    assert r.json().get("access_token")

    db = Session()
    try:
        row = db.query(models.User).filter(models.User.email == "auto_verify@example.com").first()
        assert row is not None
        assert row.email_verified is True
    finally:
        db.close()


def test_auth_me_includes_require_email_verification_flag(api_with_db, monkeypatch):
    client, Session = api_with_db
    monkeypatch.setattr("app.config.settings.require_email_verification", False)
    user = _create_user(Session, "me_flag@example.com", "password1")
    from app.auth import create_access_token

    token = create_access_token(user.id)
    r = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json().get("require_email_verification") is False
