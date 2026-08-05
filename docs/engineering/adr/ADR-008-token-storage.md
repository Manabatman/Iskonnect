# ADR-008: Browser token storage

**Status:** Accepted  
**Date:** 2026-07-31  
**Deciders:** Engineering (Phase 3 M3 security)

## Context

ISKONNECT stores JWT access and refresh tokens in `localStorage` on the SPA. React escaping is the primary XSS mitigation today. A token exfiltration via XSS would grant session access for up to the refresh-token lifetime.

Three realistic options were evaluated for launch hardening:

| Option | Description | Effort | Residual risk |
| --- | --- | --- | --- |
| **A** | Keep `localStorage` + CSP + shorter refresh TTL | S | XSS can still read tokens until CSP is enforced; mitigated by 7-day refresh window |
| **B** | HttpOnly Secure SameSite cookies + CSRF tokens | L | Requires cross-origin cookie/CSRF design for Vercel → Render API |
| **C** | Hybrid: access token in memory, refresh in HttpOnly cookie | L | Same as B for refresh path; better access-token exposure profile |

## Decision

**Adopt option A for Phase 3:**

1. Continue storing access and refresh tokens in `localStorage` (no auth rewrite during launch hardening).
2. Ship Content-Security-Policy (report-only → enforcing) on the SPA hosting layer (SEC-03).
3. Reduce default refresh-token TTL from **14 days to 7 days** (`REFRESH_TOKEN_EXPIRE_DAYS`, default `7` in `app/config.py`).

Schedule option **C** for Phase 4 if cookie infrastructure is ready.

## Consequences

- Students re-authenticate more often (every 7 days without activity vs 14). The session-expiry redirect path must preserve intended destination (existing frontend behavior).
- CSP violations must be reviewed before switching from report-only to enforcing.
- Residual risk: XSS with a bypass of CSP could still exfiltrate tokens. **Review date:** 2026-10-31 (post-launch).

## Compensating controls

- Access-token denylist in Redis on logout and password reset (SEC-02).
- Short-lived access tokens (30 minutes default).
- No secrets in the client bundle; OpenAPI disabled in production.
