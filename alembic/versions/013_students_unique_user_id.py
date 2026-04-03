"""One student profile per authenticated user (unique user_id).

Revision ID: 013
Revises: 012
Create Date: 2026-04-03

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "013"
down_revision: Union[str, None] = "012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    dup_users = conn.execute(
        sa.text(
            "SELECT user_id FROM students WHERE user_id IS NOT NULL "
            "GROUP BY user_id HAVING COUNT(*) > 1"
        )
    ).fetchall()
    for (uid,) in dup_users:
        ids = [
            r[0]
            for r in conn.execute(
                sa.text("SELECT id FROM students WHERE user_id = :u ORDER BY id DESC"),
                {"u": uid},
            ).fetchall()
        ]
        for sid in ids[1:]:
            conn.execute(sa.text("DELETE FROM students WHERE id = :sid"), {"sid": sid})

    # SQLite cannot ALTER TABLE to add constraints; use batch mode (table rebuild).
    if conn.dialect.name == "sqlite":
        with op.batch_alter_table("students") as batch_op:
            batch_op.create_unique_constraint("uq_students_user_id", ["user_id"])
    else:
        op.create_unique_constraint("uq_students_user_id", "students", ["user_id"])


def downgrade() -> None:
    conn = op.get_bind()
    if conn.dialect.name == "sqlite":
        with op.batch_alter_table("students") as batch_op:
            batch_op.drop_constraint("uq_students_user_id", type_="unique")
    else:
        op.drop_constraint("uq_students_user_id", "students", type_="unique")
