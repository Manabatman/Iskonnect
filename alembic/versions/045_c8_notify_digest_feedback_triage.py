"""C8: weekly digest preference + feedback triage columns."""

from alembic import op
import sqlalchemy as sa

revision = "045_c8_prefs_feedback"
down_revision = "044_profile_working_athlete"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("notify_weekly_digest", sa.Boolean(), nullable=False, server_default="1"),
    )
    op.add_column(
        "product_feedback",
        sa.Column("triage_status", sa.String(32), nullable=False, server_default="new"),
    )
    op.add_column(
        "product_feedback",
        sa.Column("triage_note", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("product_feedback", "triage_note")
    op.drop_column("product_feedback", "triage_status")
    op.drop_column("users", "notify_weekly_digest")
