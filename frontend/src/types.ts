export interface StudentProfile {
  full_name: string;
  email: string;
  age?: number;
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

export interface ProfileCompleteness {
  filled_fields: number;
  total_fields: number;
  low_data_warning: boolean;
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
  benefit_tuition?: boolean;
  benefit_total_value?: number | null;
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
  benefit_tuition?: boolean;
  benefit_allowance_monthly?: number | null;
  benefit_books?: boolean;
  benefit_total_value?: number | null;
  application_deadline?: string | null;
  application_open_date?: string | null;
  required_documents?: string[];
  /** Improvement tips from matching engine */
  suggestions?: string[];
  /** Top reasons the match score is not higher (gaps vs max contribution per factor) */
  why_not_higher?: string[];
  /** Policy rubric version used to compute this score */
  scoring_policy_version?: string | null;
  data_status?: string | null;
  link_status?: string | null;
  verification_source?: string | null;
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
  link: string | null;
  description: string;
  regions: string[];
  min_age: number | null;
  max_age: number | null;
  level?: string | null;
  provider_type?: string | null;
  scholarship_type?: string | null;
  benefit_tuition?: boolean;
  benefit_allowance_monthly?: number | null;
  benefit_books?: boolean;
  benefit_total_value?: number | null;
  application_deadline?: string | null;
  application_open_date?: string | null;
  is_active?: boolean;
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
