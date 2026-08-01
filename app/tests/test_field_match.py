"""Field-match level tests (DATA-03 / B7)."""

from __future__ import annotations

from app.matching.field_match import compute_field_match_level
from app.scoring.components import score_field


def test_field_match_level_ordering():
    """exact > sibling > discipline > none by component score."""
    scores = {
        "exact": score_field("exact"),
        "sibling": score_field("sibling"),
        "discipline": score_field("discipline"),
        "none": score_field("none"),
    }
    assert scores["exact"] > scores["sibling"] > scores["discipline"] > scores["none"]


def test_legacy_level_names_still_accepted():
    assert score_field("broad") == score_field("sibling")
    assert score_field("partial") == 0.4
    assert score_field("none") == 0.2


def test_devcom_communication_and_arts_levels():
    assert (
        compute_field_match_level(
            "Development Communication",
            None,
            [],
            [],
            ["Communication"],
            [],
            [],
        )
        == "discipline"
    )
    assert (
        compute_field_match_level(
            "Development Communication",
            None,
            [],
            [],
            ["Arts"],
            [],
            [],
        )
        == "discipline"
    )


def test_sibling_fields_under_same_parent():
    level = compute_field_match_level(
        "Development Communication",
        None,
        [],
        [],
        ["Journalism"],
        [],
        [],
    )
    assert level == "sibling"


def test_exact_field_and_specific_course():
    assert (
        compute_field_match_level(
            "Nursing",
            "BS Nursing",
            [],
            [],
            [],
            ["BS Nursing"],
            [],
        )
        == "exact"
    )
