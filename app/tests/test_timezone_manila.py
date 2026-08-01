"""Tests for Asia/Manila calendar helpers (TRUST-03)."""

from datetime import date, datetime, timedelta, timezone
from unittest.mock import patch

from app.matching.hard_filters import is_application_deadline_passed
from app.utils.timezone import PH_TZ, today_manila


def test_today_manila_uses_philippine_calendar():
    # 2026-08-01 01:00 Manila = 2026-07-31 17:00 UTC — still Aug 1 in PH
    frozen_utc = datetime(2026, 7, 31, 17, 0, tzinfo=timezone.utc)
    with patch("app.utils.timezone.datetime") as mock_dt:
        mock_dt.now.return_value = frozen_utc.astimezone(PH_TZ)
        assert today_manila() == date(2026, 8, 1)


def test_deadline_passed_uses_manila_not_utc_server_day():
    # Deadline July 31; at 2026-07-31 20:00 UTC it is already Aug 1 in Manila → passed
    yesterday = date(2026, 7, 31)
    frozen_utc = datetime(2026, 7, 31, 20, 0, tzinfo=timezone.utc)
    with patch("app.utils.timezone.datetime") as mock_dt:
        mock_dt.now.return_value = frozen_utc.astimezone(PH_TZ)
        assert is_application_deadline_passed(yesterday) is True

    tomorrow = date.today() + timedelta(days=1)
    assert is_application_deadline_passed(tomorrow) is False
    assert is_application_deadline_passed(None) is False
