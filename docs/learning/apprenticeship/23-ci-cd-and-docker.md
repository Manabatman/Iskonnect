# Lesson 23 — CI/CD & Docker

> **Prerequisite:** [22 — Frontend Testing](22-frontend-testing.md)

---

## Concept: CI/CD

### 1. Definition

- **CI (Continuous Integration):** Merge code → automated tests run
- **CD (Continuous Deployment):** Tests pass → auto-deploy to production

### 2. Why

Catch bugs before users do. Deploy becomes boring and repeatable.

### 3. Iskonnect pipeline

[`.github/workflows/ci.yml`](../../../.github/workflows/ci.yml)

| Job | What it does |
|-----|--------------|
| `test` | Python 3.11, `pytest app/tests/` |
| `migrate-postgres` | Postgres service, upgrade → downgrade base → upgrade |
| `frontend` | Node 22, `npm ci`, build, test |

Triggered on push/PR to `main`.

---

## Docker

### 1. Definition

**Docker** packages app + dependencies into an **image** run as **containers**.

### 2. [`Dockerfile`](../../../Dockerfile)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER appuser
CMD sh -c "gunicorn app.main:app -k uvicorn.workers.UvicornWorker ..."
```

### Commands dissected

#### `docker build`

```bash
docker build -t iskonnect-api .
```

| Aspect | Detail |
|--------|--------|
| **Meaning** | Build image from Dockerfile in cwd |
| **`-t iskonnect-api`** | Tag/name the image |
| **Internal** | Layer cache: requirements.txt layer cached until file changes |

#### `docker run`

```bash
docker run -p 8000:8000 -e DATABASE_URL=... iskonnect-api
```

| Aspect | Detail |
|--------|--------|
| **`-p 8000:8000`** | Host port 8000 → container port 8000 |
| **`-e`** | Environment variable |

#### `docker compose`

```bash
docker compose up --build
```

Uses [`docker-compose.yml`](../../../docker-compose.yml):

- **db** — Postgres 16
- **redis** — Redis 7
- **api** — builds Dockerfile, runs migrations + uvicorn

**Local prod-like stack** without installing Postgres on host.

---

## Procfile (Render/Heroku)

```
release: alembic upgrade head
web: gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w ${WEB_CONCURRENCY:-2} ...
```

- **release** — runs before new version receives traffic
- **web** — long-running HTTP process

[`railway.json`](../../../railway.json) — same pattern for Railway if used.

---

## gunicorn + uvicorn workers

| Component | Role |
|-----------|------|
| **gunicorn** | Master process, forks workers |
| **UvicornWorker** | Each worker runs ASGI app |

`WEB_CONCURRENCY=2` default — tune per CPU and memory.

`--forwarded-allow-ips='*'` — trust proxy headers for client IP (rate limiting).

---

## Exercises

### Level 1 — Understanding

1. CI vs CD?
2. Why `release` before `web`?

### Level 2 — Implementation

1. `docker compose up` — hit `http://localhost:8000/health`.

### Level 3 — Debugging

1. Container exits immediately — `docker compose logs api`.

### Level 4 — Architecture

1. Render uses native Python build, not Docker — when prefer Docker?

<details>
<summary>Solution</summary>

CI: test on merge. CD: deploy on green. Release migrates DB before code serves traffic with new schema assumptions. Docker when need exact system libs, multi-service local dev, or deploy to HF Spaces/K8s.
</details>

---

*Previous: [22 — Frontend Testing](22-frontend-testing.md) | Next: [24 — Production Deployment](24-production-deployment.md)*
