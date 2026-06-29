"""Convert scholarship JSON list columns to jsonb + GIN indexes (PostgreSQL only).

Revision ID: 029
Revises: 028
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "029"
down_revision: Union[str, None] = "028"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_JSONB_COLUMNS = (
    "needs_tags",
    "eligible_levels",
    "eligible_regions",
    "eligible_cities",
    "eligible_school_types",
    "eligible_courses_psced",
    "eligible_courses_specific",
    "priority_groups",
    "preferred_extracurriculars",
    "preferred_awards",
    "required_documents",
)


def _is_postgres() -> bool:
    bind = op.get_bind()
    return bind.dialect.name == "postgresql"


def upgrade() -> None:
    if not _is_postgres():
        return
    for col in _JSONB_COLUMNS:
        op.execute(
            sa.text(
                f"""
                ALTER TABLE scholarships
                ALTER COLUMN {col} TYPE jsonb
                USING CASE
                    WHEN {col} IS NULL OR trim({col}) = '' THEN '[]'::jsonb
                    WHEN trim({col}) LIKE '[%' THEN {col}::jsonb
                    ELSE to_jsonb(string_to_array({col}, ','))
                END
                """
            )
        )
        op.execute(
            sa.text(
                f"CREATE INDEX IF NOT EXISTS ix_scholarships_{col}_gin "
                f"ON scholarships USING gin ({col})"
            )
        )


def downgrade() -> None:
    if not _is_postgres():
        return
    for col in _JSONB_COLUMNS:
        op.execute(sa.text(f"DROP INDEX IF EXISTS ix_scholarships_{col}_gin"))
        op.execute(
            sa.text(
                f"""
                ALTER TABLE scholarships
                ALTER COLUMN {col} TYPE text
                USING {col}::text
                """
            )
        )
