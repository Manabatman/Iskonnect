"""Unit tests for study destination preference evaluator."""

from app.matching.eligibility_result import RequirementResult, _evaluate_destination_country


def _sch(**kwargs):
    base = {"countries": None}
    base.update(kwargs)
    return base


def _profile(pref: str):
    return {"study_destination_preference": pref}


def test_empty_countries_not_applicable():
    check = _evaluate_destination_country(_profile("PHILIPPINES_ONLY"), _sch(countries=[]))
    assert check.result == RequirementResult.NOT_APPLICABLE


def test_abroad_only_blocks_philippines_only_student():
    check = _evaluate_destination_country(
        _profile("PHILIPPINES_ONLY"),
        _sch(countries=["Japan"]),
    )
    assert check.result == RequirementResult.UNMET
    assert "Japan" in (check.evidence or "")


def test_abroad_only_allows_abroad_student():
    check = _evaluate_destination_country(
        _profile("ABROAD_ONLY"),
        _sch(countries=["Japan"]),
    )
    assert check.result == RequirementResult.MET


def test_ph_local_blocks_abroad_only_student():
    check = _evaluate_destination_country(
        _profile("ABROAD_ONLY"),
        _sch(countries=["Philippines"]),
    )
    assert check.result == RequirementResult.UNMET


def test_both_hosts_passes_either_preference():
    check = _evaluate_destination_country(
        _profile("BOTH"),
        _sch(countries=["Japan", "Philippines"]),
    )
    assert check.result == RequirementResult.MET


def test_default_preference_is_philippines_only():
    check = _evaluate_destination_country({}, _sch(countries=["South Korea"]))
    assert check.result == RequirementResult.UNMET
