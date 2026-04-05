"""Google Drive vault URL on students + scraper run audit table.

Revision ID: 018
Revises: 017
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "018"
down_revision: Union[str, None] = "017"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "students",
        sa.Column("google_drive_folder_url", sa.String(length=2048), nullable=True),
    )
    op.create_table(
        "scraper_runs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(length=64), nullable=False),
        sa.Column("started_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="running"),
        sa.Column("records_found", sa.Integer(), nullable=True),
        sa.Column("records_ingested", sa.Integer(), nullable=True),
        sa.Column("output_path", sa.String(length=1024), nullable=True),
        sa.Column("error_detail", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_scraper_runs_source_started", "scraper_runs", ["source", "started_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_scraper_runs_source_started", table_name="scraper_runs")
    op.drop_table("scraper_runs")
    op.drop_column("students", "google_drive_folder_url")
