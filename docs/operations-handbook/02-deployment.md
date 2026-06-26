# Part 2 — Deployment

> From an **empty computer** to a **live Iskonnect** on Vercel + Render + Supabase + Redis + SMTP + Sentry.

Read [Part 1 — Architecture](01-architecture.md) first so you know what each piece does.

---

## Deployment order (critical)

Deploy in this order or you will chase circular configuration problems:

```mermaid
flowchart LR
  A[1 GitHub repo] --> B[2 Supabase Postgres]
  B --> C[3 Run migrations]
  C --> D[4 Redis]
  D --> E[5 Render API]
  E --> F[6 Vercel frontend]
  F --> G[7 Wire CORS + API URL]
  G --> H[8 SMTP + Sentry]
  H --> I[9 GitHub Actions secrets]
  I --> J[10 Custom domain optional]
```

| Step | Why this order |
|------|----------------|
| Supabase before Render | API needs `DATABASE_URL` on first boot |
| Migrations before API | Tables must exist before routes query them |
| Render before Vercel | You need API URL for `VITE_API_BASE_URL` |
| Vercel URL before final CORS | `CORS_ORIGINS` must include exact Vercel origin |
| SMTP before public launch | Production guard requires email |

---

## Prerequisites: from empty computer

### What software you need

| Software | Version | Why |
|----------|---------|-----|
| Git | Latest | Clone repo, push deploys |
| Python | **3.11.x** | Backend runtime (see `runtime.txt`) |
| Node.js | **24.x** | Frontend build (see CI) |
| Docker Desktop | Latest | Optional local Postgres+Redis stack |
| A code editor | VS Code / Cursor | Edit env files |
| A terminal | PowerShell (Windows) | Run commands |

---

### Terminal basics (first command lesson)

Before Git or Python, you need to navigate the filesystem.

#### `pwd` — Print Working Directory

**What:** Shows the folder your terminal is "standing in."

**Why:** Commands affect files relative to current directory. Wrong folder = wrong results.

**Syntax:** `pwd` (no arguments)

**PowerShell equivalent:** `Get-Location` or `pwd` (alias exists)

**Example output:**
```
PS C:\Users\You> pwd

Path
----
C:\Users\You
```

**Meaning:** You are in your home folder.

**Analogy:** Asking "Where am I on the map?" before giving directions.

**Common mistakes:** Running `pip install` from `C:\Users\You` instead of the project folder.

**When engineers use it:** Constantly, especially after `cd` chains.

---

#### `cd` — Change Directory

**What:** Moves your terminal into another folder.

**Why:** Project commands must run from `scholarship-match/` (repo root).

**Syntax:** `cd <path>`

**Examples:**
```powershell
cd C:\Iskonnect\scholarship-match
cd frontend          # relative: into frontend subfolder
cd ..                # up one level
```

**What breaks if skipped:** `pip install -r requirements.txt` fails with "file not found."

**Alternatives:** Open terminal in VS Code with **Terminal → New Terminal** from the project folder.

---

#### `ls` — List files

**What:** Lists files and folders in current directory.

**PowerShell:** `ls` or `Get-ChildItem` or `dir`

**Example:**
```
PS C:\Iskonnect\scholarship-match> ls

    Directory: C:\Iskonnect\scholarship-match

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        6/25/2026   7:00 PM                app
d-----        6/25/2026   7:00 PM                frontend
-a----        6/25/2026   7:00 PM           1234 requirements.txt
```

**Meaning:** `d-----` = directory; `-a----` = file.

**Analogy:** Reading room numbers on a hallway before opening a door.

---

#### `mkdir` — Make directory

**What:** Creates a new folder.

**Syntax:** `mkdir <name>`

**Example:** `mkdir C:\Iskonnect` — create workspace folder before cloning.

---

### Git

#### Install Git

1. Download from https://git-scm.com/download/win
2. Install with defaults (include "Git Bash" optional; PowerShell works)

**Verify:**
```powershell
git --version
```

**Expected output:**
```
git version 2.47.0.windows.1
```

**What breaks if Git missing:** Cannot clone repo; Vercel/Render cannot pull code.

**Troubleshoot:** Restart terminal after install; check PATH.

---

#### `git clone` — Copy remote repository locally

**What:** Downloads entire project history from GitHub to your machine.

**Why:** Render and Vercel deploy from this repo; you need a local copy to develop and run migrations.

**Syntax:** `git clone <url> [<folder>]`

**Example:**
```powershell
cd C:\Iskonnect
git clone https://github.com/YOUR_ORG/scholarship-match.git
cd scholarship-match
```

**What happens internally:**
1. Git contacts GitHub over HTTPS
2. Downloads all commits, branches, files
3. Creates `.git/` hidden folder with full history
4. Checks out default branch (usually `main`)

**Expected output:**
```
Cloning into 'scholarship-match'...
remote: Enumerating objects: 5000, done.
Receiving objects: 100% (5000/5000), done.
```

**Common mistakes:**
- Cloning into a folder that already has files
- Using SSH URL without SSH keys configured (use HTTPS first)

**Alternatives:** GitHub Desktop GUI; `gh repo clone` with GitHub CLI.

---

#### `git status` — See what changed

**What:** Shows modified, staged, and untracked files.

**Why:** Before commit, confirm you're committing the right files (never `.env` with secrets).

**Syntax:** `git status`

**Example output:**
```
On branch main
Changes not staged for commit:
  modified:   docs/operations-handbook/00-index.md

Untracked files:
  .env
```

**Meaning:** `.env` is untracked (good — should stay out of git via `.gitignore`).

**When engineers use it:** Before every commit; during incident "what deployed?"

---

#### `git add`, `git commit`, `git push`

**`git add`** — Stage files for next commit  
**`git commit`** — Snapshot staged changes with message  
**`git push`** — Upload commits to GitHub (triggers CI)

```powershell
git add docs/operations-handbook/
git commit -m "Add production operations handbook"
git push origin main
```

**What breaks if you push secrets:** Credentials in git history forever. Use `.env` locally only.

**Verify:** GitHub → repository → see latest commit; Actions tab → CI running.

---

#### `git branch` / `git checkout`

**What:** `branch` lists branches; `checkout` switches branch.

```powershell
git branch
git checkout -b feature/my-change
```

**Why:** Production deploys from `main`; features use branches + pull requests.

**Modern alternative:** `git switch -c feature/my-change`

---

### Python 3.11

#### Install

1. https://www.python.org/downloads/ — download **3.11.x**
2. Check **"Add Python to PATH"** during install

**Verify:**
```powershell
python --version
```

**Expected:** `Python 3.11.9` (or similar 3.11.x)

**What breaks if wrong version:** Some dependencies may fail; CI uses 3.11.

---

#### `python -m venv .venv` — Create virtual environment

**What:** Isolated Python environment for this project only.

**Why:** Avoids conflicting packages with other projects on your machine.

**Syntax:** `python -m venv <folder>`

**Example (from repo root):**
```powershell
cd C:\Iskonnect\scholarship-match
python -m venv .venv
```

**What happens internally:** Copies Python binary + creates `Scripts/` (Windows) with isolated `pip`.

**Analogy:** A separate toolbox for this job site — don't mix wrenches from other projects.

---

#### Activate venv

**PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Expected prompt change:**
```
(.venv) PS C:\Iskonnect\scholarship-match>
```

**Common mistake:** Execution policy blocks script:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

---

#### `pip install -r requirements.txt`

**What:** Installs all Python dependencies listed in the file.

**Why:** FastAPI, SQLAlchemy, Alembic, etc. are not in stdlib.

**Syntax:** `pip install -r <file>`

**Expected output (truncated):**
```
Collecting fastapi==0.115.6
...
Successfully installed fastapi-0.115.6 sqlalchemy-2.0.36 ...
```

**Verify:**
```powershell
python -c "import fastapi; print(fastapi.__version__)"
```

**Alternatives:** `uv pip install` (faster resolver).

---

### Node.js 24

#### Install

1. https://nodejs.org/ — LTS or Current **24.x**
2. Or: `winget install OpenJS.NodeJS`

**Verify:**
```powershell
node --version
npm --version
```

**Expected:** `v24.x.x` and `10.x.x`

---

#### `npm install` — Install frontend dependencies

**What:** Reads `package-lock.json` and installs node_modules.

**Why:** React, Vite, Tailwind, Sentry SDK need to be present to build.

**Run from:**
```powershell
cd frontend
npm install
```

**Expected:** Creates `frontend/node_modules/` (large folder).

**Common mistakes:** Running from repo root (no package.json there for frontend).

---

#### `npm run build` — Production frontend build

**What:** Vite compiles TypeScript + React into static files in `frontend/dist/`.

**Why:** Vercel deploys the **output** of this command, not your source `.tsx` files.

**Syntax:** `npm run build`

**Expected output:**
```
vite v5.x building for production...
✓ built in 12s
```

**What breaks if `VITE_API_BASE_URL` wrong at build time:** Production app calls wrong API (baked into JS bundle).

---

#### `npm run dev` — Local development server

**What:** Hot-reload dev server on http://localhost:5173

**Why:** Fast iteration without deploying.

**Not used in production** — Vercel runs `npm run build` instead.

---

### Docker (optional but recommended)

#### Install Docker Desktop

https://www.docker.com/products/docker-desktop/

**Verify:**
```powershell
docker --version
docker compose version
```

---

#### `docker compose up` — Local full stack

**What:** Starts Postgres + Redis + API from [docker-compose.yml](../../docker-compose.yml).

**Why:** Practice production-like stack without cloud accounts.

**Syntax:**
```powershell
cd C:\Iskonnect\scholarship-match
docker compose up --build
```

**What happens internally:**
1. Builds API image from Dockerfile
2. Starts `db` (Postgres 16), `redis`, `api` containers
3. API runs `alembic upgrade head` then uvicorn

**Expected logs:**
```
api-1  | [startup] environment=development database=postgres @ db:5432
api-1  | INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Verify:** Open http://localhost:8000/health

**Stop:** `Ctrl+C` then `docker compose down`

---

#### `docker build` / `docker run` / `docker logs`

**`docker build -t iskonnect-api .`** — Build image from Dockerfile  
**`docker run -p 8000:8000 --env-file .env iskonnect-api`** — Run container  
**`docker logs <container_id>`** — Read container stdout

**When engineers use these:** Debugging Dockerfile issues; CI pipelines; alternative to Render.

---

### Local development quick start

**Backend (SQLite — no cloud needed):**
```powershell
cd C:\Iskonnect\scholarship-match
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Edit .env: keep DATABASE_URL=sqlite:///./dev.db
# Set RUN_MIGRATIONS_ON_STARTUP=true for first run
uvicorn app.main:app --reload --port 8000
```

#### `uvicorn` (local dev only)

**What:** ASGI server that runs FastAPI directly (single process).

**Why local only:** Simple, supports `--reload` on file changes.

**Syntax:** `uvicorn <module>:<app> --reload --port <port>`

**Example:** `uvicorn app.main:app --reload --port 8000`

**Production uses gunicorn instead** — see [Part 1](01-architecture.md#process-model-production).

**Expected startup log:**
```
[startup] environment=development database=sqlite (local dev.db) cors_origins=[...]
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Frontend:**
```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

---

## Accounts to create

Create these accounts before deploying. Use a password manager.

| # | Service | URL | Purpose | Free tier? |
|---|---------|-----|---------|------------|
| 1 | GitHub | github.com | Source code + Actions | Yes |
| 2 | Supabase | supabase.com | Postgres database | Yes |
| 3 | Render | render.com | FastAPI hosting | Yes (with cold starts) |
| 4 | Vercel | vercel.com | Frontend hosting | Yes |
| 5 | Upstash or Render Redis | upstash.com / render.com | Redis | Yes tier |
| 6 | Resend or SendGrid | resend.com | SMTP email | Free tier |
| 7 | Sentry | sentry.io | Error tracking | Free tier |
| 8 | UptimeRobot | uptimerobot.com | Uptime monitoring | Free tier |
| 9 | Domain registrar | namecheap.com / cloudflare | Custom domain (optional) | Paid ~$10-15/yr |

---

## Step 1: GitHub repository

**What:** Host code that Vercel, Render, and Actions pull from.

**Why:** Central source of truth; CI runs on every push.

**Dashboard steps:**
1. GitHub → **New repository** → name `scholarship-match` (or your choice)
2. Push local code (see `git push` above)
3. Settings → **Secrets and variables → Actions**
4. Later: add `DATABASE_URL` secret (after Supabase)

**Verify:** Repository shows files; Actions tab exists.

**Troubleshoot:** Large files blocked → check `.gitignore` excludes `node_modules`, `.venv`, `dev.db`.

---

## Step 2: Supabase (PostgreSQL)

**What:** Managed Postgres — your production database.

**Why:** Persistent storage for users, scholarships, match runs. SQLite does not work in production.

### Dashboard walkthrough

1. **supabase.com** → Sign up → **New project**
2. Choose organization → Project name: `iskonnect-prod`
3. **Database password:** generate strong password → **save in password manager**
4. Region: choose closest to Philippines (e.g. Singapore `ap-southeast-1`)
5. Wait ~2 minutes for provisioning

### Get connection string

1. Project → **Connect** (top) → **ORMs** tab or **Connection string**
2. Select **Transaction pooler** (port **6543**)
3. Copy URI; convert to SQLAlchemy format:

```
postgresql+psycopg2://postgres.PROJECT_REF:YOUR_PASSWORD@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres?sslmode=require
```

**Critical details:**
- Use `postgresql+psycopg2://` (not bare `postgresql://`)
- Append `?sslmode=require`
- Replace password with your database password

**What breaks if wrong:**
- Missing `+psycopg2` → driver errors
- Direct connection (5432) with many workers → connection exhaustion
- Wrong password → API 503 on `/health`

**Alternatives:** Neon, Railway Postgres, self-hosted Postgres (more ops burden).

**How engineers discovered poolers:** Serverless and multi-worker apps exhausted connection limits on managed Postgres.

---

## Run database migrations

**What:** Apply Alembic schema revisions to Supabase.

**Why:** Tables (`users`, `scholarships`, etc.) must exist before API starts.

### `alembic upgrade head`

**Syntax:** `alembic upgrade head`

**Meaning:**
- `alembic` — migration tool
- `upgrade` — apply migrations forward
- `head` — latest revision in `alembic/versions/`

**Run locally against Supabase (first time):**
```powershell
cd C:\Iskonnect\scholarship-match
.\.venv\Scripts\Activate.ps1
$env:DATABASE_URL = "postgresql+psycopg2://postgres.xxx:PASSWORD@....pooler.supabase.com:6543/postgres?sslmode=require"
alembic upgrade head
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001_initial
...
INFO  [alembic.runtime.migration] Running upgrade 024_xxx -> 025_xxx
```

**Verify:** Supabase → **Table Editor** → see `users`, `scholarships`, `alembic_version` tables.

**Production:** Render **Release Command** runs this automatically on each deploy:
```
alembic upgrade head
```

**Set:** `RUN_MIGRATIONS_ON_STARTUP=false` in production.

**Troubleshoot:**
- `relation already exists` → partial migration; check `alembic_version` table
- SSL error → add `?sslmode=require`

---

## Step 3: Redis

**What:** In-memory data store for shared state across gunicorn workers.

**Why:** Required by `validate_for_production()` — rate limits, email abuse caps, scholarship cache.

### Option A: Upstash (recommended for free tier)

1. upstash.com → Create account → **Create database**
2. Region: same as Supabase if possible
3. Copy **Redis URL** (starts with `rediss://` for TLS)

Set in Render later:
```
REDIS_URL=rediss://default:PASSWORD@HOST:6379
```

### Option B: Render Redis

1. Render dashboard → **New +** → **Redis**
2. Name: `iskonnect-redis`
3. Copy **Internal Redis URL** (use internal URL from Render API service)

**What breaks without Redis:** API refuses to start in production.

**Verify:** After API deploy, `GET /health` → `"cache": true`.

---

## Step 4: Render (backend API)

**What:** Runs your Python FastAPI application 24/7 (with cold starts on free tier).

**Why:** Browsers cannot run Python; Vercel only serves static frontend.

### Dashboard walkthrough

1. render.com → Sign up (GitHub login recommended)
2. **New +** → **Web Service**
3. Connect GitHub repository `scholarship-match`
4. Configure:

| Setting | Value |
|---------|-------|
| **Name** | `iskonnect-api` |
| **Region** | Singapore or closest |
| **Branch** | `main` |
| **Root directory** | *(leave blank — repo root)* |
| **Runtime** | Python 3 |
| **Build command** | `pip install -r requirements.txt` |
| **Start command** | See Procfile below |
| **Release command** | `alembic upgrade head` |

**Start command (copy from Procfile):**
```
gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w ${WEB_CONCURRENCY:-2} -b 0.0.0.0:$PORT --forwarded-allow-ips='*' --proxy-headers
```

**Do NOT use** bare `uvicorn` in production (see doc corrections in index).

5. **Instance type:** Free to start; upgrade when cold starts hurt UX.

6. Click **Create Web Service** — first deploy begins.

### Render environment variables

Add in **Environment** tab (see full checklist below).

**Minimum to boot:**
```
ENVIRONMENT=production
DATABASE_URL=postgresql+psycopg2://...
SECRET_KEY=<run: openssl rand -hex 32>
AUTH_DISABLED=false
CORS_ORIGINS=https://PLACEHOLDER.vercel.app
FRONTEND_URL=https://PLACEHOLDER.vercel.app
REDIS_URL=rediss://...
TRUST_PROXY_HEADERS=true
RUN_MIGRATIONS_ON_STARTUP=false
WEB_CONCURRENCY=2
```

Use placeholder Vercel URL first; update after Vercel deploy.

**Generate SECRET_KEY:**

#### `openssl rand -hex 32`

**What:** Outputs 32 random bytes as 64 hex characters.

**Why:** JWT signing secret must be unguessable.

**PowerShell alternative:**
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

**Expected:** `a3f8c2...` (64 characters)

**What breaks if default SECRET_KEY:** Anyone can forge JWT tokens; `validate_for_production` blocks startup.

**Verify deploy:** Render **Logs** tab:
```
[startup] environment=production database=postgres @ ...pooler.supabase.com:6543
Booting worker with pid: 123
```

**Troubleshoot:**
- `Invalid production configuration` → read error list; fix env vars
- Build failed → check `requirements.txt` pins
- 502 → workers crashing; read traceback in logs

---

## Step 5: Vercel (frontend)

**What:** Builds and hosts static React app on global CDN.

**Why:** Fast page loads worldwide; automatic HTTPS.

### Dashboard walkthrough

1. vercel.com → Sign up with GitHub
2. **Add New…** → **Project**
3. Import `scholarship-match` repository
4. Configure:

| Setting | Value |
|---------|-------|
| **Framework preset** | Vite |
| **Root directory** | `frontend` |
| **Build command** | `npm run build` (default) |
| **Output directory** | `dist` (default) |

5. **Environment variables:**

| Name | Value |
|------|-------|
| `VITE_API_BASE_URL` | `https://iskonnect-api.onrender.com` (your Render URL, **no trailing slash**) |
| `VITE_SENTRY_DSN` | *(optional)* from Sentry |
| `VITE_SENTRY_ENVIRONMENT` | `production` |
| `VITE_SENTRY_RELEASE` | git SHA or `1.0.0` |

6. **Deploy**

**Expected:** Vercel gives URL like `https://scholarship-match-abc123.vercel.app`

**Verify:** Open URL in browser; login page loads.

**What breaks:**
- Missing `VITE_API_BASE_URL` → build throws error in production mode
- Trailing slash on API URL → double-slash bugs in some paths

---

## Step 6: Wire CORS and API URL

**What:** Tell backend which browser origins may call it; tell frontend where API lives.

**Why:** Browsers enforce CORS; mismatched URLs cause silent failures.

1. Copy exact Vercel URL: `https://scholarship-match-abc123.vercel.app`
2. Render → Environment → update:
   ```
   CORS_ORIGINS=https://scholarship-match-abc123.vercel.app
   FRONTEND_URL=https://scholarship-match-abc123.vercel.app
   ```
3. Render → **Manual Deploy** → Deploy latest commit
4. Vercel → confirm `VITE_API_BASE_URL` → **Redeploy** if you changed it

**Verify:** Browser DevTools → Network → API calls return 200, not CORS errors.

---

## Step 7: SMTP (email)

**What:** Send verification and password-reset emails.

**Why:** `validate_for_production()` requires `SMTP_HOST` + `EMAIL_FROM`.

### Resend example

1. resend.com → API Keys → Create
2. Add domain `iskonnect.ph` (or use onboarding domain for testing)
3. Render env:

```
SMTP_HOST=smtp.resend.com
SMTP_PORT=587
SMTP_USER=resend
SMTP_PASSWORD=re_xxxxxxxx
SMTP_USE_TLS=true
EMAIL_FROM=noreply@yourdomain.com
```

**Verify:** Register test user; check email arrives.

**Troubleshoot:** SPF/DKIM not configured → emails go to spam; check provider DNS records.

---

## Step 8: Sentry (error tracking)

### Backend

1. sentry.io → Create project → **FastAPI**
2. Copy DSN
3. Render:
   ```
   SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx
   ```

### Frontend

1. Create project → **React**
2. Vercel:
   ```
   VITE_SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx
   VITE_SENTRY_ENVIRONMENT=production
   ```
3. Redeploy Vercel

**Verify:** Trigger test error; appears in Sentry within seconds.

See [Part 8](08-observability.md) for alert rules.

---

## Step 9: GitHub Actions secrets

**What:** Allow scheduled scraper and maintenance jobs to reach production DB.

**Why:** Scraper runs on GitHub servers, not Render.

1. GitHub → repo → **Settings → Secrets and variables → Actions**
2. **New repository secret:**
   - Name: `DATABASE_URL`
   - Value: same Supabase pooler URI as Render

**Verify:** Actions → **Scholarship scrape and ingest** → **Run workflow** → green check.

**What breaks if different DATABASE_URL:** Scraper writes to wrong database; split-brain catalog.

---

## Step 10: Create admin user

**What:** First admin account for `/admin` staging approval.

```powershell
cd C:\Iskonnect\scholarship-match
$env:DATABASE_URL = "your-supabase-uri"
python -m app.scripts.create_admin --email admin@yourdomain.com --password "StrongPass123!"
```

**Verify:** Login as admin; access `/admin` routes.

---

## Environment variables: complete checklist

### Render (backend) — all production vars

| Variable | Required | Example / notes |
|----------|----------|-----------------|
| `ENVIRONMENT` | Yes | `production` |
| `DATABASE_URL` | Yes | Supabase pooler `postgresql+psycopg2://...?sslmode=require` |
| `SECRET_KEY` | Yes | 64-char hex from `openssl rand -hex 32` |
| `AUTH_DISABLED` | Yes | `false` |
| `CORS_ORIGINS` | Yes | `https://your-app.vercel.app` |
| `FRONTEND_URL` | Yes | Same as Vercel URL |
| `REDIS_URL` | Yes | `rediss://...` or `redis://...` |
| `TRUST_PROXY_HEADERS` | Yes | `true` |
| `RUN_MIGRATIONS_ON_STARTUP` | Yes | `false` |
| `SMTP_HOST` | Yes | `smtp.resend.com` |
| `EMAIL_FROM` | Yes | `noreply@yourdomain.com` |
| `SMTP_PORT` | Usually | `587` |
| `SMTP_USER` | Usually | Provider-specific |
| `SMTP_PASSWORD` | Usually | API key |
| `SMTP_USE_TLS` | Usually | `true` |
| `SENTRY_DSN` | Recommended | From Sentry |
| `WEB_CONCURRENCY` | Recommended | `2` (increase with paid instances) |
| `STRUCTURED_LOGGING` | Optional | `true` for JSON logs |
| `DB_POOL_SIZE` | Optional | `5` |
| `DB_MAX_OVERFLOW` | Optional | `10` |

### Vercel (frontend) — public vars only

| Variable | Required | Notes |
|----------|----------|-------|
| `VITE_API_BASE_URL` | Yes | Render API origin, no trailing slash |
| `VITE_SENTRY_DSN` | Optional | Frontend Sentry |
| `VITE_SENTRY_ENVIRONMENT` | Optional | `production` |
| `VITE_SENTRY_RELEASE` | Optional | Git commit SHA |

**Never put on Vercel:** `DATABASE_URL`, `SECRET_KEY`, `SMTP_PASSWORD`, `REDIS_URL`

---

## Uptime monitoring (bonus step)

1. uptimerobot.com → **Add monitor**
2. Type: HTTP(s)
3. URL: `https://iskonnect-api.onrender.com/health`
4. Interval: 5 minutes

**Why:** Reduces Render cold starts; alerts on outages.

---

## Deployment cost estimate (free tier start)

| Service | Free tier limits | When to pay |
|---------|------------------|-------------|
| Vercel | Hobby projects | Team features |
| Render | 750 hrs/mo, cold starts | Always-on API |
| Supabase | 500MB DB, 2 projects | Growth |
| Upstash | 10K commands/day | Traffic |
| Resend | 100 emails/day | User growth |
| Sentry | 5K errors/mo | Scale |

---

## What you should have when done

| Asset | Example |
|-------|---------|
| Frontend URL | `https://scholarship-match-xxx.vercel.app` |
| API URL | `https://iskonnect-api.onrender.com` |
| Supabase project | `iskonnect-prod` |
| Redis | Upstash or Render Redis |
| Admin login | `admin@yourdomain.com` |
| GitHub secret | `DATABASE_URL` set |
| Uptime monitor | `/health` every 5 min |

**Next:** [Part 3 — Verification](03-verification.md) — prove every step worked.

---

*Previous: [Part 1 — Architecture](01-architecture.md) · Next: [Part 3 — Verification](03-verification.md)*
