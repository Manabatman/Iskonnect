# Lesson 10 — Auth: JWT & bcrypt

> **Prerequisite:** [09 — Alembic Migrations](09-alembic-migrations.md)

---

## Concept: Authentication vs authorization

| Term | Question |
|------|----------|
| **Authentication (authn)** | Who are you? |
| **Authorization (authz)** | What may you do? |

Login proves identity. Ownership checks (`profile.user_id == user.id`) prove authorization.

---

## Password storage: bcrypt

### 1. Definition

**bcrypt** is a one-way hash function designed for passwords (slow by design).

### 2. [`app/auth.py`](../../../app/auth.py)

```python
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
```

### 3. Hashing vs encryption

- **Hash:** one-way — cannot recover password from hash
- **Encryption:** reversible with key — wrong for passwords

### 4. If plaintext passwords stored

Database leak → all accounts compromised. Legal and reputational disaster.

---

## JWT (JSON Web Token)

### 1. Definition

A **JWT** is `header.payload.signature` — base64 JSON signed with `SECRET_KEY`.

### 2. Access token payload

```python
payload = {
    "sub": str(user_id),
    "role": role,
    "iat": now,
    "exp": exp,
    "typ": "access",
}
return jwt.encode(payload, settings.secret_key, algorithm="HS256")
```

### 3. Why JWT

**Stateless verification** — server checks signature without DB lookup on every request (role/user id in token).

**Tradeoff:** Cannot revoke access token before expiry without blocklist — Iskonnect uses short access (30 min) + refresh tokens in DB.

### 4. Refresh tokens

Stored **hashed** in `refresh_tokens` table. Rotation on refresh invalidates stolen tokens.

---

## `get_current_user`

Extracts `Authorization: Bearer <token>`, decodes JWT, loads `User` from DB.

### `AUTH_DISABLED=true`

Development bypass — many routes skip strict auth. **Production guard** in `config.validate_for_production()` rejects this.

---

## Email verification & password reset

Separate token types via `typ` claim:

- `email_verify` — 7-day expiry
- Password reset tokens (see `auth_routes.py`)

**Non-enumerating responses:** Register/forgot-password return same message whether email exists — prevents account enumeration.

---

## Not Supabase Auth

Iskonnect uses **custom JWT** with Supabase as **Postgres host only**. `sub` = app `users.id`, not `auth.uid()`. This matters for RLS (lesson 09).

---

## Frontend contract

[`AuthContext.tsx`](../../../frontend/src/contexts/AuthContext.tsx) stores tokens, refreshes before expiry, dispatches `scholarship-match-auth-user-changed` event.

---

## Exercises

### Level 1 — Understanding

1. Why short-lived access tokens?
2. What does `sub` contain in Iskonnect?

### Level 2 — Implementation

1. Decode a JWT payload (middle segment) with base64 — identify `exp`.

### Level 3 — Debugging

1. `401` after 30 minutes idle — trace refresh flow in AuthContext.

### Level 4 — Architecture

1. Compare session cookies vs JWT in localStorage — security tradeoffs for Iskonnect SPA.

<details>
<summary>Solution</summary>

Short access limits stolen token window. `sub` = user id string. JWT in memory/localStorage: XSS can steal token; httpOnly cookies need CSRF protection. Iskonnect uses Bearer header — standard for SPA + separate API domain.
</details>

---

*Previous: [09 — Alembic](09-alembic-migrations.md) | Next: [11 — Matching Engine Architecture](11-matching-engine-architecture.md)*
