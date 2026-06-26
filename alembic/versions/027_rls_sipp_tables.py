"""Enable RLS on SIPP/OJT tables added after migration 020.

Revision ID: 027
Revises: 026
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "027"
down_revision: Union[str, None] = "026"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_SIPP_TABLES = (
    "hte_partners",
    "internship_opportunities",
    "ojt_compliance_vault",
)


def _is_postgres(conn) -> bool:
    return conn.dialect.name == "postgresql"


def upgrade() -> None:
    conn = op.get_bind()
    if not _is_postgres(conn):
        return
    for name in _SIPP_TABLES:
        safe = name.replace('"', '""')
        op.execute(sa.text(f'ALTER TABLE public."{safe}" ENABLE ROW LEVEL SECURITY'))


def downgrade() -> None:
    conn = op.get_bind()
    if not _is_postgres(conn):
        return
    for name in _SIPP_TABLES:
        safe = name.replace('"', '""')
        op.execute(sa.text(f'ALTER TABLE public."{safe}" DISABLE ROW LEVEL SECURITY'))
