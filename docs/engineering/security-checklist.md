# Launch security checklist — required environment variables

Use this before deploying or promoting a staging build. Startup calls `Settings.validate_for_production()`; misconfiguration should **fail closed** (process exit).

## Always set in production

| Variable | Required value | Failure mode if wrong |
| --- | --- | --- |
| `ENVIRONMENT` | `production`, `staging`, or `prod` (never rely on unset — unset is treated as production validation) | Placeholder `SECRET_KEY`, SQLite, missing Redis, etc. block startup |
| `SECRET_KEY` | Random 32+ byte hex (`openssl rand -hex 32`) | Startup error; JWT forgeable if placeholder leaks |
| `DATABASE_URL` | PostgreSQL connection string (not SQLite) | Startup error |
| `REDIS_URL` | e.g. `redis://host:6379/0` | Startup error; token revocation and shared rate limits unavailable |
| `CORS_ORIGINS` | Comma-separated production frontend origin(s) | Startup error |
| `TRUST_PROXY_HEADERS` | `true` behind Render/Railway | Startup error; rate limits may use proxy IP only |
| `AUTH_DISABLED` | `false` | Startup error; auth bypass |
| `RUN_MIGRATIONS_ON_STARTUP` | `false` (use release `alembic upgrade head`) | Startup error |

## Set when email verification is enabled (default)

| Variable | Required value | Failure mode if wrong |
| --- | --- | --- |
| `REQUIRE_EMAIL_VERIFICATION` | `true` for public launch | Users can sign in unverified (warning only if `false`) |
| `SMTP_HOST` | SMTP server hostname | Startup error when verification required |
| `EMAIL_FROM` | Verified sender address | Startup error when verification required |
| `FRONTEND_URL` | Public SPA URL (non-localhost) | Broken reset/verify links; startup error |

## Local development (relaxed guards)

| Variable | Value | Notes |
| --- | --- | --- |
| `ENVIRONMENT` | **`development`** (explicit) | Required to allow placeholder `SECRET_KEY` and SQLite |
| `BIND_HOST` | `127.0.0.1` (default) | Placeholder secret blocked if binding `0.0.0.0` |
| `REDIS_URL` | Optional | Token denylist is no-op without Redis in development only |

## Recommended production optional

| Variable | Purpose |
| --- | --- |
| `SENTRY_DSN` | Error tracking |
| `STRUCTURED_LOGGING` | JSON logs |
| `ENABLE_LINK_CHECKER` | Catalog link health |
| `SUPABASE_URL` / `SUPABASE_SERVICE_ROLE_KEY` | Scholarship image uploads |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Default `7` (ADR-008) |
| `FILTER_EXPIRED_FROM_MATCHES` | Default `true` — excludes expired/broken/past-deadline listings from ranked matches; see [deployment.md](../deployment.md#matching-behavior-flags) |

## Pre-launch verification

- [ ] Startup log shows `validation_environment=production` and `active_guards` includes `redis`, `jwt-required`
- [ ] Logout rejects previous access token (Redis reachable)
- [x] No email addresses in application logs (SEC-05) — enforced by `scripts/check_pii_logs.py` in CI (A4)
- [ ] CSP report-only reviewed on SPA (SEC-03)
- [ ] ADR-008 and ADR-009 acknowledged by deploy owner
