# Scoring Engine Documentation

## Scoring Philosophy

**What the score represents:** Eligibility Fitness — a 0–100 measure of how strongly a student's profile aligns with a specific scholarship's criteria, preferences, and priorities. It is NOT a probability, NOT a recommendation confidence, and NOT a competitiveness rank against other students.

**Why weighted scoring:** Each scholarship values different dimensions (merit vs. need vs. field priority). A weighted model lets the system express these priorities as adjustable numbers rather than hard-coded logic. This mirrors how FAFSA EFC, UK Student Finance, and Canadian grant systems work.

**Why NOT machine learning:**
- No training data exists (no historical application outcomes)
- Policy compliance requires deterministic, auditable logic
- Every score component must be explainable to the student in plain language
- CHED/LGU partners demand documented, reproducible ranking criteria
- ML introduces algorithmic bias risk unacceptable in public-benefit infrastructure

**Equity handling philosophy:** Equity groups (PWD, IP, Solo Parent, 4Ps) are reflected in the **Equity Priority** weighted component (10% of the base score) when a scholarship names priority groups. They never override hard eligibility gates.

**Document readiness:** Application document completeness is **not** part of the eligibility fitness score. It is shown separately on scholarship detail and document pages so students can prepare to apply without conflating “fit” with “paperwork done.”

---

## Component Breakdown

| Component | Weight | Purpose |
|-----------|--------|---------|
| Academic Strength | 30% | How well GWA meets/exceeds scholarship minimum |
| Income Alignment | 28% | Need-based fit (lower income = higher score for need scholarships) |
| Field Alignment | 22% | PSCED-aligned course/discipline match quality |
| Geographic Relevance | 10% | Location proximity for LGU and regional scholarships |
| Equity Priority | 10% | Alignment with scholarship priority groups (PWD, IP, etc.) |

Weights sum to 100%. Factors that do not apply to a scholarship (e.g. nationwide with no region list, open to all fields) are excluded and remaining weights are renormalized.

---

## Formula Explanation

### Base Score

```
base_score = sum(component_i × normalized_weight_i) × 100
```

Each component returns a value from 0.0 to 1.0 (or is omitted when not applicable). Applicable weights are renormalized to sum to 1.0 before the weighted sum. The result is scaled to 0–100.

### Final Score

```
final_score = clamp(0, 100, base_score)
```

(Equity is included only via the **Equity Priority** component, not a separate post-hoc multiplier.)

### Component Formulas

**Academic (0.0–1.0):**
- No GWA data → 0.3 (provisional; confidence lowered)
- Meets minimum exactly → 0.75
- Exceeds by 10+ points → 1.0
- Below minimum → 0.25 (defensive; normally filtered before scoring)

**Income (0.0–1.0):**
- Merit-based scholarship → 0.5 (neutral)
- Need-based: `0.3 + 0.7 × (1.0 - income/max_threshold)` clamped to [0,1] (eligible at ceiling retains non-zero contribution)
- No income data → 0.3 (provisional)

**Field (0.0–1.0):**
- exact → 1.0, broad → 0.75, partial → 0.4, none → 0.0
- Not scored when scholarship has no field restrictions (factor excluded; weights renormalized)

**Geographic (0.0–1.0):**
- city → 1.0, region → 0.75, island_group → 0.4, none → 0.0
- Not scored when scholarship has no geographic restrictions (factor excluded; weights renormalized)

**Equity (0.0–1.0):**
- 2+ priority group matches → 1.0
- 1 match → 0.75
- 0 matches, no priority groups → 0.5
- 0 matches, scholarship has priority groups → 0.0

---

## Configuration Structure

```python
from app.scoring import WeightedDeterministicScorer, ScoringConfig

config = ScoringConfig(
    weights={
        "academic": 0.30,
        "income": 0.28,
        "field_alignment": 0.22,
        "geographic": 0.10,
        "equity_priority": 0.10,
    },
    # equity_multipliers / max_equity_multiplier: deprecated, unused in scoring (kept for compatibility)
    income_bracket_midpoints={
        "below_250k": 125_000,
        "250k_400k": 325_000,
        "400k_500k": 450_000,
        "above_500k": 600_000,
    },
)

scorer = WeightedDeterministicScorer(config=config)
```

**To adjust weights:** Modify the `weights` dict. Ensure weights sum to 1.0. No code changes required.

---

## Example Scoring Walkthrough

**Student profile:**
- GWA: 88% (normalized)
- Income: PHP 180,000
- Field: Engineering
- Region: NCR
- PWD: Yes

**Scholarship:**
- Min GWA: 75%
- Max income: PHP 250,000
- Eligible courses: Engineering
- Eligible regions: NCR
- Priority groups: PWD

**Component scores:**
- Academic: 1.0 (exceeds min by 13 points)
- Income: 0.796 (0.3 + 0.7 × (1 − 180k/250k))
- Field: 1.0 (exact match)
- Geographic: 0.75 (region match)
- Equity: 0.75 (1 priority group match)

**Base score:**
(1.0×0.30 + 0.796×0.28 + 1.0×0.22 + 0.75×0.10 + 0.75×0.10) × 100 ≈ 86.99

**Final score:** clamped to 0–100 ≈ **87.0**

---

## Inline Code Documentation Guidelines

**Where comments must exist:**
- At the top of each module: purpose and scope
- For each scoring component function: input/output semantics and edge cases
- For config fields: meaning and valid ranges

**What must be documented:**
- How missing data is handled (GWA, income)
- How scholarship type affects income scoring (merit vs need)
- How equity flags map to priority groups
- When geographic/field factors are excluded (not applicable)

**How to modify weights safely:**
1. Edit `ScoringConfig` or pass a custom config to `WeightedDeterministicScorer`
2. Ensure weights sum to 1.0
3. Run `pytest app/tests/test_scoring_engine.py` to verify
4. Document the change and rationale in this file or a changelog
