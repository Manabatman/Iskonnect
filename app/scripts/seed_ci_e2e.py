"""
Deterministic CI / E2E seed data (QA-01).

Usage:
  alembic upgrade head
  python -m app.scripts.seed_ci_e2e

Idempotent: safe to run on every CI job.
"""

from __future__ import annotations

import json
from datetime import date, timedelta

from app import models
from app.auth import hash_password
from app.db import SessionLocal
from app.utils.application_status import NEEDS_VERIFICATION, OPEN, CLOSED
from app.utils.timezone import utc_now_naive

E2E_EMAIL = "e2e-test@example.com"
E2E_PASSWORD = "E2eTestPass1!"
E2E_PROFILE_NAME = "E2E Test Student"


def _upsert_user(db) -> models.User:
    user = db.query(models.User).filter(models.User.email == E2E_EMAIL).first()
    verified_at = utc_now_naive()
    if user:
        user.password_hash = hash_password(E2E_PASSWORD)
        user.role = "student"
        user.email_verified = True
        user.email_verified_at = verified_at
    else:
        user = models.User(
            email=E2E_EMAIL,
            password_hash=hash_password(E2E_PASSWORD),
            role="student",
            email_verified=True,
            email_verified_at=verified_at,
        )
        db.add(user)
        db.flush()
    return user


def _upsert_profile(db, user_id: int) -> models.Student:
    row = db.query(models.Student).filter(models.Student.user_id == user_id).first()
    if row:
        row.full_name = E2E_PROFILE_NAME
        row.email = E2E_EMAIL
        row.age = 19
        row.education_level = "College / University"
        row.region = "National Capital Region"
        row.province = "Metro Manila"
        row.city_municipality = "Quezon City"
        row.school_type = "public"
        row.gwa_raw = "1.75"
        row.gwa_scale = "5.0"
        row.gwa_normalized = 90.0
        row.field_of_study_broad = "STEM"
        row.household_income_annual = 250_000
        row.privacy_consent_at = utc_now_naive()
        row.privacy_consent_version = "1.0"
        return row

    row = models.Student(
        user_id=user_id,
        full_name=E2E_PROFILE_NAME,
        email=E2E_EMAIL,
        age=19,
        education_level="College / University",
        region="National Capital Region",
        province="Metro Manila",
        city_municipality="Quezon City",
        school_type="public",
        gwa_raw="1.75",
        gwa_scale="5.0",
        gwa_normalized=90.0,
        field_of_study_broad="STEM",
        household_income_annual=250_000,
        privacy_consent_at=utc_now_naive(),
        privacy_consent_version="1.0",
    )
    db.add(row)
    db.flush()
    return row


def _scholarship_specs() -> list[dict]:
    future = date.today() + timedelta(days=90)
    past = date.today() - timedelta(days=10)
    return [
        {
            "title": "CI Open Merit Grant",
            "provider": "CI Test Provider",
            "link": "https://example.com/open",
            "description": "Open scholarship for E2E tests.",
            "level": "College",
            "eligible_levels": json.dumps(["College"]),
            "application_status": OPEN,
            "application_deadline": future,
            "is_active": True,
            "data_status": "active",
            "editorial_state": "published",
        },
        {
            "title": "CI Unknown Status Listing",
            "provider": "CI Test Provider",
            "link": "https://example.com/unknown",
            "description": "Listing with no lifecycle fields for TRUST-02.",
            "level": "College",
            "eligible_levels": json.dumps(["College"]),
            "application_status": None,
            "application_deadline": None,
            "is_active": True,
            "data_status": None,
            "editorial_state": "imported",
        },
        {
            "title": "CI Closed Cycle Grant",
            "provider": "CI Test Provider",
            "link": "https://example.com/closed",
            "description": "Closed scholarship for filter tests.",
            "level": "College",
            "eligible_levels": json.dumps(["College"]),
            "application_status": CLOSED,
            "application_deadline": past,
            "is_active": True,
            "data_status": "expired",
            "editorial_state": "published",
        },
        {
            "title": "CI Needs Verification Grant",
            "provider": "CI Test Provider",
            "link": "https://example.com/verify",
            "description": "Needs verification listing.",
            "level": "College",
            "eligible_levels": json.dumps(["College"]),
            "application_status": NEEDS_VERIFICATION,
            "application_deadline": future,
            "is_active": True,
            "data_status": "needs_review",
            "editorial_state": "needs_review",
        },
    ]


def _upsert_scholarships(db) -> None:
    for spec in _scholarship_specs():
        existing = (
            db.query(models.Scholarship)
            .filter(
                models.Scholarship.title == spec["title"],
                models.Scholarship.provider == spec["provider"],
            )
            .first()
        )
        if existing:
            for key, val in spec.items():
                setattr(existing, key, val)
        else:
            db.add(models.Scholarship(**spec))


def main() -> None:
    db = SessionLocal()
    try:
        user = _upsert_user(db)
        _upsert_profile(db, user.id)
        _upsert_scholarships(db)
        db.commit()
        print(f"CI E2E seed OK: user={E2E_EMAIL} id={user.id}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
