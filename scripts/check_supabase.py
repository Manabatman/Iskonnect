"""One-off: verify DATABASE_URL and list public tables (run from repo root)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import create_engine, text

from app.config import settings


def main() -> None:
    e = create_engine(settings.database_url, pool_pre_ping=True)
    with e.connect() as c:
        v = c.execute(text("select version()")).scalar()
        print("Connected OK:", (v or "")[:70], "...")
        rows = c.execute(
            text(
                """
                select table_name from information_schema.tables
                where table_schema = 'public' and table_type = 'BASE TABLE'
                order by table_name
                """
            )
        ).fetchall()
        print("Public tables:", len(rows))
        for r in rows:
            print(" -", r[0])
        ver = c.execute(text("select version_num from alembic_version")).scalar()
        print("Alembic revision:", ver)
        try:
            n = c.execute(text("select count(*) from scholarships")).scalar()
            print("Scholarships rows:", n)
        except Exception as ex:
            print("Scholarships count failed:", ex)


if __name__ == "__main__":
    main()
