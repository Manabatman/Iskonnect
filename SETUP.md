# Scholarship Match — local development & deployment

This guide covers running the API and frontend locally, deploying to **Render** (backend) + **Vercel** (frontend), troubleshooting common issues, and using **Docker Compose** as an alternative.

---

## 1. Local development setup

### Prerequisites

- **Python 3.11+**
- **Node.js 20+** and npm
- **Git**

### Backend (FastAPI + SQLite)

1. **Clone the repository** and enter the backend root (this folder, `scholarship-match/`).

2. **Create and activate a virtual environment** (examples):

   ```bash
   python -m venv .venv
   # Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment file:** copy `.env.example` to `.env` and adjust as needed. For typical local work, ensure at least:

   - `ENVIRONMENT=development`
   - `DATABASE_URL=sqlite:///./dev.db`
   - `RUN_MIGRATIONS_ON_STARTUP=true` — applies pending Alembic migrations when the API starts (convenient for local dev only).
   - `AUTH_DISABLED=true` — optional; allows hitting protected routes without JWT while developing.
   - `CORS_ORIGINS` includes your Vite dev origin, e.g. `http://localhost:5173,http://127.0.0.1:5173`.

5. **Create / upgrade the database** (recommended first-time step; `*.db` is gitignored):

   ```bash
   alembic upgrade head
   ```

   Confirm revision:

   ```bash
   alembic current
   ```

   You should see `017 (head)` when the tree is fully applied.

6. **Run the API:**

   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

7. **Verify health:**

   Open or request `http://localhost:8000/health`. A healthy instance returns JSON similar to:

   ```json
   {"status":"ok","checks":{"db":true,"cache":true}}
   ```

### Frontend (Vite)

1. From `frontend/`:

   ```bash
   npm install
   npm run dev
   ```

2. **API URL:** ensure `frontend/.env` (or `.env.local`) sets:

   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```

3. Open the dev server URL (usually `http://localhost:5173`). **Register** a test account, then **log in** to confirm the stack end-to-end.

### Optional: create an admin user

```bash
python -m app.scripts.create_admin
```

(Follow any prompts or flags defined in that script.)

---

## 2. Vercel + Render deployment

### Render (backend)

1. Create a **Web Service** from your Git repository; set the **root directory** to `scholarship-match/` (or the folder that contains `requirements.txt` and `app/`).

2. Create a **PostgreSQL** database on Render and link it to the service.

3. **Environment variables** (minimum):

   | Variable | Notes |
   |----------|--------|
   | `DATABASE_URL` | From Render Postgres (often injected when you link the DB). |
   | `SECRET_KEY` | Random secret, e.g. `openssl rand -hex 32`. |
   | `CORS_ORIGINS` | Comma-separated origins; **must include your Vercel URL** (e.g. `https://your-app.vercel.app`). |
   | `AUTH_DISABLED` | `false` in production. |
   | `ENVIRONMENT` | `production` (enforces production-safe settings in `config.py`). |

4. **Build command:** `pip install -r requirements.txt`

5. **Start command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

6. **Release command (migrations):** `alembic upgrade head`  
   Render runs this before new deploys when configured (see `render.yaml` in this repo for a blueprint-style reference).

### Vercel (frontend)

1. Import the project with **root directory** `scholarship-match/frontend`.

2. **Environment variable:**

   ```env
   VITE_API_BASE_URL=https://<your-render-service>.onrender.com
   ```

   Use your actual Render service URL (no trailing slash unless your client expects it).

3. **Build:** `npm run build`  
   **Output directory:** `dist`

4. Redeploy after changing environment variables so the build picks up `VITE_*` values.

---

## 3. Troubleshooting

| Symptom | Likely cause | What to do |
|--------|----------------|------------|
| **“Unable to connect to server”** in the UI | API not running, wrong API URL, or network/firewall | Start `uvicorn` on port 8000; set `VITE_API_BASE_URL` to the correct origin; test `GET /health` in the browser or with `curl`. |
| **`sqlite3.OperationalError: no such column: users.email_verified`** (or similar) | SQLite schema behind migrations | From `scholarship-match/`, run `alembic upgrade head`. If the DB was half-upgraded, delete `dev.db` and run `alembic upgrade head` again (local data loss). |
| **CORS error** in browser console | Frontend origin not allowed | Add the exact origin (scheme + host + port) to `CORS_ORIGINS` on the API; redeploy/restart. |
| **401** on protected routes | Auth required or bad token | Set `AUTH_DISABLED=true` only for local dev; in production, log in again and ensure the client sends `Authorization: Bearer <access_token>`. |
| **Mixed content blocked** | HTTPS page calling `http://` API | Serve the API over HTTPS (Render does) and set `VITE_API_BASE_URL` to `https://...`. |
| **`/health` shows `db: false`** | `DATABASE_URL` wrong or DB unreachable | Check connection string, Postgres status, and firewall. |

---

## 4. Docker alternative

The repo includes a **`Dockerfile`** and **`docker-compose.yml`** for a local stack: **API + Postgres + Redis**, with migrations run before Uvicorn starts.

From `scholarship-match/`:

```bash
docker compose up
```

- API: `http://localhost:8000` (per `docker-compose.yml`)
- Postgres and Redis are wired via `DATABASE_URL` and `REDIS_URL` in the compose file.

Use this when you want parity with production (Postgres) without installing Postgres locally.

---

## Quick reference

| Task | Command / location |
|------|---------------------|
| Apply all migrations | `alembic upgrade head` |
| Current revision | `alembic current` |
| Run API (dev) | `uvicorn app.main:app --reload --port 8000` |
| Run frontend | `cd frontend && npm run dev` |
| Health check | `GET http://localhost:8000/health` |
| Login API | `POST http://localhost:8000/api/v1/auth/login` |
