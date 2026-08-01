# ADR-005: React Query adoption

**Status:** Proposed  
**Date:** 2026-07-31  
**Task:** PERF-06a

## Context

Dashboard and search pages fetch data in nested `useEffect` chains (waterfall). React Query would dedupe, cache, and simplify loading/error states.

## Decision

**Pending measurement.** PERF-06a must record before/after waterfall timing. Adoption requires:

1. Documented p95 improvement on `/dashboard` and `/scholarships/search`
2. No regression in auth-sensitive cache invalidation
3. Bundle budget headroom after `@tanstack/react-query` add

If measurement does not justify the dependency, **reject** and use targeted prefetch + optimistic shell (PERF-03, PERF-05) instead.

## Consequences

- Placeholder until PERF-06a completes.
- Rejection means continued manual fetch patterns with PERF-06 collapse work.

## References

- Phase 3 master plan PERF-06, PERF-06a
- `ProfileDashboard.tsx`, `ScholarshipSearchPage.tsx`
