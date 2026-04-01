"""Add data freshness and link integrity columns to scholarships.

Revision ID: 010
Revises: 009
Create Date: 2026-03-30

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "010"
down_revision: Union[str, None] = "009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("scholarships", sa.Column("last_verified_at", sa.DateTime(), nullable=True))
    op.add_column("scholarships", sa.Column("verification_source", sa.String(), nullable=True))
    op.add_column(
        "scholarships",
        sa.Column("confidence_score", sa.Float(), nullable=True, server_default=sa.text("1.0")),
    )
    op.add_column(
        "scholarships",
        sa.Column("data_status", sa.String(), nullable=True, server_default=sa.text("'active'")),
    )
    op.add_column(
        "scholarships",
        sa.Column("link_status", sa.String(), nullable=True, server_default=sa.text("'unchecked'")),
    )
    op.add_column("scholarships", sa.Column("link_last_checked_at", sa.DateTime(), nullable=True))
    op.add_column(
        "scholarships",
        sa.Column("link_failure_count", sa.Integer(), nullable=True, server_default=sa.text("0")),
    )


def downgrade() -> None:
    op.drop_column("scholarships", "link_failure_count")
    op.drop_column("scholarships", "link_last_checked_at")
    op.drop_column("scholarships", "link_status")
    op.drop_column("scholarships", "data_status")
    op.drop_column("scholarships", "confidence_score")
    op.drop_column("scholarships", "verification_source")
    op.drop_column("scholarships", "last_verified_at")
