export type QualificationStatus =
  | "qualified"
  | "provisionally_qualified"
  | "almost_qualified"
  | "not_eligible";

export interface StudentProfile {
  full_name: string;
  email: string;
  age?: number;
  enrollment_status?: string;
  current_year_level?: number;
  region?: string;
  school?: string;
  needs?: string[];
  education_level?: string;
  gender?: string;
  birthdate?: string;
  current_academic_stage?: string;
  target_academic_year?: string;
  province?: string;
  city_municipality?: string;
  barangay?: string;
  school_type?: string;
  target_school?: string;
  gwa_raw?: string;
  gwa_scale?: string;
  gwa_normalized?: number;
  field_of_study_broad?: string;
  field_of_study_specific?: string;
  preferred_courses?: string[];
  extracurriculars?: string[];
  awards?: string[];
  household_income_annual?: number;
  income_bracket?: string;
  is_underprivileged?: boolean;
  is_pwd?: boolean;
  is_indigenous_people?: boolean;
  ip_tribe_name?: string;
  is_solo_parent_dependent?: boolean;
  is_ofw_dependent?: boolean;
  ofw_parent_type?: string;
  is_farmer_fisher_dependent?: boolean;
  is_4ps_listahanan?: boolean;
  is_military_dependent?: boolean;
  is_uniformed_service_dependent?: boolean;
  is_gsis_dependent?: boolean;
  is_sss_dependent?: boolean;
  employment_status?: string;
  evening_weekend_program?: boolean;
  athlete_level?: string;
  parent_occupation?: string;
  documents?: Array<{ type: string; status: string }>;
  privacy_consent?: boolean;
  privacy_consent_version?: string;
}

export interface MatchFactorBreakdown {
  status: string;
  user_value: string;
  requirement_value: string;
  detail?: string;
  score?: number | null;
  weighted?: number;
  max_possible?: number;
}

export interface MatchBreakdown {
  academic?: MatchFactorBreakdown;
  socioeconomic?: MatchFactorBreakdown;
  field_relevance?: MatchFactorBreakdown;
  geographic?: MatchFactorBreakdown;
  document_readiness?: MatchFactorBreakdown;
  priority_group?: MatchFactorBreakdown;
}

export interface ProfileMissingField {
  key: string;
  label: string;
  profile_link: string;
}

export interface ProfileCompleteness {
  filled_fields: number;
  total_fields: number;
  low_data_warning: boolean;
  quality_percent?: number;
  quality_filled?: number;
  quality_total?: number;
  missing_fields?: ProfileMissingField[];
  improvement_hints?: string[];
}

export interface EliminatedScholarship {
  scholarship_id?: number;
  title?: string;
  filter?: string;
  reason?: string;
}

export interface MatchDiagnostics {
  total_checked?: number;
  passed_hard_filters?: number;
  eliminated_by_filter?: Record<string, number>;
  eliminated_scholarships?: EliminatedScholarship[];
  hard_exclusions?: EliminatedScholarship[];
  missing_profile_fields?: string[];
  top_blockers?: string[];
}

export interface FieldEvidence {
  id: number;
  field_key: string;
  value_snapshot?: string | null;
  source_url?: string | null;
  source_type?: string | null;
  evidence_snippet?: string | null;
  confidence?: number | null;
  retrieved_at?: string | null;
  created_at?: string | null;
}

export interface ApplicationPreparation {
  readiness_score?: number;
  document_checklist?: Array<{ document: string; status: string }>;
  documents_ready?: number;
  documents_total?: number;
  profile_fields_filled?: number;
  profile_fields_total?: number;
}

export interface ScholarshipEligibilityDetail {
  scholarship_id: number;
  profile_id: number;
  qualification_status: string;
  requirements?: Array<{ key?: string; label?: string; result?: string; detail?: string }>;
  missing_requirements?: string[];
  qualifying_requirements?: string[];
  eligibility_confidence?: string | null;
  passes_for_matching?: boolean;
}

export interface ScholarshipVersionHistoryItem {
  version_number: number;
  changed_at?: string | null;
  changes: Record<string, unknown>;
}

export interface OrganizationProfile {
  slug: string;
  canonical_name: string;
  org_type?: string | null;
  logo_url?: string | null;
  website?: string | null;
  verification_status?: string | null;
  opportunity_count: number;
  avg_freshness_days?: number | null;
  report_count: number;
}

export interface PlanResponse {
  matches: MatchResult[];
  total: number;
  limit: number;
  offset: number;
  timeline: OpportunityTimeline;
  preparation?: { items?: unknown[]; count?: number };
  profile_completeness?: ProfileCompleteness;
  diagnostics?: MatchDiagnostics;
}

export interface UpcomingScholarship {
  id: number;
  title: string;
  provider?: string | null;
  cycle_type?: string | null;
  last_open_date?: string | null;
  last_close_date?: string | null;
  predicted_next_open?: string | null;
  link?: string | null;
  description?: string;
  image_url?: string | null;
  image_alt?: string | null;
  benefit_tuition?: boolean;
  benefit_total_value?: number | null;
}

export interface FreshnessChip {
  label: string;
  tone: "success" | "warning" | "danger" | "neutral" | string;
}

export type EligibilityState =
  | "eligible_now"
  | "eligible_soon"
  | "missing_one_requirement"
  | "prepare_now"
  | "requires_future_grade_level"
  | "requires_future_enrollment"
  | "requires_better_academic_standing"
  | "expected_next_cycle"
  | "past_opportunity"
  | "potential_match"
  | "not_eligible";

export interface OpportunityTimelineSummary {
  available_now: number;
  opening_soon: number;
  prepare_for: number;
  expected_reopening: number;
  future_eligibility: number;
  past_reference: number;
  total_actionable: number;
}

export interface OpportunityTimeline {
  summary: OpportunityTimelineSummary;
  lanes: {
    available_now: MatchResult[];
    opening_soon: MatchResult[];
    prepare_for: MatchResult[];
    expected_reopening: MatchResult[];
    future_eligibility: MatchResult[];
    past_reference: MatchResult[];
  };
  headline: string;
}

export interface MatchResult {
  id: number;
  title: string;
  provider?: string | null;
  score: number;
  final_score?: number;
  eligibility_status?: boolean;
  /** True when student meets hard filters but application deadline has passed */
  deadline_passed?: boolean;
  readiness_score?: number;
  explanation?: string[];
  breakdown?: MatchBreakdown;
  confidence?: string;
  link: string | null;
  description: string;
  regions: string[];
  min_age: number | null;
  max_age: number | null;
  level?: string | null;
  provider_type?: string | null;
  scholarship_type?: string | null;
  image_url?: string | null;
  image_alt?: string | null;
  benefit_tuition?: boolean;
  benefit_allowance_monthly?: number | null;
  benefit_books?: boolean;
  benefit_total_value?: number | null;
  application_deadline?: string | null;
  deadline_precision?: string | null;
  deadline_note?: string | null;
  application_open_date?: string | null;
  predicted_open?: string | null;
  required_documents?: string[];
  preparation?: ApplicationPreparation;
  /** Improvement tips from matching engine */
  suggestions?: string[];
  /** Top reasons the match score is not higher (gaps vs max contribution per factor) */
  why_not_higher?: string[];
  /** Policy rubric version used to compute this score */
  scoring_policy_version?: string | null;
  data_status?: string | null;
  application_status?: string | null;
  link_status?: string | null;
  verification_source?: string | null;
  last_verified_at?: string | null;
  confidence_score?: number | null;
  eligibility_state?: EligibilityState | string;
  ui_state?: "eligible_now" | "opening_soon" | "prepare_ahead" | "future_eligibility" | string;
  gap_reason?: string | null;
  next_action?: string | null;
  lifecycle_hint?: string | null;
  freshness_chips?: FreshnessChip[];
  qualification_status?: QualificationStatus | string;
  qualifying_requirements?: string[];
  missing_requirements?: string[];
  unverified_requirements?: string[];
  provisional_reason?: string | null;
  eligibility_confidence?: string;
  requirements?: Array<{
    key?: string;
    label?: string;
    kind?: string;
    result?: string;
    verified?: string;
    evidence?: string | null;
  }>;
  verification_badge?: string | null;
  verification_badge_label?: string | null;
  verification_source_label?: string | null;
  completeness_label?: string | null;
  last_reviewed_label?: string | null;
}

export interface MatchRunSummary {
  id: number;
  profile_id: number;
  created_at: string;
  /** Asia/Manila ISO from API (optional). */
  ph_created_at?: string | null;
  result_count: number;
}

export interface MatchComparisonItem {
  scholarship_id: number;
  title: string;
  provider?: string | null;
  score_a?: number | null;
  score_b?: number | null;
  score_diff?: number | null;
}

export interface MatchComparisonResponse {
  run_a: MatchRunSummary;
  run_b: MatchRunSummary;
  items: MatchComparisonItem[];
}

export interface StudentProfileResponse {
  id: number;
  full_name: string;
  email: string;
  age?: number | null;
  region?: string | null;
  school?: string | null;
  needs?: string[];
  education_level?: string | null;
  google_drive_folder_url?: string | null;
  [key: string]: unknown;
}

export interface ScholarshipInfo {
  id: number;
  title: string;
  provider?: string | null;
  provider_display?: string | null;
  link: string | null;
  description: string;
  regions: string[];
  min_age: number | null;
  max_age: number | null;
  level?: string | null;
  provider_type?: string | null;
  scholarship_type?: string | null;
  image_url?: string | null;
  image_alt?: string | null;
  benefit_tuition?: boolean;
  benefit_allowance_monthly?: number | null;
  benefit_books?: boolean;
  benefit_total_value?: number | null;
  application_deadline?: string | null;
  deadline_precision?: string | null;
  deadline_note?: string | null;
  application_open_date?: string | null;
  next_review_date?: string | null;
  field_evidence?: FieldEvidence[];
  completeness_label?: string | null;
  completeness_tier?: string | null;
  preparation?: ApplicationPreparation;
  is_active?: boolean;
  application_status?: string | null;
  data_status?: string | null;
  link_status?: string | null;
  verification_source?: string | null;
  last_verified_at?: string | null;
  verification_badge?: string | null;
  verification_badge_label?: string | null;
  verification_source_label?: string | null;
  last_reviewed_label?: string | null;
  predicted_next_open?: string | null;
  cycle_type?: string | null;
  required_documents?: string[];
}

export interface ScholarshipSearchResponse {
  results: ScholarshipInfo[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

export interface ScholarshipSearchFilters {
  region?: string;
  field?: string;
  education_level?: string;
  provider?: string;
  /** University / institution keyword (matches title, provider, description, school types) */
  school?: string;
  max_income?: number;
  /** When to apply: open_now | opening_soon | closed | previous_cycle | expected_reopen | needs_verification | archived */
  timing?: string;
  /** Life stage: high_school | college | graduate | tvet */
  life_stage?: string;
  /** @deprecated Use timing filters instead */
  include_archived?: boolean;
}

export interface SavedScholarship {
  id: number;
  scholarship_id: number;
  created_at: string;
  title?: string | null;
  provider?: string | null;
  benefit_tuition?: boolean | null;
  benefit_allowance_monthly?: number | null;
  benefit_total_value?: number | null;
  scholarship?: ScholarshipInfo;
}
