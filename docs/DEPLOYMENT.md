# ISKONNECT deployment notes

## Migrations

- **Production:** Do **not** rely on `RUN_MIGRATIONS_ON_STARTUP` (leave `false` or unset). Run migrations once per deploy:

  ```bash
  alembic upgrade head
  ```

- **Render:** Set `releaseCommand: alembic upgrade head` in `render.yaml` so migrations run before the web process starts.

- **Local:** Set `RUN_MIGRATIONS_ON_STARTUP=true` in `.env` for convenience, or run `alembic upgrade head` manually after pulling.

## Scholarship cache (multi-worker)

- **In-process cache** is per worker process. With multiple Gunicorn/Uvicorn workers, each worker has its own cache; mutations only invalidate the worker that handled the request.

- **Mitigation:** Set `REDIS_URL` (e.g. `redis://localhost:6379/0` or Upstash) so the scholarship list is cached in Redis and shared across workers. Invalidation deletes the Redis key on create/update/delete.

- **MVP:** Run a **single worker** in production if Redis is not available, and accept up to TTL (5 minutes) staleness in edge cases.

## Environment

| Variable | Production | Local dev |
|----------|------------|-----------|
| `AUTH_DISABLED` | `false` | `true` (optional) |
| `SECRET_KEY` | Strong random (`openssl rand -hex 32`) | Any |
| `RUN_MIGRATIONS_ON_STARTUP` | `false` | `true` (optional) |
| `REDIS_URL` | Recommended for multi-worker | Optional |

## CI/CD

- GitHub Actions runs `pytest` on push/PR.
- Deploy hooks (Render/Vercel) should be configured via repository secrets; see `.github/workflows/ci.yml` for optional deploy job placeholders.
