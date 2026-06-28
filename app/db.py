from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

# SQLite requires check_same_thread=False; PostgreSQL benefits from pool health checks
connect_args = {}
engine_kwargs: dict = {}
if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False
else:
    # Fast-fail on unreachable Supabase pooler (psycopg2/libpq; no prepare_threshold — psycopg3-only)
    connect_args["connect_timeout"] = 5
    connect_args["options"] = "-c statement_timeout=15000"
    engine_kwargs["pool_pre_ping"] = True
    engine_kwargs["pool_recycle"] = 300
    engine_kwargs["pool_size"] = settings.db_pool_size
    engine_kwargs["max_overflow"] = settings.db_max_overflow
    engine_kwargs["pool_timeout"] = 10

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    **engine_kwargs,
)


@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    """Enable FK cascades in SQLite (off by default)."""
    if settings.database_url.startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
