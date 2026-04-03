"""
Scoring engine configuration.
Weights and equity multipliers are adjustable without rewriting scoring logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy.orm import Session


def _default_weights() -> dict[str, float]:
    # Document readiness removed from scoring (M4) - displayed on detail page only
    return {
        "academic": 0.30,
        "income": 0.28,
        "field_alignment": 0.22,
        "geographic": 0.10,
        "equity_priority": 0.10,
    }


def _default_equity_multipliers() -> dict[str, float]:
    """Deprecated: kept for config compatibility; scoring no longer applies post-hoc equity multipliers."""
    return {
        "is_pwd": 1.08,
        "is_indigenous_people": 1.10,
        "is_solo_parent_dependent": 1.05,
        "is_4ps_listahanan": 1.07,
        "is_underprivileged": 1.06,
        "is_ofw_dependent": 1.03,
        "is_farmer_fisher_dependent": 1.04,
    }


def _default_income_bracket_midpoints() -> dict[str, int]:
    return {
        "below_250k": 125_000,
        "250k_400k": 325_000,
        "400k_500k": 450_000,
        "above_500k": 600_000,
    }


@dataclass
class ScoringConfig:
    """
    Configuration for the weighted deterministic scoring engine.
    Weights must sum to 1.0.

    equity_multipliers and max_equity_multiplier are deprecated (unused by the engine);
    equity is reflected only in the equity_priority weighted component.
    """

    policy_version: str = "v1.1"
    weights: dict[str, float] = field(default_factory=_default_weights)
    equity_multipliers: dict[str, float] = field(default_factory=_default_equity_multipliers)
    max_equity_multiplier: float = 1.15  # deprecated, unused
    income_bracket_midpoints: dict[str, int] = field(default_factory=_default_income_bracket_midpoints)

    @classmethod
    def from_db(cls, db: Session) -> ScoringConfig:
        """Load component weights from `scoring_weights` table; fall back to defaults on any error."""
        cfg = cls()
        try:
            from app import models

            rows = db.query(models.ScoringWeight).all()
        except Exception:
            return cls()
        if not rows:
            return cls()
        wmap = {r.component: float(r.weight) for r in rows}
        for key in list(cfg.weights.keys()):
            if key in wmap:
                cfg.weights[key] = wmap[key]
        return cfg
