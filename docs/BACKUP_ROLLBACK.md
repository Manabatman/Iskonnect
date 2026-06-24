# Supabase Backup, PITR, and Rollback Runbook

## Overview

Iskonnect production data lives in **Supabase Postgres**. This runbook covers backups, point-in-time recovery (PITR), and safe rollback after a bad deploy or migration.

## Daily backups (Supabase)

1. Open **Supabase Dashboard → Project → Database → Backups**.
2. Confirm **daily backups** are enabled on your plan.
3. For production, enable **Point-in-Time Recovery (PITR)** if available (Pro plan+).
4. Note your **recovery window** (e.g. 7 days) in your team wiki.

## Before risky changes

- [ ] Take a manual backup or confirm a recent automatic backup exists.
- [ ] Run `alembic upgrade head` on a staging database first.
- [ ] Deploy backend with `release: alembic upgrade head` (Procfile / Railway `releaseCommand`).
- [ ] Keep `RUN_MIGRATIONS_ON_STARTUP=false` in production.

## Rollback: application only (no schema change)

1. Redeploy the previous backend/frontend build in Render/Railway/Vercel.
2. Verify `/health` returns `status: ok` and `/ready` returns `ready`.
3. Smoke-test login, match run, and scholarship search.

## Rollback: bad migration

1. **Stop** new traffic (maintenance mode or scale API to 0).
2. In Supabase, use **PITR** or restore from backup to a **new** database branch/instance if the migration corrupted data.
3. Update `DATABASE_URL` to the restored instance only after verification.
4. Fix the migration locally; test `alembic upgrade` + `alembic downgrade` on a copy.
5. Redeploy with corrected migration chain.

## Rollback: `alembic downgrade` (safe, reversible migrations only)

```bash
cd scholarship-match
alembic downgrade -1   # one revision back
# or
alembic downgrade <revision_id>
```

Only use when the downgrade script is tested and no irreversible data transforms ran.

## Verify after recovery

```bash
curl -s https://YOUR_API/health | jq .
curl -s https://YOUR_API/ready | jq .
pytest app/tests/   # against staging DB
```

## Scheduled maintenance jobs

| Job | Schedule | Workflow |
|-----|----------|----------|
| Deadline / catalog maintenance | Daily | `.github/workflows/deadline-maintenance.yml` |
| Scraper + ingest | Mon/Thu | `.github/workflows/scraper.yml` |
| Retention scan | Weekly | `.github/workflows/retention-cleanup.yml` |
