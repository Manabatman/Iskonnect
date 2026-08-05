# ADR-007: Candidate prefiltering for `/plan`



**Status:** Proposed (decision gate recorded — flag **not** enabled)  

**Date:** 2026-07-31  

**Updated:** 2026-08-01 (B13 evidence)  

**Task:** PERF-07



## Context



The `/plan` match endpoint evaluates eligibility against the catalog. At 300+ listings, Python-side filtering becomes a latency bottleneck.



## Decision



**Ship SQL prefilter behind feature flag, default off.** Enable only when all three criteria are evidenced in production-like conditions.



## Decision gate (B13 — 2026-08-01)



| Criterion | Required | Evidence | Met? |

| --- | --- | --- | --- |

| 1. MATCH-08 parity SQLite + Postgres | Same outcomes prefilter on/off | `test_plan_prefilter_parity.py` green in CI (A6); Postgres job on `migrate-postgres` | **Yes** |

| 2. Eval + persona green both modes | No regression with flag on | `PLAN_PREFILTER_ENABLED=true`: eval regression 4/4 pass; parity 3/3 pass (2 Postgres skipped locally without URL) | **Yes** |

| 3. p95 warm `/plan` match core ≤800 ms | Part XII budget | `measure_plan_prefilter.py` @ 117 active / 38 publishable: publishable p95 **3.9 ms** (full) / **4.0 ms** (prefilter); all-active p95 **11.3 ms** — see `reports/b13-plan-prefilter-bench.json` | **Yes at current scale** |



**Flag status:** `PLAN_PREFILTER_ENABLED` remains **`false`** (default). B13 records evidence only; production flip requires explicit approval after **300-listing scale** re-measurement and HTTP-level `/plan` p95 (not match-core only).



## Consequences



- Two code paths until flag default changes — parity tests remain mandatory.

- Index work (PERF-14) may be required at 300+ publishable rows.

- Re-benchmark with `python -m app.scripts.measure_plan_prefilter` after each major catalog import.



## References



- `app/api/v1/matches.py` — `_prefilter_scholarships_query`, `_scholarship_dicts_for_profile`

- `app/scripts/measure_plan_prefilter.py` — B13 benchmark

- `app/tests/test_plan_prefilter_parity.py` — MATCH-08

- `docs/engineering/perf-baseline.md` — measurement log

- `docs/engineering/reports/b13-plan-prefilter-bench.json`

