"""Per-application Drive folder URL + soft remove timestamp on applications.

Revision ID: 019
Revises: 018
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision: str = "019"
down_revision: Union[str, None] = "018"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    insp = inspect(bind)
    cols = {c["name"] for c in insp.get_columns("applications")}
    if "drive_folder_url" not in cols:
        op.add_column("applications", sa.Column("drive_folder_url", sa.String(length=2048), nullable=True))
    if "removed_at" not in cols:
        op.add_column("applications", sa.Column("removed_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    insp = inspect(bind)
    cols = {c["name"] for c in insp.get_columns("applications")}
    if "removed_at" in cols:
        op.drop_column("applications", "removed_at")
    if "drive_folder_url" in cols:
        op.drop_column("applications", "drive_folder_url")
