# Lesson 12 — Scoring Engine Internals

> **Prerequisite:** [11 — Matching Engine Architecture](11-matching-engine-architecture.md)

---

## Concept: Deterministic scoring

### 1. Definition

**Deterministic:** Same inputs → same score, every time. No randomness, no ML black box.

### 2. Why for Iskonnect

Students must **trust** explanations. "Why did I rank #3?" must be answerable from breakdown text.

### 3. Problem solved

**Transparency** for policy-aware scholarships (merit + need + equity).

### 4. Alternatives

ML ranker (higher accuracy potential, lower explainability). Iskonnect chose explainable rules first.

---

## Module map

| File | Role |
|------|------|
| [`engine.py`](../../../app/scoring/engine.py) | `WeightedDeterministicScorer` — orchestrates components |
| [`components.py`](../../../app/scoring/components.py) | Individual score factors (GWA, income, field, geo, equity) |
| [`config.py`](../../../app/scoring/config.py) | Weights, thresholds, policy version string |
| [`explanation.py`](../../../app/scoring/explanation.py) | Human-readable strings, `why_not_higher`, suggestions |

See also [`SCORING_ENGINE.md`](../../../SCORING_ENGINE.md) for design notes.

---

## ScoringPayload → ScoringResult

Input highlights ([`scoring_port.py`](../../../app/matching/scoring_port.py)):

- `gwa_normalized`, `household_income_annual`, `income_bracket`
- `field_match_level`: exact | broad | partial | none
- `geographic_match_level`: city | region | island_group | none
- `equity_flags`: dict of boolean policy flags
- Scholarship requirements: `min_gwa_required`, `max_income_threshold`, `priority_groups`

Output:

- `final_score` (0–100 scale)
- `breakdown` dict per component
- `explanation[]` bullet strings
- `confidence`: high | medium | low (data completeness)
- `suggestions[]` — how to improve eligibility
- `why_not_higher[]` — near-miss transparency

---

## Weighted matrix

[`config.py`](../../../app/scoring/config.py) defines weights summing to policy (e.g. merit vs need vs alignment). Changing weights bumps `scoring_policy_version` for audit.

**Document readiness** is tracked separately — **not** part of eligibility fit score (README principle).

---

## Field match levels

Computed in `match_service._get_field_match_level()` using [`FIELD_HIERARCHY`](../../../app/taxonomy/psced_fields.py) — e.g. Engineering student matches STEM-eligible scholarship as "broad".

---

## Confidence

Low profile completeness → `confidence: low` — honest about weak data (missing GWA, income).

**Senior evaluation:** Better to say "low confidence" than fake precision.

---

## Deprecated shims

`compute_equity_multiplier`, `score_readiness` — compatibility shims marked deprecated. Tests may still reference — know before deleting.

---

## Exercises

### Level 1 — Understanding

1. Why is document readiness excluded from fit score?
2. What four field match levels exist?

### Level 2 — Implementation

1. Read one `explanation.py` builder function — list inputs it uses.

### Level 3 — Debugging

1. Two students same GWA, different scores — trace `breakdown` diff in API response.

### Level 4 — Architecture

1. Stakeholder wants equity to count double. Which files change? What tests run?

<details>
<summary>Solution</summary>

Documents are application logistics, not eligibility for discovery. Field levels: exact, broad, partial, none. Change weights in config.py, bump policy version, run test_scoring_engine.py and integration match tests.
</details>

---

*Previous: [11 — Matching Engine](11-matching-engine-architecture.md) | Next: [13 — Domain Taxonomies](13-domain-taxonomies.md)*
