"""Add authoritative application_status column to scholarships."""

from alembic import op
import sqlalchemy as sa

revision = "030_add_application_status"
down_revision = "029_jsonb_eligibility_gin"
branch_labels = None
depends_on = None


def _backfill_application_status(connection) -> None:
    from app.models import Scholarship
    from app.utils.application_status import sync_application_status
    from sqlalchemy.orm import Session

    session = Session(bind=connection)
    try:
        for row in session.query(Scholarship).all():
            sync_application_status(row)
        session.commit()
    finally:
        session.close()


def upgrade() -> None:
    op.add_column(
        "scholarships",
        sa.Column("application_status", sa.String(), nullable=True),
    )
    op.create_index(
        "ix_scholarships_application_status",
        "scholarships",
        ["application_status"],
        unique=False,
    )
    _backfill_application_status(op.get_bind())


def downgrade() -> None:
    op.drop_index("ix_scholarships_application_status", table_name="scholarships")
    op.drop_column("scholarships", "application_status")
