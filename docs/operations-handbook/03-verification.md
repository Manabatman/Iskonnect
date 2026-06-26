# Part 3 — How to Verify Everything

> After every deployment step, **prove** it worked. Hope is not a strategy.

This part teaches verification commands in **Command Apprenticeship** depth. Cross-reference: first appearances are here for `curl` and `psql`.

---

## Verification mindset

| Question | Tool |
|----------|------|
| Is the API alive? | `curl /health` |
| Is the database reachable? | `/health` → `db: true` or `psql` |
| Is Redis working? | `/health` → `cache: true` |
| Is the frontend built correctly? | Open Vercel URL |
| Did migrations apply? | Supabase Table Editor or `alembic current` |
| Are env vars correct? | Render/Vercel dashboard + startup logs |

---

## `curl` — Command Apprenticeship (first appearance)

**What:** Command-line tool to make HTTP requests.

**Why:** Test API without browser; scriptable; shows raw status codes and headers.

**Install (Windows):** Built into Windows 10+ PowerShell as `curl.exe` (alias). Or use `Invoke-WebRequest`.

**Syntax:** `curl [options] <URL>`

| Flag | Meaning |
|------|---------|
| `-s` | Silent (hide progress meter) |
| `-S` | Show errors even in silent mode |
| `-i` | Include response headers |
| `-o` | Write body to file |
| `-w "%{http_code}"` | Print only status code |
| `-H "Header: value"` | Add request header |
| `-X POST` | HTTP method |
| `-d '{"key":"val"}'` | Request body |

**PowerShell equivalent:**
```powershell
Invoke-RestMethod -Uri "https://api.example.com/health"
Invoke-WebRequest -Uri "https://api.example.com/health" -UseBasicParsing
```

**Analogy:** `curl` is like knocking on a door and reading the answer slip — without walking through the whole building (browser).

**Common mistakes:**
- Forgetting `https://`
- Trailing slash causing redirect loops
- PowerShell `curl` alias pointing to `Invoke-WebRequest` with different syntax — use `curl.exe` for consistency

**When engineers use it:** Every deploy; every incident; CI smoke tests.

---

## API health checks

Replace `YOUR_API` with your Render URL (e.g. `https://iskonnect-api.onrender.com`).

### `GET /health`

**What we're doing:** Checking API + DB + Redis + last scraper run.

**Why:** UptimeRobot uses this; returns 503 if DB is down.

**Command:**
```powershell
curl.exe -s https://YOUR_API/health
```

**Expected (healthy):**
```json
{
  "status": "ok",
  "checks": {
    "db": true,
    "cache": true,
    "scraper_last": null
  }
}
```

**Line-by-line meaning:**
| Field | Meaning |
|-------|---------|
| `status: "ok"` | Core dependency (DB) is up |
| `checks.db: true` | `SELECT 1` succeeded |
| `checks.cache: true` | Redis PING succeeded |
| `scraper_last: null` | No scraper run logged yet (OK on fresh deploy) |

**HTTP status:** Must be **200**. If **503**, DB is down.

**Verify status code only:**
```powershell
curl.exe -s -o NUL -w "%{http_code}" https://YOUR_API/health
```
**Expected:** `200`

**What breaks if skipped:** You won't know DB credential errors until users report empty data.

**Troubleshoot 503:**
1. Render logs → search `health_db_check_failed`
2. Verify `DATABASE_URL` in Render env
3. Supabase dashboard → project not paused
4. Test connection from local machine with same URI

---

### `GET /ready`

**What:** Stricter readiness probe (DB only).

**Command:**
```powershell
curl.exe -s https://YOUR_API/ready
```

**Expected:**
```json
{"status": "ready"}
```

**HTTP 503 expected when:** Database unreachable.

---

### `GET /metrics`

**What:** Lightweight operational counters.

**Why:** Quick sanity check on data volume.

**Command:**
```powershell
curl.exe -s https://YOUR_API/metrics
```

**Expected (example):**
```json
{
  "scholarships": 150,
  "users": 12,
  "staging_pending": 3
}
```

**Security note:** Publicly exposed — consider restricting by IP on paid plans if counts are sensitive.

**Healthy signals:**
- `scholarships` > 0 after data import
- `staging_pending` reasonable after scraper runs

---

## Verify each deployment component

### After Supabase setup

| Check | How | Expected |
|-------|-----|----------|
| Project active | Supabase dashboard | Green status |
| Tables exist | Table Editor | `users`, `scholarships`, `alembic_version` |
| Pooler works | `alembic upgrade head` locally | No SSL/connection errors |

---

### After migrations

**Command:**
```powershell
alembic current
```

**Expected output:**
```
025_xxx (head)
```

**Meaning:** Database schema matches latest revision.

**Supabase verify:** Table Editor → `alembic_version` → one row with version num.

---

### After Redis setup

| Check | How | Expected |
|-------|-----|----------|
| Redis reachable | `/health` → `cache: true` | Not `false` or `not_configured` |
| Upstash dashboard | Metrics tab | Commands incrementing |

**Degraded but running:** If `cache: false` but `status: ok`, API still serves requests (cache falls back to per-process memory) — fix Redis before launch since production guard requires `REDIS_URL` at startup.

---

### After Render deploy

| Check | Where | Expected |
|-------|-------|----------|
| Build succeeded | Render → Events | Green "Deploy live" |
| Release command | Render → Logs | `Running upgrade -> 025` |
| Workers booted | Logs | `Booting worker with pid` × WEB_CONCURRENCY |
| Startup config | Logs | `[startup] environment=production` |
| No config error | Logs | No `Invalid production configuration` |

**Log search phrases:**
```
[startup] environment=production
Booting worker
Invalid production configuration  ← BAD
alembic_upgrade_on_startup_failed  ← BAD in production
```

---

### After Vercel deploy

| Check | How | Expected |
|-------|-----|----------|
| Build succeeded | Vercel → Deployments | Ready ✓ |
| Site loads | Browser | Login page, no blank screen |
| API URL baked in | DevTools → Sources → search `onrender.com` | Your Render host present |
| No localhost in prod | Same search | No `localhost:8000` |

**Command (build locally to verify):**
```powershell
cd frontend
$env:VITE_API_BASE_URL = "https://YOUR_API.onrender.com"
npm run build
```

**Expected:** Build completes; `dist/` contains JS with API URL embedded.

---

### After CORS wiring

**Browser test:**
1. Open Vercel URL
2. F12 → Console
3. Attempt login or any API call

**Healthy:** Network tab shows `200` responses from Render.

**Broken:** Red CORS error:
```
Access to fetch at 'https://api...' from origin 'https://app...' has been blocked by CORS policy
```

**Fix:** `CORS_ORIGINS` must match **exact** origin including `https://`, no trailing slash.

---

### After SMTP setup

| Check | How | Expected |
|-------|-----|----------|
| Register new user | App UI | 200 response |
| Email received | Inbox (check spam) | Verification link |
| Render logs | Search `smtp` or `email` | No authentication errors |

**curl register test:**
```powershell
curl.exe -s -X POST https://YOUR_API/api/v1/auth/register `
  -H "Content-Type: application/json" `
  -d '{"email":"test-verify@example.com","password":"TestPass123!"}'
```

**Expected:** JSON with `detail` message (may include tokens for new user).

---

### After GitHub Actions secret

| Check | How | Expected |
|-------|-----|----------|
| Secret exists | Settings → Secrets | `DATABASE_URL` listed |
| Manual workflow run | Actions → Scraper → Run workflow | Green ✓ |
| Staging rows | Supabase → `scholarships_staging` | New pending rows OR skip file if unchanged |
| Scraper health | `/health` → `scraper_last` | Recent timestamp after run |

---

## Database verification

### `psql` — Command Apprenticeship (first appearance)

**What:** PostgreSQL interactive terminal client.

**Why:** Run SQL directly against Supabase for debugging.

**Install:** Comes with PostgreSQL client tools, or use Supabase **SQL Editor** in browser (easier for beginners).

**Syntax:** `psql "<connection_string>"`

**From Supabase dashboard (recommended):**
1. SQL Editor → New query
2. Run:

```sql
SELECT COUNT(*) AS scholarship_count FROM scholarships;
SELECT COUNT(*) AS user_count FROM users;
SELECT COUNT(*) AS pending_staging FROM scholarships_staging WHERE status = 'pending';
SELECT version_num FROM alembic_version;
```

**Expected:** Counts match `/metrics` endpoint.

**Common queries for verification:**

```sql
-- Active scholarships only
SELECT COUNT(*) FROM scholarships WHERE is_active = true;

-- Recent users
SELECT id, email, role, created_at FROM users ORDER BY created_at DESC LIMIT 5;

-- Last match run
SELECT id, student_id, created_at FROM match_runs ORDER BY created_at DESC LIMIT 1;

-- Last scraper run
SELECT source, status, started_at, records_found FROM scraper_runs ORDER BY started_at DESC LIMIT 1;
```

**Troubleshoot:** Permission denied → using wrong role; use pooler credentials from Supabase Connect panel.

---

## Authenticated API verification

### Login and get token

```powershell
$response = curl.exe -s -X POST https://YOUR_API/api/v1/auth/login `
  -H "Content-Type: application/json" `
  -d '{"email":"admin@yourdomain.com","password":"YourPassword"}'
echo $response
```

**Expected:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "...",
  "token_type": "bearer",
  "user_id": 1,
  "role": "admin"
}
```

### Call protected endpoint

```powershell
curl.exe -s https://YOUR_API/api/v1/scholarships `
  -H "Authorization: Bearer eyJ..."
```

**Expected:** JSON array of scholarships (may be paginated).

**401 means:** Token expired, wrong `SECRET_KEY` between deploys, or `AUTH_DISABLED` mismatch.

---

## Log inspection guide

### Render logs

**Where:** Render dashboard → your service → **Logs**

**What to look for:**

| Log pattern | Meaning |
|-------------|---------|
| `[startup] environment=production` | Good boot |
| `[request_id] GET /health 200` | Health checks passing |
| `unhandled_exception` | 500 errors — check Sentry |
| `health_db_check_failed` | DB connection problem |
| `health_redis_check_failed` | Redis problem |
| `Rate limit exceeded` | Abuse protection working |

**Real-time tail (if Render CLI installed):**
```powershell
render logs -r iskonnect-api --tail
```

---

### Vercel logs

**Where:** Vercel → Project → Deployments → select deploy → **Functions / Build Logs**

**Frontend errors** appear in browser console and Sentry, not Vercel server logs (static hosting).

---

### GitHub Actions logs

**Where:** Actions tab → workflow run → each step

**Healthy scraper log ending:**
```
ingest_scraped created=5 skipped_dup=120 skipped_live=10
```

---

## End-to-end verification checklist

Use after full deploy ([DEPLOYMENT_CHECKLIST.md](../DEPLOYMENT_CHECKLIST.md) expanded):

```
[ ] curl /health → 200, status ok, db true, cache true
[ ] curl /ready → 200
[ ] curl /metrics → scholarships > 0 (after import)
[ ] Vercel URL loads login page
[ ] Register → email received
[ ] Login → dashboard loads
[ ] Profile save → 200
[ ] Find matches → match_runs row in DB
[ ] Admin /admin loads (admin user)
[ ] GitHub scraper workflow green (optional)
[ ] Sentry receives test error (optional)
[ ] UptimeRobot monitor green
```

---

## Verification after code updates

| Change type | Re-verify |
|-------------|-----------|
| Backend code | `/health`, affected API routes, Render logs |
| Frontend code | Vercel redeploy, browser hard refresh (Ctrl+Shift+R) |
| Env var on Render | Manual redeploy, `/health`, startup logs |
| Env var on Vercel (`VITE_*`) | **Must redeploy** — rebuild required |
| New migration | `alembic current`, release command logs, smoke tests |
| CORS / domain change | Browser CORS check from new origin |

---

## Common verification failures

| Symptom | Likely cause | Verify command |
|---------|--------------|----------------|
| `/health` 503 | Bad `DATABASE_URL` | `curl /health`; Render logs |
| `cache: false` | Bad `REDIS_URL` | Upstash/Render Redis dashboard |
| CORS error | `CORS_ORIGINS` mismatch | Compare exact Vercel URL |
| Frontend calls localhost | `VITE_API_BASE_URL` not set at build | Rebuild Vercel with env |
| 401 on all routes | Expired token or `SECRET_KEY` changed | Fresh login |
| API slow first request | Render cold start | Wait 30s; UptimeRobot helps |
| Empty scholarships | No import/scraper yet | `SELECT COUNT(*) FROM scholarships` |
| Emails not sent | SMTP misconfig | Render logs; test register |

---

*Previous: [Part 2 — Deployment](02-deployment.md) · Next: [Part 4 — Domains and DNS](04-domains-and-dns.md)*
