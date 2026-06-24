"""Guardian consent, PSGC geo codes on students (RA 10173 / geographic precision).

Revision ID: 024
Revises: 023
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision: str = "024"
down_revision: Union[str, None] = "023"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_exists(table: str, column: str, bind) -> bool:
    return column in {c["name"] for c in inspect(bind).get_columns(table)}


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "sqlite":
        with op.batch_alter_table("students") as batch:
            if not _column_exists("students", "psgc_code", bind):
                batch.add_column(sa.Column("psgc_code", sa.String(9), nullable=True))
            if not _column_exists("students", "guardian_full_name", bind):
                batch.add_column(sa.Column("guardian_full_name", sa.String(255), nullable=True))
            if not _column_exists("students", "guardian_email", bind):
                batch.add_column(sa.Column("guardian_email", sa.String(255), nullable=True))
            if not _column_exists("students", "guardian_consent_at", bind):
                batch.add_column(sa.Column("guardian_consent_at", sa.DateTime(), nullable=True))
        return

    if not _column_exists("students", "psgc_code", bind):
        op.add_column("students", sa.Column("psgc_code", sa.String(9), nullable=True))
        op.create_index("ix_students_psgc_code", "students", ["psgc_code"], unique=False)
    if not _column_exists("students", "guardian_full_name", bind):
        op.add_column("students", sa.Column("guardian_full_name", sa.String(255), nullable=True))
    if not _column_exists("students", "guardian_email", bind):
        op.add_column("students", sa.Column("guardian_email", sa.String(255), nullable=True))
    if not _column_exists("students", "guardian_consent_at", bind):
        op.add_column("students", sa.Column("guardian_consent_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    cols = ("guardian_consent_at", "guardian_email", "guardian_full_name", "psgc_code")
    if bind.dialect.name == "sqlite":
        return
    if _column_exists("students", "psgc_code", bind):
        op.drop_index("ix_students_psgc_code", table_name="students")
    for col in cols:
        if _column_exists("students", col, bind):
            op.drop_column("students", col)
