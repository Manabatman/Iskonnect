# Observability

## Sentry

### Backend
- Set `SENTRY_DSN` and `ENVIRONMENT=production` in Render.
- Unhandled exceptions are captured in the global handler with tags: `request_id`, `path`.

### Frontend
- Set `VITE_SENTRY_DSN`, optional `VITE_SENTRY_ENVIRONMENT`, `VITE_SENTRY_RELEASE` (e.g. git SHA) in Vercel.

### Recommended alert (Sentry dashboard)

Create one alert rule:

- **Name:** Production error spike
- **Condition:** Number of events in issue is greater than 10 in 5 minutes
- **Filter:** `environment:production`
- **Action:** Email or Slack to on-call

This catches deploy regressions and abuse without alert fatigue from single 404s.

## Request correlation

Clients may send `X-Request-ID`; the API returns it on errors and logs it on every request.

## Metrics

`GET /metrics` returns lightweight counts (scholarships, users, staging pending). **Requires admin JWT** (`Authorization: Bearer <admin access token>`). Use from an authenticated admin session or ops script — not for public uptime checks (use `/health` instead).
