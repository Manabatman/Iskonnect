"""Indexes for common query paths (matches, search, notifications).

Revision ID: 017
Revises: 016
"""
from typing import Sequence, Union

from alembic import op

revision: str = "017"
down_revision: Union[str, None] = "016"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index("ix_scholarships_is_active", "scholarships", ["is_active"], unique=False)
    op.create_index(
        "ix_scholarships_active_data_status",
        "scholarships",
        ["is_active", "data_status"],
        unique=False,
    )
    op.create_index("ix_notifications_user_read", "notifications", ["user_id", "is_read"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_notifications_user_read", table_name="notifications")
    op.drop_index("ix_scholarships_active_data_status", table_name="scholarships")
    op.drop_index("ix_scholarships_is_active", table_name="scholarships")
