# Contributing to Iskonnect

Thank you for your interest in contributing. This project helps Filipino students find scholarships they can realistically apply for.

## Getting started

1. Fork and clone the repository
2. Set up locally (see [README.md](../README.md))
3. Create a branch for your change

### Local setup (quick)

```bash
# Backend
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
python seed_data.py
uvicorn app.main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open http://localhost:5173 — API at http://localhost:8000/docs

## Running tests

```bash
# Backend
python -m pytest app/tests/ -v

# Frontend
cd frontend && npm run typecheck && npm test
```

## Code guidelines

- Match existing patterns in the file you are editing
- Keep changes focused — one concern per PR
- Do not commit secrets (`.env`, API keys, database dumps)
- For catalog data changes, use the **staging workflow** — never write directly to production tables

## Data contributions

Scholarship imports must go through staging:

1. Prepare CSV per [docs/import_csv_contract.md](docs/import_csv_contract.md)
2. Import: `python -m app.scripts.csv_to_staging --csv your_file.csv`
3. Review in Admin → Staging
4. Approve rows individually

Field corrections use `python -m app.scripts.apply_field_changes` — see [docs/verification.md](docs/verification.md).

## Pull requests

- Describe what changed and why
- Link related issues if applicable
- Confirm tests pass locally
- For UI changes, include a brief description of the visual change

## Documentation

| Doc | Purpose |
|-----|---------|
| [docs/architecture.md](docs/architecture.md) | System design |
| [docs/api.md](docs/api.md) | API reference |
| [docs/deployment.md](docs/deployment.md) | Production deploy |
| [docs/verification.md](docs/verification.md) | Catalog data pipeline |

## Questions

Open a GitHub issue or reach out via the Contact page on the live site.
