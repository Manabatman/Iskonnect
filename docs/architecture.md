# Architecture

How Iskonnect fits together: runtime components, request flow, matching engine, and future opportunity types.

## System overview

```
Browser  →  Vercel (static React SPA)
              ↓  HTTPS (VITE_API_BASE_URL)
           Render (FastAPI + gunicorn)
              ↓  SQL (DATABASE_URL)
           Supabase (PostgreSQL)

GitHub Actions  →  same Supabase (catalog maintenance, link checks, retention)
```

| Component | Role |
|-----------|------|
| **Vercel** | Serves built React app only — no Python |
| **Render** | FastAPI API at `/api/v1/...` (gunicorn + Uvicorn workers in production) |
| **Supabase** | PostgreSQL via SQLAlchemy + Alembic (not the Supabase JS client) |
| **Redis** | Rate limits, scholarship list cache (production) |
| **GitHub Actions** | CI, scheduled catalog maintenance, deadline reminders |

## Request flow

1. User opens the Vercel-hosted SPA (`frontend/src/App.tsx`).
2. Data calls use `apiFetch()` in `frontend/src/api/client.ts`.
3. Render handles the route under `app/api/v1/`, opens a DB session, returns JSON.

**Cold starts (Render free tier):** First request after idle can take 15–30+ seconds. The frontend shows a short “Connecting to server…” banner.

## Key backend modules

| Path | Purpose |
|------|---------|
| `app/api/v1/` | REST endpoints |
| `app/models.py` | SQLAlchemy models |
| `app/matching/` | Hard filters + match orchestration |
| `app/scoring/` | Pluggable weighted scoring engine |
| `app/jobs/` | Catalog maintenance, link checking |
| `app/utils/data_completeness.py` | Publishability scoring |
| `app/utils/verification_display.py` | Trust badges on catalog rows |

## Data model (high level)

- **Live catalog:** `scholarships` — search and matching source of truth
- **Staging:** `scholarships_staging` — CSV/research imports await admin approval
- **Profiles:** `students` — multi-step profile builder data
- **Matches:** `match_runs` — persisted match sessions

Past application deadlines roll to cycle metadata (`last_close_date`, `expected_reopen`) — a closed cycle does **not** mean the program is discontinued. `is_active=false` is reserved for permanently discontinued programs.

## Matching engine

Two-stage pipeline:

1. **Hard eligibility filters** (`app/matching/hard_filters.py`) — age, education level, income, region, GWA, etc. Applied before scoring. Returns a deterministic `EligibilityResult`.
2. **Weighted scoring** (`app/scoring/`) — ranks scholarships that pass hard filters.

### Scoring philosophy

The match score is **eligibility fitness** (0–100): how well a profile aligns with a scholarship's criteria. It is not a probability, competitiveness rank, or ML prediction.

| Component | Weight | Purpose |
|-----------|--------|---------|
| Academic Strength | 30% | GWA vs. scholarship minimum |
| Income Alignment | 28% | Need-based fit |
| Field Alignment | 22% | PSCED course/discipline match |
| Geographic Relevance | 10% | Location for LGU/regional programs |
| Equity Priority | 10% | Priority groups (PWD, IP, Solo Parent, etc.) |

Non-applicable components are excluded and remaining weights renormalize. Document readiness is tracked separately — not part of the fitness score.

Implementation: `app/scoring/components.py`, `app/scoring/engine.py`.

## Future opportunity types

Scholarship is the first `opportunity_type`. The platform is designed to extend to internships, grants, fellowships, and competitions using shared primitives:

- Persistent student profile
- `EligibilityResult` contract
- Two-stage filter + score engine
- Verification and completeness gates

New modules add datasets and rule mappings — not forked matching engines. See `frontend/src/constants/opportunityTypes.ts` for the product roadmap.

## Environment variables

| Variable | Where | Purpose |
|----------|--------|---------|
| `VITE_API_BASE_URL` | Vercel | Render API origin (no trailing slash) |
| `DATABASE_URL` | Render, GitHub Actions | Supabase pooler URI |
| `CORS_ORIGINS` | Render | Allowed browser origins |
| `SECRET_KEY`, `ENVIRONMENT` | Render | JWT and production guards |
| `REDIS_URL`, `SMTP_*`, `FRONTEND_URL` | Render | Rate limits, email, auth links |

Never put `DATABASE_URL` or `SECRET_KEY` in Vercel — the frontend bundle is public.

## Troubleshooting

| Symptom | Check |
|---------|--------|
| “Unable to reach the server” | Local: uvicorn on :8000? Production: Render cold start, CORS, `VITE_API_BASE_URL` |
| CORS error | `CORS_ORIGINS` must match Vercel origin exactly |
| Empty search | `scholarships.is_active`, completeness score, publishability threshold |
| `/health` returns 503 | `DATABASE_URL`, Supabase status, Redis (if configured) |

## Health endpoints

- `GET /health` — DB/cache checks; returns 503 when degraded
- `GET /ready` — Stricter DB ping

Point uptime monitoring at `/health`.
