"""Tests for progressive login lockout."""

from unittest.mock import MagicMock, patch

from app.utils import login_lockout


def test_is_login_locked_false_without_redis(monkeypatch):
    monkeypatch.setattr(login_lockout.settings, "redis_url", None)
    assert login_lockout.is_login_locked("user@example.com") is False


@patch("app.utils.login_lockout._get_redis")
def test_is_login_locked_true_at_threshold(mock_get_redis):
    mock_redis = MagicMock()
    mock_redis.get.return_value = "5"
    mock_get_redis.return_value = mock_redis
    assert login_lockout.is_login_locked("user@example.com") is True


@patch("app.utils.login_lockout._get_redis")
def test_record_failed_login_increments(mock_get_redis):
    mock_redis = MagicMock()
    mock_redis.pipeline.return_value.execute.return_value = [3, True]
    mock_get_redis.return_value = mock_redis
    count = login_lockout.record_failed_login("user@example.com")
    assert count == 3
