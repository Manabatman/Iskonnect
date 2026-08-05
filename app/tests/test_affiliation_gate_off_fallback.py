"""Affiliation evaluator runs when required codes exist even if GATE_AFFILIATIONS is off."""

import json

from app.config import settings
from app.matching.eligibility_gates import evaluate_required_affiliations


def test_required_affiliation_evaluated_when_gate_off(monkeypatch):
    monkeypatch.setattr(settings, "gate_affiliations", False)
    sch = {"required_affiliation_codes": json.dumps(["gsis_member"])}
    profile = {"is_gsis_dependent": False}
    check = evaluate_required_affiliations(profile, sch)
    assert check.result.value == "unmet"

    profile_ok = {"is_gsis_dependent": True}
    check_ok = evaluate_required_affiliations(profile_ok, sch)
    assert check_ok.result.value == "met"


def test_no_required_codes_stays_not_applicable(monkeypatch):
    monkeypatch.setattr(settings, "gate_affiliations", False)
    check = evaluate_required_affiliations({}, {})
    assert check.result.value == "not_applicable"
