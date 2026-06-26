"""Tests for client IP extraction behind reverse proxies."""

from unittest.mock import MagicMock

import pytest

from app.utils.client_ip import get_client_ip


def _request(*, client_host: str = "10.0.0.1", xff: str | None = None):
    req = MagicMock()
    req.client = MagicMock(host=client_host)
    req.headers = {}
    if xff is not None:
        req.headers["x-forwarded-for"] = xff
    return req


def test_uses_direct_peer_when_proxy_not_trusted(monkeypatch):
    monkeypatch.setattr("app.config.settings.trust_proxy_headers", False)
    req = _request(client_host="203.0.113.5", xff="198.51.100.2")
    assert get_client_ip(req) == "203.0.113.5"


def test_uses_xff_leftmost_when_proxy_trusted(monkeypatch):
    monkeypatch.setattr("app.config.settings.trust_proxy_headers", True)
    req = _request(client_host="10.0.0.1", xff="198.51.100.2, 10.0.0.1")
    assert get_client_ip(req) == "198.51.100.2"
