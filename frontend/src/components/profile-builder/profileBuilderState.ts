export interface ProfileBuilderState {
  full_name: string;
  email: string;
  age: string;
  gender: string;

  education_level: string;
  current_academic_stage: string;
  enrollment_status: string;
  current_year_level: string;
  target_academic_year: string;
  school: string;
  school_type: string;
  target_school: string;
  gwa_raw: string;
  gwa_scale: string;

  region: string;
  province: string;
  city_municipality: string;
  barangay: string;
  household_income_annual: string;
  income_bracket: string;
  parent_occupation: string;

  field_of_study_broad: string;
  field_of_study_specific: string;
  preferred_course_1: string;
  preferred_course_2: string;
  preferred_course_3: string;
  extracurriculars: string;
  awards: string;

  needs: string;
  is_underprivileged: string;
  is_pwd: string;
  is_indigenous_people: string;
  is_solo_parent_dependent: string;
  is_ofw_dependent: string;
  is_farmer_fisher_dependent: string;
  is_4ps_listahanan: string;
  is_military_dependent: string;
  is_uniformed_service_dependent: string;
  is_gsis_dependent: string;
  is_sss_dependent: string;
  employment_status: string;
  evening_weekend_program: string;
  athlete_level: string;
  /** "on" when user accepts RA 10173 consent (required to save). */
  privacy_consent: string;
}

export const DRAFT_KEY = "iskonnect_profile_draft";

/** Remove device-local profile builder draft (call on login/register/logout). */
export function clearProfileDraft(): void {
  try {
    localStorage.removeItem(DRAFT_KEY);
  } catch {
    /* ignore */
  }
}

/** Required to save profile — completion % reflects these only (CLARITY-06). */
export const SAVE_REQUIRED_FIELDS: (keyof ProfileBuilderState)[] = [
  "full_name",
  "email",
  "region",
  "privacy_consent",
];

/** RA priority flags — any number can apply; not required for 100% completion. */
export const PRIORITY_GROUP_FIELDS: (keyof ProfileBuilderState)[] = [
  "is_underprivileged",
  "is_pwd",
  "is_indigenous_people",
  "is_solo_parent_dependent",
  "is_ofw_dependent",
  "is_farmer_fisher_dependent",
  "is_4ps_listahanan",
  "is_military_dependent",
  "is_uniformed_service_dependent",
  "is_gsis_dependent",
  "is_sss_dependent",
];

/** Not counted toward profile-builder completion % (optional UX fields). */
export const OPTIONAL_PROFILE_FIELDS = new Set<keyof ProfileBuilderState>([
  "barangay",
  "target_school",
  "preferred_course_2",
  "preferred_course_3",
  "extracurriculars",
  "awards",
  "parent_occupation",
  "employment_status",
  "evening_weekend_program",
  "athlete_level",
  "age",
  "gender",
  "education_level",
  "current_academic_stage",
  "enrollment_status",
  "current_year_level",
  "target_academic_year",
  "school",
  "school_type",
  "gwa_raw",
  "gwa_scale",
  "province",
  "city_municipality",
  "household_income_annual",
  "income_bracket",
  "field_of_study_broad",
  "field_of_study_specific",
  "preferred_course_1",
  "needs",
  ...PRIORITY_GROUP_FIELDS,
]);

export const INITIAL_STATE: ProfileBuilderState = {
  full_name: "",
  email: "",
  age: "",
  gender: "",

  education_level: "",
  current_academic_stage: "",
  enrollment_status: "",
  current_year_level: "",
  target_academic_year: "",
  school: "",
  school_type: "",
  target_school: "",
  gwa_raw: "",
  gwa_scale: "",

  region: "",
  province: "",
  city_municipality: "",
  barangay: "",
  household_income_annual: "",
  income_bracket: "",
  parent_occupation: "",

  field_of_study_broad: "",
  field_of_study_specific: "",
  preferred_course_1: "",
  preferred_course_2: "",
  preferred_course_3: "",
  extracurriculars: "",
  awards: "",

  needs: "",
  is_underprivileged: "",
  is_pwd: "",
  is_indigenous_people: "",
  is_solo_parent_dependent: "",
  is_ofw_dependent: "",
  is_farmer_fisher_dependent: "",
  is_4ps_listahanan: "",
  is_military_dependent: "",
  is_uniformed_service_dependent: "",
  is_gsis_dependent: "",
  is_sss_dependent: "",
  employment_status: "",
  evening_weekend_program: "",
  athlete_level: "",
  privacy_consent: "",
};

export type ProfileBuilderStepDef = {
  id: number;
  label: string;
  shortLabel: string;
  fields: (keyof ProfileBuilderState)[];
};

export const PROFILE_BUILDER_STEPS: ProfileBuilderStepDef[] = [
  {
    id: 1,
    label: "Personal Info",
    shortLabel: "Personal",
    fields: ["full_name", "email"],
  },
  {
    id: 2,
    label: "Education",
    shortLabel: "Education",
    fields: [],
  },
  {
    id: 3,
    label: "Location and Background",
    shortLabel: "Location",
    fields: ["region"],
  },
  {
    id: 4,
    label: "Field of Study and Skills",
    shortLabel: "Skills",
    fields: [],
  },
  {
    id: 5,
    label: "Eligibility and Goals",
    shortLabel: "Goals",
    fields: ["privacy_consent"],
  },
];

function isFieldFilled(key: keyof ProfileBuilderState, value: string): boolean {
  const v = (value ?? "").trim();
  if (key === "full_name") return v.length >= 2;
  if (key.startsWith("is_") || key === "privacy_consent" || key === "evening_weekend_program") {
    return v === "on";
  }
  return v.length > 0;
}

/** Validate fields required before leaving a step (CLARITY-05). */
export function validateProfileBuilderStep(
  stepId: number,
  state: ProfileBuilderState,
  emailValid: (email: string) => { valid: boolean; message?: string }
): string | null {
  if (stepId === 1) {
    if (!state.full_name?.trim() || state.full_name.trim().length < 2) {
      return "Please enter your full name (at least 2 characters).";
    }
    if (!state.email?.trim()) {
      return "Please enter your email address.";
    }
    const check = emailValid(state.email);
    if (!check.valid) {
      return check.message ?? "Please enter a valid email address.";
    }
    return null;
  }
  if (stepId === 3) {
    if (!state.region?.trim()) {
      return "Please select your region before continuing.";
    }
    return null;
  }
  return null;
}

export function computeStepCompletion(
  state: ProfileBuilderState,
  stepId: number
): { filled: number; total: number } {
  const step = PROFILE_BUILDER_STEPS.find((s) => s.id === stepId);
  if (!step) return { filled: 0, total: 0 };

  let filled = 0;
  for (const key of step.fields) {
    if (isFieldFilled(key, state[key])) filled += 1;
  }
  return { filled, total: step.fields.length };
}

export function computeOverallCompletion(state: ProfileBuilderState): number {
  let filled = 0;
  for (const key of SAVE_REQUIRED_FIELDS) {
    if (isFieldFilled(key, state[key])) filled += 1;
  }
  return Math.round((filled / SAVE_REQUIRED_FIELDS.length) * 100);
}

export type ProfileBuilderAction =
  | { type: "SET_FIELD"; field: keyof ProfileBuilderState; value: string }
  | { type: "LOAD_DRAFT"; draft: Partial<Record<string, string>> }
  | { type: "RESET" };

export function profileBuilderReducer(
  state: ProfileBuilderState,
  action: ProfileBuilderAction
): ProfileBuilderState {
  switch (action.type) {
    case "SET_FIELD":
      return { ...state, [action.field]: action.value };
    case "LOAD_DRAFT": {
      const next = { ...state };
      for (const key of Object.keys(INITIAL_STATE) as (keyof ProfileBuilderState)[]) {
        const v = action.draft[key as string];
        if (v !== undefined && typeof v === "string") {
          next[key] = v;
        }
      }
      return next;
    }
    case "RESET":
      return { ...INITIAL_STATE };
    default:
      return state;
  }
}

/** Merge device-local draft with server profile — server wins when both have a value (TRUST-01). */
export function mergeProfileDrafts(
  local: Partial<Record<string, string>>,
  server: Partial<Record<string, string>>
): Partial<Record<string, string>> {
  const merged: Partial<Record<string, string>> = { ...local };
  for (const key of Object.keys(INITIAL_STATE) as (keyof ProfileBuilderState)[]) {
    const sk = key as string;
    const serverVal = server[sk];
    const localVal = local[sk];
    if (serverVal !== undefined && String(serverVal).trim()) {
      merged[sk] = serverVal;
    } else if (localVal !== undefined && String(localVal).trim()) {
      merged[sk] = localVal;
    }
  }
  return merged;
}

export function parseDraftFromStorage(raw: string | null): Partial<Record<string, string>> | null {
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw) as unknown;
    if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) {
      return parsed as Partial<Record<string, string>>;
    }
  } catch {
    /* ignore */
  }
  return null;
}
