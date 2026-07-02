# Iskonnect

**Policy-aware scholarship matching for Filipino students.**

Iskonnect helps students discover scholarships they can realistically apply for—not just browse listings. Students build a structured profile; the platform applies **hard eligibility filters**, **Philippine policy-aware priority groups**, and a **transparent scoring engine**, then explains *why* each program matched.

> **Status:** Public Beta (v1.0 Beta) — July 2026. Core flows work end-to-end; catalog and matching logic are still being expanded.

**Live stack:** Vercel (frontend) · Render (API) · Supabase (Postgres) · Redis (rate limits & cache)  
**Deploy guide:** [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)  
**Python on Render:** `.python-version` pins **3.11.x** (avoids Render defaulting to 3.14).

---

## Why Iskonnect?

Scholarship information in the Philippines is scattered across government portals, LGU sites, university pages, and aggregators. Students often miss programs they qualify for—or waste time on ones they don’t.

Iskonnect centralizes opportunities in a **structured catalog** and matches them to a **rich student profile** (academics, location, income, priority groups, documents).

---

## What it does

| Capability | Description |
|------------|-------------|
| **Scholarship search** | Public browse/filter at `/scholarships/search` (no login required) |
| **Student profiles** | Multi-step profile builder (personal, academic, geographic, socioeconomic data) |
| **Hard eligibility filters** | Age, education level, income ceiling, GWA, region, and related gates applied *before* scoring |
| **Match planning** | `GET /api/v1/plan/{profile_id}` returns ranked matches, timeline buckets, preparation hints, and completeness |
| **Match explanations** | Per-scholarship breakdown: academic, income, geography, field fit, priority groups |
| **Document readiness** | Tracks required vs. available documents for applications (separate from eligibility score) |
| **PSCED alignment** | Course/field matching via Philippine Standard Classification of Education (PSCED) buckets |
| **Saved scholarships & applications** | Bookmark programs and track application status (authenticated) |
| **Admin & data pipeline** | Admin-verified CSV/staging import, data-quality monitoring, link checking, deadline maintenance |

### Policy-aware priority groups

Matching considers groups commonly recognized in Philippine scholarship policy, including references to:

- **RA 7277** — Magna Carta for Persons with Disabilities  
- **RA 7279** — Urban Development and Housing Act  
- **RA 8371** — Indigenous Peoples Rights Act  
- **RA 11861** — Expanded Solo Parents Welfare Act  

### Modular scoring

The ranking engine is **pluggable**: a default rule-based scorer ships with the app; alternative scorers can be swapped without rewriting the API or frontend.

---

## Tech stack

| Layer | Technologies |
|-------|----------------|
| **Backend** | Python 3.11, FastAPI, SQLAlchemy, Alembic, Pydantic, JWT auth |
| **Database** | SQLite (`dev.db`) locally · PostgreSQL (Supabase) in production |
| **Cache / limits** | Redis (production) |
| **Frontend** | React, TypeScript, Vite, Tailwind CSS |
| **Ops** | GitHub Actions (CI, maintenance crons), Sentry (optional) |

---


---

## Quick start (local)

You need **two terminals**: API on `:8000`, UI on `:5173`.

### Prerequisites

- Python **3.11**
- Node.js **18+** (CI uses Node 24)
- Git

### 1. Clone & backend

git clone https://github.com/YOUR_ORG/YOUR_REPO.git
cd scholarship-match   # or cd into the app folder if using a monorepo

python -m venv venv
# Windows:  .\venv\Scripts\Activate.ps1
# macOS/Linux:  source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
cp frontend/.env.example frontend/.env

Recommended local .env settings:

ENVIRONMENT=development
DATABASE_URL=sqlite:///./dev.db
RUN_MIGRATIONS_ON_STARTUP=true
REQUIRE_EMAIL_VERIFICATION=false
AUTH_DISABLED=false
Create DB tables and seed sample data:

python seed_data.py
uvicorn app.main:app --reload --port 8000
API: http://localhost:8000
Docs: http://localhost:8000/docs
Health: http://localhost:8000/health
2. Frontend
cd frontend
npm install
npm run dev
App: http://localhost:5173
Search: http://localhost:5173/scholarships/search
frontend/.env should include:

VITE_API_BASE_URL=http://localhost:8000
3. Windows shortcut
From the repo root (monorepo):

START_BOTH.bat
Runs backend + frontend in separate windows. Seed manually with python seed_data.py if the catalog is empty.

Optional: larger demo catalog
For hundreds of verified CSV rows, place files in `../.cursor/plans/data/` (`philscholar.csv`, `sikap.csv`, `scholarships.csv`), then:

python -m app.scripts.seed_demo_csvs
Past-deadline rows remain in the DB as past_deadline so matching demos still work.

Authentication (local vs production)
Setting	Local dev	Production
AUTH_DISABLED
false (recommended)
false
REQUIRE_EMAIL_VERIFICATION
false for easy testing
true + SMTP configured
Accounts
Register at /register (separate from production DB)
Supabase Postgres
Local SQLite is not the same database as production—create a test account locally.

API overview
Base path: /api/v1 · Auth: Bearer JWT on protected routes

Method	Endpoint	Description
GET
/health
Health check (DB, cache, maintenance job metadata)
POST
/auth/register
Create account
POST
/auth/login
Login → access + refresh tokens
GET
/auth/me
Current user
GET
/profiles/me
Current student profile
POST
/profiles
Create or update profile
GET
/scholarships/search
Browse & filter catalog (public)
GET
/plan/{profile_id}
Matches + timeline + preparation + completeness
POST
/match-runs
Run and persist a full match session
GET
/saved-scholarships
User’s saved programs
POST
/scholarships/staging/import
Admin: bulk import to staging
Interactive reference (development only): http://localhost:8000/docs

Data pipeline (high level)
CSV / research import → staging → admin approve → live catalog
Completeness scoring + publishability gate on every write and nightly maintenance
Details: docs/operations-handbook/06-data-pipeline.md

Documentation
Doc	Purpose
docs/DEPLOYMENT.md
Vercel + Render + Supabase production setup
docs/HANDBOOK.md
Local dev, debugging, common errors
docs/operations-handbook/00-index.md
Full ops handbook
../START_HERE.md
Monorepo quick start (if applicable)
Development
# Backend tests
python -m pytest app/tests/
# Frontend tests
cd frontend && npm test
Roadmap / known limits
Catalog coverage is growing (national programs first; LGU and institutional grants in progress)
Matching is explainable and policy-aware but not a substitute for official provider verification
Always confirm deadlines and requirements on the primary source link before applying
License
See LICENSE if present in the repository.

Contributing
Issues and PRs welcome. For large data imports, use the staging workflow rather than writing directly to production tables.

