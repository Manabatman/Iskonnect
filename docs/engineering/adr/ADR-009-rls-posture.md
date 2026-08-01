# ADR-009: Postgres RLS posture

**Status:** Accepted  
**Date:** 2026-07-31  
**Deciders:** Engineering (Phase 3 M3 security)

## Context

Migration `020` enables Row Level Security on several tables with **no policies** (deny-all for PostgREST). A blueprint exists in `docs/supabase_rls_blueprint.sql` for future Supabase Auth integration.

Production authentication uses **custom JWT via FastAPI** (`app/auth.py`), not Supabase Auth. The API connects as the database table owner; **RLS is bypassed** for application queries today.

## Decision

**FastAPI is the sole authorization enforcement layer for launch.**

- Do **not** apply RLS policies from the blueprint while the API uses the service role / owner connection.
- Keep RLS enabled without policies on exposed tables only if PostgREST/public SQL access is blocked (current posture).
- Revisit RLS when/if browser clients authenticate through Supabase Auth and `users.id` aligns with `auth.uid()`.

## Compensating controls

- Per-route ownership checks (`require_profile_owner`, `get_current_user_id`).
- Cross-user isolation covered by pytest authz tests.
- Admin routes gated by `require_admin`.
- No direct client access to Postgres; all student data flows through the API.

## Consequences

- A misconfigured direct DB connection with a non-owner role could see less data (deny-all), but the owner connection used by the API must remain protected.
- Defense-in-depth via RLS is deferred until auth model migration.

**Review date:** When Supabase Auth migration is scoped (Phase 4+).
