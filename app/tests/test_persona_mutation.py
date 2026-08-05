"""MATCH-05 (B4): config weight perturbations must break ranking invariants."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.matching.match_service import MatchService
from app.scoring.config import ScoringConfig, _default_weights
from app.scoring.engine import WeightedDeterministicScorer

FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "persona_catalog.json"
WEIGHT_KEYS = tuple(_default_weights().keys())


def _load_catalog() -> dict:
    with FIXTURE_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def _rank_index(profile: dict, scholarships: list[dict], weights: dict[str, float]) -> dict[int, int]:
    cfg = ScoringConfig()
    cfg.weights = dict(weights)
    service = MatchService(scoring_engine=WeightedDeterministicScorer(cfg))
    results, _ = service.get_matches(profile, scholarships)
    return {int(r["id"]): idx for idx, r in enumerate(results)}


def _broken_invariant_count(
    personas: list[dict],
    scholarships: list[dict],
    weights: dict[str, float],
) -> int:
    broken = 0
    for persona in personas:
        rank = _rank_index(persona["profile"], scholarships, weights)
        for inv in persona.get("ranking_invariants") or []:
            above, below = int(inv["above"]), int(inv["below"])
            if above not in rank or below not in rank:
                continue
            if rank[above] >= rank[below]:
                broken += 1
    return broken


def _zero_weight(weights: dict[str, float], key: str) -> dict[str, float]:
    w = dict(weights)
    w[key] = 0.0
    total = sum(w.values())
    if total <= 0:
        return w
    return {k: v / total for k, v in w.items()}


def _invert_weight(weights: dict[str, float], key: str) -> dict[str, float]:
    """Collapse importance onto the strongest non-key component."""
    w = dict(weights)
    dominant = max((k for k in w if k != key), key=lambda k: w[k])
    w[key] = 0.02
    w[dominant] = 0.88
    remaining = [k for k in w if k not in (key, dominant)]
    share = 0.10 / len(remaining)
    for other in remaining:
        w[other] = share
    return w


def _dominant_weight(weights: dict[str, float], key: str) -> dict[str, float]:
    """Single-weight dominance — second perturbation when invert/swap is too subtle."""
    w = {k: 0.01 for k in weights}
    w[key] = 0.96
    return w


@pytest.fixture(scope="module")
def catalog():
    return _load_catalog()


@pytest.fixture(scope="module")
def scholarships(catalog):
    return catalog["scholarships"]


@pytest.fixture(scope="module")
def personas(catalog):
    return [p for p in catalog["personas"] if p.get("ranking_invariants")]


def _assert_perturbation_breaks_invariant(
    weight_key: str,
    personas: list[dict],
    scholarships: list[dict],
) -> None:
    base = _default_weights()
    perturbations = (
        ("zero", _zero_weight(base, weight_key)),
        ("invert", _invert_weight(base, weight_key)),
        ("dominant", _dominant_weight(base, weight_key)),
    )
    for name, weights in perturbations:
        if _broken_invariant_count(personas, scholarships, weights) > 0:
            return
    pytest.fail(
        f"weight {weight_key!r}: zero, invert, and dominant perturbations left all "
        f"ranking invariants intact — layer 3 is decorative for this component"
    )


@pytest.mark.parametrize("weight_key", WEIGHT_KEYS)
def test_weight_perturbation_breaks_ranking_invariant(weight_key, personas, scholarships):
    """Zeroing or inverting any single scoring weight must break at least one ordering invariant."""
    _assert_perturbation_breaks_invariant(weight_key, personas, scholarships)
