"""Tests for PSGC geographic matching helpers."""

from app.taxonomy.psgc import normalize_psgc_code, psgc_codes_match, lookup_psgc_name


def test_normalize_psgc_code_pads_to_nine():
    assert normalize_psgc_code("13") == "130000000"
    assert normalize_psgc_code("137401000") == "137401000"


def test_psgc_region_prefix_match():
    assert psgc_codes_match("137401000", "130000000", level="region") is True
    assert psgc_codes_match("137401000", "140000000", level="region") is False


def test_lookup_seed_name():
    assert lookup_psgc_name("137401000") == "Binondo"
