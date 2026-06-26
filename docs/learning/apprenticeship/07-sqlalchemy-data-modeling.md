# Lesson 07 — SQLAlchemy & Data Modeling

> **Prerequisite:** [06 — FastAPI & Request Lifecycle](06-fastapi-and-request-lifecycle.md)

---

## Concept: Relational database

### 1. Definition

A **relational database** stores data in **tables** (rows and columns) with relationships via **foreign keys**.

### 2. Why Postgres (Supabase)

ACID transactions, indexes, JSON support, mature hosting, connection pooling.

### 3. Problem solved

**Structured queries:** "All scholarships where `max_income_threshold >= student income`."

### 4. Before ORMs

Raw SQL strings in every route — SQL injection risk, no type hints.

### 5. ORM alternative

**SQLAlchemy Core** (SQL expressions without classes). Iskonnect uses **ORM** for models + occasional `text()` for health checks.

---

## Concept: ORM (Object-Relational Mapper)

### 1. Definition

Maps Python classes to SQL tables. A `Student` instance ↔ row in `students`.

### 2. [`app/db.py`](../../../app/db.py)

```python
engine = create_engine(settings.database_url, ...)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### Connection pooling (Postgres)

```python
engine_kwargs["pool_pre_ping"] = True   # drop dead connections
engine_kwargs["pool_recycle"] = 300     # recycle every 5 min
engine_kwargs["pool_size"] = settings.db_pool_size
```

**Why:** Render opens limited DB connections; pooling reuses them across requests.

**Production failure:** `pool_size` too high → Supabase connection limit exhausted → `too many connections`.

### SQLite dev mode

```python
if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False
```

SQLite default forbids cross-thread access; FastAPI workers need `check_same_thread=False`.

---

## [`app/models.py`](../../../app/models.py)

Central ORM definitions. Key entities:

| Model | Table | Purpose |
|-------|-------|---------|
| `User` | `users` | Login account, role |
| `Student` | `students` | Scholarship profile (linked via `user_id`) |
| `Scholarship` | `scholarships` | Catalog row |
| `Application` | `applications` | Student applied to scholarship |
| `SavedScholarship` | `saved_scholarships` | Bookmarks |
| `MatchRun` | `match_runs` | Historical match results |
| `RefreshToken` | `refresh_tokens` | Hashed refresh tokens |
| `DocumentChecklist` | `document_checklists` | Per-scholarship doc tracking |

### Ownership pattern

Migration `002` added `user_id` on `students` — **every profile belongs to one user**. Routes check `profile.user_id == current_user.id` before read/write.

**If ownership check removed:** IDOR vulnerability — user A reads user B's profile.

---

## Session lifecycle

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Typical route:

```python
@router.get("/profiles/{profile_id}")
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    row = db.query(models.Student).filter(models.Student.id == profile_id).first()
```

**`db.commit()`** — persist changes. **`db.rollback()`** — undo on error.

**Common mistake:** Forgetting `commit()` — data disappears when session closes.

---

## JSON in columns

Many scholarship fields store JSON arrays as `Text`:

```python
eligible_regions = Column(Text)  # '["ncr", "region iii"]'
```

Parsed at runtime via [`app/utils/json_helpers.py`](../../../app/utils/json_helpers.py) `parse_json()`.

**Tradeoff:** Flexible schema vs query performance. Indexes on JSON require migration to JSONB (future optimization).

---

## Foreign keys and cascades

Migrations `022`, `023` added FK cascades — deleting a user can cascade to profiles/applications per defined rules.

**Senior question:** ON DELETE CASCADE vs SET NULL — wrong choice loses data or orphans rows.

---

## Exercises

### Level 1 — Understanding

1. Difference between `engine` and `SessionLocal`?
2. Why `pool_pre_ping`?

### Level 2 — Implementation

1. Query all active scholarships with SQLAlchemy in a Python shell (`python -c` or REPL).

### Level 3 — Debugging

1. Simulate "too many connections" — what env vars and code control pool size?

### Level 4 — Architecture

1. When would you denormalize match results into `match_runs` instead of recomputing every page load?

<details>
<summary>Solution</summary>

Engine manages connections; SessionLocal creates per-request Unit of Work. pool_pre_ping tests connection before checkout — avoids stale SSL disconnects from Supabase pooler. match_runs store snapshot for history/comparison — recomputing is expensive and scores change when catalog updates.
</details>

---

*Previous: [06 — FastAPI](06-fastapi-and-request-lifecycle.md) | Next: [08 — Pydantic & Schemas](08-pydantic-validation-and-schemas.md)*
