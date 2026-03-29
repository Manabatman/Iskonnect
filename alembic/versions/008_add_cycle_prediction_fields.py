"""Add cycle prediction fields to scholarships table

Revision ID: 008
Revises: 007
Create Date: 2025-03-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "008"
down_revision: Union[str, None] = "007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "scholarships",
        sa.Column("last_open_date", sa.Date(), nullable=True),
    )
    op.add_column(
        "scholarships",
        sa.Column("last_close_date", sa.Date(), nullable=True),
    )
    op.add_column(
        "scholarships",
        sa.Column("cycle_type", sa.String(), nullable=True),
    )
    # Backfill from existing application dates
    op.execute(
        "UPDATE scholarships SET last_open_date = application_open_date WHERE application_open_date IS NOT NULL"
    )
    op.execute(
        "UPDATE scholarships SET last_close_date = application_deadline WHERE application_deadline IS NOT NULL"
    )


def downgrade() -> None:
    op.drop_column("scholarships", "cycle_type")
    op.drop_column("scholarships", "last_close_date")
    op.drop_column("scholarships", "last_open_date")
