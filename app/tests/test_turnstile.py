"""Tests for Cloudflare Turnstile verification (optional gate)."""

from unittest.mock import MagicMock, patch

import pytest

from app.utils import turnstile


def test_verify_turnstile_noop_when_secret_unset(monkeypatch):
    monkeypatch.setattr(turnstile.settings, "turnstile_secret_key", None)
    assert turnstile.verify_turnstile(None) is True
    assert turnstile.verify_turnstile("") is True


def test_verify_turnstile_requires_token_when_enabled(monkeypatch):
    monkeypatch.setattr(turnstile.settings, "turnstile_secret_key", "test-secret")
    assert turnstile.verify_turnstile(None) is False
    assert turnstile.verify_turnstile("") is False


@patch("app.utils.turnstile.httpx.Client")
def test_verify_turnstile_success(mock_client_cls, monkeypatch):
    monkeypatch.setattr(turnstile.settings, "turnstile_secret_key", "test-secret")
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"success": True}
    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.post.return_value = mock_resp
    mock_client_cls.return_value = mock_client

    assert turnstile.verify_turnstile("valid-token", "127.0.0.1") is True
