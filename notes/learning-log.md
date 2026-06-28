# ISKONNECT Learning Log

Use one section per study session. Copy the template below for each day.

---

## Session template

```markdown
## YYYY-MM-DD — [Topic]

**Retrieval (before):** What I think happens when...

**Did today:**

**Retrieval (after):** Without looking — files, endpoints, tables involved

**Confused about:**

**Tomorrow:**
```

---

## Sessions

## 2026-06-23 — [Database Migrations]

**Retrieval (before):** What I thought was that alembic migrations are the one that seeds the database when it fact it is seed_data python script that does that

**Did today:** I learned about alembic and how schema differs from data. Imagine it like a filling cabinet. Schema is the structure folders while data is the actual papers that lives in those folders

**Retrieval (after):** Without looking — scholarship-match --> alembic --> versions

**Confused about:** 

What command applies all pending migrations? - alembic upgrade heard
Where does Alembic store which migration version is current? - alembic_version table where it contains something like 021 inside the database itself
What does Will assume non-transactional DDL tell you about SQLite? - DDL (Data definition Language) because DML (data manipulation language) is often transactional (there may be rollbacks possible) but for DDL, it is usually not transactional so there is no rollbacks. By saying will assume non-transactional DDL, Alembic is saying "I know sqlite schema changes DDL cant always be rolled back in a transaction, so alembic wont assume it can wrap them safely"

**Tomorrow:** Continue phase 0


