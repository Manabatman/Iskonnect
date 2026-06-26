# Lesson 26 — Maintenance, Code Audits & Rebuild Capstone

> **Prerequisite:** [25 — Operations & Incident Response](25-operations-and-incident-response.md)

---

## Reading legacy code (your own)

### The 30-minute onboarding ritual

1. Read [00-index](00-index.md) repo map
2. Skim [`app/main.py`](../../../app/main.py) — routers and middleware
3. Trace one feature vertically (register → auth → dashboard → match)
4. Read latest migration (`025_...`)
5. Run app locally with `AUTH_DISABLED=true`
6. Run `pytest` and `npm test`

You are now oriented enough to ship a small fix.

---

## Safe refactoring rules

1. **Tests first** — if no test, write one capturing current behavior
2. **One concern per PR** — don't mix rename + feature
3. **Additive migrations** — never edit deployed revision files
4. **Feature flags** — for risky UI (`featureFlags.ts` pattern)
5. **Invalidate caches** — after scholarship mutations

---

## Pull request review checklist

- [ ] Authz: can user A access user B's data?
- [ ] Migrations: upgrade + downgrade tested?
- [ ] Secrets: no `.env` in diff?
- [ ] API contract: frontend types updated?
- [ ] Performance: unbounded list queries?
- [ ] Observability: errors logged with context?
- [ ] User-visible copy: brand **Iskonnect**?

---

## Technical debt evaluation

| Signal | Action |
|--------|--------|
| Duplicate logic in 3+ routes | Extract service function |
| Deprecated shim unused | Delete + update tests |
| String geo matching | Plan PSGC migration |
| RLS enabled, no policies | Document risk, don't false-comfort |
| Sponsor portal unused | Gate removal with migration down-path |

Reference: production sanitation blueprint in repo plans.

---

## Code audit process

1. **Inventory** — routes, tables, external deps
2. **Threat model** — auth, IDOR, injection, rate limits
3. **Data map** — PII columns (RA 10173), retention
4. **Dependency CVE scan**
5. **Findings report** — severity, owner, deadline

---

## Production release checklist

- [ ] CI green on `main`
- [ ] `alembic upgrade head` on staging
- [ ] Smoke tests on staging
- [ ] Changelog updated ([`data/changelog.ts`](../../../frontend/src/data/changelog.ts))
- [ ] Render release command succeeds
- [ ] Vercel redeploy if `VITE_*` changed
- [ ] Sentry release tag set
- [ ] Monitor 30 min post-deploy

---

# CAPSTONE: Rebuild Iskonnect from empty folder

Complete this checklist without copy-pasting the repo. Use lessons 02–25 as reference.

## Phase A — Foundation (Day 1)

```bash
mkdir Iskonnect && cd Iskonnect
mkdir scholarship-match && cd scholarship-match
git init
python -m venv venv
# activate venv
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings alembic
```

- [ ] Create `app/__init__.py`, `app/main.py` with `/health`
- [ ] Create `requirements.txt` via `pip freeze`
- [ ] Run `uvicorn app.main:app --reload --port 8000`
- [ ] Verify `/health` in browser

## Phase B — Data layer (Day 2–3)

- [ ] `app/db.py` — engine, SessionLocal, get_db
- [ ] `app/models.py` — Student, Scholarship (match migration 001 columns)
- [ ] `alembic init alembic`
- [ ] First migration `001_initial_schema`
- [ ] `alembic upgrade head`
- [ ] Seed script with 5+ scholarships

## Phase C — API (Day 4–5)

- [ ] `app/schemas.py` — Pydantic models
- [ ] `app/api/v1/scholarships.py` — GET list
- [ ] `app/api/v1/profiles.py` — POST/GET profile
- [ ] Mount routers in `main.py` with `/api/v1` prefix
- [ ] Test in `/docs`

## Phase D — Matching (Day 6–8)

- [ ] `app/taxonomy/gwa_normalizer.py`
- [ ] `app/taxonomy/regions.py`
- [ ] `app/matching/hard_filters.py`
- [ ] `app/matching/scoring_port.py`
- [ ] `app/scoring/` — WeightedDeterministicScorer
- [ ] `app/matching/match_service.py`
- [ ] `app/api/v1/matches.py`
- [ ] pytest for hard filter + one integration match

## Phase E — Auth (Day 9–10)

- [ ] Migration 002-style users + user_id on students
- [ ] `app/auth.py` — bcrypt, JWT, get_current_user
- [ ] `app/api/v1/auth_routes.py` — register, login, refresh
- [ ] `AUTH_DISABLED` for local dev
- [ ] `test_authz_isolation.py` — cross-user 403

## Phase F — Frontend (Day 11–14)

```bash
cd frontend
npm create vite@latest . -- --template react-ts
npm install react-router-dom tailwindcss @sentry/react
```

- [ ] `api/client.ts` — apiFetch, API_BASE_URL
- [ ] `contexts/AuthContext.tsx`
- [ ] Pages: Landing, Login, Register, ProfileBuilder, MatchResults
- [ ] `App.tsx` routes + layouts
- [ ] CORS on backend for `localhost:5173`

## Phase G — Production features (Day 15–20)

- [ ] Redis cache + rate limiting
- [ ] Sentry backend + frontend
- [ ] Docker compose local stack
- [ ] GitHub Actions CI
- [ ] Migrations through match_history, applications, saved (006–007, 015)
- [ ] Deploy Render + Vercel + Supabase per lesson 24

## Phase H — Graduation self-assessment

Rate yourself 1–5 on each goal:

| # | Goal | Score 1–5 | Evidence |
|---|------|-----------|----------|
| 1 | Rebuild from empty folder | | Capstone phases A–G |
| 2 | Explain architectural decisions | | Teach matching pipeline to peer |
| 3 | Understand important files | | Trace request without IDE |
| 4 | Debug production issues | | Tabletop incident from lesson 25 |
| 5 | Add features safely | | Ship small PR with tests |
| 6 | Maintain long-term | | Dependency update PR |
| 7 | Deploy and operate | | Staging deploy + health checks |
| 8 | Build without AI | | Phase C from memory |

**Graduation threshold:** Average ≥ 4, no goal below 3.

---

## Where to go next

- **CHED CMO 104 SIPP/OJT** — migration 025 tables, compliance vault
- **PSGC full integration** — replace string geo matching
- **Guardian consent workflow** — minor users (post-launch milestone)
- **Service layer extraction** — if routes grow past 200 lines

---

## Final exercises

### Level 4 — Architecture (capstone)

1. Execute Phase A–C entirely in a fresh folder named `iskonnect-rebuild-practice`.
2. Time yourself. Target: Phase A–C in < 8 hours by second attempt.

### Level 4 — Maintenance

1. Pick one file from `app/api/v1/`. Write a one-page audit: purpose, callers, risks, test coverage.

---

*Previous: [25 — Operations](25-operations-and-incident-response.md) | Home: [00 — Index](00-index.md)*

**Congratulations.** You have completed the Iskonnect From-Zero Apprenticeship curriculum.
