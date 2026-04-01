from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional, Any


# === Match Breakdown (Structure Only) ===
class MatchFactorSchema(BaseModel):
    category: Optional[str] = None
    status: str  # met, exceeded, partial, missing, disqualified
    user_value: str
    requirement_value: str
    detail: Optional[str] = None


class MatchBreakdownSchema(BaseModel):
    academic: Optional[dict] = None
    socioeconomic: Optional[dict] = None
    field_relevance: Optional[dict] = None
    geographic: Optional[dict] = None
    document_readiness: Optional[dict] = None
    priority_group: Optional[dict] = None


# === Student Profile ===
class StudentProfile(BaseModel):
    full_name: str
    email: EmailStr
    age: Optional[int] = None
    region: Optional[str] = None
    school: Optional[str] = None
    needs: Optional[List[str]] = []
    education_level: Optional[str] = None
    # New fields
    gender: Optional[str] = None
    birthdate: Optional[date] = None
    current_academic_stage: Optional[str] = None
    target_academic_year: Optional[str] = None
    province: Optional[str] = None
    city_municipality: Optional[str] = None
    barangay: Optional[str] = None
    school_type: Optional[str] = None
    target_school: Optional[str] = None
    gwa_raw: Optional[str] = None
    gwa_scale: Optional[str] = None
    gwa_normalized: Optional[float] = None
    field_of_study_broad: Optional[str] = None
    field_of_study_specific: Optional[str] = None
    preferred_courses: Optional[List[str]] = []
    extracurriculars: Optional[List[str]] = []
    awards: Optional[List[str]] = []
    household_income_annual: Optional[int] = None
    income_bracket: Optional[str] = None
    is_underprivileged: Optional[bool] = False
    is_pwd: Optional[bool] = False
    is_indigenous_people: Optional[bool] = False
    ip_tribe_name: Optional[str] = None
    is_solo_parent_dependent: Optional[bool] = False
    is_ofw_dependent: Optional[bool] = False
    ofw_parent_type: Optional[str] = None
    is_farmer_fisher_dependent: Optional[bool] = False
    is_4ps_listahanan: Optional[bool] = False
    parent_occupation: Optional[str] = None
    documents: Optional[List[dict]] = []
    # RA 10173 — must be true to submit (validated server-side)
    privacy_consent: bool = False
    privacy_consent_version: Optional[str] = "ra10173-v1"

    @field_validator("privacy_consent")
    @classmethod
    def require_privacy_consent(cls, v: bool) -> bool:
        if not v:
            raise ValueError("You must accept the privacy notice to continue (Data Privacy Act of 2012 / RA 10173).")
        return v


class StudentProfileResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    age: Optional[int] = None
    region: Optional[str] = None
    school: Optional[str] = None
    needs: Optional[List[str]] = []
    education_level: Optional[str] = None
    gender: Optional[str] = None
    birthdate: Optional[date] = None
    current_academic_stage: Optional[str] = None
    target_academic_year: Optional[str] = None
    province: Optional[str] = None
    city_municipality: Optional[str] = None
    barangay: Optional[str] = None
    school_type: Optional[str] = None
    target_school: Optional[str] = None
    gwa_raw: Optional[str] = None
    gwa_scale: Optional[str] = None
    gwa_normalized: Optional[float] = None
    field_of_study_broad: Optional[str] = None
    field_of_study_specific: Optional[str] = None
    preferred_courses: Optional[List[str]] = []
    extracurriculars: Optional[List[str]] = []
    awards: Optional[List[str]] = []
    household_income_annual: Optional[int] = None
    income_bracket: Optional[str] = None
    is_underprivileged: Optional[bool] = False
    is_pwd: Optional[bool] = False
    is_indigenous_people: Optional[bool] = False
    ip_tribe_name: Optional[str] = None
    is_solo_parent_dependent: Optional[bool] = False
    is_ofw_dependent: Optional[bool] = False
    ofw_parent_type: Optional[str] = None
    is_farmer_fisher_dependent: Optional[bool] = False
    is_4ps_listahanan: Optional[bool] = False
    parent_occupation: Optional[str] = None
    documents: Optional[List[dict]] = []
    privacy_consent_at: Optional[datetime] = None
    privacy_consent_version: Optional[str] = None

    class Config:
        from_attributes = True


# === Scholarship ===
class Scholarship(BaseModel):
    title: str
    provider: Optional[str] = None
    source: Optional[str] = None
    countries: Optional[List[str]] = []
    regions: Optional[List[str]] = []
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    needs_tags: Optional[List[str]] = []
    level: Optional[str] = None
    link: Optional[str] = None
    description: Optional[str] = None
    provider_type: Optional[str] = None
    scholarship_type: Optional[str] = None
    eligible_levels: Optional[List[str]] = []
    eligible_regions: Optional[List[str]] = []
    eligible_cities: Optional[List[str]] = []
    residency_required: Optional[bool] = False
    eligible_school_types: Optional[List[str]] = []
    eligible_courses_psced: Optional[List[str]] = []
    eligible_courses_specific: Optional[List[str]] = []
    max_income_threshold: Optional[int] = None
    min_gwa_normalized: Optional[float] = None
    priority_groups: Optional[List[str]] = []
    preferred_extracurriculars: Optional[List[str]] = []
    preferred_awards: Optional[List[str]] = []
    benefit_tuition: Optional[bool] = False
    benefit_allowance_monthly: Optional[int] = None
    benefit_books: Optional[bool] = False
    benefit_miscellaneous: Optional[str] = None
    benefit_total_value: Optional[int] = None
    required_documents: Optional[List[str]] = []
    has_qualifying_exam: Optional[bool] = False
    has_interview: Optional[bool] = False
    has_essay_requirement: Optional[bool] = False
    has_return_service: Optional[bool] = False
    application_deadline: Optional[date] = None
    application_open_date: Optional[date] = None
    academic_year_target: Optional[str] = None
    is_active: Optional[bool] = True

    @field_validator("link")
    @classmethod
    def validate_link(cls, v: Optional[str]) -> Optional[str]:
        if v and v.strip() and not v.strip().startswith(("http://", "https://")):
            raise ValueError("Link must be a valid HTTP or HTTPS URL")
        return v


class ScholarshipResponse(BaseModel):
    id: int
    title: str
    provider: Optional[str] = None
    source: Optional[str] = None
    countries: Optional[List[str]] = []
    regions: Optional[List[str]] = []
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    needs_tags: Optional[List[str]] = []
    level: Optional[str] = None
    link: Optional[str] = None
    description: Optional[str] = None
    provider_type: Optional[str] = None
    scholarship_type: Optional[str] = None
    eligible_levels: Optional[List[str]] = []
    eligible_regions: Optional[List[str]] = []
    eligible_cities: Optional[List[str]] = []
    residency_required: Optional[bool] = False
    eligible_school_types: Optional[List[str]] = []
    eligible_courses_psced: Optional[List[str]] = []
    eligible_courses_specific: Optional[List[str]] = []
    preferred_extracurriculars: Optional[List[str]] = []
    preferred_awards: Optional[List[str]] = []
    max_income_threshold: Optional[int] = None
    min_gwa_normalized: Optional[float] = None
    priority_groups: Optional[List[str]] = []
    benefit_tuition: Optional[bool] = False
    benefit_allowance_monthly: Optional[int] = None
    benefit_books: Optional[bool] = False
    benefit_total_value: Optional[int] = None
    required_documents: Optional[List[str]] = []
    has_qualifying_exam: Optional[bool] = False
    has_interview: Optional[bool] = False
    has_essay_requirement: Optional[bool] = False
    has_return_service: Optional[bool] = False
    application_deadline: Optional[date] = None
    application_open_date: Optional[date] = None
    academic_year_target: Optional[str] = None
    is_active: Optional[bool] = True
    # Data reliability & link integrity (optional; backward compatible)
    last_verified_at: Optional[datetime] = None
    verification_source: Optional[str] = None
    confidence_score: Optional[float] = None
    data_status: Optional[str] = None
    link_status: Optional[str] = None
    link_last_checked_at: Optional[datetime] = None
    link_failure_count: Optional[int] = None

    class Config:
        from_attributes = True


class ScholarshipReportCreate(BaseModel):
    scholarship_id: int
    issue_type: str  # broken_link | wrong_deadline | outdated_info | other
    description: Optional[str] = None


class ScholarshipReportResponse(BaseModel):
    id: int
    scholarship_id: int
    user_id: Optional[int] = None
    issue_type: str
    description: Optional[str] = None
    status: str
    created_at: datetime
    reviewed_at: Optional[datetime] = None
    reviewer_id: Optional[int] = None

    class Config:
        from_attributes = True


class ScoringWeightItem(BaseModel):
    component: str
    weight: float


class ScoringWeightResponse(BaseModel):
    weights: List[ScoringWeightItem] = []


class ScoringWeightsUpdateRequest(BaseModel):
    weights: List[ScoringWeightItem] = Field(
        ...,
        description="All five components; weights must sum to 1.0",
    )


class AuditLogResponse(BaseModel):
    id: int
    actor_id: Optional[int] = None
    actor_type: Optional[str] = None
    action: str
    resource_type: Optional[str] = None
    resource_id: Optional[int] = None
    details: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    type: str
    title: str
    body: Optional[str] = None
    scholarship_id: Optional[int] = None
    is_read: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


# === Match Response (Expanded) ===
class MatchResponse(BaseModel):
    id: int
    title: str
    provider: Optional[str] = None
    score: float
    final_score: Optional[float] = None
    eligibility_status: Optional[bool] = None
    readiness_score: Optional[float] = None
    explanation: Optional[List[str]] = []
    breakdown: Optional[dict] = None
    confidence: Optional[str] = None
    link: Optional[str] = None
    description: Optional[str] = None
    regions: Optional[List[str]] = []
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    level: Optional[str] = None
    provider_type: Optional[str] = None
    scholarship_type: Optional[str] = None
    benefit_tuition: Optional[bool] = None
    benefit_allowance_monthly: Optional[int] = None
    benefit_books: Optional[bool] = None
    benefit_total_value: Optional[int] = None
    application_deadline: Optional[str] = None
    required_documents: Optional[List[str]] = []
    suggestions: Optional[List[str]] = []


# === Upcoming Scholarship (Cycle Prediction) ===
class UpcomingScholarship(BaseModel):
    id: int
    title: str
    provider: Optional[str] = None
    cycle_type: Optional[str] = None
    last_open_date: Optional[str] = None
    last_close_date: Optional[str] = None
    predicted_next_open: Optional[str] = None
    link: Optional[str] = None
    description: Optional[str] = None
    benefit_tuition: Optional[bool] = None
    benefit_total_value: Optional[int] = None


# === Match History ===
class MatchRunSummary(BaseModel):
    id: int
    profile_id: int
    created_at: datetime
    result_count: int


class MatchRunDetail(BaseModel):
    id: int
    profile_id: int
    created_at: datetime
    results: List[MatchResponse]


class MatchComparisonItem(BaseModel):
    scholarship_id: int
    title: str
    provider: Optional[str] = None
    score_a: Optional[float] = None
    score_b: Optional[float] = None
    score_diff: Optional[float] = None


class MatchComparisonResponse(BaseModel):
    run_a: MatchRunSummary
    run_b: MatchRunSummary
    items: List[MatchComparisonItem]


class CreateMatchRunRequest(BaseModel):
    profile_id: int


# === Scholarship Search ===
class ScholarshipSearchResponse(BaseModel):
    results: List[ScholarshipResponse] = []
    total: int = 0
    page: int = 1
    limit: int = 20
    total_pages: int = 0


class ScholarshipFilterOptions(BaseModel):
    providers: List[str] = []
    education_levels: List[str] = []
    regions: List[str] = []
    fields_of_study: List[str] = []


# === Saved Scholarships ===
class SaveScholarshipRequest(BaseModel):
    scholarship_id: int


class SavedScholarshipResponse(BaseModel):
    id: int
    scholarship_id: int
    created_at: datetime
    scholarship: Optional[ScholarshipResponse] = None

    class Config:
        from_attributes = True


class SavedScholarshipListResponse(BaseModel):
    saved: List[SavedScholarshipResponse] = []
    total: int = 0
