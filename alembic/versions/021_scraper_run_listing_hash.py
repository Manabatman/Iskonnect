"""Add listing_content_sha256 to scraper_runs for change-detection between scrapes.

Revision ID: 021
Revises: 020
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision: str = "021"
down_revision: Union[str, None] = "020"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    insp = inspect(bind)
    cols = {c["name"] for c in insp.get_columns("scraper_runs")}
    if "listing_content_sha256" not in cols:
        op.add_column(
            "scraper_runs",
            sa.Column("listing_content_sha256", sa.String(length=64), nullable=True),
        )


def downgrade() -> None:
    bind = op.get_bind()
    insp = inspect(bind)
    cols = {c["name"] for c in insp.get_columns("scraper_runs")}
    if "listing_content_sha256" in cols:
        op.drop_column("scraper_runs", "listing_content_sha256")
