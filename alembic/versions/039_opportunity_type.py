"""Add opportunity_type and type_attributes to scholarships."""

from alembic import op
import sqlalchemy as sa

revision = "039_opportunity_type"
down_revision = "038_field_evidence"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "scholarships",
        sa.Column(
            "opportunity_type",
            sa.String(),
            nullable=False,
            server_default="scholarship",
        ),
    )
    op.add_column(
        "scholarships",
        sa.Column("type_attributes", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("scholarships", "type_attributes")
    op.drop_column("scholarships", "opportunity_type")
