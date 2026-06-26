# Lesson 14 — Redis, Cache & Rate Limiting

> **Prerequisite:** [13 — Domain Taxonomies](13-domain-taxonomies.md)

---

## Concept: Caching

### 1. Definition

**Caching** stores expensive computation results for reuse.

### 2. Why Redis

In-memory, fast, **shared across gunicorn workers**. Process-local cache is invisible to other workers.

### 3. Problem solved

Listing hundreds of scholarships on every match request hammers Postgres.

---

## Scholarship list cache

[`app/scholarship_cache.py`](../../../app/scholarship_cache.py)

```
REDIS_KEY = "iskonnect:scholarships_json:v1"
TTL_SECONDS = 300
```

**Flow:**

1. Try Redis `GET`
2. Else try in-process cache (5 min TTL)
3. Else query DB via `build_all_dicts(db)`
4. Write to Redis `SETEX` and process cache

**Invalidate:** `invalidate_scholarship_cache()` on scholarship create/update/delete.

**Without Redis:** Each worker has separate cache — stale data up to TTL or inconsistent counts.

---

## Rate limiting

### 1. Definition

**Rate limiting** caps requests per client per time window — abuse protection.

### 2. [`app/limiter.py`](../../../app/limiter.py)

```python
limiter = Limiter(key_func=get_client_ip, storage_uri=_storage)
```

- `storage_uri` = `REDIS_URL` or `memory://`
- `SlowAPIMiddleware` in `main.py` enforces limits

### 3. Client IP behind proxy

[`app/utils/client_ip.py`](../../../app/utils/client_ip.py) — reads `X-Forwarded-For` when behind Render reverse proxy. **Bug class:** all users share one IP → everyone rate-limited together.

### 4. Email abuse protection (launch hardening)

Per-email cooldown + daily caps on register/forgot/resend — Redis counters, non-enumerating responses.

---

## Multi-worker deployment

[`Procfile`](../../../Procfile) / [`Dockerfile`](../../../Dockerfile):

```
gunicorn ... -w ${WEB_CONCURRENCY:-2} -k uvicorn.workers.UvicornWorker
```

**Why gunicorn:** Multiple processes handle concurrent requests. **Requires Redis** for shared rate limit and cache.

`validate_for_production()` requires `REDIS_URL` in production.

---

## Tradeoffs

| Strategy | Pros | Cons |
|----------|------|------|
| No cache | Always fresh | Slow, DB load |
| Process cache | Simple | Inconsistent multi-worker |
| Redis cache | Fast, shared | Staleness, ops dependency |

---

## Exercises

### Level 1 — Understanding

1. Why 300s TTL for scholarships?
2. What happens if Redis down?

### Level 2 — Implementation

1. Hit `/api/v1/scholarships` twice — observe cache behavior in logs (if enabled).

### Level 3 — Debugging

1. Admin updates scholarship but list stale — trace invalidation call in `scholarships.py`.

### Level 4 — Architecture

1. Design cache for match results per profile — would you? Why or why not?

<details>
<summary>Solution</summary>

TTL balances freshness vs load. Redis failure: fallback to process cache + DB; rate limit may be per-worker only. Match results change when profile or catalog changes — cache key complexity high; match_runs table already stores history snapshots.
</details>

---

*Previous: [13 — Taxonomies](13-domain-taxonomies.md) | Next: [15 — Middleware & Observability](15-middleware-observability-sentry.md)*
