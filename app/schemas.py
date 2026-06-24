from datetime import date, datetime
from typing import Any, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator

EducationLevel = Literal["Grade 11", "Grade 12", "High School", "College", "TVET", "Graduate"]
GenderOption = Literal["Male", "Female", "Other"]
SchoolTypeOption = Literal["Public", "Private"]
ProviderTypeOption = Literal["Government", "Private", "LGU", "Institutional"]
ScholarshipTypeOption = Literal["Merit-and-Need", "Need", "Affiliation", "Merit-based"]


# === Student Profile ===
class DocumentEntry(BaseModel):
    """Structured document row from the client."""

    model_config = ConfigDict(extra="ignore")

    type: str = Field(..., min_length=1, max_length=128)
    status: str = Field(..., min_length=1, max_length=64)


class StudentProfile(BaseModel):
    full_name: str
    email: EmailStr
    age: Optional[int] = Field(default=None, ge=10, le=80)
    region: Optional[str] = None
    school: Optional[str] = None
    needs: Optional[List[str]] = []
    education_level: Optional[EducationLevel] = None
    gender: Optional[GenderOption] = None
    birthdate: Optional[date] = None
    current_academic_stage: Optional[str] = None
    target_academic_year: Optional[str] = None
    province: Optional[str] = None
    city_municipality: Optional[str] = None
    barangay: Optional[str] = None
    psgc_code: Optional[str] = Field(default=None, max_length=9)
    school_type: Optional[SchoolTypeOption] = None
    target_school: Optional[str] = None
    gwa_raw: Optional[str] = None
    gwa_scale: Optional[str] = None
    gwa_normalized: Optional[float] = Field(default=None, ge=0, le=100)
    field_of_study_broad: Optional[str] = None
    field_of_study_specific: Optional[str] = None
    preferred_courses: Optional[List[str]] = []
    extracurriculars: Optional[List[str]] = []
    awards: Optional[List[str]] = []
    household_income_annual: Optional[int] = Field(default=None, ge=0)
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
    guardian_full_name: Optional[str] = Field(default=None, max_length=255)
    guardian_email: Optional[EmailStr] = None
    guardian_consent: bool = False
    documents: Optional[List[DocumentEntry]] = []
    # RA 10173 — must be true to submit (validated server-side)
    privacy_consent: bool = False
    privacy_consent_version: Optional[str] = "ra10173-v1"

    @field_validator(
        "education_level",
        "gender",
        "school_type",
        mode="before",
    )
    @classmethod
    def empty_str_to_none(cls, v: Any) -> Any:
        if v == "":
            return None
        return v

    @field_validator("documents", mode="before")
    @classmethod
    def coerce_documents(cls, v: Any) -> Any:
        if v is None:
            return v
        if not isinstance(v, list):
            return v
        out = []
        for item in v:
            if isinstance(item, dict):
                out.append(DocumentEntry.model_validate(item))
            else:
                out.append(item)
        return out

    @field_validator("privacy_consent")
    @classmethod
    def require_privacy_consent(cls, v: bool) -> bool:
        if not v:
            raise ValueError("You must accept the privacy notice to continue (Data Privacy Act of 2012 / RA 10173).")
        return v

    @model_validator(mode="after")
    def require_guardian_consent_for_minors(self) -> "StudentProfile":
        """Profiles for users under 18 require guardian consent (RA 10173)."""
        is_minor = self.age is not None and self.age < 18
        if not is_minor and self.birthdate is not None:
            today = date.today()
            years = today.year - self.birthdate.year
            if (today.month, today.day) < (self.birthdate.month, self.birthdate.day):
                years -= 1
            is_minor = years < 18
        if is_minor and not self.guardian_consent:
            raise ValueError(
                "Guardian or parent consent is required for users under 18 years of age."
            )
        if is_minor and not (self.guardian_full_name or "").strip():
            raise ValueError("Guardian full name is required for users under 18.")
        return self


class GoogleDriveVaultUpdate(BaseModel):
    """Update only the user's linked Google Drive folder (document vault)."""

    google_drive_folder_url: Optional[str] = Field(default=None, max_length=2048)

    @field_validator("google_drive_folder_url")
    @classmethod
    def validate_drive_url(cls, v: Optional[str]) -> Optional[str]:
        if v is None or (isinstance(v, str) and not v.strip()):
            return None
        s = v.strip()
        if not s.startswith("https://"):
            raise ValueError("URL must use https://")
        if "drive.google.com" not in s and "docs.google.com" not in s:
            raise ValueError("URL must be a Google Drive or Docs link")
        return s


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
    google_drive_folder_url: Optional[str] = None
    profile_access_token: Optional[str] = None

    class Config:
        from_attributes = True


# === Scholarship ===
class Scholarship(BaseModel):
    title: str
    provider: Optional[str] = None
    source: Optional[str] = None
    countries: Optional[List[str]] = []
    regions: Optional[List[str]] = []
    min_age: Optional[int] = Field(default=None, ge=0, le=120)
    max_age: Optional[int] = Field(default=None, ge=0, le=120)
    needs_tags: Optional[List[str]] = []
    level: Optional[str] = None
    link: Optional[str] = None
    description: Optional[str] = None
    provider_type: Optional[ProviderTypeOption] = None
    scholarship_type: Optional[ScholarshipTypeOption] = None
    eligible_levels: Optional[List[str]] = []
    eligible_regions: Optional[List[str]] = []
    eligible_cities: Optional[List[str]] = []
    residency_required: Optional[bool] = False
    eligible_school_types: Optional[List[str]] = []
    eligible_courses_psced: Optional[List[str]] = []
    eligible_courses_specific: Optional[List[str]] = []
    max_income_threshold: Optional[int] = Field(default=None, ge=0)
    min_gwa_normalized: Optional[float] = Field(default=None, ge=0, le=100)
    priority_groups: Optional[List[str]] = []
    preferred_extracurriculars: Optional[List[str]] = []
    preferred_awards: Optional[List[str]] = []
    benefit_tuition: Optional[bool] = False
    benefit_allowance_monthly: Optional[int] = Field(default=None, ge=0)
    benefit_books: Optional[bool] = False
    benefit_miscellaneous: Optional[str] = None
    benefit_total_value: Optional[int] = Field(default=None, ge=0)
    required_documents: Optional[List[str]] = []
    has_qualifying_exam: Optional[bool] = False
    has_interview: Optional[bool] = False
    has_essay_requirement: Optional[bool] = False
    has_return_service: Optional[bool] = False
    application_deadline: Optional[date] = None
    application_open_date: Optional[date] = None
    academic_year_target: Optional[str] = None
    is_active: Optional[bool] = True

    @field_validator("provider_type", "scholarship_type", mode="before")
    @classmethod
    def scholarship_empty_str_to_none(cls, v: Any) -> Any:
        if v == "":
            return None
        return v

    @model_validator(mode="after")
    def check_age_range(self) -> "Scholarship":
        if self.min_age is not None and self.max_age is not None and self.min_age > self.max_age:
            raise ValueError("min_age must be less than or equal to max_age")
        return self

    @model_validator(mode="after")
    def check_application_dates(self) -> "Scholarship":
        if (
            self.application_open_date is not None
            and self.application_deadline is not None
            and self.application_open_date > self.application_deadline
        ):
            raise ValueError("application_open_date must be on or before application_deadline")
        return self

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


ReportIssueType = Literal["broken_link", "wrong_deadline", "outdated_info", "wrong_eligibility", "other"]


class ScholarshipReportCreate(BaseModel):
    scholarship_id: int
    issue_type: ReportIssueType
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
    why_not_higher: Optional[List[str]] = []
    scoring_policy_version: Optional[str] = None


class MatchResponseMinimal(BaseModel):
    """Lightweight match row for list views (<50KB payloads)."""

    id: int
    title: str
    provider: Optional[str] = None
    score: float
    final_score: Optional[float] = None
    eligibility_status: Optional[bool] = None
    confidence: Optional[str] = None
    application_deadline: Optional[str] = None


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
    ph_created_at: Optional[str] = None  # Asia/Manila ISO for display


class MatchRunDetail(BaseModel):
    id: int
    profile_id: int
    created_at: datetime
    results: List[MatchResponse]
    ph_created_at: Optional[str] = None  # Asia/Manila ISO for display


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


class SavedScholarshipSummary(BaseModel):
    """Slim saved-scholarship row without nested full scholarship payload."""

    id: int
    scholarship_id: int
    created_at: datetime
    title: Optional[str] = None
    provider: Optional[str] = None
    benefit_tuition: Optional[bool] = None
    benefit_allowance_monthly: Optional[int] = None
    benefit_total_value: Optional[int] = None


class SavedScholarshipListResponse(BaseModel):
    saved: List[SavedScholarshipSummary] = []
    total: int = 0


# === SIPP / OJT (CHED CMO 104) ===
class HtePartnerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    industry: Optional[str] = Field(default=None, max_length=128)
    moa_status: Optional[str] = Field(default="pending", max_length=32)
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = Field(default=None, max_length=32)
    is_active: bool = True


class HtePartnerResponse(HtePartnerBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InternshipOpportunityBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    priority_courses: Optional[List[str]] = []
    region: Optional[str] = None
    province: Optional[str] = None
    psgc_code: Optional[str] = Field(default=None, max_length=9)
    slots: Optional[int] = Field(default=None, ge=0)
    allowance_status: Optional[str] = Field(default=None, max_length=32)
    allowance_amount: Optional[float] = Field(default=None, ge=0)
    application_deadline: Optional[date] = None
    is_active: bool = True


class InternshipOpportunityResponse(InternshipOpportunityBase):
    id: int
    hte_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OjtComplianceVaultBase(BaseModel):
    document_type: str = Field(..., max_length=48)
    template_version: Optional[str] = Field(default=None, max_length=32)
    prefilled_fields: Optional[dict[str, Any]] = None
    external_url: Optional[str] = Field(default=None, max_length=2048)
    status: str = Field(default="pending", max_length=32)


class OjtComplianceVaultResponse(OjtComplianceVaultBase):
    id: int
    student_id: int
    internship_id: Optional[int] = None
    guardian_consent_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
