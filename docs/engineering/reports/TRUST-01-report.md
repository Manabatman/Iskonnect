# TRUST-01 — Profile draft preserved across registration

**Status:** Shipped  
**Date:** 2026-07-31

## Changes

- `AuthContext`: clear draft only on logout or when switching from user A to user B; anonymous → authenticated keeps local draft.
- `ProfileBuilderPage`: skip reset on anonymous → auth; merge server profile with local draft via `mergeProfileDrafts`.
- `profileBuilderState.mergeProfileDrafts`: server values win when both present.

## Verification

- Vitest: `scholarshipStatus.test.ts`, `profileBuilderState.test.ts`
- Manual: fill fields anonymously → register → fields intact
