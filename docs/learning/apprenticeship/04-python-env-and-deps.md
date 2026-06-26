# Lesson 04 — Python Environment & Dependencies

> **Prerequisite:** [03 — Git & Version Control](03-git-and-version-control.md)

---

## Concept: Python interpreter

### 1. Definition

The **Python interpreter** (`python`) executes `.py` files line by line.

### 2. Why version matters

Iskonnect targets **Python 3.11** (see `.python-version`). Syntax and stdlib differ across 3.9 vs 3.12 vs 3.14.

### 3. Problem solved

Consistent runtime across laptop, CI, Render.

### 4. Before version pinning

"It works on my machine" — production ran different Python → subtle bugs.

### 5. Check version

```bash
python --version
# Python 3.11.x
```

---

## Concept: Virtual environment (`venv`)

### 1. Definition

A **virtual environment** is an isolated folder with its own `python` and `pip`, separate from system Python.

### 2. Why it exists

Project A needs `fastapi==0.115`; Project B needs `0.100`. venvs prevent conflict.

### 3. Problem solved

**Dependency isolation.**

### 4. Before venv

`pip install --user` globally — dependency hell.

### 5. Alternatives

- **conda** — data science stacks
- **poetry** / **uv** — lockfiles + venv management
- **Docker** — isolates entire OS (lesson 23)

### 6. Tradeoffs

venv is stdlib, simple. Poetry adds better lockfiles but extra tooling.

### Command: `python -m venv venv`

| Aspect | Detail |
|--------|--------|
| **Syntax** | `python -m venv venv` |
| **Meaning** | Create folder `venv/` with isolated Python |
| **`-m venv`** | Run stdlib `venv` module as script |
| **Internal** | Copies or links Python binary + pip into `venv/` |
| **Output** | New `venv/` directory |
| **Mistakes** | Committing `venv/` to git — must be in `.gitignore` |

### Activate venv

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**bash/macOS:**

```bash
source venv/bin/activate
```

Prompt shows `(venv)`. `which python` points inside `venv/`.

### Deactivate

```bash
deactivate
```

---

## Concept: pip and `requirements.txt`

### 1. Definition

**pip** installs Python packages from PyPI. **`requirements.txt`** lists packages with pinned versions.

### 2. Iskonnect's [`requirements.txt`](../../../requirements.txt)

```
gunicorn==23.0.0
fastapi==0.115.6
uvicorn[standard]==0.32.1
sqlalchemy==2.0.36
pydantic[email]==2.10.3
...
```

### 3. Command: `pip install -r requirements.txt`

| Aspect | Detail |
|--------|--------|
| **Syntax** | `pip install -r requirements.txt` |
| **Meaning** | Install every line in file at exact version |
| **Why pin versions** | Reproducible builds — CI and Render get identical deps |
| **Internal** | Downloads wheels from PyPI, installs into venv `site-packages` |
| **Output** | `Successfully installed fastapi-0.115.6 ...` |
| **Mistakes** | Running without activated venv → installs globally |
| **Variations** | `pip freeze > requirements.txt` (capture current — review before commit) |

### What each major dependency does

| Package | Role in Iskonnect |
|---------|-------------------|
| `fastapi` | Web framework, routes, OpenAPI |
| `uvicorn` | ASGI server (dev + worker class) |
| `gunicorn` | Multi-process process manager (production) |
| `sqlalchemy` | ORM, talks to Postgres/SQLite |
| `psycopg2-binary` | Postgres driver |
| `alembic` | Migrations |
| `pydantic` | Request/response validation |
| `PyJWT` + `bcrypt` | Auth tokens + password hashing |
| `redis` | Cache + rate limit counters |
| `slowapi` | Rate limiting middleware |
| `sentry-sdk` | Error tracking |
| `pytest` | Tests |
| `httpx` | HTTP client (tests, scrapers) |
| `beautifulsoup4` + `lxml` | HTML parsing (scrapers) |

---

## Day-0 rebuild sequence

```bash
cd scholarship-match
python -m venv venv
# activate venv (see above)
pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy pydantic
pip freeze > requirements.txt
```

First `requirements.txt` might be 4 lines. Iskonnect's grew as features added auth, Redis, Sentry, etc.

---

## Python package layout: why `app/`

```
scholarship-match/
├── app/
│   ├── __init__.py      # marks app as importable package
│   └── main.py
└── requirements.txt
```

- **`app`** is the Python **package** name.
- `uvicorn app.main:app` means: module `app.main`, variable `app`.
- Without `app/__init__.py` (Python 3.3+ namespace packages can work but Iskonnect uses explicit package).

**If you renamed `app/` to `iskonnect/`:** Every import and uvicorn command must change — high cost, why folder stayed `scholarship-match/` at root but package is `app`.

---

## How engineers think

| Level | Behavior |
|-------|----------|
| Beginner | Installs packages globally |
| Intermediate | Always uses venv, pins major versions |
| Senior | Pins all versions, audits CVEs, tests upgrade PRs separately |

**Production failure:** Render defaults to Python 3.14, package incompatible → build fails. Fix: `.python-version` file with `3.11`.

---

## Exercises

### Level 1 — Understanding

1. What happens if you delete `venv/`?
2. Why is `psycopg2-binary` needed for Supabase but not for SQLite dev?

### Level 2 — Implementation

1. Fresh venv. Install only `fastapi` and `uvicorn`. Run a one-file `hello.py` with `FastAPI()` and `uvicorn hello:app`.

### Level 3 — Debugging

1. `ModuleNotFoundError: fastapi` — list three causes and fixes.

### Level 4 — Architecture

1. Compare pinning in `requirements.txt` vs using Poetry `poetry.lock`. When would you migrate Iskonnect?

<details>
<summary>Solution</summary>

Deleting venv removes installed packages — recreate with `python -m venv` + `pip install -r requirements.txt`. psycopg2 is Postgres adapter; SQLite uses built-in `sqlite3`. ModuleNotFound: (1) venv not activated, (2) forgot pip install, (3) wrong cwd/python. Poetry helps when dep resolution conflicts grow; Iskonnect's requirements.txt is manageable until team size or dep conflicts justify migration cost.
</details>

---

*Previous: [03 — Git & Version Control](03-git-and-version-control.md) | Next: [05 — Project Genesis Day 0](05-project-genesis-day0.md)*
