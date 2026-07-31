# ISKONNECT Performance Baseline

> **Owner:** Engineering  
> **Created:** P1-01 (login waterfall instrumentation)  
> **Updated:** _fill after each measurement run_

This document records **measured** login and dashboard timings. Do not optimize until numbers exist here.

---

## How to capture

### Backend (`Server-Timing` header)

Every API response includes a `wall;dur=…` metric from request middleware. Auth routes add phase breakdowns:

| Endpoint | Phase metrics |
| --- | --- |
| `POST /api/v1/auth/login` | `db-lookup`, `bcrypt`, `token-issue`, `wall` |
| `GET /api/v1/auth/me` | `auth-resolve`, `wall` |

**DevTools:** Network tab → select request → Response Headers → `Server-Timing`

**curl:**

```bash
curl -s -D - -o /dev/null -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"YOUR_EMAIL","password":"YOUR_PASSWORD"}' | grep -i server-timing
```

### Frontend (`performance.mark` / `performance.measure`)

After P1-01 ships, the login → dashboard path emits marks:

| Mark / measure | Meaning |
| --- | --- |
| `login:submit` | User clicked Sign in |
| `login:login-response` | `POST /login` returned tokens |
| `login:login-request` | measure: submit → login-response |
| `login:auth-me-start` | `GET /auth/me` began |
| `login:auth-me-done` | User object available in AuthContext |
| `login:auth-me` | measure: auth-me-start → auth-me-done |
| `login:navigate-dashboard` | React Router navigated to `/dashboard` |
| `login:dashboard-shell` | Dashboard layout rendered with user |
| `login:dashboard-data` | Profile + match-runs wave complete |
| `login:dashboard-matches` | Latest match results visible |

**Dev console:** After login, run:

```javascript
performance.getEntriesByType("measure")
  .filter((e) => e.name.startsWith("login:"))
  .forEach((e) => console.log(e.name, e.duration.toFixed(1) + "ms"));
```

Or use the helper: `window.__iskonnectLogLoginWaterfall?.()` (dev only, added in P1-01).

### Environment matrix

Record **each** scenario separately — cold vs warm backend changes results dramatically.

| Scenario | Backend | Network | Notes |
| --- | --- | --- | --- |
| Local warm | `uvicorn` already running | localhost | Best-case dev baseline |
| Local cold | Restart uvicorn, first request | localhost | Simulates cold worker |
| Render warm | Instance recently pinged | Production API URL | Typical returning user |
| Render cold | No request ≥15 min | Production API URL | Worst-case first visit |

---

## Login waterfall (target diagram)

```
User clicks Sign in
        ↓
[client] login:submit
        ↓
POST /api/v1/auth/login          ← Server-Timing: db-lookup, bcrypt, token-issue, wall
        ↓
[client] login:login-response
        ↓
GET /api/v1/auth/me              ← Server-Timing: auth-resolve, wall   (removed in P1-03)
        ↓
[client] login:auth-me-done
        ↓
Navigate /dashboard
        ↓
[client] login:dashboard-shell
        ↓
Parallel: GET /profiles/me, GET /match-runs, GET /saved-scholarships
        ↓
[client] login:dashboard-data
        ↓
Serial: GET /plan/{id}, GET /match-runs/{id}
        ↓
[client] login:dashboard-matches
        ↓
First meaningful dashboard content painted
```

---

## Baseline measurements

### Local warm (_date: ___)

| Step | Client (ms) | Server-Timing (ms) | Notes |
| --- | --- | --- | --- |
| submit → login-response | | db-lookup: / bcrypt: / token-issue: / wall: | |
| login-response → auth-me-done | | wall: | |
| submit → dashboard-shell | | | |
| submit → dashboard-data | | | |
| submit → dashboard-matches | | | |
| **Total submit → matches** | | | |

### Render warm (_date: ___)

| Step | Client (ms) | Server-Timing (ms) | Notes |
| --- | --- | --- | --- |
| submit → login-response | | | |
| login-response → auth-me-done | | | |
| **Total submit → matches** | | | |

### Render cold (_date: ___)

| Step | Client (ms) | Server-Timing (ms) | Notes |
| --- | --- | --- | --- |
| submit → login-response | | | First request after spin-down |
| **Total submit → matches** | | | |

---

## After Phase 1 (comparison)

Fill after P1-03…P1-11 complete. Goal: measurable improvement with evidence, not guesses.

| Metric | Before (baseline) | After Phase 1 | Delta |
| --- | --- | --- | --- |
| Login requests (count) | 2 (login + /me) | 1 (P1-03) | |
| submit → dashboard-data p75 warm | | | |
| submit → dashboard-matches p75 warm | | | |
| Render cold first-byte | | | |

---

## Related tasks

- **P1-01** — Instrumentation (this document + code)
- **P1-03** — Remove `/auth/me` round trip on login path
- **P1-07** — Skeletons (perceived performance)
- **PERF-07** — SQL prefilter for `/plan`
