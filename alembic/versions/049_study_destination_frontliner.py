"""Pre-beta profile fields — study destination preference and medical frontliner dependent."""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "049"
down_revision: Union[str, None] = "048"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

AFFILIATION_SEED = (
    ("medical_frontliner_dependent", "equity", "Medical frontliner dependent"),
)


def upgrade() -> None:
    op.add_column(
        "students",
        sa.Column(
            "study_destination_preference",
            sa.String(),
            nullable=False,
            server_default="PHILIPPINES_ONLY",
        ),
    )
    op.add_column(
        "students",
        sa.Column("is_medical_frontliner_dependent", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    conn = op.get_bind()
    for code, kind, label in AFFILIATION_SEED:
        conn.execute(
            sa.text(
                "INSERT INTO affiliation_codes (code, kind, label) "
                "SELECT :code, :kind, :label WHERE NOT EXISTS "
                "(SELECT 1 FROM affiliation_codes WHERE code = :code)"
            ),
            {"code": code, "kind": kind, "label": label},
        )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text("DELETE FROM affiliation_codes WHERE code = 'medical_frontliner_dependent'")
    )
    op.drop_column("students", "is_medical_frontliner_dependent")
    op.drop_column("students", "study_destination_preference")
