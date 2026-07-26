"""Ensure scholarship_versions.scholarship_id cascades on delete (PostgreSQL)."""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import inspect

revision: str = "043_scholarship_versions_cascade"
down_revision: Union[str, None] = "042_reports_corrections"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return
    table = "scholarship_versions"
    col = "scholarship_id"
    cname = "scholarship_versions_scholarship_id_fkey"
    fks = {fk["name"] for fk in inspect(bind).get_foreign_keys(table)}
    if cname in fks:
        try:
            op.drop_constraint(cname, table, type_="foreignkey")
        except Exception:
            pass
    op.create_foreign_key(cname, table, "scholarships", [col], ["id"], ondelete="CASCADE")


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return
    table = "scholarship_versions"
    col = "scholarship_id"
    cname = "scholarship_versions_scholarship_id_fkey"
    try:
        op.drop_constraint(cname, table, type_="foreignkey")
    except Exception:
        pass
    op.create_foreign_key(cname, table, "scholarships", [col], ["id"])
