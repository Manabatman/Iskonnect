# P1-01 Report

## Objective

Instrument login and dashboard waterfall with `Server-Timing` (backend) and `performance.mark`/`measure` (frontend); document capture in `perf-baseline.md`.

## Files changed

- `app/utils/server_timing.py` — new
- `app/tests/test_server_timing.py` — new
- `app/middleware/request_logger.py` — `wall;dur` on every response
- `app/api/v1/auth_routes.py` — login phase timing
- `frontend/src/utils/perfTiming.ts` — new
- `frontend/src/utils/perfTiming.test.ts` — new
- `frontend/src/api/client.ts` — dev Server-Timing log
- `frontend/src/contexts/AuthContext.tsx` — auth-me timing marks
- `frontend/src/pages/LoginPage.tsx` — submit mark
- `frontend/src/pages/ProfileDashboard.tsx` — dashboard data/matches marks
- `docs/engineering/perf-baseline.md` — methodology
- `docs/engineering/reports/README.md` — new
- `docs/engineering/ISKONNECT_PRODUCT_REFINEMENT_MASTER_PLAN.md` — §6.6–6.7

## Before

No structured login waterfall; no `Server-Timing` on auth routes.

## After

- `POST /login` exposes `db-lookup`, `bcrypt`, `token-issue`, `wall`
- Client marks: `submit` → `login-response` → `auth-me-*` → `dashboard-data` → `dashboard-matches`
- Dev: `window.__iskonnectLogLoginWaterfall()` prints a table

## Performance

Fill baseline tables in `perf-baseline.md` after local sign-in run.

## Tests

- [x] `pytest app/tests/test_server_timing.py` (3 passed)
- [x] `npm run typecheck`
- [x] `npm run test` (perfTiming tests pass; 1 pre-existing profileBuilderState failure unrelated)
- [x] `npm run lint` (no new errors in changed files)
- [ ] E2E — N/A until AUDIT-13

## Regression risk

**Low** — additive instrumentation only.

## Rollback

Revert this commit; no migrations.

## Follow-ups

- P1-03 — remove `/auth/me` on login path
- P1-07 — skeletons at dashboard shell
