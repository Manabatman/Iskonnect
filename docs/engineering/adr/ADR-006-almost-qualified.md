# ADR-006: Implement `almost_qualified` eligibility state

**Status:** Accepted  
**Date:** 2026-07-31  
**Task:** MATCH-04

## Context

`QualificationStatus.ALMOST_QUALIFIED` existed in the API contract, TypeScript types, and UI badge component but was never returned by `_derive_status`. This dead state wasted the most actionable UX moment: telling a student they are one achievable requirement away from qualifying.

## Decision

**Implement** `almost_qualified` rather than remove it.

Definition: exactly **one** applicable requirement is `UNMET`, and that requirement's key is **achievable** (the student can close the gap):

| Achievable keys | Rationale |
| --- | --- |
| `gwa` | Student can raise grades |
| `education_level` | Student may advance to required level |
| `year_level` | Student advances year-over-year |
| `enrollment_status` | Status may change next term |
| `field` | Student may change course alignment |

**Not achievable:** `income` is intentionally excluded from this set. When household income exceeds a scholarship ceiling, the student is `not_eligible` even if income is the only unmet requirement — see `_ACHIEVABLE_UNMET_KEYS` in `app/matching/eligibility_result.py:71-73` and `test_income_bracket_over_ceiling_not_eligible` in `app/tests/test_eligibility_contract.py`. Treating income as "one requirement away" would mislead students about need-based gates.

Immutable failures (region, citizenship, school, members-only, age over max, **income over ceiling**, etc.) remain `not_eligible` even when only one requirement fails.

Evaluation order in `_derive_status`:

1. Single achievable `UNMET` → `almost_qualified`
2. Any other `UNMET` → `not_eligible`
3. Any `UNKNOWN` → `provisionally_qualified`
4. Otherwise existing provisional/qualified logic

`passes_for_matching` remains limited to `qualified` and `provisionally_qualified`. Almost-qualified pairs are surfaced on detail/timeline surfaces, not in the ranked match list.

## Consequences

- Students see a honest "one requirement away" signal instead of a silent exclusion or false qualified state.
- Persona and eval suites must assert the almost / not-eligible boundary per requirement class.
- Future work: group almost-qualified matches separately on the dashboard (Phase 4 UI polish).

## Alternatives considered

- **Remove the state everywhere** — simpler schema but loses high-value UX; rejected per product brief.
