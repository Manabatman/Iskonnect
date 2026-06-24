"""Tests for deadline-passed eligibility messaging."""

from datetime import date, timedelta

from app.matching.hard_filters import DEADLINE_PASSED_MESSAGE, is_application_deadline_passed
from app.matching.match_service import MatchService


def test_is_application_deadline_passed():
    yesterday = date.today() - timedelta(days=1)
    tomorrow = date.today() + timedelta(days=1)
    assert is_application_deadline_passed(yesterday) is True
    assert is_application_deadline_passed(tomorrow) is False
    assert is_application_deadline_passed(None) is False


def test_match_includes_deadline_passed_message():
    profile = {
        "full_name": "Test Student",
        "email": "deadline@test.com",
        "age": 20,
        "education_level": "College",
        "region": "NCR",
        "gwa_normalized": 90.0,
    }
    past = date.today() - timedelta(days=5)
    scholarships = [
        {
            "id": 1,
            "title": "Past Deadline Grant",
            "provider": "Test",
            "link": "https://example.com/past",
            "description": "Test",
            "application_deadline": past,
            "is_active": True,
            "data_status": "active",
        }
    ]
    service = MatchService()
    results, diagnostics = service.get_matches(profile, scholarships)
    assert len(results) == 1
    match = results[0]
    assert match["deadline_passed"] is True
    assert match["eligibility_status"] is False
    assert DEADLINE_PASSED_MESSAGE in match["explanation"]
    assert diagnostics.get("deadline_passed_match_count") == 1
