# Lesson 25 — Operations & Incident Response

> **Prerequisite:** [24 — Production Deployment](24-production-deployment.md)

---

## Monitoring stack

| Layer | Tool | What you watch |
|-------|------|----------------|
| Errors | Sentry | Stack traces, spike alerts |
| Logs | Render dashboard | Startup, request_id lines |
| Health | `/health`, `/ready` | DB, Redis, scraper status |
| Metrics | `/metrics` | Row counts, staging queue |
| DB | Supabase dashboard | Connections, disk, slow queries |

Guides: [`OBSERVABILITY.md`](../../OBSERVABILITY.md), [`MONITORING_GUIDE.md`](../../MONITORING_GUIDE.md)

---

## Sentry alert rule

- **Condition:** >10 events in 5 minutes
- **Filter:** `environment:production`
- **Action:** Email/Slack on-call

Single 404s should not page you — spikes should.

---

## Incident response playbook

### 1. Detect

- User report + `request_id`
- Sentry alert
- Render health check failing
- Uptime monitor (optional)

### 2. Triage (5 min)

| Check | Command/action |
|-------|----------------|
| API up? | `curl /health` |
| Recent deploy? | Render deploy history |
| DB up? | Supabase status page |
| Redis? | health `cache` field |

### 3. Mitigate

- **Bad deploy:** Rollback to previous Render/Vercel build
- **DB migration failure:** Stop traffic, see backup runbook
- **Rate limit storm:** Identify IP, adjust limits, enable Redis
- **DDoS/abuse:** Cloudflare/WAF, tighten rate limits

### 4. Resolve

- Fix root cause in code
- Add regression test
- Deploy through CI
- Post-incident note (what, why, prevention)

### 5. Communicate

Status page or social post if user-facing outage > 15 min.

---

## Backups & rollback

[`BACKUP_ROLLBACK.md`](../../BACKUP_ROLLBACK.md)

### Daily

Confirm Supabase automatic backups enabled. Pro plan: **PITR** (point-in-time recovery).

### App-only rollback

1. Redeploy previous build
2. `/health` + smoke tests

### Bad migration rollback

1. Stop traffic
2. PITR restore to new DB instance OR `alembic downgrade` if safe
3. Fix migration, test CI migrate job
4. Redeploy

**Never** `downgrade` on production without tested downgrade script.

---

## Scaling

### Current bottlenecks

| Resource | Symptom | Action |
|----------|---------|--------|
| CPU | Slow matches | More gunicorn workers (memory tradeoff) |
| DB connections | `too many connections` | Lower pool_size, use Supabase pooler |
| Memory | OOM kill | Reduce workers, slim payloads |
| Render cold start | 30s first request | Paid plan, warmup ping |

### Connection pooling

[`app/db.py`](../../../app/db.py) — `pool_size`, `max_overflow`, `pool_recycle=300`.

**Formula:** `workers × pool_size` must stay under Supabase connection limit.

---

## Scheduled jobs

| Workflow | Schedule |
|----------|----------|
| `scraper.yml` | Mon/Thu |
| `deadline-maintenance.yml` | Daily |
| `retention-cleanup.yml` | Weekly |

Require GitHub secret `DATABASE_URL`.

---

## Security operations

- Rotate `SECRET_KEY` only with forced re-login plan
- Audit `AUTH_DISABLED` never in production env
- Review Sentry for PII leaks
- Keep dependencies updated (`pip audit`, `npm audit`)

---

## Exercises

### Level 1 — Understanding

1. `/health` vs `/ready`?
2. What is PITR?

### Level 2 — Implementation

1. Find a Sentry issue (or simulate) and trace `request_id` in logs.

### Level 3 — Debugging

1. Tabletop: "All users 503" — write first three commands you run.

### Level 4 — Architecture

1. Design status page architecture for Iskonnect MVP.

<details>
<summary>Solution</summary>

health: deep checks DB/redis. ready: can serve traffic. PITR: restore DB to any second in window. Commands: curl health, check Render status, check Supabase. Status: external uptime on /health, cached incident JSON on static page or third-party (Instatus).
</details>

---

*Previous: [24 — Deployment](24-production-deployment.md) | Next: [26 — Capstone](26-maintenance-and-rebuild-capstone.md)*
