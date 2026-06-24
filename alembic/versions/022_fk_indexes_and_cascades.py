"""FK indexes and ON DELETE cascades for orphan-prone relationships.

Revision ID: 022
Revises: 021
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision: str = "022"
down_revision: Union[str, None] = "021"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _index_names(table: str, bind) -> set[str]:
    return {idx["name"] for idx in inspect(bind).get_indexes(table)}


def upgrade() -> None:
    bind = op.get_bind()
    indexes = {
        "notifications": "ix_notifications_scholarship_id",
        "scholarship_reports": "ix_scholarship_reports_reviewer_id",
        "scholarships": "ix_scholarships_sponsor_id",
    }
    for table, idx_name in indexes.items():
        if idx_name not in _index_names(table, bind):
            col = "reviewer_id" if table == "scholarship_reports" else (
                "sponsor_id" if table == "scholarships" else "scholarship_id"
            )
            op.create_index(idx_name, table, [col], unique=False)

    if bind.dialect.name == "postgresql":
        fk_updates = [
            ("match_results", "match_results_scholarship_id_fkey", "scholarship_id"),
            ("saved_scholarships", "saved_scholarships_scholarship_id_fkey", "scholarship_id"),
            ("notifications", "notifications_scholarship_id_fkey", "scholarship_id"),
            ("scholarship_reports", "scholarship_reports_scholarship_id_fkey", "scholarship_id"),
        ]
        for table, cname, col in fk_updates:
            try:
                op.drop_constraint(cname, table, type_="foreignkey")
            except Exception:
                pass
            op.create_foreign_key(cname, table, "scholarships", [col], ["id"], ondelete="CASCADE")


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        fk_updates = [
            ("match_results", "match_results_scholarship_id_fkey", "scholarship_id"),
            ("saved_scholarships", "saved_scholarships_scholarship_id_fkey", "scholarship_id"),
            ("notifications", "notifications_scholarship_id_fkey", "scholarship_id"),
            ("scholarship_reports", "scholarship_reports_scholarship_id_fkey", "scholarship_id"),
        ]
        for table, cname, col in fk_updates:
            try:
                op.drop_constraint(cname, table, type_="foreignkey")
            except Exception:
                pass
            op.create_foreign_key(cname, table, "scholarships", [col], ["id"])

    for idx_name, table in [
        ("ix_scholarships_sponsor_id", "scholarships"),
        ("ix_scholarship_reports_reviewer_id", "scholarship_reports"),
        ("ix_notifications_scholarship_id", "notifications"),
    ]:
        if idx_name in _index_names(table, bind):
            op.drop_index(idx_name, table_name=table)
