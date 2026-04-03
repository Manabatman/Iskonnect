"""Add scoring explanation fields to match_results.

Revision ID: 012
Revises: 011
Create Date: 2026-04-03

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "012"
down_revision: Union[str, None] = "011"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("match_results", sa.Column("suggestions", sa.Text(), nullable=True))
    op.add_column("match_results", sa.Column("confidence", sa.String(), nullable=True))
    op.add_column("match_results", sa.Column("why_not_higher", sa.Text(), nullable=True))
    op.add_column("match_results", sa.Column("scoring_policy_version", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("match_results", "scoring_policy_version")
    op.drop_column("match_results", "why_not_higher")
    op.drop_column("match_results", "confidence")
    op.drop_column("match_results", "suggestions")
