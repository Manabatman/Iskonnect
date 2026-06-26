"""SIPP/OJT compliance tables (CHED CMO 104).

Revision ID: 025
Revises: 024
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "025"
down_revision: Union[str, None] = "024"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hte_partners",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("industry", sa.String(128), nullable=True),
        sa.Column("moa_status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("contact_email", sa.String(255), nullable=True),
        sa.Column("contact_phone", sa.String(32), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )

    op.create_table(
        "internship_opportunities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("hte_id", sa.Integer(), sa.ForeignKey("hte_partners.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("priority_courses", sa.Text(), nullable=True),
        sa.Column("region", sa.String(64), nullable=True),
        sa.Column("province", sa.String(128), nullable=True),
        sa.Column("psgc_code", sa.String(9), nullable=True),
        sa.Column("slots", sa.Integer(), nullable=True),
        sa.Column("allowance_status", sa.String(32), nullable=True),
        sa.Column("allowance_amount", sa.Float(), nullable=True),
        sa.Column("application_deadline", sa.Date(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_internship_opportunities_hte_id", "internship_opportunities", ["hte_id"])
    op.create_index("ix_internship_opportunities_psgc_code", "internship_opportunities", ["psgc_code"])

    op.create_table(
        "ojt_compliance_vault",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("student_id", sa.Integer(), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column(
            "internship_id",
            sa.Integer(),
            sa.ForeignKey("internship_opportunities.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("document_type", sa.String(48), nullable=False),
        sa.Column("template_version", sa.String(32), nullable=True),
        sa.Column("prefilled_fields", sa.Text(), nullable=True),
        sa.Column("external_url", sa.String(2048), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("guardian_consent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_ojt_compliance_vault_student_id", "ojt_compliance_vault", ["student_id"])
    op.create_index("ix_ojt_compliance_vault_internship_id", "ojt_compliance_vault", ["internship_id"])


def downgrade() -> None:
    op.drop_index("ix_ojt_compliance_vault_internship_id", table_name="ojt_compliance_vault")
    op.drop_index("ix_ojt_compliance_vault_student_id", table_name="ojt_compliance_vault")
    op.drop_table("ojt_compliance_vault")
    op.drop_index("ix_internship_opportunities_psgc_code", table_name="internship_opportunities")
    op.drop_index("ix_internship_opportunities_hte_id", table_name="internship_opportunities")
    op.drop_table("internship_opportunities")
    op.drop_table("hte_partners")
