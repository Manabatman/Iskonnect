"""
Shared pytest fixtures for Iskonnect backend tests.

Provides in-memory SQLite engine/session and optional FastAPI TestClient
for integration tests that need a database.
"""

import os

# Avoid Alembic upgrading the developer's DATABASE_URL during TestClient lifespan
# (schema for tests comes from Base.metadata.create_all on the in-memory engine).
os.environ.setdefault("RUN_MIGRATIONS_ON_STARTUP", "false")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401 — register ORM models on Base
from app.db import Base, get_db


@pytest.fixture
def sqlite_engine():
    """In-memory SQLite engine with StaticPool (single connection for thread safety)."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def db_session(sqlite_engine):
    """SQLAlchemy session bound to in-memory SQLite with all tables created."""
    Session = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def api_with_db(sqlite_engine):
    """HTTP client against the FastAPI app with DB overridden to in-memory SQLite."""
    from app.main import app

    SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_engine)

    def override_get_db():
        db = SessionTesting()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client, SessionTesting
    app.dependency_overrides.clear()
