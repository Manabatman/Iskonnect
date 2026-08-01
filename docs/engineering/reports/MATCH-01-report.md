# MATCH-01 Report — Provisional eligibility disclosure

## Objective

Disclose which requirements are unverified when a match is `provisionally_qualified`.

## Changes

- `EligibilityResult` derives `unverified_requirements` and `provisional_reason` from `UNKNOWN` checks.
- Match API payloads include both fields (`match_service.py`, `schemas.py`, serialization keys).
- `build_explanation` skips the confident “you meet the listed requirements” fallback when provisional.
- Frontend `ScholarshipCardV2` and `MatchAnalysisModal` render `UnverifiedRequirementsList` with profile-builder links.

## Verification

- `test_citizenship_missing_is_unknown` asserts citizenship UNKNOWN propagates to unverified list.
- Persona suite (`test_persona_matching.py`) — run after implementation.

## Notes

Provisional matches now lead with “We could not verify: …” in explanations. This is intentional accuracy, not a regression.
