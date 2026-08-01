"""Taxonomy expansion tests (DATA-01 / DATA-02 / DATA-06 / B6)."""

from __future__ import annotations

from app.taxonomy.psced_fields import (
    FIELD_HIERARCHY,
    LEGACY_BROAD_DISCIPLINES,
    NORMALIZED_FIELDS,
    PSCED_BROAD_DISCIPLINES,
    resolve_field_ancestors,
    resolve_normalized_field,
)
from app.taxonomy.tvet_qualifications import tvet_qualifications_for_stage


def test_broad_disciplines_unchanged():
    """§15.1 rule 1: the ten legacy broad disciplines stay byte-identical."""
    expected = {
        "STEM": "Science, Technology, Engineering, Mathematics",
        "Engineering": "Engineering and Technology",
        "IT": "Information Technology",
        "Medical": "Medicine and Health Sciences",
        "Business": "Business and Accountancy",
        "Education": "Education and Teacher Training",
        "Agriculture": "Agriculture, Forestry, Fisheries",
        "Arts": "Arts and Humanities",
        "Law": "Law",
        "Architecture": "Architecture and Planning",
    }
    assert PSCED_BROAD_DISCIPLINES == expected
    assert LEGACY_BROAD_DISCIPLINES == tuple(expected.keys())


def test_taxonomy_has_target_field_count():
    assert len(NORMALIZED_FIELDS) >= 85


def test_taxonomy_hierarchy_resolves_upward():
    """Generous upward resolution: DevCom -> Communication -> Arts."""
    chain = resolve_field_ancestors("Development Communication")
    assert "development communication" in chain
    assert "communication" in chain
    assert "arts" in chain

    eng_chain = resolve_field_ancestors("Civil Engineering")
    assert "civil engineering" in eng_chain
    assert "engineering" in eng_chain
    assert "stem" in eng_chain

    hospitality_chain = resolve_field_ancestors("Hospitality Management")
    assert "tourism & hospitality" in hospitality_chain
    assert "business" in hospitality_chain


def test_sub_discipline_hierarchy_edges():
    required = {
        "Communication": ["Arts"],
        "Social Sciences": ["Arts"],
        "Tourism & Hospitality": ["Business"],
        "Maritime": ["Engineering"],
        "Aviation": ["Engineering"],
        "Sports Science": ["Education"],
    }
    for child, parents in required.items():
        assert FIELD_HIERARCHY.get(child) == parents


def test_course_alias_resolves_to_field():
    assert resolve_normalized_field("BSDevCom") == "Development Communication"
    assert resolve_normalized_field("bsit") == "Information Technology"


def test_tvet_only_offered_for_tvet_stage():
    assert tvet_qualifications_for_stage("TVET")
    assert not tvet_qualifications_for_stage("College")
    assert not tvet_qualifications_for_stage(None)
