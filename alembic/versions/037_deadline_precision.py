"""037 — deadline precision metadata on scholarships."""

from alembic import op
import sqlalchemy as sa

revision = "037_deadline_precision"
down_revision = "036_enrollment_timing"
branch_labels = None
depends_on = None


def _is_postgres() -> bool:
    bind = op.get_bind()
    return bind.dialect.name == "postgresql"


def upgrade() -> None:
    op.add_column("scholarships", sa.Column("deadline_precision", sa.String(), nullable=True))
    op.add_column("scholarships", sa.Column("deadline_note", sa.Text(), nullable=True))
    op.add_column("scholarships", sa.Column("deadline_source_url", sa.String(), nullable=True))

    if not _is_postgres():
        return

    op.execute(
        """
        UPDATE scholarships SET deadline_precision = 'exact'
        WHERE deadline_precision IS NULL
          AND verification_source IN ('manual', 'team_verified', 'partner')
        """
    )
    op.execute(
        """
        UPDATE scholarships SET deadline_precision = 'estimated'
        WHERE deadline_precision IS NULL
          AND verification_source = 'csv_import'
        """
    )
    op.execute(
        """
        UPDATE scholarships SET deadline_precision = 'rolling'
        WHERE deadline_precision IS NULL
          AND cycle_type = 'rolling'
        """
    )
    op.execute(
        """
        UPDATE scholarships SET deadline_precision = 'not_announced'
        WHERE deadline_precision IS NULL
          AND application_deadline IS NULL
        """
    )
    op.execute(
        """
        UPDATE scholarships SET deadline_precision = COALESCE(deadline_precision, 'estimated')
        WHERE deadline_precision IS NULL
        """
    )


def downgrade() -> None:
    op.drop_column("scholarships", "deadline_source_url")
    op.drop_column("scholarships", "deadline_note")
    op.drop_column("scholarships", "deadline_precision")
