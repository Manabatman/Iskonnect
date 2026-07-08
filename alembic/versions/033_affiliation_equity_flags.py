"""Add affiliation-sector equity flags on student profiles."""

from alembic import op
import sqlalchemy as sa

revision = "033_affiliation_equity"
down_revision = "032_notify_prefs"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("students", sa.Column("is_military_dependent", sa.Boolean(), nullable=False, server_default=sa.text("false")))
    op.add_column("students", sa.Column("is_uniformed_service_dependent", sa.Boolean(), nullable=False, server_default=sa.text("false")))
    op.add_column("students", sa.Column("is_gsis_dependent", sa.Boolean(), nullable=False, server_default=sa.text("false")))
    op.add_column("students", sa.Column("is_sss_dependent", sa.Boolean(), nullable=False, server_default=sa.text("false")))


def downgrade() -> None:
    op.drop_column("students", "is_sss_dependent")
    op.drop_column("students", "is_gsis_dependent")
    op.drop_column("students", "is_uniformed_service_dependent")
    op.drop_column("students", "is_military_dependent")
