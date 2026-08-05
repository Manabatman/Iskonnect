"""C9: aggregate-only outbound referral click counts (no PII)."""

from alembic import op
import sqlalchemy as sa

revision = "046_referral_click_daily"
down_revision = "045_c8_prefs_feedback"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "referral_click_daily",
        sa.Column("day", sa.Date(), nullable=False),
        sa.Column("scholarship_id", sa.Integer(), sa.ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False),
        sa.Column("surface", sa.String(32), nullable=False),
        sa.Column("link_kind", sa.String(32), nullable=False),
        sa.Column("click_count", sa.Integer(), nullable=False, server_default="0"),
        sa.PrimaryKeyConstraint("day", "scholarship_id", "surface", "link_kind"),
    )
    op.create_index("ix_referral_click_daily_day", "referral_click_daily", ["day"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_referral_click_daily_day", table_name="referral_click_daily")
    op.drop_table("referral_click_daily")
