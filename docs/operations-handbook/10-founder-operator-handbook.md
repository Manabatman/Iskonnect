# Part 10 — Founder Operator Handbook

> Daily, weekly, and monthly rituals so Iskonnect stays healthy without AI assistance.

This is your **operating cadence** — print it, bookmark it, follow it.

---

## Role definition: founder-operator

You are simultaneously:
- **CEO** — product direction, user feedback
- **SRE** — uptime, incidents, deploys
- **Data steward** — scholarship catalog quality
- **Support** — first responder to user issues

This handbook prioritizes **high-signal, low-time** checks.

---

## Daily checklist (~10 minutes)

### Morning health check

| # | Task | Command / location | Healthy |
|---|------|-------------------|---------|
| 1 | API uptime | UptimeRobot dashboard | Green |
| 2 | Health endpoint | `curl.exe -s https://YOUR_API/health` | `"status":"ok"`, `"db":true` |
| 3 | Error spike | Sentry → Issues (last 24h) | No new critical |
| 4 | Metrics snapshot | `curl.exe -s https://YOUR_API/metrics` | Counts stable or growing |
| 5 | Render logs skim | Render → Logs → last 50 lines | No `unhandled_exception` |

**PowerShell one-liner (save as `daily-check.ps1`):**
```powershell
$api = "https://YOUR_API.onrender.com"
Write-Host "=== Health ===" -ForegroundColor Cyan
curl.exe -s "$api/health" | ConvertFrom-Json | ConvertTo-Json
Write-Host "`n=== Metrics ===" -ForegroundColor Cyan
curl.exe -s "$api/metrics" | ConvertFrom-Json | ConvertTo-Json
Write-Host "`n=== HTTP Status ===" -ForegroundColor Cyan
curl.exe -s -o NUL -w "health: %{http_code}`n" "$api/health"
```

**Expected health output:**
```json
{
  "status": "ok",
  "checks": {
    "db": true,
    "cache": true,
    "scraper_last": { "source": "philscholar", "status": "success", ... }
  }
}
```

### User-facing quick test (2 min)

| # | Action | Pass criteria |
|---|--------|---------------|
| 1 | Open homepage | Loads < 5s |
| 2 | Login as test user | Dashboard appears |
| 3 | Scholarship search | Results return |

### If anything fails

→ [Part 7 — Operations](07-operations.md) runbooks

---

## Daily: dashboards to inspect

| Dashboard | URL | Look for |
|-----------|-----|----------|
| UptimeRobot | uptimerobot.com | Downtime events |
| Render | dashboard.render.com | Deploy status, log errors |
| Sentry | sentry.io | New issues count |
| Supabase | supabase.com/dashboard | Project active (not paused) |

### Admin UI daily (if staging active)

1. Login as admin → `/admin`
2. **System** tab → raw `/health` JSON
3. **Staging** → pending count — approve or reject new rows
4. **Reports** → unresolved scholarship issue reports

---

## Weekly checklist (~30 minutes)

### Monday: data and catalog

| # | Task | How | Action if bad |
|---|------|-----|---------------|
| 1 | Scraper ran | GitHub Actions → scraper workflow | Manual run |
| 2 | Staging queue | `SELECT COUNT(*) FROM scholarships_staging WHERE status='pending'` | Approve batch |
| 3 | Active scholarships | `/metrics` → scholarships count | Investigate if dropped |
| 4 | Expired programs | `SELECT COUNT(*) FROM scholarships WHERE data_status='expired'` | Expected growth OK |
| 5 | Dead links | Admin reports tab | Deactivate or fix |

### Wednesday: users and engagement

| # | Task | SQL / location |
|---|------|----------------|
| 1 | New users this week | `SELECT COUNT(*) FROM users WHERE created_at > NOW() - INTERVAL '7 days'` |
| 2 | Match activity | `SELECT COUNT(*) FROM match_runs WHERE created_at > NOW() - INTERVAL '7 days'` |
| 3 | Feedback | Admin → Feedback tab |
| 4 | Top errors | Sentry → sort by frequency |

### Friday: security and deploy hygiene

| # | Task | Pass |
|---|------|------|
| 1 | CI green on main | GitHub Actions all ✓ |
| 2 | Dependencies | No critical CVE alerts (GitHub Dependabot) |
| 3 | Secrets not rotated accidentally | Login still works |
| 4 | Backup exists | Supabase → Backups → recent snapshot |
| 5 | Review deploy diff | `git log --oneline -10` — anything unexpected? |

### Weekly commands

```powershell
# From repo root — run test suite locally
python -m pytest app/tests/ -q --tb=no

# Check alembic matches production
alembic current

# Git: what shipped this week
git log --oneline --since="7 days ago"
```

---

## Monthly checklist (~2 hours)

### Infrastructure and cost

| # | Task | Details |
|---|------|---------|
| 1 | Review bills | Render, Supabase, Vercel, Upstash, domain, email |
| 2 | Supabase disk usage | Dashboard → Settings → Usage |
| 3 | Upgrade decision | See [Part 9 — Scaling](09-scaling.md) |
| 4 | SSL certificates | Auto-renew OK? (Vercel/Render dashboards) |
| 5 | Domain renewal | Registrar — renew if expiring < 60 days |

### Data quality audit

```sql
-- Duplicate links in live catalog
SELECT LOWER(TRIM(link)), COUNT(*) 
FROM scholarships 
WHERE link IS NOT NULL AND link != ''
GROUP BY 1 HAVING COUNT(*) > 1;

-- Scholarships with no provider
SELECT COUNT(*) FROM scholarships WHERE provider IS NULL OR provider = '';

-- Staging backlog age
SELECT MIN(created_at), MAX(created_at), COUNT(*) 
FROM scholarships_staging WHERE status = 'pending';

-- Inactive users (retention job input)
SELECT COUNT(*) FROM users 
WHERE last_login_at < NOW() - INTERVAL '365 days';
```

### Security monthly

| # | Task |
|---|------|
| 1 | Confirm `AUTH_DISABLED=false` on Render |
| 2 | Confirm no secrets in git (`git log -p` search for passwords) |
| 3 | Review admin accounts — remove ex-team members |
| 4 | Rotate `SMTP_PASSWORD` if provider recommends |
| 5 | Review Sentry for PII leaks in error messages |

### Metrics analysis (month over month)

Track in a spreadsheet:

| Metric | This month | Last month | Trend |
|--------|------------|------------|-------|
| Total users | | | |
| Match runs | | | |
| Active scholarships | | | |
| Staging approved | | | |
| Sentry issues | | | |
| Uptime % | | | |
| Avg API response (subjective) | | | |

### Maintenance tasks

| Task | Schedule | Workflow |
|------|----------|----------|
| Deadline maintenance | Daily (automated) | `deadline-maintenance.yml` |
| Scraper | Mon/Thu (automated) | `scraper.yml` |
| Retention cleanup | Weekly (automated) | `retention-cleanup.yml` |
| Dependency updates | Monthly (manual) | `pip` / `npm audit fix` |
| Alembic migration review | As needed | Before any schema change |

### Backup verification (monthly)

1. Supabase → Database → Backups → confirm recent backup
2. Document recovery window (7 days free / longer on Pro)
3. Optional: restore to **staging project** quarterly (drill)

See [BACKUP_ROLLBACK.md](../BACKUP_ROLLBACK.md).

---

## Incident response quick card

```
1. ACKNOWLEDGE — note time, symptoms
2. CHECK /health — 200 or 503?
3. CHECK Render logs — last 10 min
4. CHECK Supabase — project paused?
5. MITIGATE — rollback deploy OR fix env var OR resume Supabase
6. VERIFY — smoke tests from Part 5
7. COMMUNICATE — update users if > 15 min outage
8. POSTMORTEM — within 48 hours
```

---

## Operator calendar (at a glance)

| When | What |
|------|------|
| **Daily** | Uptime, /health, /metrics, Sentry skim, homepage login test |
| **Mon weekly** | Scraper, staging queue, catalog counts |
| **Wed weekly** | Users, matches, feedback |
| **Fri weekly** | CI, backups, git log review |
| **Monthly** | Bills, disk, security, metrics spreadsheet, backup drill |
| **Mon/Thu** | Scraper runs automatically — verify in Actions |
| **Daily 03:00 PHT** | Deadline maintenance (automated) |

---

## Commands cheat sheet (operator edition)

```powershell
# Health
curl.exe -s https://YOUR_API/health

# Metrics
curl.exe -s https://YOUR_API/metrics

# Ready
curl.exe -s https://YOUR_API/ready

# Login (get token)
curl.exe -s -X POST https://YOUR_API/api/v1/auth/login -H "Content-Type: application/json" -d "{\"email\":\"...\",\"password\":\"...\"}"

# Run tests before risky change
python -m pytest app/tests/ -q

# Migration status
alembic current

# Local stack
docker compose up --build

# Frontend build verify
cd frontend; npm run build
```

---

## Graduation: you are ready when you can...

- [ ] Deploy from empty computer without this doc open (but keep it for reference)
- [ ] Explain why gunicorn not uvicorn in production
- [ ] Read `/health` JSON and know what's wrong from each field
- [ ] Trace a scholarship from scraper to match result naming every file
- [ ] Roll back a bad deploy in under 10 minutes
- [ ] Respond to "matches are wrong" with a structured investigation
- [ ] Know when to upgrade from free tier before users complain
- [ ] Complete daily checklist in under 10 minutes

---

## Where to go next

| Need | Resource |
|------|----------|
| Code-deep learning | [apprenticeship curriculum](../learning/apprenticeship/00-index.md) |
| Short deploy reference | [DEPLOYMENT.md](../DEPLOYMENT.md) |
| Post-deploy smoke tests | [DEPLOYMENT_CHECKLIST.md](../DEPLOYMENT_CHECKLIST.md) |
| Scoring internals | [SCORING_ENGINE.md](../../SCORING_ENGINE.md) |

---

*Previous: [Part 9 — Scaling](09-scaling.md) · [Back to Index](00-index.md)*
