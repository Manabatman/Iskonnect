# Deployment checklist (free stack)

Use **Vercel** (frontend), **Render** (FastAPI), **Supabase** (Postgres), and **GitHub Actions** (CI + scrapers).

Beginner-oriented architecture and debugging: **[HANDBOOK.md](HANDBOOK.md)**.

## Order

1. Deploy **Vercel** first (root directory `frontend`) to obtain `https://….vercel.app`.
2. Create **Render** Web Service (Python **3.11** — repo includes `.python-version`). Set `CORS_ORIGINS` to your Vercel URL.
3. Set **Vercel** `VITE_API_BASE_URL` to your Render URL and redeploy.

## Render (backend)

- **Runtime:** Python (not Docker unless you prefer).
- **Build:** `pip install -r requirements.txt`
- **Start:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Release / Pre-deploy:** `alembic upgrade head`
- **Env:** `DATABASE_URL` (Supabase pooler, `postgresql+psycopg2://…?sslmode=require`), `SECRET_KEY` (random hex), `ENVIRONMENT=production`, `AUTH_DISABLED=false`, `CORS_ORIGINS`, `RUN_MIGRATIONS_ON_STARTUP=false`

## Vercel (frontend)

- **Root directory:** `frontend`
- **Env:** `VITE_API_BASE_URL` = Render URL (no trailing slash). Do **not** put `DATABASE_URL` or `SECRET_KEY` here.

## Supabase

- Run migrations locally: `python -m alembic upgrade head` with `DATABASE_URL` pointing at Supabase.
- GitHub secret `DATABASE_URL`: same URI as Render (for scraper + deadline workflows).

## GitHub Actions

- **DATABASE_URL** repository secret required for `scraper.yml` and `deadline-maintenance.yml`.
- Workflows use Python **3.11**; CI frontend uses Node **22** (see `.github/workflows/ci.yml`).
