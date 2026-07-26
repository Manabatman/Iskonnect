"""Add editorial_state lifecycle column to scholarships."""

from alembic import op
import sqlalchemy as sa

revision = "041_editorial_state"
down_revision = "040_organizations"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "scholarships",
        sa.Column("editorial_state", sa.String(), nullable=True),
    )
    op.execute(
        """
        UPDATE scholarships SET editorial_state = CASE
            WHEN is_active IS NOT TRUE THEN 'archived'
            WHEN data_status = 'needs_review' THEN 'needs_review'
            WHEN data_status = 'broken_link' THEN 'needs_review'
            WHEN is_active IS TRUE THEN 'published'
            ELSE 'draft'
        END
        WHERE editorial_state IS NULL
        """
    )


def downgrade() -> None:
    op.drop_column("scholarships", "editorial_state")
