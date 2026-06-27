"""Add optional image_url and image_alt to scholarships.

Revision ID: 028
Revises: 027
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "028"
down_revision: Union[str, None] = "027"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("scholarships", sa.Column("image_url", sa.String(length=2048), nullable=True))
    op.add_column("scholarships", sa.Column("image_alt", sa.String(length=300), nullable=True))


def downgrade() -> None:
    op.drop_column("scholarships", "image_alt")
    op.drop_column("scholarships", "image_url")
