from sqlalchemy import Column, Integer, String, Text, Float, Boolean, Date, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.sql import func
from app.db import Base


class User(Base):
    """User account for authentication."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, server_default="student")  # student | admin | sponsor | school_verifier
    email_verified = Column(Boolean, nullable=False, server_default="0")
    email_verified_at = Column(DateTime, nullable=True)
    password_reset_token_hash = Column(String(128), nullable=True)
    password_reset_expires_at = Column(DateTime, nullable=True)


class RefreshToken(Base):
    """Rotating refresh token (hashed at rest)."""

    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = Column(String(128), nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)
    revoked_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class Sponsor(Base):
    """Scholarship provider organization (B2B)."""

    __tablename__ = "sponsors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    org_type = Column(String(64), nullable=True)
    contact_email = Column(String(255), nullable=True)
    logo_url = Column(String(512), nullable=True)
    website = Column(String(512), nullable=True)
    is_active = Column(Boolean, nullable=False, server_default="1")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class SponsorUser(Base):
    """Links users to sponsor orgs for reviewer workflows."""

    __tablename__ = "sponsor_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    sponsor_id = Column(Integer, ForeignKey("sponsors.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(64), nullable=False, server_default="reviewer")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class School(Base):
    """Educational institution for verification workflows."""

    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    region = Column(String(128), nullable=True)
    province = Column(String(128), nullable=True)
    school_type = Column(String(64), nullable=True)
    is_active = Column(Boolean, nullable=False, server_default="1")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class SchoolUser(Base):
    """Links users to schools for verification."""

    __tablename__ = "school_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(64), nullable=False, server_default="verifier")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class Student(Base):
    """Student profile with policy-aligned eligibility fields."""

    __tablename__ = "students"
    __table_args__ = (UniqueConstraint("user_id", name="uq_students_user_id"),)

    # === CORE IDENTITY ===
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    # === HARD FILTER FIELDS (deal-breakers) ===
    education_level = Column(String)  # Grade 11, Grade 12, College 1st Year, etc.
    current_academic_stage = Column(String)  # Junior HS, Senior HS, Undergraduate, Postgraduate, TVET, ALS
    target_academic_year = Column(String)  # e.g. 2026-2027
    region = Column(String)
    province = Column(String)
    city_municipality = Column(String)
    barangay = Column(String)
    school_type = Column(String)  # Public | Private

    # === SCORING INPUT FIELDS (continuous/ranked signals) ===
    school = Column(String)
    target_school = Column(String)
    gwa_raw = Column(String)  # Raw input: e.g. "1.25" or "94" or "3.8"
    gwa_scale = Column(String)  # 5.0_scale | 4.0_scale | percentage
    gwa_normalized = Column(Float)  # 0-100 normalized percentage
    field_of_study_broad = Column(String)  # PSCED broad discipline code
    field_of_study_specific = Column(String)  # Specific course/major name (legacy; first of preferred_courses)
    preferred_courses = Column(Text)  # JSON list of up to 3 course names, e.g. ["BS Computer Science", "BS IT"]
    extracurriculars = Column(Text)  # JSON list
    awards = Column(Text)  # JSON list

    # === EQUITY CLASSIFICATION FLAGS (RA-based) ===
    household_income_annual = Column(Integer)
    income_bracket = Column(String)  # below_250k | 250k_400k | 400k_500k | above_500k
    is_underprivileged = Column(Boolean, default=False)
    is_pwd = Column(Boolean, default=False)
    is_indigenous_people = Column(Boolean, default=False)
    ip_tribe_name = Column(String)
    is_solo_parent_dependent = Column(Boolean, default=False)
    is_ofw_dependent = Column(Boolean, default=False)
    ofw_parent_type = Column(String)  # land_based | sea_based | null
    is_farmer_fisher_dependent = Column(Boolean, default=False)
    is_4ps_listahanan = Column(Boolean, default=False)
    parent_occupation = Column(String)

    # === DOCUMENT INVENTORY (readiness tracking) ===
    documents = Column(Text)  # JSON: [{"type": "ITR", "status": "uploaded"}, ...]

    # === METADATA ===
    age = Column(Integer)
    gender = Column(String)
    birthdate = Column(Date)
    profile_completeness = Column(Float)
    needs = Column(Text)  # JSON-encoded list (legacy)
    privacy_consent_at = Column(DateTime, nullable=True)
    privacy_consent_version = Column(String, nullable=True)
    google_drive_folder_url = Column(String(2048), nullable=True)
    psgc_code = Column(String(9), nullable=True, index=True)
    guardian_full_name = Column(String(255), nullable=True)
    guardian_email = Column(String(255), nullable=True)
    guardian_consent_at = Column(DateTime, nullable=True)


class Scholarship(Base):
    """Scholarship with policy-aligned eligibility and benefit fields."""

    __tablename__ = "scholarships"

    # === CORE ===
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    provider = Column(String)
    source = Column(String)  # Data provenance: "philscholar", "sikap", etc.
    link = Column(String)
    dedupe_key = Column(String, unique=True, index=True, nullable=True)
    description = Column(Text)
    countries = Column(String)  # CSV string (legacy)

    # === HARD FILTER FIELDS (must-match or score=0) ===
    regions = Column(String)  # CSV string (legacy)
    eligible_levels = Column(Text)  # JSON list: ["College", "Graduate"]
    eligible_regions = Column(Text)  # JSON list
    eligible_cities = Column(Text)  # JSON list for LGU-specific grants
    residency_required = Column(Boolean, default=False)
    eligible_school_types = Column(Text)  # JSON: ["Public", "Private"]
    eligible_courses_psced = Column(Text)  # JSON list of PSCED broad codes
    eligible_courses_specific = Column(Text)  # JSON list of specific course names
    citizenship_required = Column(String, default="Filipino")
    max_income_threshold = Column(Integer)
    min_gwa_normalized = Column(Float)
    min_age = Column(Integer)
    max_age = Column(Integer)

    # === SCORING INPUT FIELDS (for weighted evaluation) ===
    provider_type = Column(String)  # Government | Private | LGU | Institutional
    scholarship_type = Column(String)  # Merit | Need | Merit-and-Need | Affiliation
    priority_groups = Column(Text)  # JSON list
    members_only = Column(Boolean, default=False, nullable=False)
    preferred_extracurriculars = Column(Text)  # JSON list
    preferred_awards = Column(Text)  # JSON list

    # === BENEFIT PACKAGE (display + scoring context) ===
    benefit_tuition = Column(Boolean, default=False)
    benefit_allowance_monthly = Column(Integer)
    benefit_books = Column(Boolean, default=False)
    benefit_miscellaneous = Column(Text)
    benefit_total_value = Column(Integer)

    # === DOCUMENT REQUIREMENTS ===
    required_documents = Column(Text)  # JSON list
    has_qualifying_exam = Column(Boolean, default=False)
    has_interview = Column(Boolean, default=False)
    has_essay_requirement = Column(Boolean, default=False)
    has_return_service = Column(Boolean, default=False)

    # === TIMELINE ===
    application_deadline = Column(Date)
    application_open_date = Column(Date)
    academic_year_target = Column(String)

    # === CYCLE PREDICTION ===
    last_open_date = Column(Date, nullable=True)
    last_close_date = Column(Date, nullable=True)
    cycle_type = Column(String, nullable=True)  # "annual" | "semester" | "rolling"

    # === METADATA ===
    is_active = Column(Boolean, default=True)
    level = Column(String)  # Legacy: High School, College, TVET, Graduate
    needs_tags = Column(Text)  # JSON-encoded list (legacy)
    sponsor_id = Column(Integer, ForeignKey("sponsors.id", ondelete="SET NULL"), nullable=True, index=True)

    # === DATA RELIABILITY & LINK INTEGRITY ===
    last_verified_at = Column(DateTime, nullable=True)
    verification_source = Column(String, nullable=True)  # manual | scraper | partner | csv_import
    confidence_score = Column(Float, nullable=True)
    data_status = Column(String, nullable=True)  # active | expiring_soon | expired | needs_review | broken_link
    link_status = Column(String, nullable=True)  # ok | broken | timeout | unchecked
    link_last_checked_at = Column(DateTime, nullable=True)
    link_failure_count = Column(Integer, nullable=True)


class ScholarshipStaging(Base):
    """Queued scholarship rows from CSV/import before admin approval."""

    __tablename__ = "scholarships_staging"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    provider = Column(String)
    source = Column(String)
    payload_json = Column(Text, nullable=False)
    status = Column(String, nullable=False, server_default="pending")  # pending | approved | rejected
    dedupe_key = Column(String, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    reviewed_at = Column(DateTime, nullable=True)


class MatchRun(Base):
    """A single match run for a user's profile."""

    __tablename__ = "match_runs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    profile_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class MatchResult(Base):
    """One scholarship result within a match run."""

    __tablename__ = "match_results"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("match_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    scholarship_id = Column(Integer, ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Float, nullable=False)
    final_score = Column(Float, nullable=True)
    explanation = Column(Text, nullable=True)  # JSON-encoded list
    breakdown = Column(Text, nullable=True)  # JSON-encoded dict
    suggestions = Column(Text, nullable=True)  # JSON-encoded list
    confidence = Column(String, nullable=True)
    why_not_higher = Column(Text, nullable=True)  # JSON-encoded list
    scoring_policy_version = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class SavedScholarship(Base):
    """User-bookmarked scholarship."""

    __tablename__ = "saved_scholarships"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    scholarship_id = Column(Integer, ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "scholarship_id", name="uq_saved_scholarships_user_scholarship"),
    )


class ScholarshipReport(Base):
    """User-reported issues on a scholarship (admin review queue)."""

    __tablename__ = "scholarship_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    scholarship_id = Column(Integer, ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False, index=True)
    issue_type = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, nullable=False, server_default="pending")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    reviewed_at = Column(DateTime, nullable=True)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)


class ScoringWeight(Base):
    """Admin-configurable matching component weights."""

    __tablename__ = "scoring_weights"

    id = Column(Integer, primary_key=True, index=True)
    component = Column(String, nullable=False, unique=True)
    weight = Column(Float, nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)


class ScholarshipVersion(Base):
    """Historical snapshot / diff when a scholarship row changes."""

    __tablename__ = "scholarship_versions"

    id = Column(Integer, primary_key=True, index=True)
    scholarship_id = Column(Integer, ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)
    changes = Column(Text, nullable=False)
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    changed_at = Column(DateTime, server_default=func.now(), nullable=False)


class AuditLog(Base):
    """Append-only audit trail for compliance and debugging."""

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, nullable=True, index=True)
    actor_type = Column(String, nullable=True)
    action = Column(String, nullable=False, index=True)
    resource_type = Column(String, nullable=True)
    resource_id = Column(Integer, nullable=True)
    details = Column(Text, nullable=True)
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class Notification(Base):
    """In-app notification for a user."""

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=True)
    scholarship_id = Column(Integer, ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=True, index=True)
    is_read = Column(Boolean, nullable=True, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class Application(Base):
    """Student application to a scholarship program."""

    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("user_id", "scholarship_id", name="uq_applications_user_scholarship"),
        Index("ix_applications_user_status", "user_id", "status"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    scholarship_id = Column(Integer, ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(64), nullable=False, server_default="preparing")
    notes = Column(Text, nullable=True)
    drive_folder_url = Column(String(2048), nullable=True)
    removed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class ApplicationStatusEvent(Base):
    """Append-only status history for an application."""

    __tablename__ = "application_status_events"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True)
    from_status = Column(String(64), nullable=True)
    to_status = Column(String(64), nullable=False)
    actor_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class DocumentChecklist(Base):
    """Per-application document readiness tracking."""

    __tablename__ = "document_checklists"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True)
    document_type = Column(String(128), nullable=False)
    status = Column(String(64), nullable=False, server_default="not_started")
    notes = Column(Text, nullable=True)
    file_url = Column(String(512), nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class VerificationRequest(Base):
    """School-side enrollment or eligibility verification."""

    __tablename__ = "verification_requests"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    verification_type = Column(String(64), nullable=False, server_default="enrollment")
    status = Column(String(64), nullable=False, server_default="pending")
    requested_at = Column(DateTime, server_default=func.now(), nullable=False)
    verified_at = Column(DateTime, nullable=True)
    verifier_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    notes = Column(Text, nullable=True)


class ProductFeedback(Base):
    """In-app product feedback (separate from scholarship issue reports)."""

    __tablename__ = "product_feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    category = Column(String(64), nullable=False)
    message = Column(Text, nullable=False)
    contact_email = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class ScraperRun(Base):
    """One execution of a catalog scraper (observability)."""

    __tablename__ = "scraper_runs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(64), nullable=False, index=True)
    started_at = Column(DateTime, server_default=func.now(), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(32), nullable=False, server_default="running")
    records_found = Column(Integer, nullable=True)
    records_ingested = Column(Integer, nullable=True)
    output_path = Column(String(1024), nullable=True)
    error_detail = Column(Text, nullable=True)
    # SHA-256 hex (64 chars) of raw listing HTML for change detection; null for legacy rows
    listing_content_sha256 = Column(String(64), nullable=True)


class HtePartner(Base):
    """Host Training Establishment for SIPP/OJT placements (CHED CMO 104)."""

    __tablename__ = "hte_partners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    industry = Column(String(128), nullable=True)
    moa_status = Column(String(32), nullable=False, server_default="pending")
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(32), nullable=True)
    is_active = Column(Boolean, nullable=False, server_default="1")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class InternshipOpportunity(Base):
    """Internship slot offered by an HTE."""

    __tablename__ = "internship_opportunities"

    id = Column(Integer, primary_key=True, index=True)
    hte_id = Column(Integer, ForeignKey("hte_partners.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    priority_courses = Column(Text, nullable=True)  # JSON array of PSCED codes
    region = Column(String(64), nullable=True)
    province = Column(String(128), nullable=True)
    psgc_code = Column(String(9), nullable=True, index=True)
    slots = Column(Integer, nullable=True)
    allowance_status = Column(String(32), nullable=True)
    allowance_amount = Column(Float, nullable=True)
    application_deadline = Column(Date, nullable=True)
    is_active = Column(Boolean, nullable=False, server_default="1")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class OjtComplianceVault(Base):
    """Pre-populated SIPP compliance documents stored in external vault URLs."""

    __tablename__ = "ojt_compliance_vault"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    internship_id = Column(Integer, ForeignKey("internship_opportunities.id", ondelete="SET NULL"), nullable=True, index=True)
    document_type = Column(String(48), nullable=False)
    template_version = Column(String(32), nullable=True)
    prefilled_fields = Column(Text, nullable=True)  # JSON merge-data
    external_url = Column(String(2048), nullable=True)
    status = Column(String(32), nullable=False, server_default="pending")
    guardian_consent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
