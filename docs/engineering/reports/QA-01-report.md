# QA-01 — Real backend in CI

**Status:** Shipped  
**Date:** 2026-07-31

## Changes

- Added `app/scripts/seed_ci_e2e.py` — deterministic E2E user and catalog rows.
- Added `.github/workflows/ci.yml` `e2e` job: Postgres, migrate, seed, uvicorn, preview build, Playwright smoke + axe.

## Verification

- Local: `python -m app.scripts.seed_ci_e2e` after `alembic upgrade head`
- CI: `e2e` job on push/PR to `main`
