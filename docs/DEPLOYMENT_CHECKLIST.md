# Deployment checklist (manual verification)

Use this after deploying frontend (Vercel) and API (e.g. Hugging Face Spaces) and running migrations on Supabase.

## One-time setup

- [ ] Supabase project created; **Transaction pooler** connection string copied (`postgresql+psycopg2://...:6543/...`).
- [ ] `alembic upgrade head` run against production `DATABASE_URL` (or `RUN_MIGRATIONS_ON_STARTUP=true` on first boot only).
- [ ] `SECRET_KEY` set (e.g. `openssl rand -hex 32`).
- [ ] `ENVIRONMENT=production`, `AUTH_DISABLED=false`.
- [ ] `CORS_ORIGINS` includes your Vercel URL exactly.
- [ ] Frontend `VITE_API_BASE_URL` points to the public API URL.
- [ ] Admin user created (`python -m app.scripts.create_admin` or SQL).
- [ ] GitHub repository **Secret** `DATABASE_URL` set for the scraper workflow.
- [ ] UptimeRobot monitor on `https://YOUR-API/health` (5 min interval).

## Smoke tests

- [ ] Register → login → profile builder → save profile.
- [ ] Dashboard loads; Document Vault, Financial Planner, Review Center, Career Roadmap visible.
- [ ] **Find my matches** creates a row in `match_runs`.
- [ ] **Find My Matches** from Search also creates a run and opens results with `?run=`.
- [ ] Saved scholarships sort shows newest saved first on dashboard.
- [ ] Admin `/admin` tabs load (as admin user).
- [ ] `GET /health` returns `"db": true` and optional `scraper_last` after a scraper run.

## Hugging Face Spaces (Docker)

- [ ] Space **Settings → Variables**: `PORT` is usually set by HF to **7860** for Docker; image uses `${PORT:-8000}`.
- [ ] If the Space sleeps, UptimeRobot reduces cold starts.

## Optional

- [ ] `SENTRY_DSN` / `VITE_SENTRY_DSN` for error tracking.
- [ ] `REDIS_URL` if you use shared cache across workers.
