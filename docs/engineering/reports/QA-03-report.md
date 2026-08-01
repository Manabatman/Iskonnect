# QA-03 — Frontend coverage ratchet

**Task:** QA-03 (Phase 3 M1)  
**Ratcheted:** 2026-08-01 (Track A, milestone A8)  
**Command:** `cd frontend && npm test -- --coverage`

## Measured baseline (2026-08-01)

| Metric | Measured | Threshold (floor) |
| --- | ---: | ---: |
| Statements | 14.81% | **14** |
| Lines | 14.81% | **14** |
| Functions | 30.31% | **30** |
| Branches | 42.37% | **42** |

Suite at measurement: **15** test files, **43** tests (all green).

Configuration: `frontend/vite.config.ts` → `test.coverage.thresholds`.

Backend baseline (separate gate): pytest `--cov-fail-under=70` in `pytest.ini` (71.42% measured at Phase 3 exit).

## Enforcement

CI runs `npm test -- --coverage` in the `frontend` job (`.github/workflows/ci.yml`). Any decrease below the floored thresholds fails the build.

## Override procedure (R-15 §22 — coverage ratchet)

Use only when an urgent fix would otherwise be blocked **and** adding tests in the same PR is infeasible.

1. **Single PR only** — temporarily lower one or more thresholds in `vite.config.ts`.
2. **PR description must state:**
   - Why tests could not land in the same PR
   - The follow-up milestone or issue that will restore coverage (with owner)
   - The re-measured baseline target after follow-up
3. **If the baseline permanently changes** (e.g. new untested surface merged intentionally), re-run `npm test -- --coverage`, floor the new numbers, and add an [Appendix G](../PROJECT_HANDOFF_PHASE1_TO_PHASE3.md#appendix-g-decision-log) entry with date and measured values.
4. **Do not** disable coverage in CI or skip the frontend job without the same written follow-up.

Same discipline as other CI guards (A4): allowlist/escape hatches require justification in the PR and handoff when they become permanent.

## Re-baseline checklist

When raising the floor after adding tests:

```bash
cd frontend
npm test -- --coverage
```

Update `vite.config.ts` thresholds to the new floored percentages and this report’s table. Add an Appendix G row if the floor increases by more than 2 points on any metric.
