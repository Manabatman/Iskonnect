"""Hard filter diagnostics: per-scholarship disqualification reasons."""

from app.matching.hard_filters import filter_scholarships


def test_eliminated_scholarships_in_diagnostics():
    profile = {
        "age": 25,
        "education_level": "College",
        "region": "NCR",
        "gwa_normalized": 50.0,
    }
    scholarships = [
        {
            "id": 99,
            "title": "High GWA Only",
            "min_gwa_normalized": 90.0,
            "is_active": True,
        }
    ]
    passed, diag = filter_scholarships(profile, scholarships)
    assert len(passed) == 0
    eliminated = diag.get("eliminated_scholarships") or []
    assert len(eliminated) == 1
    assert eliminated[0]["scholarship_id"] == 99
    assert eliminated[0]["filter"] == "gwa"
