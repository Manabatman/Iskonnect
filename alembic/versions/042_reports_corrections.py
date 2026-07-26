"""Add correction fields to scholarship_reports."""

from alembic import op
import sqlalchemy as sa

revision = "042_reports_corrections"
down_revision = "041_editorial_state"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("scholarship_reports", sa.Column("field_key", sa.String(), nullable=True))
    op.add_column("scholarship_reports", sa.Column("proposed_value", sa.Text(), nullable=True))
    op.add_column(
        "scholarship_reports",
        sa.Column("evidence_url", sa.String(2048), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("scholarship_reports", "evidence_url")
    op.drop_column("scholarship_reports", "proposed_value")
    op.drop_column("scholarship_reports", "field_key")
