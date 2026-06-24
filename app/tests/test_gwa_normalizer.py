"""Regression tests for GWA normalization (locked to current linear formulas)."""

import pytest

from app.taxonomy.gwa_normalizer import normalize_gwa, resolve_gwa_scale


class TestFivePointScale:
    @pytest.mark.parametrize(
        "raw,expected",
        [
            (1.0, 100.0),
            (1.25, 93.75),
            (2.0, 75.0),
            (3.0, 50.0),
            (4.0, 25.0),
            (5.0, 0.0),
        ],
    )
    def test_5_0_scale_linear(self, raw, expected):
        assert normalize_gwa(raw, "5.0_scale") == pytest.approx(expected)
        assert normalize_gwa(raw, "5.0") == pytest.approx(expected)

    def test_5_0_below_one_maps_to_100(self):
        assert normalize_gwa(0.5, "5.0_scale") == 100.0

    def test_5_0_above_five_maps_to_zero(self):
        assert normalize_gwa(5.5, "5.0_scale") == 0.0


class TestFourPointScale:
    @pytest.mark.parametrize(
        "raw,expected",
        [
            (0.0, 0.0),
            (1.0, 25.0),
            (2.0, 50.0),
            (3.0, 75.0),
            (4.0, 100.0),
        ],
    )
    def test_4_0_scale_linear(self, raw, expected):
        assert normalize_gwa(raw, "4.0_scale") == pytest.approx(expected)
        assert normalize_gwa(raw, "4.0") == pytest.approx(expected)

    def test_4_0_above_four_caps_at_100(self):
        assert normalize_gwa(4.5, "4.0_scale") == 100.0


class TestPercentageAndDefault:
    def test_percentage_clamped(self):
        assert normalize_gwa(85, "percentage") == 85.0
        assert normalize_gwa(-10, "percentage") == 0.0
        assert normalize_gwa(150, "percentage") == 100.0

    def test_empty_scale_treats_as_percentage(self):
        assert normalize_gwa(80, "") == 80.0
        assert normalize_gwa(80, None) == 80.0

    def test_invalid_input_returns_none(self):
        assert normalize_gwa(None, "5.0_scale") is None
        assert normalize_gwa("not-a-number", "5.0_scale") is None


class TestScaleAliases:
    def test_alias_map(self):
        assert resolve_gwa_scale("NUMERIC_1_TO_5") == "5.0_scale"
        assert resolve_gwa_scale("numeric_4_scale") == "4.0_scale"
        assert resolve_gwa_scale("percentage_75_to_100") == "percentage"

    def test_unknown_scale_ambiguous_value_returns_none(self):
        assert normalize_gwa(2.5, "unknown_scale") is None

    def test_unknown_scale_high_percentage_still_works(self):
        assert normalize_gwa(92, "unknown_scale") == 92.0


class TestStringParsing:
    def test_comma_decimal(self):
        assert normalize_gwa("3,5", "5.0_scale") == pytest.approx(37.5)
