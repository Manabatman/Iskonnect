"""
Shared pytest fixtures for ISKONNECT backend tests.

Provides in-memory SQLite engine/session and optional FastAPI TestClient
for integration tests that need a database.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base


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
