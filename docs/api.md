# API Reference

Base path: `/api/v1`  
Auth: Bearer JWT on protected routes

## Interactive docs (local development)

With the API running locally:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

Production exposes the same schema at your Render URL (e.g. `https://your-api.onrender.com/docs`). Restrict public access in production if you prefer not to expose interactive docs.

## Core endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/health` | No | Health check (DB, cache, maintenance metadata) |
| GET | `/ready` | No | Database readiness |
| POST | `/auth/register` | No | Create account |
| POST | `/auth/login` | No | Login → access + refresh tokens |
| GET | `/auth/me` | Yes | Current user |
| GET | `/profiles/me` | Yes | Current student profile |
| POST | `/profiles` | Yes | Create or update profile |
| GET | `/scholarships/search` | No | Browse and filter catalog |
| GET | `/scholarships/{id}` | No | Scholarship detail |
| GET | `/plan/{profile_id}` | Yes | Matches + timeline + preparation |
| POST | `/match-runs` | Yes | Run and persist a full match session |
| GET | `/saved-scholarships` | Yes | User's saved programs |
| POST | `/scholarships/staging/import` | Admin | Bulk import to staging |

## Admin endpoints

Admin routes require an account with admin role. Key groups:

- **Staging:** approve/reject imported rows
- **Data quality:** completeness tiers, verification queues
- **Analytics:** catalog quality metrics
- **Scholarship CRUD:** create, edit, image upload

See `/docs` for the full admin surface.

## Metrics

`GET /metrics` returns lightweight counts (scholarships, users, staging pending). **Requires admin JWT** — not for public uptime checks.

## Request correlation

Clients may send `X-Request-ID`; the API returns it on errors and logs it on every request.
