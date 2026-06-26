# Lesson 24 — Production Deployment

> **Prerequisite:** [23 — CI/CD & Docker](23-ci-cd-and-docker.md)

---

## Architecture overview

```mermaid
flowchart LR
  User[User browser] --> DNS[DNS iskonnect.ph]
  DNS --> Vercel[Vercel CDN SPA]
  Vercel -->|VITE_API_BASE_URL| Render[Render Web Service]
  Render --> Supabase[(Supabase Postgres)]
  Render --> RedisCloud[(Redis)]
  Render --> Sentry[Sentry]
```

**Split hosting:** Static frontend on Vercel (free tier, global CDN). Python API on Render (long-running process). Database on Supabase (managed Postgres).

Full checklist: [`docs/DEPLOYMENT.md`](../../DEPLOYMENT.md)

---

## Deploy order (critical)

1. **Vercel first** — get `https://your-app.vercel.app`
2. **Render second** — set `CORS_ORIGINS` to Vercel URL
3. **Vercel env** — set `VITE_API_BASE_URL` to Render URL, **redeploy**

Wrong order → CORS errors or frontend pointing to localhost.

---

## Supabase setup

### 1. Create project

Dashboard → New project → region (Singapore closest to PH users).

### 2. Connection string

**Settings → Database → Connection string → URI**

Use **pooler** URL for serverless/long connections:

```
postgresql+psycopg2://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres?sslmode=require
```

**Why `sslmode=require`:** Encrypt data in transit.

### 3. Run migrations locally first

```bash
export DATABASE_URL="postgresql+psycopg2://..."
alembic upgrade head
```

### 4. What Supabase is NOT used for

**Supabase Auth** — Iskonnect uses custom JWT in FastAPI. Supabase = Postgres host + backups + dashboard.

---

## Render (backend)

| Setting | Value |
|---------|-------|
| Runtime | Python 3.11 (`.python-version`) |
| Build | `pip install -r requirements.txt` |
| Start | `gunicorn ...` or Procfile |
| Release | `alembic upgrade head` |
| Health check path | `/health` |

### Required environment variables

| Variable | Example |
|----------|---------|
| `DATABASE_URL` | Supabase pooler URI |
| `SECRET_KEY` | `openssl rand -hex 32` |
| `ENVIRONMENT` | `production` |
| `AUTH_DISABLED` | `false` |
| `CORS_ORIGINS` | `https://your-app.vercel.app` |
| `REDIS_URL` | Redis provider URL |
| `RUN_MIGRATIONS_ON_STARTUP` | `false` |
| `SENTRY_DSN` | Sentry project DSN |

**`validate_for_production()`** in [`app/config.py`](../../../app/config.py) fails startup if `SECRET_KEY` is default or auth disabled.

---

## Vercel (frontend)

| Setting | Value |
|---------|-------|
| Root directory | `frontend` |
| Framework | Vite |
| Build | `npm run build` |
| Output | `dist` |

### Environment variables (public)

| Variable | Value |
|----------|-------|
| `VITE_API_BASE_URL` | `https://your-api.onrender.com` (no trailing slash) |
| `VITE_SENTRY_DSN` | optional |
| `VITE_SENTRY_ENVIRONMENT` | `production` |
| `VITE_SENTRY_RELEASE` | git SHA |

**Never** put `SECRET_KEY` or `DATABASE_URL` on Vercel.

---

## DNS & SSL

### Custom domain (e.g. `iskonnect.ph`)

1. Buy domain at registrar
2. **Vercel:** add domain → copy DNS records (CNAME/A)
3. **Render:** add custom domain for API subdomain (`api.iskonnect.ph`)
4. SSL certificates auto-provisioned (Let's Encrypt)

### DNS record types

| Type | Purpose |
|------|---------|
| **A** | Points apex domain to IP |
| **CNAME** | Points subdomain to another hostname |
| **TXT** | Verification, SPF for email |

**Propagation:** 5 minutes to 48 hours.

---

## Email delivery

Registration verification and password reset use SMTP or transactional email provider configured in backend env (see `app/utils/email.py`).

**Production:** Use dedicated provider (Resend, SendGrid, etc.) — not personal Gmail.

---

## Post-deploy smoke test

```bash
curl https://YOUR_API/health
curl https://YOUR_API/ready
```

Browser:

1. Register new account
2. Verify email (if enabled)
3. Complete profile
4. Run matches
5. Save a scholarship

---

## Exercises

### Level 1 — Understanding

1. Why deploy Vercel before Render CORS?
2. Pooler vs direct Postgres port?

### Level 2 — Implementation

1. Deploy to free tier staging with test names — document URLs in learning log.

### Level 3 — Debugging

1. Browser CORS error — list three misconfigurations to check.

### Level 4 — Architecture

1. Draw env var flow: which vars exist only on Render, only on Vercel, only in GitHub Secrets.

<details>
<summary>Solution</summary>

Need frontend URL before CORS_ORIGINS. Pooler (6543) handles connection multiplexing for many workers. CORS: wrong origin, missing https, typo trailing slash mismatch. Render: DATABASE_URL, SECRET_KEY, REDIS_URL. Vercel: VITE_*. GitHub: DATABASE_URL for scraper workflows.
</details>

---

*Previous: [23 — CI/CD](23-ci-cd-and-docker.md) | Next: [25 — Operations & Incident Response](25-operations-and-incident-response.md)*
