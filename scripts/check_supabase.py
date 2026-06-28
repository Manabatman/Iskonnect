"""One-off: verify DATABASE_URL and list public tables (run from repo root)."""
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import create_engine, text

from app.config import settings


def _validate_database_url(url: str) -> list[str]:
    """Return warnings for production Postgres URL shape (Supabase pooler)."""
    warnings: list[str] = []
    u = (url or "").strip()
    if not u.lower().startswith("postgres"):
        return warnings
    if "+psycopg2" not in u.lower():
        warnings.append("DATABASE_URL should use postgresql+psycopg2:// (this app uses psycopg2-binary)")
    parsed = urlparse(u.replace("postgresql+psycopg2", "postgresql", 1))
    port = parsed.port
    if port and port != 6543:
        warnings.append(
            f"DATABASE_URL port is {port}; Supabase transaction pooler expects 6543 "
            "(direct 5432 can exhaust connections with multiple workers)"
        )
    if "sslmode=require" not in u.lower():
        warnings.append("DATABASE_URL should include ?sslmode=require for Supabase")
    return warnings


def main() -> None:
    url = settings.database_url
    for w in _validate_database_url(url):
        print("WARNING:", w)
    e = create_engine(url, pool_pre_ping=True, connect_args={"connect_timeout": 5} if not url.startswith("sqlite") else {})
    with e.connect() as c:
        if url.startswith("sqlite"):
            v = c.execute(text("select sqlite_version()")).scalar()
            print("Connected OK (sqlite):", v)
            print("(Postgres pooler URL checks apply when DATABASE_URL is postgresql+psycopg2://...:6543/...?sslmode=require)")
            return
        else:
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
        if ver != "028_scholarship_image":
            print("WARNING: expected alembic head 028_scholarship_image; run: alembic upgrade head")
        try:
            n = c.execute(text("select count(*) from scholarships")).scalar()
            print("Scholarships rows:", n)
        except Exception as ex:
            print("Scholarships count failed:", ex)
        try:
            pending = c.execute(
                text("select count(*) from scholarships_staging where status = 'pending'")
            ).scalar()
            print("Staging pending rows:", pending)
        except Exception as ex:
            print("Staging pending count failed:", ex)


if __name__ == "__main__":
    main()
