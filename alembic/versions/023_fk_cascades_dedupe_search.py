"""FK cascades, dedupe uniqueness, and search indexes.

Revision ID: 023
Revises: 022
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect, text

revision: str = "023"
down_revision: Union[str, None] = "022"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_exists(table: str, column: str, bind) -> bool:
    return column in {c["name"] for c in inspect(bind).get_columns(table)}


def _index_names(table: str, bind) -> set[str]:
    return {idx["name"] for idx in inspect(bind).get_indexes(table)}


def upgrade() -> None:
    bind = op.get_bind()

    if not _column_exists("scholarships", "dedupe_key", bind):
        op.add_column("scholarships", sa.Column("dedupe_key", sa.String(), nullable=True))
        op.create_index("ix_scholarships_dedupe_key", "scholarships", ["dedupe_key"], unique=False)

    # Backfill dedupe_key from title|provider|link
    if bind.dialect.name == "postgresql":
        op.execute(
            text(
                """
                UPDATE scholarships SET dedupe_key = left(
                    encode(
                        digest(
                            lower(trim(coalesce(title, ''))) || '|' ||
                            lower(trim(coalesce(provider, ''))) || '|' ||
                            lower(trim(coalesce(link, ''))),
                            'sha256'
                        ),
                        'hex'
                    ),
                    64
                )
                WHERE dedupe_key IS NULL
                """
            )
        )
    else:
        # SQLite fallback: Python-less backfill skipped; keys set on new rows
        pass

    if "uq_scholarships_dedupe_key" not in _index_names("scholarships", bind):
        try:
            op.create_index("uq_scholarships_dedupe_key", "scholarships", ["dedupe_key"], unique=True)
        except Exception:
            pass

    # Partial unique: one pending staging row per dedupe_key
    if bind.dialect.name == "postgresql":
        op.execute(
            text(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS uq_staging_pending_dedupe_key
                ON scholarship_staging (dedupe_key)
                WHERE status = 'pending' AND dedupe_key IS NOT NULL
                """
            )
        )

        fk_updates = [
            ("match_runs", "match_runs_user_id_fkey", "users", "user_id", "CASCADE"),
            ("match_runs", "match_runs_profile_id_fkey", "students", "profile_id", "CASCADE"),
            ("match_results", "match_results_run_id_fkey", "match_runs", "run_id", "CASCADE"),
            ("notifications", "notifications_user_id_fkey", "users", "user_id", "CASCADE"),
            ("saved_scholarships", "saved_scholarships_user_id_fkey", "users", "user_id", "CASCADE"),
        ]
        for table, cname, ref_table, col, ondelete in fk_updates:
            try:
                op.drop_constraint(cname, table, type_="foreignkey")
            except Exception:
                pass
            op.create_foreign_key(cname, table, ref_table, [col], ["id"], ondelete=ondelete)

        # Trigram search index (L1)
        op.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        op.execute(
            text(
                """
                CREATE INDEX IF NOT EXISTS ix_scholarships_title_trgm
                ON scholarships USING gin (title gin_trgm_ops)
                """
            )
        )


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute(text("DROP INDEX IF EXISTS ix_scholarships_title_trgm"))
        op.execute(text("DROP INDEX IF EXISTS uq_staging_pending_dedupe_key"))
    if "uq_scholarships_dedupe_key" in _index_names("scholarships", bind):
        op.drop_index("uq_scholarships_dedupe_key", table_name="scholarships")
    if _column_exists("scholarships", "dedupe_key", bind):
        op.drop_index("ix_scholarships_dedupe_key", table_name="scholarships")
        op.drop_column("scholarships", "dedupe_key")
