"""038 — field_evidence table and scholarship verification metadata."""

from alembic import op
import sqlalchemy as sa

revision = "038_field_evidence"
down_revision = "037_deadline_precision"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "field_evidence",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("scholarship_id", sa.Integer(), sa.ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("field_key", sa.String(128), nullable=False),
        sa.Column("value_snapshot", sa.Text(), nullable=True),
        sa.Column("source_url", sa.String(2048), nullable=True),
        sa.Column("source_type", sa.String(64), nullable=True),
        sa.Column("evidence_snippet", sa.Text(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("retrieved_at", sa.DateTime(), nullable=True),
        sa.Column("reviewer_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("superseded_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_field_evidence_sch_field", "field_evidence", ["scholarship_id", "field_key"])

    op.add_column(
        "scholarships",
        sa.Column("verified_by", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
    )
    op.add_column("scholarships", sa.Column("next_review_date", sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column("scholarships", "next_review_date")
    op.drop_column("scholarships", "verified_by")
    op.drop_index("ix_field_evidence_sch_field", table_name="field_evidence")
    op.drop_table("field_evidence")
