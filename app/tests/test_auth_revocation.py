"""SEC-02: access-token revocation via Redis denylist."""

from app.auth import _access_token_revoked, create_access_token, decode_token, revoke_access_token


class _FakeRedis:
    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    def setex(self, key: str, ttl: int, value: str) -> None:
        self._store[key] = value

    def get(self, key: str) -> str | None:
        return self._store.get(key)


def test_logout_invalidates_access_token(api_with_db, monkeypatch):
    client, Session = api_with_db
    fake = _FakeRedis()
    monkeypatch.setattr("app.config.settings.redis_url", "redis://test/0")
    monkeypatch.setattr("app.auth._redis_client", lambda: fake)

    reg = client.post(
        "/api/v1/auth/register",
        json={"email": "revoke_user@example.com", "password": "password1234"},
    )
    assert reg.status_code == 200
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "revoke_user@example.com", "password": "password1234"},
    )
    assert login.status_code == 200
    tokens = login.json()
    access = tokens["access_token"]
    refresh = tokens["refresh_token"]

    me_before = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access}"},
    )
    assert me_before.status_code == 200

    logout = client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": refresh},
        headers={"Authorization": f"Bearer {access}"},
    )
    assert logout.status_code == 200

    me_after = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access}"},
    )
    assert me_after.status_code == 401


def test_revocation_fail_closed_without_redis_outside_development(monkeypatch):
    monkeypatch.setattr("app.config.settings.redis_url", None)
    monkeypatch.setattr("app.config.settings.environment", "production")
    monkeypatch.setattr("app.auth._redis_client", lambda: None)

    token = create_access_token(1)
    revoke_access_token(token)
    assert decode_token(token) is None
    assert _access_token_revoked("any-jti") is True


def test_revocation_no_op_without_redis_in_development(monkeypatch):
    monkeypatch.setattr("app.config.settings.redis_url", None)
    monkeypatch.setattr("app.config.settings.environment", "development")
    monkeypatch.setattr("app.auth._redis_client", lambda: None)

    token = create_access_token(2)
    assert decode_token(token) is not None
    assert _access_token_revoked("any-jti") is False
