# Deployment checklist (free stack)

Use **Vercel** (frontend), **Render** (FastAPI + gunicorn), **Supabase** (Postgres), **Redis** (Upstash or Render), **SMTP** (Resend/SendGrid), and **GitHub Actions** (CI + crons).

Beginner-oriented architecture and debugging: **[HANDBOOK.md](HANDBOOK.md)**.

**Complete production operations handbook (deploy → operate → scale):** **[operations-handbook/00-index.md](operations-handbook/00-index.md)**.

## Order

1. Deploy **Vercel** first (root directory `frontend`) to obtain `https://….vercel.app`.
2. Create **Render** Web Service (Python **3.11** — repo includes `.python-version`). Set `CORS_ORIGINS` to your Vercel URL.
3. Set **Vercel** `VITE_API_BASE_URL` to your Render URL and redeploy.

## Render (backend)

- **Runtime:** Python (not Docker unless you prefer). Render reads [Procfile](../../Procfile) for start/release commands.
- **Build:** `pip install -r requirements.txt`
- **Start (from Procfile):** `gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w ${WEB_CONCURRENCY:-2} -b 0.0.0.0:$PORT --forwarded-allow-ips='*' --proxy-headers`
- **Release / Pre-deploy:** `alembic upgrade head`
- **Required env vars:**
  - `DATABASE_URL` — Supabase transaction pooler (`postgresql+psycopg2://…:6543/…?sslmode=require`)
  - `SECRET_KEY` — random hex (`openssl rand -hex 32`)
  - `ENVIRONMENT=production`
  - `AUTH_DISABLED=false`
  - `RUN_MIGRATIONS_ON_STARTUP=false`
  - `CORS_ORIGINS` — your Vercel URL (and custom domain when ready)
  - `REDIS_URL` — required for shared rate limits, email abuse caps, scholarship cache
  - `TRUST_PROXY_HEADERS=true` — correct client IP behind Render
  - `WEB_CONCURRENCY=2` (or higher)
  - `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `EMAIL_FROM` — auth emails
  - `FRONTEND_URL` — public frontend URL (password reset / verify links)
- **Recommended:** `SENTRY_DSN`, `STRUCTURED_LOGGING=true`, `ACCESS_TOKEN_EXPIRE_MINUTES=30`

## Vercel (frontend)

- **Root directory:** `frontend`
- **Env:** `VITE_API_BASE_URL` = Render URL (no trailing slash). Do **not** put `DATABASE_URL` or `SECRET_KEY` here.
- **Recommended:** `VITE_SENTRY_DSN`, `VITE_SENTRY_ENVIRONMENT=production`, `VITE_SENTRY_RELEASE` (git SHA)

## Supabase

- Run migrations locally: `python -m alembic upgrade head` with `DATABASE_URL` pointing at Supabase. Head revision is **027**.
- Enable backups: see **[BACKUPS.md](BACKUPS.md)** (PITR or scheduled `pg_dump`).
- GitHub secret `DATABASE_URL`: same URI as Render (for scraper, deadline, and retention workflows).

## GitHub Actions

- **DATABASE_URL** repository secret required for `scraper.yml`, `deadline-maintenance.yml`, and `retention-cleanup.yml`.
- Workflows use Python **3.11**; CI frontend uses Node **24** (see `.github/workflows/ci.yml`).

## Deprecated configs

Do **not** use [render.yaml](../../render.yaml) for the live stack — it targets Render Postgres + uvicorn and is kept only as an optional blueprint. Production uses Supabase + gunicorn + GitHub Actions crons.
