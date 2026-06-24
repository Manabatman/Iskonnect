"""Enable Row Level Security on all public base tables (Supabase Data API hardening).

Supabase exposes the public schema via PostgREST. Tables without RLS trigger Security Advisor
warnings. Enabling RLS with no policies blocks anon/authenticated from seeing rows via the
Data API. Direct Postgres connections used by this FastAPI app run as the table owner role
from migrations, which bypasses RLS unless FORCE ROW LEVEL SECURITY is set (we do not).

Revision ID: 020
Revises: 019
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "020"
down_revision: Union[str, None] = "019"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _public_base_tables(conn) -> list[str]:
    rows = conn.execute(
        sa.text(
            """
            SELECT c.relname
            FROM pg_class c
            JOIN pg_namespace n ON n.oid = c.relnamespace
            WHERE n.nspname = 'public'
              AND c.relkind = 'r'
            ORDER BY c.relname
            """
        )
    ).fetchall()
    return [r[0] for r in rows]


def _is_postgres(conn) -> bool:
    return conn.dialect.name == "postgresql"


def upgrade() -> None:
    conn = op.get_bind()
    if not _is_postgres(conn):
        # RLS is PostgreSQL-only; local SQLite dev skips this revision.
        return
    for name in _public_base_tables(conn):
        safe = name.replace('"', '""')
        op.execute(sa.text(f'ALTER TABLE public."{safe}" ENABLE ROW LEVEL SECURITY'))


def downgrade() -> None:
    conn = op.get_bind()
    if not _is_postgres(conn):
        return
    for name in _public_base_tables(conn):
        safe = name.replace('"', '""')
        op.execute(sa.text(f'ALTER TABLE public."{safe}" DISABLE ROW LEVEL SECURITY'))
