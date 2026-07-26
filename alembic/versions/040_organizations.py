"""Create organizations table and link scholarships."""

from alembic import op
import sqlalchemy as sa

revision = "040_organizations"
down_revision = "039_opportunity_type"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(), nullable=False, unique=True, index=True),
        sa.Column("canonical_name", sa.String(), nullable=False),
        sa.Column("aliases", sa.Text(), nullable=True),
        sa.Column("org_type", sa.String(), nullable=True),
        sa.Column("official_domains", sa.Text(), nullable=True),
        sa.Column("logo_url", sa.String(2048), nullable=True),
        sa.Column("website", sa.String(2048), nullable=True),
        sa.Column("verification_status", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )
    op.add_column(
        "scholarships",
        sa.Column(
            "organization_id",
            sa.Integer(),
            sa.ForeignKey("organizations.id", ondelete="SET NULL"),
            nullable=True,
            index=True,
        ),
    )

    # Raw SQL backfill: models.Scholarship includes editorial_state (added in 041).
    bind = op.get_bind()
    from sqlalchemy import text

    from app.taxonomy.organizations import _infer_org_type, slugify_org_name

    providers = bind.execute(
        text(
            """
            SELECT trim(provider) AS name, max(provider_type) AS provider_type
            FROM scholarships
            WHERE provider IS NOT NULL AND btrim(provider) <> ''
            GROUP BY trim(provider)
            """
        )
    ).mappings().all()

    slug_counts: dict[str, int] = {}
    for row in providers:
        name = row["name"]
        key = name.lower()
        org_id = bind.execute(
            text("SELECT id FROM organizations WHERE lower(canonical_name) = :key"),
            {"key": key},
        ).scalar()
        if org_id is None:
            base_slug = slugify_org_name(name)
            slug_counts[base_slug] = slug_counts.get(base_slug, 0) + 1
            slug = base_slug if slug_counts[base_slug] == 1 else f"{base_slug}-{slug_counts[base_slug]}"
            org_id = bind.execute(
                text(
                    """
                    INSERT INTO organizations (
                        slug, canonical_name, aliases, org_type, official_domains, verification_status
                    )
                    VALUES (:slug, :name, '[]', :org_type, '[]', 'unverified')
                    RETURNING id
                    """
                ),
                {"slug": slug, "name": name, "org_type": _infer_org_type(row["provider_type"])},
            ).scalar()

        bind.execute(
            text(
                """
                UPDATE scholarships SET organization_id = :org_id
                WHERE provider = :name AND organization_id IS NULL
                """
            ),
            {"org_id": org_id, "name": name},
        )


def downgrade() -> None:
    op.drop_column("scholarships", "organization_id")
    op.drop_table("organizations")
