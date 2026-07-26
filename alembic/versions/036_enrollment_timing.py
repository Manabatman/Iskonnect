"""036 — enrollment timing fields on students and scholarships."""

from alembic import op
import sqlalchemy as sa

revision = "036_enrollment_timing"
down_revision = "035_school_eligibility"
branch_labels = None
depends_on = None

_NEW_SCH_JSON = ("eligible_year_levels", "eligible_enrollment_status")


def _is_postgres() -> bool:
    bind = op.get_bind()
    return bind.dialect.name == "postgresql"


def upgrade() -> None:
    op.add_column("students", sa.Column("enrollment_status", sa.String(), nullable=True))
    op.add_column("students", sa.Column("current_year_level", sa.Integer(), nullable=True))
    op.add_column("students", sa.Column("next_year_level", sa.Integer(), nullable=True))
    op.add_column("students", sa.Column("expected_graduation_date", sa.Date(), nullable=True))
    op.add_column("students", sa.Column("citizenship", sa.String(), nullable=True, server_default="Filipino"))

    for col in _NEW_SCH_JSON:
        op.add_column("scholarships", sa.Column(col, sa.Text(), nullable=True))

    if _is_postgres():
        for col in _NEW_SCH_JSON:
            op.execute(
                sa.text(
                    f"""
                    ALTER TABLE scholarships
                    ALTER COLUMN {col} TYPE jsonb
                    USING CASE
                        WHEN {col} IS NULL OR trim({col}) = '' THEN '[]'::jsonb
                        WHEN trim({col}) LIKE '[%' THEN {col}::jsonb
                        ELSE to_jsonb(string_to_array({col}, ','))
                    END
                    """
                )
            )


def downgrade() -> None:
    for col in reversed(_NEW_SCH_JSON):
        op.drop_column("scholarships", col)
    op.drop_column("students", "expected_graduation_date")
    op.drop_column("students", "citizenship")
    op.drop_column("students", "next_year_level")
    op.drop_column("students", "current_year_level")
    op.drop_column("students", "enrollment_status")
