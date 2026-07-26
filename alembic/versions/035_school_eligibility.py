"""035 — school eligibility columns and student school_id fields."""

from alembic import op
import sqlalchemy as sa

revision = "035_school_eligibility"
down_revision = "034_catalog_audit"
branch_labels = None
depends_on = None

_NEW_JSONB_COLS = (
    "eligible_schools",
    "eligible_school_systems",
    "eligible_school_categories",
)


def _is_postgres() -> bool:
    bind = op.get_bind()
    return bind.dialect.name == "postgresql"


def upgrade() -> None:
    op.add_column("students", sa.Column("school_id", sa.String(), nullable=True))
    op.add_column("students", sa.Column("target_school_id", sa.String(), nullable=True))

    for col in _NEW_JSONB_COLS:
        op.add_column("scholarships", sa.Column(col, sa.Text(), nullable=True))

    if _is_postgres():
        for col in _NEW_JSONB_COLS:
            op.execute(
                sa.text(
                    f"""
                    ALTER TABLE scholarships
                    ALTER COLUMN {col} TYPE jsonb
                    USING CASE
                        WHEN {col} IS NULL OR trim({col}) = '' THEN '[]'::jsonb
                        WHEN trim({col}) LIKE '[%' THEN {col}::jsonb
                        ELSE to_jsonb(string_to_array({col}, ','))
                    END
                    """
                )
            )

        # Backfill eligible_schools from provider/title heuristics for known HEI programs
        _PROVIDER_SCHOOL_MAP = [
            ("pup", "%PUP%", "%Polytechnic University of the Philippines%"),
            ("university-of-santo-tomas", "%UST%", "%University of Santo Tomas%"),
            ("ateneo-de-manila-university", "%Ateneo%", "%ADMU%"),
            ("de-la-salle-university", "%DLSU%", "%De La Salle University%"),
            ("university-of-the-philippines-diliman", "%UP Diliman%", "%UPD%"),
            ("university-of-the-philippines-manila", "%UP Manila%", "%UPM%"),
            ("university-of-the-philippines-los-banos", "%UP Los Ba%", "%UPLB%"),
            ("pamantasan-ng-lungsod-ng-maynila", "%PLM%", "%Pamantasan ng Lungsod%"),
        ]
        for sid, *patterns in _PROVIDER_SCHOOL_MAP:
            cond = " OR ".join(
                f"(provider ILIKE '{p}' OR title ILIKE '{p}')" for p in patterns
            )
            op.execute(
                sa.text(
                    f"""
                    UPDATE scholarships
                    SET eligible_schools = '["{sid}"]'::jsonb
                    WHERE ({cond})
                      AND (eligible_schools IS NULL OR eligible_schools = '[]'::jsonb)
                    """
                )
            )

        # Backfill student school_id from free-text school column
        op.execute(
            """
            CREATE OR REPLACE FUNCTION _iskonnect_resolve_school_id(name text) RETURNS text AS $$
            DECLARE
              norm text;
            BEGIN
              IF name IS NULL OR trim(name) = '' THEN RETURN NULL; END IF;
              norm := lower(trim(name));
              IF norm IN ('pup', 'polytechnic university of the philippines') THEN RETURN 'polytechnic-university-of-the-philippines'; END IF;
              IF norm IN ('ust', 'university of santo tomas') THEN RETURN 'university-of-santo-tomas'; END IF;
              IF norm IN ('dlsu', 'de la salle university') THEN RETURN 'de-la-salle-university'; END IF;
              IF norm IN ('ateneo', 'ateneo de manila university', 'admu') THEN RETURN 'ateneo-de-manila-university'; END IF;
              IF norm LIKE 'up diliman%' OR norm = 'upd' THEN RETURN 'university-of-the-philippines-diliman'; END IF;
              IF norm LIKE 'up manila%' OR norm = 'upm' THEN RETURN 'university-of-the-philippines-manila'; END IF;
              IF norm LIKE 'up los ba%' OR norm = 'uplb' THEN RETURN 'university-of-the-philippines-los-banos'; END IF;
              IF norm IN ('plm', 'pamantasan ng lungsod ng maynila') THEN RETURN 'pamantasan-ng-lungsod-ng-maynila'; END IF;
              RETURN NULL;
            END;
            $$ LANGUAGE plpgsql IMMUTABLE;
            """
        )
        op.execute(
            """
            UPDATE students SET school_id = _iskonnect_resolve_school_id(school)
            WHERE school_id IS NULL AND school IS NOT NULL;
            """
        )
        op.execute(
            """
            UPDATE students SET target_school_id = _iskonnect_resolve_school_id(target_school)
            WHERE target_school_id IS NULL AND target_school IS NOT NULL;
            """
        )
        op.execute("DROP FUNCTION IF EXISTS _iskonnect_resolve_school_id(text);")


def downgrade() -> None:
    for col in reversed(_NEW_JSONB_COLS):
        op.drop_column("scholarships", col)
    op.drop_column("students", "target_school_id")
    op.drop_column("students", "school_id")
