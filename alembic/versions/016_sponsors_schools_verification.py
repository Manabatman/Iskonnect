"""Sponsor and school roles, verification requests, scholarship ownership.

Revision ID: 016
Revises: 015
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "016"
down_revision: Union[str, None] = "015"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "sponsors",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("org_type", sa.String(64), nullable=True),
        sa.Column("contact_email", sa.String(255), nullable=True),
        sa.Column("logo_url", sa.String(512), nullable=True),
        sa.Column("website", sa.String(512), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("1"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
    )

    op.create_table(
        "sponsor_users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("sponsor_id", sa.Integer(), sa.ForeignKey("sponsors.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("role", sa.String(64), nullable=False, server_default="reviewer"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.UniqueConstraint("user_id", "sponsor_id", name="uq_sponsor_users_user_sponsor"),
    )

    op.create_table(
        "schools",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("region", sa.String(128), nullable=True),
        sa.Column("province", sa.String(128), nullable=True),
        sa.Column("school_type", sa.String(64), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("1"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
    )

    op.create_table(
        "school_users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("school_id", sa.Integer(), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("role", sa.String(64), nullable=False, server_default="verifier"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.UniqueConstraint("user_id", "school_id", name="uq_school_users_user_school"),
    )

    op.create_table(
        "verification_requests",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("application_id", sa.Integer(), sa.ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("school_id", sa.Integer(), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("verification_type", sa.String(64), nullable=False, server_default="enrollment"),
        sa.Column("status", sa.String(64), nullable=False, server_default="pending"),
        sa.Column("requested_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.Column("verified_at", sa.DateTime(), nullable=True),
        sa.Column("verifier_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
    )

    conn = op.get_bind()
    if conn.dialect.name == "sqlite":
        with op.batch_alter_table("scholarships") as batch_op:
            batch_op.add_column(sa.Column("sponsor_id", sa.Integer(), nullable=True))
            batch_op.create_foreign_key(
                "fk_scholarships_sponsor_id",
                "sponsors",
                ["sponsor_id"],
                ["id"],
                ondelete="SET NULL",
            )
    else:
        op.add_column("scholarships", sa.Column("sponsor_id", sa.Integer(), nullable=True))
        op.create_foreign_key(
            "fk_scholarships_sponsor_id",
            "scholarships",
            "sponsors",
            ["sponsor_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade() -> None:
    conn = op.get_bind()
    if conn.dialect.name == "sqlite":
        with op.batch_alter_table("scholarships") as batch_op:
            batch_op.drop_constraint("fk_scholarships_sponsor_id", type_="foreignkey")
            batch_op.drop_column("sponsor_id")
    else:
        op.drop_constraint("fk_scholarships_sponsor_id", "scholarships", type_="foreignkey")
        op.drop_column("scholarships", "sponsor_id")
    op.drop_table("verification_requests")
    op.drop_table("school_users")
    op.drop_table("schools")
    op.drop_table("sponsor_users")
    op.drop_table("sponsors")
