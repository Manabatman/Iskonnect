"""
Scoring engine interface contract.

Defines WHAT the scoring engine receives and returns — not the scoring formula.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ScoringPayload:
    """Inputs required by the weighted deterministic scoring engine."""

    gwa_normalized: float | None
    household_income_annual: int | None
    income_bracket: str | None
    field_match_level: str  # exact | sibling | discipline | partial | none (+ legacy broad)
    geographic_match_level: str  # city | region | island_group | none
    equity_flags: dict[str, bool]

    scholarship_type: str
    min_gwa_required: float | None
    max_income_threshold: int | None
    priority_groups: list[str]

    profile_region: str | None = None
    profile_city: str | None = None
    eligible_regions: list | None = None
    eligible_cities: list | None = None
    has_geographic_restriction: bool = True
    has_field_restriction: bool = True
    is_provisional: bool = False


@dataclass
class ScoringResult:
    """Structured output from a single student–scholarship scoring pass."""

    final_score: float
    eligibility_status: bool
    breakdown: dict
    explanation: list[str]
    readiness_score: float
    confidence: str  # high | medium | low
    suggestions: list[str] = field(default_factory=list)
    why_not_higher: list[str] = field(default_factory=list)
    scoring_policy_version: str = ""


class ScoringEnginePort(ABC):
    """Interface that scoring engine implementations must satisfy."""

    @abstractmethod
    def score(self, payload: ScoringPayload) -> ScoringResult:
        """Score a single student-scholarship pair."""
        ...
