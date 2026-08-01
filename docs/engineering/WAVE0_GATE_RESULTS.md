# Wave 0 — Gate Results and Freeze Record

> **Date:** 2026-08-01  
> **Pre-checkpoint SHA:** `009238c60c2d4d478c4646370e08a47e8008f826`  
> **Branch created:** `feature/design-system-v1`  
> **Purpose:** Record gate status before design-system implementation waves.

---

## Freeze summary

- Single checkpoint commit captures Phase 3 (M0–M8), C4–C5 landing work, and the `docs/design/` specification suite.
- Hero source JPGs extracted from `009238c` to `frontend/.hero-sources/` (gitignored, not shipped).
- Design documents in `docs/design/` are the source of truth for Waves 1–9.

---

## Frontend gates

| Gate | Command | Result | Notes |
| --- | --- | --- | --- |
| Lint | `npm run lint` | **FAIL** | 3 errors, 26 warnings |
| Typecheck | `npm run typecheck` | **FAIL** | See errors below |
| Unit tests | `npm run test` | **FAIL** | 69 passed, 1 failed |
| Build | `npm run build` | **PASS** | Vite production build OK |
| Bundle budget | `npm run audit:bundle-budget` | **PASS** | entry 45.2 KB, vendor 108.9 KB gzip |
| Design tokens | `npm run audit:design-tokens` | **PASS** | DS-17 guarded paths clean |

### Lint errors (must fix in later waves)

| File | Issue |
| --- | --- |
| `FieldOfStudyStep.test.tsx:2` | Unused import `screen` |
| `useScholarshipSearch.ts:102` | Unused variable `err` |
| `ScholarshipDetailPage.tsx:16` | Unused import `ERROR_COPY` |

### Typecheck errors

| File | Issue |
| --- | --- |
| `FieldOfStudyStep.test.tsx:16` | Partial `ProfileBuilderState` in test fixture |
| `copyLint.test.ts` | Missing `@types/node` for `node:fs`, `node:path`, `process` |
| `trackOutboundClick.test.ts:23` | Tuple type assertion |

### Failing unit test

| Test | Issue |
| --- | --- |
| `ScholarshipCardV2.test.tsx` | `getByText("Needs verification")` finds multiple elements (badge + freshness chip) |

---

## Backend gates

| Gate | Command | Result | Notes |
| --- | --- | --- | --- |
| Pytest (full) | `python -m pytest app/tests/ -q` | **INCOMPLETE** | Full suite exceeded 13 min in this environment; re-run locally before Wave 1 |

Re-run before Wave 1:

```bash
python -m pytest app/tests/ -q
```

---

## Pre-existing failures — do not block Wave 0

These failures exist at checkpoint time. Wave 1 is additive-only and should not introduce new failures. Fix lint/typecheck/test regressions in the wave that touches each file, or in a dedicated cleanup commit before CI hard-gates.

---

## Hero source extraction

| File | Size | Dimensions | Aspect |
| --- | ---: | --- | --- |
| `hero-1-source.jpg` | 1,928,158 B | 5184×3456 | 3:2 |
| `hero-2-source.jpg` | 1,783,356 B | 6720×4480 | 3:2 |
| `hero-3-source.jpg` | 1,150,361 B | 5263×3509 | 3:2 |

Location: `frontend/.hero-sources/` (gitignored).

Crop assessment: [WAVE0_HERO_SOURCE_ASSESSMENT.md](../design/WAVE0_HERO_SOURCE_ASSESSMENT.md)

---

## Wave 3 reference

Pre-checkpoint SHA for hero recovery: **`009238c`**. If hero sources are lost, re-extract with:

```bash
git show 009238c:frontend/public/images/hero/hero-1.jpg > frontend/.hero-sources/hero-1-source.jpg
```

---

## Document history

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-01 | Initial Wave 0 gate record |
