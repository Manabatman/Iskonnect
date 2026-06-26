# Deployment checklist (manual verification)

Use this after deploying frontend (**Vercel**) and API (**Render**) and running migrations on **Supabase** (head revision **027**).

## One-time setup

- [ ] Supabase project created; **Transaction pooler** connection string copied (`postgresql+psycopg2://...:6543/...?sslmode=require`).
- [ ] `python -m alembic upgrade head` run against production `DATABASE_URL` (verify `alembic_version` = `027`).
- [ ] Backups enabled — see [BACKUPS.md](BACKUPS.md) (PITR or scheduled `pg_dump`).
- [ ] `SECRET_KEY` set (e.g. `openssl rand -hex 32`).
- [ ] `ENVIRONMENT=production`, `AUTH_DISABLED=false`, `RUN_MIGRATIONS_ON_STARTUP=false`.
- [ ] `REDIS_URL` set (required — shared rate limits, email abuse caps, scholarship cache).
- [ ] `TRUST_PROXY_HEADERS=true` (Render — correct client IP for rate limits).
- [ ] `WEB_CONCURRENCY=2` (or higher) — gunicorn workers via [Procfile](../Procfile).
- [ ] `SMTP_HOST`, `EMAIL_FROM`, `FRONTEND_URL` set for auth emails.
- [ ] `CORS_ORIGINS` includes your Vercel URL exactly.
- [ ] Frontend `VITE_API_BASE_URL` points to the public API URL (no trailing slash).
- [ ] Admin user created: `python -m app.scripts.create_admin <email> <password>`.
- [ ] GitHub **Secret** `DATABASE_URL` set for `scraper.yml`, `deadline-maintenance.yml`, `retention-cleanup.yml`.
- [ ] UptimeRobot on `https://YOUR-API/health` (5 min). Expect **200** with `"status":"ok"`; **503** = DB down.

## Production validation (run on live domain)

### Auth

| Check | Expected | If it fails |
|-------|----------|-------------|
| Register | 200 + tokens; row in `users` with `email_verified=false` | SMTP/CORS; check Render logs |
| Verify email | Link sets `email_verified=true` | `FRONTEND_URL`, SMTP logs |
| Login (unverified) | **403** when SMTP configured | By design — verify first |
| Login (verified) | 200 + tokens | Credentials, Redis |
| Password reset | Email received; reset works; refresh tokens revoked | SMTP, `FRONTEND_URL` |
| Logout | Refresh token revoked in DB | |

### Core product

| Check | Expected | DB / logs |
|-------|----------|-----------|
| Profile save | `students` row linked to `user_id` | `students` table |
| Find matches | `match_runs` + `match_results` rows | Match API logs |
| Explanations | Each result has `explanation` JSON | `match_results` |
| Saved scholarships | `saved_scholarships` row | |
| Mobile | Layout usable on phone viewport | — |

### Admin & data pipeline

| Check | Expected | DB / logs |
|-------|----------|-----------|
| `/admin` | Loads for admin role only | `users.role=admin` |
| `GET /metrics` (admin JWT) | Counts JSON | Not public — 401 without token |
| Scraper workflow | `scraper_runs` row; optional `scholarships_staging` pending | GitHub Actions logs |
| Staging approve | New `scholarships` row, staging `approved` | Admin API |

### Ops

| Check | Expected |
|-------|----------|
| `GET /health` | 200, `"db": true` |
| Redis | `/health` `cache` not `"error"` when `REDIS_URL` set |
| Rate limit | Rapid login → 429 |
| Sentry | Test error appears when DSN set |
| Performance | Match run completes in reasonable time (watch cold start) |

## Smoke tests (quick path)

- [ ] Register → verify email → login → profile builder → save profile.
- [ ] Dashboard loads; **Find my matches** creates a `match_runs` row.
- [ ] Admin `/admin` and analytics load.
- [ ] `curl https://YOUR-API/health` → `"status":"ok"`.
- [ ] `curl -H "Authorization: Bearer ADMIN_TOKEN" https://YOUR-API/metrics` → counts JSON.

## Optional

- [ ] `SENTRY_DSN` / `VITE_SENTRY_DSN` for error tracking.
- [ ] `VITE_SENTRY_ENVIRONMENT=production` and `VITE_SENTRY_RELEASE` (git SHA) on Vercel.
- [ ] Sentry alert: >10 errors in 5 min on `environment:production` ([OBSERVABILITY.md](OBSERVABILITY.md)).

## Friends cohort launch

1. Complete all checks above on production URLs.
2. Invite 5–10 friends; monitor Sentry + `/health` + `scraper_runs` for 48 hours.
3. Fix any P0 issues before wider promotion.
