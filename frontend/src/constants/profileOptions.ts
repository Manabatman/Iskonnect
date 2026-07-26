/** Shared select options for profile builder and related UI. */

export const EDUCATION_LEVELS = [
  { value: "", label: "Select target education level" },
  { value: "Grade 11", label: "Grade 11" },
  { value: "Grade 12", label: "Grade 12" },
  { value: "High School", label: "High School" },
  { value: "College", label: "College" },
  { value: "TVET", label: "TVET" },
  { value: "Graduate", label: "Graduate" },
] as const;

export const ACADEMIC_STAGES = [
  { value: "", label: "Select stage" },
  { value: "Junior HS", label: "Junior High School" },
  { value: "Senior HS", label: "Senior High School" },
  { value: "Undergraduate", label: "College Undergraduate" },
  { value: "Postgraduate", label: "Postgraduate" },
  { value: "TVET", label: "TVET" },
  { value: "ALS", label: "ALS Completer" },
] as const;

export const SCHOOL_TYPES = [
  { value: "", label: "Select" },
  { value: "Public", label: "Public" },
  { value: "Private", label: "Private" },
] as const;

export const GWA_SCALES = [
  { value: "", label: "Select scale" },
  { value: "percentage", label: "Percentage (0-100)" },
  { value: "5.0_scale", label: "5.0 Scale (1.0 highest)" },
  { value: "4.0_scale", label: "4.0 Scale (4.0 highest)" },
] as const;

export const ENROLLMENT_STATUSES = [
  { value: "", label: "Select enrollment status" },
  { value: "enrolled", label: "Currently enrolled" },
  { value: "incoming_freshman", label: "Incoming freshman" },
  { value: "transferee", label: "Transferee" },
  { value: "returning", label: "Returning student" },
  { value: "graduating", label: "Graduating this year" },
  { value: "on_leave", label: "On leave / LOA" },
] as const;

export const YEAR_LEVELS = [
  { value: "", label: "Select year level" },
  { value: "11", label: "Grade 11" },
  { value: "12", label: "Grade 12" },
  { value: "1", label: "College 1st Year" },
  { value: "2", label: "College 2nd Year" },
  { value: "3", label: "College 3rd Year" },
  { value: "4", label: "College 4th Year" },
  { value: "5", label: "College 5th Year+" },
] as const;

export const EQUITY_FLAG_MAP: Record<string, string> = {
  Underprivileged: "is_underprivileged",
  PWD: "is_pwd",
  IP: "is_indigenous_people",
  "Solo Parent Dependent": "is_solo_parent_dependent",
  "OFW Dependent": "is_ofw_dependent",
  "Farmer/Fisher Dependent": "is_farmer_fisher_dependent",
  "4Ps/Listahanan": "is_4ps_listahanan",
  "Military Dependents": "is_military_dependent",
  "Uniformed Service Dependents": "is_uniformed_service_dependent",
  "GSIS Dependent": "is_gsis_dependent",
  "SSS Dependent": "is_sss_dependent",
};
