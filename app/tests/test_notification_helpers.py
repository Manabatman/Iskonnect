"""Tests for match-run notification creation."""

from unittest.mock import MagicMock, patch

from app.utils.notification_helpers import create_notifications_for_match_results


def test_notifications_skipped_when_disabled():
    db = MagicMock()
    with patch("app.utils.notification_helpers.settings") as s:
        s.enable_notifications = False
        create_notifications_for_match_results(
            db,
            1,
            [{"id": 1, "title": "X", "final_score": 99, "application_deadline": "2099-12-31"}],
        )
    db.add.assert_not_called()
    db.commit.assert_not_called()


def test_notifications_commits_when_enabled():
    db = MagicMock()
    with patch("app.utils.notification_helpers.settings") as s:
        s.enable_notifications = True
        create_notifications_for_match_results(
            db,
            1,
            [
                {
                    "id": 1,
                    "title": "Strong Match",
                    "final_score": 85,
                    "application_deadline": "2099-06-01",
                }
            ],
        )
    assert db.add.call_count >= 1
    db.commit.assert_called_once()
