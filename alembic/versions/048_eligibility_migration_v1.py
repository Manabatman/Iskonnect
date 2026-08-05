"""Eligibility migration v1 — sparse columns, conflict scopes, affiliations.

Revision ID: 048_eligibility_migration_v1
Revises: 047
Create Date: 2026-08-05
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "048"
down_revision: Union[str, None] = "047"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

CONFLICT_SCOPES = (
    ("national_stufap", "National StuFAP / government grant", "Cannot hold another national government scholarship"),
    ("lgu_grant", "LGU scholarship", "Cannot hold another LGU scholarship from a different locality"),
)

AFFILIATION_CODES = (
    ("ncfrs", "registry", "NCFRS / 4Ps registry member"),
    ("rsbsa", "registry", "RSBSA registered farmer/fisher"),
    ("sra", "registry", "SRA registered sugar worker household"),
    ("gsis_member", "employment", "GSIS member or dependent"),
    ("sss_member", "employment", "SSS member or dependent"),
    ("hei_faculty", "employment", "HEI faculty or staff"),
    ("pwd", "equity", "Person with disability"),
    ("ip", "equity", "Indigenous peoples"),
    ("solo_parent_dependent", "equity", "Solo parent dependent"),
    ("ofw_dependent", "equity", "OFW dependent"),
    ("military_dependent", "equity", "Military/AFP dependent"),
    ("uniformed_service_dependent", "equity", "Uniformed service dependent"),
    ("farmer_fisher_dependent", "equity", "Farmer/fisher dependent"),
    ("4ps_listahanan", "equity", "4Ps/Listahanan household"),
)


def upgrade() -> None:
    op.add_column("scholarships", sa.Column("max_prior_tertiary_units", sa.Integer(), nullable=True))
    op.add_column("scholarships", sa.Column("min_work_experience_years", sa.Integer(), nullable=True))
    op.add_column("scholarships", sa.Column("max_class_rank", sa.Integer(), nullable=True))
    op.add_column("scholarships", sa.Column("max_class_percentile", sa.Float(), nullable=True))
    op.add_column("scholarships", sa.Column("academic_gate_mode", sa.String(8), nullable=True))
    op.add_column("scholarships", sa.Column("allow_transferee", sa.Boolean(), nullable=True))
    op.add_column("scholarships", sa.Column("allow_shiftee", sa.Boolean(), nullable=True))
    op.add_column(
        "scholarships",
        sa.Column("first_undergraduate_only", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column("scholarships", sa.Column("min_residency_years", sa.Integer(), nullable=True))
    op.add_column("scholarships", sa.Column("age_as_of_date", sa.Date(), nullable=True))
    op.add_column("scholarships", sa.Column("age_as_of_rule", sa.String(32), nullable=True))
    op.add_column("scholarships", sa.Column("max_parent_salary_grade", sa.Integer(), nullable=True))
    op.add_column("scholarships", sa.Column("parent_program_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_scholarships_parent_program_id",
        "scholarships",
        "scholarships",
        ["parent_program_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.add_column("students", sa.Column("prior_tertiary_units", sa.Integer(), nullable=True))
    op.add_column("students", sa.Column("class_rank", sa.Integer(), nullable=True))
    op.add_column("students", sa.Column("class_size", sa.Integer(), nullable=True))
    op.add_column("students", sa.Column("work_experience_years", sa.Integer(), nullable=True))
    op.add_column("students", sa.Column("marital_status", sa.String(), nullable=True))
    op.add_column("students", sa.Column("parent_salary_grade", sa.Integer(), nullable=True))
    op.add_column("students", sa.Column("parent_status", sa.String(), nullable=True))
    op.add_column("students", sa.Column("is_hei_faculty_or_staff", sa.Boolean(), nullable=True))
    op.add_column("students", sa.Column("residency_years_in_locality", sa.Integer(), nullable=True))

    op.create_table(
        "conflict_scopes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(64), nullable=False, unique=True),
        sa.Column("label", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
    )
    op.create_table(
        "scholarship_conflict_scopes",
        sa.Column("scholarship_id", sa.Integer(), sa.ForeignKey("scholarships.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("scope_id", sa.Integer(), sa.ForeignKey("conflict_scopes.id", ondelete="CASCADE"), primary_key=True),
    )
    op.create_table(
        "student_active_grant_scopes",
        sa.Column("student_id", sa.Integer(), sa.ForeignKey("students.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("scope_id", sa.Integer(), sa.ForeignKey("conflict_scopes.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("source", sa.String(64), nullable=True),
        sa.Column("verified", sa.Boolean(), nullable=False, server_default=sa.false()),
    )

    op.create_table(
        "affiliation_codes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(64), nullable=False, unique=True),
        sa.Column("kind", sa.String(32), nullable=False),
        sa.Column("label", sa.String(255), nullable=False),
    )
    op.create_table(
        "scholarship_required_affiliations",
        sa.Column("scholarship_id", sa.Integer(), sa.ForeignKey("scholarships.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("affiliation_id", sa.Integer(), sa.ForeignKey("affiliation_codes.id", ondelete="CASCADE"), primary_key=True),
    )
    op.create_table(
        "student_affiliations",
        sa.Column("student_id", sa.Integer(), sa.ForeignKey("students.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("affiliation_id", sa.Integer(), sa.ForeignKey("affiliation_codes.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("attested_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )

    conn = op.get_bind()
    for code, label, desc in CONFLICT_SCOPES:
        conn.execute(
            sa.text(
                "INSERT INTO conflict_scopes (code, label, description) VALUES (:code, :label, :desc)"
            ),
            {"code": code, "label": label, "desc": desc},
        )
    for code, kind, label in AFFILIATION_CODES:
        conn.execute(
            sa.text("INSERT INTO affiliation_codes (code, kind, label) VALUES (:code, :kind, :label)"),
            {"code": code, "kind": kind, "label": label},
        )


def downgrade() -> None:
    op.drop_table("student_affiliations")
    op.drop_table("scholarship_required_affiliations")
    op.drop_table("affiliation_codes")
    op.drop_table("student_active_grant_scopes")
    op.drop_table("scholarship_conflict_scopes")
    op.drop_table("conflict_scopes")

    op.drop_column("students", "residency_years_in_locality")
    op.drop_column("students", "is_hei_faculty_or_staff")
    op.drop_column("students", "parent_status")
    op.drop_column("students", "parent_salary_grade")
    op.drop_column("students", "marital_status")
    op.drop_column("students", "work_experience_years")
    op.drop_column("students", "class_size")
    op.drop_column("students", "class_rank")
    op.drop_column("students", "prior_tertiary_units")

    op.drop_constraint("fk_scholarships_parent_program_id", "scholarships", type_="foreignkey")
    op.drop_column("scholarships", "parent_program_id")
    op.drop_column("scholarships", "max_parent_salary_grade")
    op.drop_column("scholarships", "age_as_of_rule")
    op.drop_column("scholarships", "age_as_of_date")
    op.drop_column("scholarships", "min_residency_years")
    op.drop_column("scholarships", "first_undergraduate_only")
    op.drop_column("scholarships", "allow_shiftee")
    op.drop_column("scholarships", "allow_transferee")
    op.drop_column("scholarships", "academic_gate_mode")
    op.drop_column("scholarships", "max_class_percentile")
    op.drop_column("scholarships", "max_class_rank")
    op.drop_column("scholarships", "min_work_experience_years")
    op.drop_column("scholarships", "max_prior_tertiary_units")
