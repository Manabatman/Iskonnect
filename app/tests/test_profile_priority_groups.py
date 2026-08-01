"""Tests for DATA-08 profile-derived priority groups."""

from app.matching.eligibility_result import RequirementResult, _evaluate_members_only
from app.scoring.components import score_equity
from app.taxonomy.profile_priority_groups import (
    profile_priority_groups,
    profile_student_athlete,
    profile_working_student,
)


def test_profile_working_student_employment():
    assert profile_working_student({"employment_status": "part-time"}) is True
    assert profile_working_student({"employment_status": "none"}) is False


def test_profile_working_student_evening_program():
    assert profile_working_student({"evening_weekend_program": True}) is True


def test_profile_student_athlete_levels():
    assert profile_student_athlete({"athlete_level": "varsity"}) is True
    assert profile_student_athlete({"athlete_level": "club"}) is True
    assert profile_student_athlete({"athlete_level": ""}) is False


def test_profile_priority_groups_order():
    groups = profile_priority_groups(
        {"employment_status": "full-time", "athlete_level": "national"}
    )
    assert groups == ["Working Student", "Student Athlete"]


def test_score_equity_profile_priority_match():
    flags = {"working_student": True, "student_athlete": False}
    score = score_equity(flags, ["Working Student"])
    assert score == 0.75


def test_members_only_working_student_met():
    sch = {"members_only": True, "priority_groups": '["Working Student"]'}
    profile = {"employment_status": "part-time"}
    check = _evaluate_members_only(profile, sch)
    assert check.result == RequirementResult.MET


def test_members_only_student_athlete_unmet():
    sch = {"members_only": True, "priority_groups": '["Student Athlete"]'}
    profile = {"athlete_level": ""}
    check = _evaluate_members_only(profile, sch)
    assert check.result == RequirementResult.UNMET
