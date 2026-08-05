"""Enable RLS on tables created after migration 020's blanket enable."""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "047"
down_revision: Union[str, None] = "046_referral_click_daily"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLES = ("organizations", "field_evidence", "referral_click_daily")


def _is_postgres(conn) -> bool:
    return conn.dialect.name == "postgresql"


def upgrade() -> None:
    conn = op.get_bind()
    if not _is_postgres(conn):
        return
    for name in TABLES:
        safe = name.replace('"', '""')
        op.execute(sa.text(f'ALTER TABLE public."{safe}" ENABLE ROW LEVEL SECURITY'))


def downgrade() -> None:
    conn = op.get_bind()
    if not _is_postgres(conn):
        return
    for name in TABLES:
        safe = name.replace('"', '""')
        op.execute(sa.text(f'ALTER TABLE public."{safe}" DISABLE ROW LEVEL SECURITY'))
