# Lesson 15 — Middleware, Observability & Sentry

> **Prerequisite:** [14 — Redis, Cache & Rate Limiting](14-redis-cache-and-rate-limiting.md)

---

## Concept: Observability

### 1. Definition

**Observability** = ability to understand system state from outputs: **logs**, **metrics**, **traces**, **errors**.

### 2. Why it exists

Production has no debugger attached. You infer state from telemetry.

### 3. Problem solved

**Mean time to recovery (MTTR)** — find and fix 3 AM incidents.

---

## Request ID

[`app/middleware/request_logger.py`](../../../app/middleware/request_logger.py)

```python
rid = request.headers.get("x-request-id") or str(uuid.uuid4())
request.state.request_id = rid
response.headers["X-Request-ID"] = rid
```

Correlate: user report → API error body `request_id` → server logs → Sentry event.

**Global handler** in `main.py` tags Sentry `request_id` and returns it in 500 JSON.

---

## Structured logging

[`app/utils/logging_config.py`](../../../app/utils/logging_config.py) — `setup_logging(settings.structured_logging)`.

Startup logs: environment, DB host (no credentials), CORS origins.

---

## Sentry

### Backend ([`main.py`](../../../app/main.py))

```python
sentry_sdk.init(
    dsn=settings.sentry_dsn,
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1,
    environment=settings.environment,
)
```

### Frontend ([`frontend/src/main.tsx`](../../../frontend/src/main.tsx))

```typescript
Sentry.init({
  dsn: sentryDsn,
  environment: sentryEnv,
  release: sentryRelease,
});
```

**PII scrubbing:** Never send passwords, tokens, full profile to Sentry. See [`docs/OBSERVABILITY.md`](../../OBSERVABILITY.md).

**Alert rule:** Error spike > N events in 5 minutes → email/Slack.

---

## Security headers middleware

[`app/middleware/security_headers.py`](../../../app/middleware/security_headers.py) — HSTS, X-Content-Type-Options, etc.

Defense in depth — browser-level protections.

---

## Metrics endpoint

`GET /metrics` — scholarship count, user count, staging pending. Lightweight ops dashboard seed.

---

## Typical incident workflow

1. User reports error with `request_id`
2. Search Render logs for `[request_id]`
3. If unhandled, find Sentry issue
4. Reproduce locally with same path/body
5. Fix + test + deploy
6. Mark Sentry resolved

---

## Exercises

### Level 1 — Understanding

1. Three pillars of observability?
2. Why `traces_sample_rate=0.1`?

### Level 2 — Implementation

1. Trigger intentional 500 in dev — find `request_id` in response.

### Level 3 — Debugging

1. Sentry shows error but no user context — what tags to add?

### Level 4 — Architecture

1. Design on-call runbook for "match endpoint 500 spike" — 5 checklist items.

<details>
<summary>Solution</summary>

Logs, metrics, traces (errors often fourth pillar). 10% trace sampling controls cost/volume. Add user_id hash, path, release — not email. Runbook: check Render deploy, DB connectivity, Redis, recent migration, scholarship cache corrupt JSON, rollback if needed.
</details>

---

*Previous: [14 — Redis](14-redis-cache-and-rate-limiting.md) | Next: [16 — Background Jobs & Data Ingest](16-background-jobs-and-data-ingest.md)*
