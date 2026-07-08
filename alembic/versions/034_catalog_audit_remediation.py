"""Catalog audit remediation: priority groups, members_only, verification, regions."""

from alembic import op

revision = "034_catalog_audit"
down_revision = "033_affiliation_equity"
branch_labels = None
depends_on = None


def _is_postgres() -> bool:
    bind = op.get_bind()
    return bind.dialect.name == "postgresql"


def upgrade() -> None:
    if not _is_postgres():
        return

    # Normalize fragmented priority_groups to canonical equity IDs.
    op.execute(
        """
        UPDATE scholarships SET priority_groups = (
          SELECT COALESCE(jsonb_agg(DISTINCT mapped), '[]'::jsonb)
          FROM (
            SELECT CASE
              WHEN v IN ('4Ps', 'Listahanan') THEN '4Ps/Listahanan'
              WHEN v = 'Solo Parent Dependents' THEN 'Solo Parent Dependent'
              WHEN v = 'Farmers and Fishers Dependents' THEN 'Farmer/Fisher Dependent'
              WHEN v IN (
                'Indigenous Peoples (Lumad)',
                'Indigenous Peoples (IP)',
                'IP Academic Achievers',
                'CAR Indigenous Youth'
              ) THEN 'IP'
              ELSE v
            END AS mapped
            FROM jsonb_array_elements_text(priority_groups) AS t(v)
          ) sub
        )
        WHERE priority_groups IS NOT NULL AND priority_groups <> '[]'::jsonb
        """
    )

    # Affiliation-restricted programs: exclusive membership gate.
    op.execute(
        """
        UPDATE scholarships SET members_only = true
        WHERE id IN (56, 62)
           OR (scholarship_type = 'Affiliation' AND priority_groups::text ~* '(military|uniformed)')
        """
    )

    op.execute(
        """
        UPDATE scholarships SET members_only = true,
               priority_groups = '["GSIS Dependent"]'::jsonb
        WHERE id = 7 AND (priority_groups IS NULL OR priority_groups = '[]'::jsonb)
        """
    )

    op.execute(
        """
        UPDATE scholarships SET members_only = true,
               priority_groups = '["SSS Dependent"]'::jsonb
        WHERE id = 8 AND (priority_groups IS NULL OR priority_groups = '[]'::jsonb)
        """
    )

    # Backfill verification metadata for legacy import rows.
    op.execute(
        """
        UPDATE scholarships
        SET verification_source = COALESCE(verification_source, 'csv_import'),
            last_verified_at = COALESCE(last_verified_at, NOW())
        WHERE verification_source IS NULL OR last_verified_at IS NULL
        """
    )

    # Demote broken-link rows still marked open.
    op.execute(
        """
        UPDATE scholarships SET data_status = 'needs_review'
        WHERE data_status = 'broken_link' AND application_status = 'open'
        """
    )

    op.execute(
        """
        UPDATE scholarships SET application_status = 'needs_verification'
        WHERE data_status = 'needs_review' AND application_status = 'open'
        """
    )

    # Canonicalize NCR region labels in eligible_regions JSON.
    op.execute(
        """
        UPDATE scholarships SET eligible_regions = (
          SELECT COALESCE(jsonb_agg(DISTINCT mapped), '[]'::jsonb)
          FROM (
            SELECT CASE
              WHEN lower(v) IN ('metro manila', 'national capital region') THEN 'NCR'
              ELSE v
            END AS mapped
            FROM jsonb_array_elements_text(eligible_regions) AS t(v)
          ) sub
        )
        WHERE eligible_regions IS NOT NULL
          AND eligible_regions <> '[]'::jsonb
          AND (
            eligible_regions @> '["Metro Manila"]'::jsonb
            OR eligible_regions @> '["National Capital Region"]'::jsonb
          )
        """
    )


def downgrade() -> None:
    # Data remediation is not reversed automatically.
    pass
