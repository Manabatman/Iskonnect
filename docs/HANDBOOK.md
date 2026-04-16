# ISKONNECT beginner handbook

How your live system fits together, what each piece does, and what to check when something breaks.

## 1. Mental model (four boxes)

```
Browser  →  Vercel (static React app)
              ↓  HTTPS API calls (VITE_API_BASE_URL)
           Render (FastAPI Python server)
              ↓  SQL over DATABASE_URL
           Supabase (PostgreSQL)

GitHub Actions → same Supabase (optional scheduled scrape → staging; daily catalog maintenance)
```

- **Vercel** only serves built HTML/JS/CSS. It does **not** run your Python code.
- **Render** runs **FastAPI** (`uvicorn app.main:app`). This is where `/api/v1/...` lives.
- **Supabase** is **Postgres**. Your API talks to it with **SQLAlchemy** (see `app/db.py`, `app/models.py`) and **Alembic** migrations — not the Supabase JS client in this repo.
- **GitHub Actions** run scripts that connect to the **same** `DATABASE_URL` (repository secret): optional PhilScholar scrape + ingest, and daily catalog maintenance.

## 2. One request, end to end

1. User opens `https://your-app.vercel.app`.
2. The browser loads the SPA and runs React (`frontend/src/App.tsx`).
3. Data calls use `apiFetch()` in `frontend/src/api/client.ts` → `fetch(VITE_API_BASE_URL + "/api/v1/...")`.
4. Render receives the HTTP request, runs the matching route under `app/api/v1/`, opens a DB session, returns JSON.

**Cold starts (Render free tier):** If nobody has hit the API for a while, the first request can take **15–30+ seconds**. The frontend waits up to **30 seconds** and shows a short “Connecting to server…” banner when requests are in flight.

## 3. Environment variables (what goes where)

| Variable | Where | Purpose |
|----------|--------|---------|
| `VITE_API_BASE_URL` | **Vercel** (build env) | Full origin of your Render API, e.g. `https://iskonnect-api.onrender.com` — **no** trailing slash. Changing it requires a **new Vercel deploy** (Vite bakes it in at build time). |
| `DATABASE_URL` | **Render** + **GitHub Actions secret** | Supabase **transaction pooler** URI with `postgresql+psycopg2://...?sslmode=require`. |
| `CORS_ORIGINS` | **Render** | Comma-separated list of allowed **browser origins** (your Vercel URL **exactly**: `https://….vercel.app`). Must match or the browser blocks API calls. |
| `SECRET_KEY`, `ENVIRONMENT`, `AUTH_DISABLED` | **Render** | JWT signing and production guards (`app/config.py`). |

Never put `DATABASE_URL` or `SECRET_KEY` in Vercel — the frontend is public.

## 4. Health checks and monitoring

- **`GET /health`** — Returns JSON with `status: "ok"` or `"degraded"`. If the DB (or Redis, when configured) fails checks, the API returns **HTTP 503** so uptime monitors alert you.
- **`GET /ready`** — Stricter DB ping; also returns **503** if the database is unreachable.

Point **UptimeRobot** (or similar) at `/health` every few minutes to reduce Render cold starts and to detect outages.

## 5. Data: scholarships, staging, maintenance

- **Live catalog:** `scholarships` table (what search and matching use).
- **Staging queue:** `scholarships_staging` — scraper output lands here; **admin approves** before it becomes a live row.
- **Catalog maintenance** (GitHub Action `Scholarship deadline maintenance`): runs `python -m app.scripts.expire_scholarship_deadlines`, which calls **`app.jobs.catalog_maintenance.run_catalog_maintenance()`** — past deadlines → `is_active=false` + `data_status=expired`, stale verification → `needs_review`, then **scholarship list cache invalidation** (Redis if set; always safe to call).

## 6. If X breaks, check Y

| Symptom | Check |
|---------|--------|
| “Unable to reach the server” / spinner forever | Render service **asleep**? Wait up to ~30s. Wrong `VITE_API_BASE_URL`? Browser **Network** tab: request URL and CORS errors. |
| CORS error in console | `CORS_ORIGINS` on Render must include **exact** Vercel origin (`https://`, no typo). |
| 401 on API | Log in again; token in `localStorage`. `AUTH_DISABLED` should be `false` in production. |
| Empty search / no matches | Supabase **Table Editor** → `scholarships`: rows exist? `is_active`? |
| Scraper not updating | Cron may be disabled in `.github/workflows/scraper.yml`; try **Run workflow** manually. Logs: **Scholarship scrape and ingest**; secret **`DATABASE_URL`** must match Render’s DB. |
| `/health` 503 | `DATABASE_URL`, Supabase project status, network. Render logs for traceback. |
| Deployed frontend still calls old API | Rebuild Vercel after changing `VITE_*` env vars. |

## 7. Safe local workflow

1. Copy `.env.example` → `.env` at repo root; use SQLite for quick dev unless you need Postgres parity.
2. `alembic upgrade head`
3. `uvicorn app.main:app --reload --port 8000`
4. In `frontend/`: `npm install` && `npm run dev`, with `VITE_API_BASE_URL=http://localhost:8000`
5. Before production changes: `npm run build` and `python -m pytest app/tests/ -v`

## 8. What not to change without a plan

- Do not point GitHub Actions at a **different** `DATABASE_URL` than production — you will split-brain the catalog.
- Do not set `AUTH_DISABLED=true` outside local debugging.
- Do not skip `alembic upgrade head` on production deploys (use Render **release** command per `docs/DEPLOYMENT.md`).

## 9. Dashboard tools: Review Center Finder and Career Roadmap

Both features open **Google AI Mode** in a new tab: the app builds a detailed natural-language query and navigates to Google Search with `udm=50` (AI-style synthesized answer view). **No API key** and no server-side generative AI in this repo — Google’s page does the synthesis.

- **URL builder:** `frontend/src/utils/googleAiModeSearch.ts` (`buildGoogleAiModeSearchUrl`).
- **Review Center:** `frontend/src/components/dashboard/ReviewCenterFinderCard.tsx` — query includes location, fees, passing rates, schedule, online vs face-to-face, reviews.
- **Career Roadmap:** `frontend/src/components/dashboard/CareerRoadmapCard.tsx` — query covers roles, skills, PHP salary bands, progression, certifications (Philippines context).

> Google may change how `udm=50` behaves or rename parameters. If links stop opening AI Mode, update the helper and retest in an incognito window.

## 10. Scraping (PhilScholar)

The workflow **Scholarship scrape and ingest** may have its **`schedule` block commented out** to pause automated scraping while keeping **manual** runs (`workflow_dispatch`). To turn scraping back on, uncomment `schedule` in `.github/workflows/scraper.yml` and commit.

The app still works without new scrapes: **admin entry**, **CSV import**, and **staging approval** populate scholarships.

## 11. Branding: logo and header font

| Asset | Path |
|-------|------|
| Default (light UI) logo | `frontend/public/images/logo.svg` |
| Dark UI logo | `frontend/public/images/logo-dark.svg` |

**Header / body font:** **Inter** — loaded in `frontend/index.html` (Google Fonts `<link>`) and set as Tailwind `font-sans` in `frontend/tailwind.config.js` (`theme.extend.fontFamily.sans`).

## 12. Profile builder: two education fields

- **Current academic stage** — where you are in school today (e.g. Senior HS, Undergraduate).
- **Target education level for scholarship** — the level you want to find scholarships **for** (stored as `education_level` in the API; can differ from your current stage).

## 13. Where to read more

- **[DEPLOYMENT.md](DEPLOYMENT.md)** — ordered deploy steps (canonical for Vercel + Render + Supabase + Actions).
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** — smoke tests after a release.
- **[MONITORING_GUIDE.md](MONITORING_GUIDE.md)** — daily/weekly checks.
