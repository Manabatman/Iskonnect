"""
Weighted deterministic scoring engine.
Implements ScoringEnginePort with configurable weights.
"""

from app.matching.scoring_port import ScoringEnginePort, ScoringPayload, ScoringResult
from app.scoring.components import (
    score_academic,
    score_equity,
    score_field,
    score_geographic,
    score_income,
)
from app.scoring.config import ScoringConfig
from app.scoring.explanation import (
    assess_confidence,
    build_breakdown,
    build_explanation,
    build_improvement_suggestions,
    build_why_not_higher,
)


class WeightedDeterministicScorer(ScoringEnginePort):
    """
    Deterministic weighted scoring engine.
    Same input -> same output. Every component is explainable.
    """

    def __init__(self, config: ScoringConfig | None = None):
        self.config = config or ScoringConfig()

    @staticmethod
    def _normalized_weights(payload: ScoringPayload, weights: dict[str, float]) -> dict[str, float]:
        """Zero out non-applicable factors and renormalize so applicable weights sum to 1.0."""
        w = {k: float(v) for k, v in weights.items()}
        if not payload.has_geographic_restriction:
            w["geographic"] = 0.0
        if not payload.has_field_restriction:
            w["field_alignment"] = 0.0
        total = sum(w.values())
        if total <= 0:
            n = max(len(w), 1)
            return {k: 1.0 / n for k in w}
        return {k: v / total for k, v in w.items()}

    def score(self, payload: ScoringPayload) -> ScoringResult:
        # 1. Compute each component (0.0 - 1.0)
        components = {
            "academic": score_academic(
                payload.gwa_normalized,
                payload.min_gwa_required,
            ),
            "income": score_income(
                payload.household_income_annual,
                payload.income_bracket,
                payload.max_income_threshold,
                payload.scholarship_type or "",
                self.config.income_bracket_midpoints,
            ),
            "field_alignment": score_field(payload.field_match_level),
            "geographic": score_geographic(payload.geographic_match_level),
            "equity_priority": score_equity(
                payload.equity_flags,
                payload.priority_groups,
            ),
        }

        norm = self._normalized_weights(payload, self.config.weights)

        # 2. Weighted sum -> base score (0-100)
        base_score = sum(components[key] * norm[key] for key in components) * 100

        # 3. Clamp to 0-100 (equity is only in equity_priority component, no post-hoc multiplier)
        final_score = max(0.0, min(100.0, base_score))

        breakdown = build_breakdown(components, payload, norm)
        explanation = build_explanation(components, payload)
        confidence = assess_confidence(payload)
        suggestions = build_improvement_suggestions(components, payload)
        why_not_higher = build_why_not_higher(components, payload, norm)

        return ScoringResult(
            final_score=round(final_score, 2),
            eligibility_status=True,
            breakdown=breakdown,
            explanation=explanation,
            readiness_score=0.0,  # No longer used in scoring; documents shown on detail page only
            confidence=confidence,
            suggestions=suggestions,
            why_not_higher=why_not_higher,
            scoring_policy_version=self.config.policy_version,
        )
