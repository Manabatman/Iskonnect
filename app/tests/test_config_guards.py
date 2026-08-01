"""SEC-01: startup configuration guards."""

import pytest

from app.config import DEFAULT_SECRET_KEY_VALUE, settings


def test_unset_environment_rejects_placeholder_secret(monkeypatch):
    monkeypatch.setattr(settings, "environment", "")
    monkeypatch.setattr(settings, "secret_key", DEFAULT_SECRET_KEY_VALUE)
    monkeypatch.setattr(settings, "bind_host", "127.0.0.1")
    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        settings.validate_for_production()


def test_development_allows_placeholder_secret_on_loopback(monkeypatch):
    monkeypatch.setattr(settings, "environment", "development")
    monkeypatch.setattr(settings, "secret_key", DEFAULT_SECRET_KEY_VALUE)
    monkeypatch.setattr(settings, "bind_host", "127.0.0.1")
    settings.validate_for_production()


def test_non_loopback_bind_rejects_placeholder_secret_even_in_development(monkeypatch):
    monkeypatch.setattr(settings, "environment", "development")
    monkeypatch.setattr(settings, "secret_key", DEFAULT_SECRET_KEY_VALUE)
    monkeypatch.setattr(settings, "bind_host", "0.0.0.0")
    with pytest.raises(RuntimeError, match="BIND_HOST"):
        settings.validate_for_production()


def test_production_rejects_auth_disabled(monkeypatch):
    monkeypatch.setattr(settings, "environment", "production")
    monkeypatch.setattr(settings, "secret_key", "a" * 64)
    monkeypatch.setattr(settings, "auth_disabled", True)
    monkeypatch.setattr(settings, "database_url", "postgresql://user:pass@db.example.com/app")
    monkeypatch.setattr(settings, "cors_origins", "https://iskonnect.ph")
    monkeypatch.setattr(settings, "redis_url", "redis://localhost:6379/0")
    monkeypatch.setattr(settings, "trust_proxy_headers", True)
    monkeypatch.setattr(settings, "require_email_verification", False)
    with pytest.raises(RuntimeError, match="AUTH_DISABLED"):
        settings.validate_for_production()


def test_production_requires_redis(monkeypatch):
    monkeypatch.setattr(settings, "environment", "production")
    monkeypatch.setattr(settings, "secret_key", "a" * 64)
    monkeypatch.setattr(settings, "database_url", "postgresql://user:pass@db.example.com/app")
    monkeypatch.setattr(settings, "cors_origins", "https://iskonnect.ph")
    monkeypatch.setattr(settings, "redis_url", None)
    monkeypatch.setattr(settings, "trust_proxy_headers", True)
    monkeypatch.setattr(settings, "require_email_verification", False)
    with pytest.raises(RuntimeError, match="REDIS_URL"):
        settings.validate_for_production()


def test_unrecognized_environment_treated_as_production(monkeypatch):
    monkeypatch.setattr(settings, "environment", "staging-ish")
    monkeypatch.setattr(settings, "secret_key", DEFAULT_SECRET_KEY_VALUE)
    monkeypatch.setattr(settings, "bind_host", "127.0.0.1")
    assert settings.resolved_validation_environment() == "production"
    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        settings.validate_for_production()


def test_active_guards_include_production_validation_outside_development(monkeypatch):
    monkeypatch.setattr(settings, "environment", "")
    monkeypatch.setattr(settings, "secret_key", "custom-secret")
    assert "production-config-validation" in settings.active_guards()


def test_refresh_token_default_ttl_is_seven_days():
    assert settings.refresh_token_expire_days == 7
