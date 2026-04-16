"""Add scholarship_reports, scoring_weights, scholarship_versions, audit_logs, notifications.

Revision ID: 011
Revises: 010
Create Date: 2026-03-30

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "011"
down_revision: Union[str, None] = "010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "scholarship_reports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("scholarship_id", sa.Integer(), nullable=False),
        sa.Column("issue_type", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default=sa.text("'pending'")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.Column("reviewed_at", sa.DateTime(), nullable=True),
        sa.Column("reviewer_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["reviewer_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["scholarship_id"], ["scholarships.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_scholarship_reports_id"), "scholarship_reports", ["id"], unique=False)
    op.create_index(op.f("ix_scholarship_reports_user_id"), "scholarship_reports", ["user_id"], unique=False)
    op.create_index(
        op.f("ix_scholarship_reports_scholarship_id"),
        "scholarship_reports",
        ["scholarship_id"],
        unique=False,
    )

    op.create_table(
        "scoring_weights",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("component", sa.String(), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["updated_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("component", name="uq_scoring_weights_component"),
    )
    op.create_index(op.f("ix_scoring_weights_id"), "scoring_weights", ["id"], unique=False)

    op.create_table(
        "scholarship_versions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("scholarship_id", sa.Integer(), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("changes", sa.Text(), nullable=False),
        sa.Column("changed_by", sa.Integer(), nullable=True),
        sa.Column("changed_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.ForeignKeyConstraint(["changed_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["scholarship_id"], ["scholarships.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_scholarship_versions_id"), "scholarship_versions", ["id"], unique=False)
    op.create_index(
        op.f("ix_scholarship_versions_scholarship_id"),
        "scholarship_versions",
        ["scholarship_id"],
        unique=False,
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("actor_id", sa.Integer(), nullable=True),
        sa.Column("actor_type", sa.String(), nullable=True),
        sa.Column("action", sa.String(), nullable=False),
        sa.Column("resource_type", sa.String(), nullable=True),
        sa.Column("resource_id", sa.Integer(), nullable=True),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("ip_address", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_audit_logs_id"), "audit_logs", ["id"], unique=False)
    op.create_index(op.f("ix_audit_logs_actor_id"), "audit_logs", ["actor_id"], unique=False)
    op.create_index(op.f("ix_audit_logs_action"), "audit_logs", ["action"], unique=False)

    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("body", sa.Text(), nullable=True),
        sa.Column("scholarship_id", sa.Integer(), nullable=True),
        sa.Column("is_read", sa.Boolean(), nullable=True, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.ForeignKeyConstraint(["scholarship_id"], ["scholarships.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_notifications_id"), "notifications", ["id"], unique=False)
    op.create_index(op.f("ix_notifications_user_id"), "notifications", ["user_id"], unique=False)

    # Seed default scoring weights (matches app/scoring/config.py defaults)
    op.execute(
        """
        INSERT INTO scoring_weights (id, component, weight) VALUES
        (1, 'academic', 0.30),
        (2, 'income', 0.28),
        (3, 'field_alignment', 0.22),
        (4, 'geographic', 0.10),
        (5, 'equity_priority', 0.10)
        """
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_notifications_user_id"), table_name="notifications")
    op.drop_index(op.f("ix_notifications_id"), table_name="notifications")
    op.drop_table("notifications")

    op.drop_index(op.f("ix_audit_logs_action"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_actor_id"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_id"), table_name="audit_logs")
    op.drop_table("audit_logs")

    op.drop_index(op.f("ix_scholarship_versions_scholarship_id"), table_name="scholarship_versions")
    op.drop_index(op.f("ix_scholarship_versions_id"), table_name="scholarship_versions")
    op.drop_table("scholarship_versions")

    op.drop_index(op.f("ix_scoring_weights_id"), table_name="scoring_weights")
    op.drop_table("scoring_weights")

    op.drop_index(op.f("ix_scholarship_reports_scholarship_id"), table_name="scholarship_reports")
    op.drop_index(op.f("ix_scholarship_reports_user_id"), table_name="scholarship_reports")
    op.drop_index(op.f("ix_scholarship_reports_id"), table_name="scholarship_reports")
    op.drop_table("scholarship_reports")
