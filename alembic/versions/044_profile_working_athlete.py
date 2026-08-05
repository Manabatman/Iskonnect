"""Add employment_status, evening_weekend_program, athlete_level to students.

Revision ID: 044_profile_working_athlete
Revises: 043_scholarship_versions_cascade
Create Date: 2026-08-01

Track B B9 (DATA-08): profile fields for Working Student and Student Athlete priority groups.
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "044_profile_working_athlete"
down_revision: Union[str, None] = "043_scholarship_versions_cascade"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "students",
        sa.Column("employment_status", sa.String(), nullable=True),
    )
    op.add_column(
        "students",
        sa.Column("evening_weekend_program", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "students",
        sa.Column("athlete_level", sa.String(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("students", "athlete_level")
    op.drop_column("students", "evening_weekend_program")
    op.drop_column("students", "employment_status")
