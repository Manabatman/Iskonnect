"""Add per-user notification preference columns."""

from alembic import op
import sqlalchemy as sa

revision = "032_notify_prefs"
down_revision = "031_data_completeness_score"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("notify_deadline_reminders", sa.Boolean(), nullable=False, server_default="1"),
    )
    op.add_column(
        "users",
        sa.Column("notify_new_matches", sa.Boolean(), nullable=False, server_default="1"),
    )


def downgrade() -> None:
    op.drop_column("users", "notify_new_matches")
    op.drop_column("users", "notify_deadline_reminders")
