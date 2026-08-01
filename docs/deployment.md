# Deployment

Production stack: **Vercel** (frontend) · **Render** (API) · **Supabase** (Postgres) · **Redis** · **GitHub Actions** (CI + crons).

See also: [architecture.md](architecture.md) for system overview.

## Deploy order

1. Deploy **Vercel** first (root directory `frontend`) → `https://….vercel.app`
2. Create **Render** Web Service (Python **3.11** — `.python-version` in repo). Set `CORS_ORIGINS` to your Vercel URL.
3. Set **Vercel** `VITE_API_BASE_URL` to your Render URL and redeploy.

## Render (backend)

- **Build:** `pip install -r requirements.txt`
- **Start (Procfile):** `gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w ${WEB_CONCURRENCY:-2} -b 0.0.0.0:$PORT --forwarded-allow-ips='*' --proxy-headers`
- **Release:** `alembic upgrade head`

### Required environment variables

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | Supabase transaction pooler (`postgresql+psycopg2://…:6543/…?sslmode=require`) |
| `SECRET_KEY` | JWT signing (`openssl rand -hex 32`) |
| `ENVIRONMENT` | `production` |
| `AUTH_DISABLED` | `false` |
| `RUN_MIGRATIONS_ON_STARTUP` | `false` (use release command) |
| `CORS_ORIGINS` | Vercel URL (exact origin, no trailing slash) |
| `REDIS_URL` | Rate limits, cache |
| `TRUST_PROXY_HEADERS` | `true` |
| `WEB_CONCURRENCY` | `2` or higher |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `EMAIL_FROM` | Auth emails |
| `FRONTEND_URL` | Public frontend URL for reset/verify links |

### Recommended

`SENTRY_DSN`, `STRUCTURED_LOGGING=true`, `ACCESS_TOKEN_EXPIRE_MINUTES=30`

### Matching behavior flags

| Variable | Default | Purpose |
|----------|---------|---------|
| `FILTER_EXPIRED_FROM_MATCHES` | `true` | When `true`, scholarships with `data_status` in `expired`, `broken_link`, or `past_deadline` fail the hard `data_status` check in matching (`app/matching/eligibility_result.py`, `_evaluate_data_status`). Set to `false` only if you need expired listings to remain eligible in ranked match results (e.g. local debugging). Defined in `app/config.py`; consumed via `settings.filter_expired_from_matches`. |
| `PLAN_PREFILTER_ENABLED` | `false` | When `true`, `/plan` uses SQL prefilter (`_prefilter_scholarships_query`) before scoring. **Do not enable in production** until ADR-007 decision gate is re-run at ≥300 publishable listings and HTTP `/plan` p95 is confirmed ≤800 ms. Benchmark: `python -m app.scripts.measure_plan_prefilter`. Parity: `app/tests/test_plan_prefilter_parity.py`. |

Do **not** change this flag in production without re-running persona and eval regression tests — it affects who appears in `/plan` results.

## Vercel (frontend)

- **Root directory:** `frontend`
- **Env:** `VITE_API_BASE_URL` = Render URL (no trailing slash)
- **Optional:** `VITE_SENTRY_DSN`, `VITE_SENTRY_ENVIRONMENT=production`, `VITE_SENTRY_RELEASE`

Do **not** put `DATABASE_URL` or `SECRET_KEY` in Vercel.

## Supabase

- Run migrations: `python -m alembic upgrade head` with `DATABASE_URL` pointing at Supabase
- Enable backups (see [Backups](#backups) below)
- GitHub secret `DATABASE_URL`: same URI as Render (for maintenance workflows)

### Scholarship images (optional)

1. Create public bucket `scholarship-images` in Supabase Storage
2. Allow public `SELECT`; uploads use service role on the backend only
3. On Render set `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `SCHOLARSHIP_IMAGE_BUCKET=scholarship-images`
4. Admins upload via `POST /api/v1/scholarships/{id}/image`

## GitHub Actions

Repository secret **`DATABASE_URL`** required for:

- Catalog maintenance (`deadline-maintenance.yml`)
- Link checking
- Retention cleanup

CI uses Python **3.11** and Node **24** (`.github/workflows/ci.yml`).

## Observability

### Sentry

- **Backend:** `SENTRY_DSN` + `ENVIRONMENT=production` on Render
- **Frontend:** `VITE_SENTRY_DSN` on Vercel

Recommended alert: >10 errors in 5 minutes on `environment:production`.

### Monitoring

- Point **UptimeRobot** (or similar) at `GET /health` every few minutes
- `GET /metrics` requires admin JWT — ops use only

## Backups

Iskonnect does not run backups inside the app. Use Supabase before public launch.

### Option A — Point-in-Time Recovery (recommended)

Supabase Dashboard → Project Settings → Database → Backups → enable PITR.

### Option B — Manual pg_dump

Use the **direct** connection (port **5432**, not the pooler):

```bash
pg_dump -h db.<PROJECT_REF>.supabase.co -p 5432 -U postgres -d postgres -Fc -f iskonnect-backup-$(date +%Y%m%d).dump
```

Store dumps off-site. **Never commit dumps to git.**

### Before launch

- [ ] At least one backup method enabled
- [ ] Tested restore to a non-production database once
- [ ] Secrets stored in a password manager, not the repo

After a bad migration: restore DB from backup, then redeploy the last known-good API commit.

## Deprecated configs

Do **not** use `render.yaml` for the live stack — it targets Render Postgres + uvicorn and is kept only as an optional blueprint.

## Post-deploy smoke test

1. `GET /health` → `status: "ok"`
2. Open Vercel URL → search loads scholarships
3. Register/login flow works
4. Admin staging tab reachable (admin account)
