"""Add data_completeness_score to scholarships."""

from alembic import op
import sqlalchemy as sa

revision = "031_data_completeness_score"
down_revision = "030_add_application_status"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "scholarships",
        sa.Column("data_completeness_score", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("scholarships", "data_completeness_score")
