# P1-03 Report

## Objective

Return user fields and `has_profile` from `POST /auth/login` (and register/refresh) so the client can skip the `/auth/me` round trip on the login path.

## Files changed

- `app/api/v1/auth_routes.py` — extended `TokenResponse`, `RegisterResponse`, `UserMeResponse`; `_token_response` helper
- `app/tests/test_auth_extended.py` — login/me `has_profile` tests
- `frontend/src/contexts/AuthContext.tsx` — `userFromTokenPayload`, `skipFetchUserRef`, login/register set user directly
- `frontend/src/contexts/AuthContext.test.ts` — payload mapping and routing helper tests

## Before

Login stored tokens then `useEffect` called `/auth/me`, adding a second request to the critical path.

## After

Login/register populate `AuthUser` (including `hasProfile`) from the token response; cold-start session restore still uses `/auth/me` with `has_profile`.

## Tests

- [x] `pytest app/tests/test_auth_extended.py`
- [x] `npm run lint`, `typecheck`, `test`, `build`

## Regression risk

**Low** — additive response fields; session restore unchanged except `has_profile` on `/auth/me`.

## Rollback

Revert this commit; clients fall back to `/auth/me` on every login.

## Follow-ups

- P1-05 — wire `getPostAuthPath` in LoginPage/RegisterPage
