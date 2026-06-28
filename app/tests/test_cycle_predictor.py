"""Tests for scholarship cycle prediction."""

from datetime import date

import pytest

from app.prediction.cycle_predictor import get_upcoming_scholarships, predict_next_open


def test_predict_next_open_annual():
    last = date(2025, 3, 1)
    assert predict_next_open(last, "annual") == date(2026, 3, 1)


def test_predict_next_open_semester():
    last = date(2025, 3, 1)
    assert predict_next_open(last, "semester") == date(2025, 9, 1)


def test_predict_next_open_semester_wraps_year():
    last = date(2025, 9, 1)
    assert predict_next_open(last, "semester") == date(2026, 3, 1)


def test_predict_next_open_rolling():
    last = date(2025, 3, 1)
    assert predict_next_open(last, "rolling") == date.today()


def test_predict_next_open_invalid_returns_none():
    assert predict_next_open(date(2025, 3, 1), "") is None
    assert predict_next_open(date(2025, 3, 1), "unknown") is None


def test_get_upcoming_scholarships_returns_qualifying_with_future_prediction():
    # Use last_open_date so predicted_next_open (last_open + 1 year) is in the future
    from datetime import date, timedelta
    last_open = date.today() - timedelta(days=200)  # ~6.5 months ago
    last_close = last_open.replace(month=min(last_open.month + 4, 12))
    profile = {
        "age": 20,
        "education_level": "College",
        "region": "Metro Manila",
        "household_income_annual": 200000,
        "gwa_normalized": 92.0,
        "field_of_study_broad": "Engineering",
    }
    scholarships = [
        {
            "id": 1,
            "title": "Test Scholarship",
            "provider": "Test",
            "cycle_type": "annual",
            "last_open_date": last_open.isoformat(),
            "last_close_date": last_close.isoformat(),
            "eligible_levels": ["College"],
            "eligible_regions": [],
            "eligible_cities": [],
            "regions": [],
            "min_age": 16,
            "max_age": 25,
            "max_income_threshold": 400000,
            "min_gwa_normalized": 90.0,
            "eligible_courses_psced": ["Engineering"],
            "eligible_school_types": ["Public", "Private"],
            "residency_required": False,
        }
    ]
    result = get_upcoming_scholarships(profile, scholarships)
    assert len(result) == 1
    assert result[0]["title"] == "Test Scholarship"
    assert "image_url" in result[0]
    assert "image_alt" in result[0]
    expected_next = (last_open.replace(year=last_open.year + 1)).isoformat()
    assert result[0]["predicted_next_open"] == expected_next
