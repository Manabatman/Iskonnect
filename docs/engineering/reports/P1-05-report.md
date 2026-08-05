# P1-05 Report

## Objective

Route newly registered users without a profile to `/profile-builder` instead of an empty dashboard.

## Files changed

- `frontend/src/pages/LoginPage.tsx` — `getPostAuthPath` after login
- `frontend/src/pages/RegisterPage.tsx` — `getPostAuthPath` after register

## Tests

- [x] Covered by `AuthContext.test.ts` (`getPostAuthPath`)
- [x] `npm run lint`, `typecheck`, `test`, `build`

## Regression risk

Low — users with profiles still land on dashboard; explicit `returnTo` preserved.
