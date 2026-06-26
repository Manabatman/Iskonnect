# Iskonnect Production Operations Handbook

> **Purpose:** Teach you to deploy, operate, debug, and scale Iskonnect in production — from an empty computer to confident founder-operator — using **only** the architecture that exists in this repository today.

**Repository root:** `scholarship-match/`  
**Live stack (ground truth):** Vercel (frontend) · Render (FastAPI + gunicorn) · Supabase (Postgres) · Redis · GitHub Actions (CI + crons) · SMTP (email) · Sentry (errors)

---

## How to read this handbook

1. **Read Parts 1–4 in order** the first time. Later parts assume you understand architecture, deployment, verification, and DNS.
2. **Do every exercise** before skipping ahead. Mastery comes from running commands yourself.
3. **Open cited files** in your editor while reading. This is a map of a real codebase, not abstract theory.
4. **Keep a log** of what you deployed, every URL, every env var, and every password (in a password manager — never in git).
5. **Cross-link, don't duplicate:** Deep backend/frontend lessons live in [apprenticeship curriculum](../learning/apprenticeship/00-index.md). This handbook focuses on **production operations**.

### Seven teaching rules (used in every section)

For every action in this handbook you will find:

| # | Question | Why it matters |
|---|----------|----------------|
| 1 | **What** are we doing? | You must know the step before you run it. |
| 2 | **Why** are we doing it? | Steps without reasons are forgotten under stress. |
| 3 | **What breaks** if we skip it? | Production failures are usually skipped steps. |
| 4 | **Alternatives?** | Trade-offs make you a better engineer. |
| 5 | **How did engineers discover this?** | History explains "weird" conventions. |
| 6 | **How do we verify** it worked? | Deploy without verify = hope, not engineering. |
| 7 | **How do we troubleshoot** it? | Incidents happen; runbooks save sleep. |

### Command Apprenticeship Mode

The **first time** each command family appears, you get a full breakdown:

- Syntax breakdown
- Example output (line by line)
- Real-world analogy
- Common mistakes
- Alternatives
- When engineers use it
- **Windows PowerShell** variant where different from bash

Subsequent parts cross-reference the first appearance. See [Command reference (first appearances)](#command-reference-first-appearances) below.

---

## Table of contents

| Part | File | What you will master |
|------|------|----------------------|
| **1** | [01-architecture.md](01-architecture.md) | Production topology, request lifecycle, auth/email/redis/matching/scraper/monitoring flows |
| **2** | [02-deployment.md](02-deployment.md) | Empty computer → accounts → dashboard deploy of every component |
| **3** | [03-verification.md](03-verification.md) | curl, health checks, logs, DB checks after every deploy step |
| **4** | [04-domains-and-dns.md](04-domains-and-dns.md) | Buy domain, DNS records, SSL, connect Vercel + Render |
| **5** | [05-testing-production.md](05-testing-production.md) | Registration, login, matching, admin, scraper, authz, rate limits |
| **6** | [06-data-pipeline.md](06-data-pipeline.md) | Source → scraper → staging → approval → match → recommendation |
| **7** | [07-operations.md](07-operations.md) | Deploy updates, rollback, outages, incident runbooks |
| **8** | [08-observability.md](08-observability.md) | Logging, Sentry, metrics, alerts, healthy vs broken |
| **9** | [09-scaling.md](09-scaling.md) | 100 → 100k users: bottlenecks, costs, infra changes |
| **10** | [10-founder-operator-handbook.md](10-founder-operator-handbook.md) | Daily / weekly / monthly operator checklists |

---

## Graduation goals

By the end of Part 10 you should be able to:

1. Deploy Iskonnect from scratch on Vercel + Render + Supabase + Redis.
2. Explain every deployment decision and env var.
3. Debug production issues without AI assistance.
4. Operate the platform daily with confidence.
5. Scale responsibly as users grow.
6. Trace a scholarship from PhilScholar to a student's match results.

---

## Glossary

| Term | Definition | First deep dive |
|------|------------|-----------------|
| **SPA** | Single Page Application — one HTML shell, JavaScript handles navigation | [Part 1](01-architecture.md) |
| **API** | Application Programming Interface — programs talking over HTTP | [Part 1](01-architecture.md) |
| **ASGI** | Async Server Gateway Interface — Python standard for async web servers | [Part 1](01-architecture.md) |
| **CORS** | Cross-Origin Resource Sharing — browser security for API calls from another domain | [Part 1](01-architecture.md) |
| **JWT** | JSON Web Token — signed blob carrying user identity (custom auth, not Supabase Auth) | [Part 1](01-architecture.md) |
| **ORM** | Object-Relational Mapper — Python classes ↔ database tables (SQLAlchemy) | [Part 6](06-data-pipeline.md) |
| **Migration** | Versioned script that changes DB schema (Alembic) | [Part 2](02-deployment.md) |
| **Pooler** | Supabase connection proxy — many app connections share few DB connections | [Part 2](02-deployment.md) |
| **Release command** | Script run **before** new code goes live (here: `alembic upgrade head`) | [Part 2](02-deployment.md) |
| **Hard filter** | Stage 1 rule that completely excludes a scholarship | [Part 6](06-data-pipeline.md) |
| **Scoring** | Stage 2 weighted ranking of survivors | [Part 6](06-data-pipeline.md) |
| **Staging** | `scholarships_staging` table — scraped rows awaiting admin approval | [Part 6](06-data-pipeline.md) |
| **dedupe_key** | Hash key preventing duplicate staging rows | [Part 6](06-data-pipeline.md) |
| **Cold start** | Render spins down idle services; first request is slow | [Part 1](01-architecture.md) |
| **PITR** | Point-in-Time Recovery — restore DB to a specific moment | [Part 7](07-operations.md) |

---

## Repository map (production-relevant)

```
scholarship-match/
├── app/
│   ├── main.py              # FastAPI entry, /health, /ready, /metrics, middleware
│   ├── config.py            # Env vars + validate_for_production() guard
│   ├── auth.py              # JWT + bcrypt (NOT Supabase Auth)
│   ├── db.py                # SQLAlchemy engine + get_db()
│   ├── models.py            # ORM tables
│   ├── limiter.py           # slowapi rate limiter (Redis or memory)
│   ├── scholarship_cache.py # Redis scholarship list cache
│   ├── api/v1/              # HTTP route handlers
│   ├── matching/            # Stage 1 hard filters + orchestration
│   ├── scoring/             # Stage 2 weighted scorer
│   ├── scrapers/            # PhilScholar scraper
│   ├── scripts/             # ingest_scraped, import_scholarships, create_admin
│   └── jobs/                # catalog_maintenance, retention, link_checker
├── alembic/                 # Migrations 001–025+
├── frontend/
│   ├── vercel.json          # SPA rewrite rules
│   └── src/
│       ├── main.tsx         # Sentry init
│       ├── api/client.ts    # HTTP client → VITE_API_BASE_URL
│       └── contexts/AuthContext.tsx
├── Procfile                 # release + gunicorn web (AUTHORITATIVE for Render)
├── Dockerfile               # Container image (gunicorn + healthcheck)
├── docker-compose.yml       # Local Postgres + Redis + API
├── .env.example             # All env var documentation
└── .github/workflows/       # ci.yml, scraper.yml, deadline-maintenance.yml
```

---

## Authoritative production configuration

`app/config.py` → `validate_for_production()` is the **single source of truth** for required production env vars. If any check fails, the API **refuses to start**.

| Variable | Required in production | Purpose |
|----------|------------------------|---------|
| `ENVIRONMENT` | `production` | Enables production guards |
| `SECRET_KEY` | Non-default random hex | JWT signing |
| `AUTH_DISABLED` | `false` | JWT required on routes |
| `DATABASE_URL` | Postgres (Supabase pooler) | Data store |
| `CORS_ORIGINS` | At least one non-localhost URL | Browser API access |
| `SMTP_HOST` + `EMAIL_FROM` | Both set | Verification + password reset emails |
| `FRONTEND_URL` | Non-localhost URL | Links inside emails |
| `RUN_MIGRATIONS_ON_STARTUP` | `false` | Use release command instead |
| `REDIS_URL` | Set | Shared rate limits + cache across workers |
| `TRUST_PROXY_HEADERS` | `true` | Real client IP behind Render proxy |

Full deploy table: [Part 2 — Environment variables](02-deployment.md#environment-variables-complete-checklist).

---

## Doc corrections (read this before older docs)

Some older files in the repo are **slightly out of date**. This handbook is authoritative.

| File | Issue | Correct value |
|------|-------|---------------|
| [docs/DEPLOYMENT.md](../DEPLOYMENT.md) | Start command shows `uvicorn` | Use **gunicorn** from [Procfile](../../Procfile): `gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w ${WEB_CONCURRENCY:-2} ...` |
| [docs/HANDBOOK.md](../HANDBOOK.md) | Same uvicorn mention | Same correction |
| [render.yaml](../../render.yaml) | Marked **DEPRECATED** (line 1) | Deploy via Render **dashboard** + Supabase Postgres, not this blueprint |
| [docs/DEPLOYMENT.md](../DEPLOYMENT.md) | Node 22 in CI note | CI uses Node **24** per `.github/workflows/ci.yml` |
| Supabase in this repo | Hosted Postgres only | Auth is **custom JWT** in `app/auth.py`, NOT Supabase Auth |

---

## Related existing docs

| Doc | Role |
|-----|------|
| [DEPLOYMENT.md](../DEPLOYMENT.md) | Short deploy checklist (superseded in detail by Part 2) |
| [DEPLOYMENT_CHECKLIST.md](../DEPLOYMENT_CHECKLIST.md) | Post-deploy smoke tests (expanded in Part 5) |
| [HANDBOOK.md](../HANDBOOK.md) | Beginner mental model (expanded in Part 1) |
| [OBSERVABILITY.md](../OBSERVABILITY.md) | Sentry setup (expanded in Part 8) |
| [MONITORING_GUIDE.md](../MONITORING_GUIDE.md) | Monitoring overview (expanded in Part 8) |
| [BACKUP_ROLLBACK.md](../BACKUP_ROLLBACK.md) | Backup/rollback (expanded in Part 7) |
| [apprenticeship/00-index.md](../learning/apprenticeship/00-index.md) | Code-deep curriculum (lessons 01–26) |

---

## Command reference (first appearances)

Commands are taught in full at these locations:

| Family | First full lesson | Also used in |
|--------|-------------------|--------------|
| **Terminal** (`pwd`, `cd`, `ls`, `mkdir`) | [Part 2 — Prerequisites](02-deployment.md#prerequisites-from-empty-computer) | Parts 3, 6, 7 |
| **Git** (`clone`, `add`, `commit`, `push`, `branch`) | [Part 2 — Git setup](02-deployment.md#git-setup) | Part 7 |
| **Python** (`python`, `pip`, `venv`) | [Part 2 — Python](02-deployment.md#python-311) | Parts 3, 6 |
| **Node** (`npm install`, `npm run build`) | [Part 2 — Node.js](02-deployment.md#nodejs-24) | Part 3 |
| **Docker** (`build`, `run`, `logs`) | [Part 2 — Docker](02-deployment.md#docker-optional-but-recommended) | Part 3 |
| **Alembic** (`upgrade`, `revision`) | [Part 2 — Migrations](02-deployment.md#run-database-migrations) | Parts 6, 7 |
| **psql** | [Part 3 — Database checks](03-verification.md#database-verification) | Parts 5, 7 |
| **curl** | [Part 3 — API verification](03-verification.md#api-health-checks) | Parts 5, 7, 8 |
| **uvicorn** (local dev only) | [Part 2 — Local dev](02-deployment.md#local-development-quick-start) | — |
| **gunicorn** (production) | [Part 1 — Backend flow](01-architecture.md#backend-request-flow) | Part 2 |
| **grep**, **ps**, **netstat** | [Part 7 — Debugging](07-operations.md#debugging-toolkit) | Part 8 |

---

## Suggested study pace

| Parts | Focus | Suggested time |
|-------|-------|----------------|
| 1–2 | Understand + deploy | 3–5 days |
| 3–4 | Verify + domain | 1–2 days |
| 5–6 | Test + data pipeline | 2–3 days |
| 7–8 | Operate + observe | 2–3 days |
| 9–10 | Scale + daily habits | 1–2 days |

---

*Next: [Part 1 — Architecture](01-architecture.md)*
