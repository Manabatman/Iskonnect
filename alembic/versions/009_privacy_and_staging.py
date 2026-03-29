"""Add privacy consent columns and scholarships_staging for CSV ingestion queue.

Revision ID: 009
Revises: 008
Create Date: 2026-03-29

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "009"
down_revision: Union[str, None] = "008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("students", sa.Column("privacy_consent_at", sa.DateTime(), nullable=True))
    op.add_column("students", sa.Column("privacy_consent_version", sa.String(), nullable=True))

    op.create_table(
        "scholarships_staging",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("provider", sa.String(), nullable=True),
        sa.Column("source", sa.String(), nullable=True),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.Column("status", sa.String(), nullable=False, server_default="pending"),
        sa.Column("dedupe_key", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.Column("reviewed_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_scholarships_staging_dedupe_key", "scholarships_staging", ["dedupe_key"], unique=False)
    op.create_index("ix_scholarships_staging_status", "scholarships_staging", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_scholarships_staging_status", table_name="scholarships_staging")
    op.drop_index("ix_scholarships_staging_dedupe_key", table_name="scholarships_staging")
    op.drop_table("scholarships_staging")
    op.drop_column("students", "privacy_consent_version")
    op.drop_column("students", "privacy_consent_at")
