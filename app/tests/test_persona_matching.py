"""41-persona matching safety net (QA-05 / B5)."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from app.matching.match_service import MatchService
from app.taxonomy.equity_groups import EQUITY_GROUP_IDS
from app.utils.application_status import APPLICATION_STATUSES

FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "persona_catalog.json"
GOLDEN_DIR = FIXTURE_PATH.parent / "golden"
_PR_ID_PATTERN = re.compile(r"^PR-\d{2}$")
_GWA_THRESHOLD_SCALES = frozenset({"percentage", "5.0_scale", "4.0_scale"})
_BREAKDOWN_KEYS = frozenset({"academic", "socioeconomic", "field_relevance", "geographic", "priority_group"})
_WHY_NOT_HIGHER_SCORE_CEILING = 100.0


def _load_catalog() -> dict:
    with FIXTURE_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def _match_ids(profile: dict, scholarships: list[dict]) -> set[int]:
    service = MatchService()
    results, _ = service.get_matches(profile, scholarships)
    return {int(r["id"]) for r in results}


def _ranked_matches(profile: dict, scholarships: list[dict]) -> list[dict]:
    service = MatchService()
    results, _ = service.get_matches(profile, scholarships)
    return results


def _golden_rows(results: list[dict]) -> list[dict]:
    return [
        {
            "id": int(r["id"]),
            "title": r.get("title"),
            "qualification_status": r.get("qualification_status"),
            "final_score": float(
                r.get("final_score") if r.get("final_score") is not None else r.get("score", 0)
            ),
            "deadline_passed": bool(r.get("deadline_passed")),
        }
        for r in results
    ]


def _human_readable_lines(match: dict) -> list[str]:
    lines: list[str] = []
    for item in match.get("explanation") or []:
        if isinstance(item, str) and item.strip():
            lines.append(item.strip())
    reason = match.get("provisional_reason")
    if isinstance(reason, str) and reason.strip():
        lines.append(reason.strip())
    return lines


def _assert_explanation_quality(persona_id: str, match: dict) -> None:
    sid = match.get("id")
    breakdown = match.get("breakdown")
    assert isinstance(breakdown, dict) and breakdown, f"{persona_id}/{sid}: breakdown missing or empty"
    assert _BREAKDOWN_KEYS <= set(breakdown.keys()), (
        f"{persona_id}/{sid}: breakdown missing keys {sorted(_BREAKDOWN_KEYS - set(breakdown.keys()))}"
    )

    readable = _human_readable_lines(match)
    assert readable, f"{persona_id}/{sid}: no human-readable explanation lines"

    score = float(match.get("final_score") if match.get("final_score") is not None else match.get("score", 0))
    if score < _WHY_NOT_HIGHER_SCORE_CEILING:
        why_not = [line for line in (match.get("why_not_higher") or []) if isinstance(line, str) and line.strip()]
        assert why_not, f"{persona_id}/{sid}: score {score} < 100 but why_not_higher empty"


@pytest.fixture(scope="module")
def catalog():
    return _load_catalog()


@pytest.fixture(scope="module")
def scholarships(catalog):
    return catalog["scholarships"]


@pytest.mark.parametrize(
    "persona",
    _load_catalog()["personas"],
    ids=[p["id"] for p in _load_catalog()["personas"]],
)
def test_persona_inclusions_and_exclusions(persona, scholarships):
    ids = _match_ids(persona["profile"], scholarships)
    for sid in persona.get("must_include", []):
        assert sid in ids, (
            f"{persona['id']}: expected scholarship {sid} in matches. "
            f"Notes: {persona.get('notes', '')}. Got: {sorted(ids)}"
        )
    for sid in persona.get("must_exclude", []):
        assert sid not in ids, (
            f"{persona['id']}: scholarship {sid} must be excluded. "
            f"Notes: {persona.get('notes', '')}. Got: {sorted(ids)}"
        )


def test_persona_mutation_detects_income_bug(scholarships):
    """Deliberate wrong income logic should fail at least one persona."""
    catalog = _load_catalog()
    persona = next(p for p in catalog["personas"] if p["id"] == "high_income_merit")
    profile = dict(persona["profile"])
    profile["household_income_annual"] = 50_000
    ids = _match_ids(profile, scholarships)
    assert 103 in ids


def test_persona_pr_ids_are_unique_and_present():
    """Every shipped persona maps to Refinement PR ids without collisions (A2)."""
    personas = _load_catalog()["personas"]
    seen: dict[str, str] = {}
    for persona in personas:
        slug = persona["id"]
        pr_ids = persona.get("pr_ids")
        assert pr_ids, f"{slug}: pr_ids must be non-empty (see docs/engineering/persona-id-map.md)"
        assert isinstance(pr_ids, list), f"{slug}: pr_ids must be a list"
        for pr_id in pr_ids:
            assert _PR_ID_PATTERN.match(pr_id), f"{slug}: invalid pr_id {pr_id!r}"
            assert pr_id not in seen, (
                f"PR id {pr_id} claimed by both {seen[pr_id]!r} and {slug!r}"
            )
            seen[pr_id] = slug
    assert len(seen) == len(personas), "each persona must contribute at least one unique PR id"


def test_fixture_catalog_has_minimum_size(catalog):
    assert len(catalog["scholarships"]) >= 40


def test_fixture_catalog_covers_all_restriction_types(catalog):
    """MATCH-01 (B1): every catalog dimension has at least one fixture row."""
    scholarships = catalog["scholarships"]

    application_statuses = {s.get("application_status") for s in scholarships}
    assert APPLICATION_STATUSES <= application_statuses

    assert any(s.get("data_status") == "needs_review" for s in scholarships)

    scholarship_types = {s.get("scholarship_type") for s in scholarships}
    assert {"Need", "Merit-based", "Merit-and-Need"} <= scholarship_types

    assert any(not s.get("eligible_regions") for s in scholarships)
    assert any(s.get("eligible_regions") for s in scholarships)

    assert any(s.get("eligible_schools") for s in scholarships)
    assert any(s.get("eligible_school_types") == ["Public"] for s in scholarships)
    assert any(s.get("eligible_school_types") == ["Private"] for s in scholarships)
    assert any(
        not s.get("eligible_schools")
        and not s.get("eligible_school_systems")
        and (not s.get("eligible_school_types") or len(s["eligible_school_types"]) >= 2)
        for s in scholarships
    )

    assert any(s.get("eligible_courses_psced") for s in scholarships)
    assert any(s.get("eligible_courses_specific") for s in scholarships)

    gwa_scales = {s.get("_gwa_threshold_scale") for s in scholarships if s.get("_gwa_threshold_scale")}
    assert _GWA_THRESHOLD_SCALES <= gwa_scales

    assert any(s.get("max_income_threshold") == 250_000 for s in scholarships)
    assert any(s.get("max_income_threshold") == 400_000 for s in scholarships)
    assert any(s.get("max_income_threshold") == 500_000 for s in scholarships)
    assert any(
        s.get("scholarship_type") == "Merit-based" and s.get("max_income_threshold") in (None, 0)
        for s in scholarships
    )

    priority_labels: set[str] = set()
    for s in scholarships:
        for label in s.get("priority_groups") or []:
            priority_labels.add(label)
    for group in EQUITY_GROUP_IDS:
        assert group in priority_labels, f"missing equity/priority fixture for {group!r}"

    assert any(s.get("members_only") and "GSIS Dependent" in (s.get("priority_groups") or []) for s in scholarships)
    assert any(s.get("members_only") and "SSS Dependent" in (s.get("priority_groups") or []) for s in scholarships)

    assert any(s.get("min_age") is not None for s in scholarships)
    assert any(s.get("max_age") is not None for s in scholarships)
    assert any(s.get("eligible_year_levels") for s in scholarships)
    assert any(s.get("eligible_enrollment_status") for s in scholarships)
    assert any(s.get("application_deadline") for s in scholarships)
    assert any(s.get("citizenship_required") for s in scholarships)

    levels = {level for s in scholarships for level in (s.get("eligible_levels") or [])}
    assert "TVET" in levels
    assert "Graduate" in levels


@pytest.mark.parametrize(
    "persona",
    _load_catalog()["personas"],
    ids=[p["id"] for p in _load_catalog()["personas"]],
)
def test_every_persona_has_all_three_layers(persona):
    """Layers 1–3 must stay non-empty so personas cannot become vacuous (B2)."""
    slug = persona["id"]
    assert persona.get("must_include") or persona.get("must_exclude"), f"{slug}: layer 1 empty"
    assert persona.get("expected_status"), f"{slug}: layer 2 (expected_status) empty"
    assert persona.get("ranking_invariants"), f"{slug}: layer 3 (ranking_invariants) empty"
    golden_path = GOLDEN_DIR / f"{slug}.json"
    assert golden_path.is_file(), f"{slug}: missing golden file"
    golden = json.loads(golden_path.read_text(encoding="utf-8"))
    assert golden.get("ordered_results"), f"{slug}: golden ordered_results empty"


@pytest.mark.parametrize(
    "persona",
    _load_catalog()["personas"],
    ids=[p["id"] for p in _load_catalog()["personas"]],
)
def test_persona_status_expectations(persona, scholarships):
    from app.matching.eligibility_result import evaluate_eligibility

    ranked = _ranked_matches(persona["profile"], scholarships)
    by_id = {int(r["id"]): r for r in ranked}

    for sid_str, expected in (persona.get("expected_status") or {}).items():
        sid = int(sid_str)
        assert sid in by_id, f"{persona['id']}: scholarship {sid} not in ranked matches"
        assert by_id[sid].get("qualification_status") == expected, (
            f"{persona['id']}: ranked status for {sid} expected {expected}, "
            f"got {by_id[sid].get('qualification_status')}"
        )

    sch_by_id = {int(s["id"]): s for s in scholarships}
    for sid_str, expected in (persona.get("expected_detail_status") or {}).items():
        sid = int(sid_str)
        detail = evaluate_eligibility(persona["profile"], sch_by_id[sid]).status.value
        assert detail == expected, (
            f"{persona['id']}: detail eligibility for {sid} expected {expected}, got {detail}"
        )


@pytest.mark.parametrize(
    "persona",
    _load_catalog()["personas"],
    ids=[p["id"] for p in _load_catalog()["personas"]],
)
def test_persona_ranking_invariants(persona, scholarships):
    ranked = _ranked_matches(persona["profile"], scholarships)
    rank_index = {int(r["id"]): idx for idx, r in enumerate(ranked)}

    for inv in persona.get("ranking_invariants") or []:
        above, below = int(inv["above"]), int(inv["below"])
        assert above in rank_index, f"{persona['id']}: invariant above {above} not in results"
        assert below in rank_index, f"{persona['id']}: invariant below {below} not in results"
        assert rank_index[above] < rank_index[below], (
            f"{persona['id']}: expected {above} above {below}; "
            f"indices {rank_index[above]} vs {rank_index[below]}"
        )


@pytest.mark.parametrize(
    "persona",
    _load_catalog()["personas"],
    ids=[p["id"] for p in _load_catalog()["personas"]],
)
def test_persona_goldens_match(persona, scholarships):
    golden_path = GOLDEN_DIR / f"{persona['id']}.json"
    golden = json.loads(golden_path.read_text(encoding="utf-8"))
    actual = _golden_rows(_ranked_matches(persona["profile"], scholarships))
    assert actual == golden["ordered_results"], (
        f"{persona['id']}: golden drift — regenerate with "
        f"python -m app.scripts.regenerate_persona_goldens --persona {persona['id']}"
    )


def test_persona_suite_covers_provisional_and_almost_detail():
    """B2 guardrails: UNKNOWN → provisional in ranked list; almost_qualified on detail path."""
    personas = _load_catalog()["personas"]
    ranked_provisional = any(
        status == "provisionally_qualified"
        for persona in personas
        for status in (persona.get("expected_status") or {}).values()
    )
    detail_almost = any(
        status == "almost_qualified"
        for persona in personas
        for status in (persona.get("expected_detail_status") or {}).values()
    )
    assert ranked_provisional, "expected at least one provisionally_qualified ranked status"
    assert detail_almost, "expected at least one almost_qualified detail status"


@pytest.mark.parametrize(
    "persona",
    _load_catalog()["personas"],
    ids=[p["id"] for p in _load_catalog()["personas"]],
)
def test_every_match_has_explanation(persona, scholarships):
    """MATCH-06 (B3): breakdown, readable reasons, and why_not_higher below a perfect score."""
    for match in _ranked_matches(persona["profile"], scholarships):
        _assert_explanation_quality(persona["id"], match)


@pytest.mark.parametrize(
    "persona",
    _load_catalog()["personas"],
    ids=[p["id"] for p in _load_catalog()["personas"]],
)
def test_provisional_names_unverified_requirement(persona, scholarships):
    """MATCH-06 (B3): provisional rows must name what we could not verify."""
    for match in _ranked_matches(persona["profile"], scholarships):
        if match.get("qualification_status") != "provisionally_qualified":
            continue
        unverified = [u for u in (match.get("unverified_requirements") or []) if str(u).strip()]
        assert unverified, (
            f"{persona['id']}/{match.get('id')}: provisionally_qualified without unverified_requirements"
        )


def test_pr15_gwa_scale_equivalence(scholarships):
    """PR-15: equivalent normalized GWAs across percentage, 5.0, and 4.0 scales."""
    from app.taxonomy.gwa_normalizer import GWA_SCALE_4_0, GWA_SCALE_5_0, GWA_SCALE_PERCENTAGE, normalize_gwa

    base_profile = {
        "age": 19,
        "education_level": "College",
        "region": "National Capital Region",
        "school_type": "Public",
        "household_income_annual": 200_000,
        "field_of_study_broad": "STEM",
        "preferred_courses": [],
    }
    scales = (
        (88, GWA_SCALE_PERCENTAGE),
        (1.48, GWA_SCALE_5_0),
        (3.52, GWA_SCALE_4_0),
    )
    normalized = [normalize_gwa(raw, scale) for raw, scale in scales]
    assert all(n is not None for n in normalized)
    assert max(normalized) - min(normalized) <= 0.5

    match_sets = []
    for (raw, scale), norm in zip(scales, normalized):
        profile = dict(base_profile, gwa_normalized=norm)
        match_sets.append(_match_ids(profile, scholarships))
    assert match_sets[0] == match_sets[1] == match_sets[2]


def test_pr24_region_aliases_produce_identical_matches(scholarships):
    """PR-24: CALABARZON region strings normalize to identical match sets."""
    base = {
        "age": 19,
        "education_level": "College",
        "school_type": "Public",
        "household_income_annual": 200_000,
        "gwa_normalized": 88,
        "field_of_study_broad": "STEM",
        "preferred_courses": [],
    }
    regions = ("CALABARZON", "Region 4A", "Region IV-A - CALABARZON")
    sets = [_match_ids({**base, "region": r}, scholarships) for r in regions]
    assert sets[0] == sets[1] == sets[2]


def test_pr41_over_constrained_never_empty(scholarships):
    """PR-41: over-constrained profiles return near-misses, never an empty list."""
    persona = next(p for p in _load_catalog()["personas"] if p["id"] == "over_constrained_near_miss")
    results = _ranked_matches(persona["profile"], scholarships)
    assert results, "over-constrained profile must not yield an empty match list"
    for match in results:
        assert _human_readable_lines(match), f"near-miss {match.get('id')} lacks explanation"
