export interface ProfileBuilderState {
  full_name: string;
  email: string;
  age: string;
  gender: string;

  education_level: string;
  current_academic_stage: string;
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

/** Not counted toward profile-builder completion % (optional UX fields). */
export const OPTIONAL_PROFILE_FIELDS = new Set<keyof ProfileBuilderState>([
  "barangay",
  "target_school",
  "preferred_course_2",
  "preferred_course_3",
  "extracurriculars",
  "awards",
  "parent_occupation",
]);

/** RA priority flags — any number can apply; not required for 100% completion. */
export const PRIORITY_GROUP_FIELDS: (keyof ProfileBuilderState)[] = [
  "is_underprivileged",
  "is_pwd",
  "is_indigenous_people",
  "is_solo_parent_dependent",
  "is_ofw_dependent",
  "is_farmer_fisher_dependent",
  "is_4ps_listahanan",
];

export const INITIAL_STATE: ProfileBuilderState = {
  full_name: "",
  email: "",
  age: "",
  gender: "",

  education_level: "",
  current_academic_stage: "",
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
    fields: ["full_name", "email", "age", "gender"],
  },
  {
    id: 2,
    label: "Education",
    shortLabel: "Education",
    fields: [
      "education_level",
      "current_academic_stage",
      "target_academic_year",
      "school",
      "school_type",
      "target_school",
      "gwa_raw",
      "gwa_scale",
    ].filter((k) => !OPTIONAL_PROFILE_FIELDS.has(k)),
  },
  {
    id: 3,
    label: "Location and Background",
    shortLabel: "Location",
    fields: [
      "region",
      "province",
      "city_municipality",
      "barangay",
    ].filter((k) => !OPTIONAL_PROFILE_FIELDS.has(k)),
  },
  {
    id: 4,
    label: "Field of Study and Skills",
    shortLabel: "Skills",
    fields: [
      "field_of_study_broad",
      "field_of_study_specific",
      "preferred_course_1",
      "preferred_course_2",
      "preferred_course_3",
      "extracurriculars",
      "awards",
    ].filter((k) => !OPTIONAL_PROFILE_FIELDS.has(k)),
  },
  {
    id: 5,
    label: "Eligibility and Goals",
    shortLabel: "Goals",
    // Priority RA flags are optional for %; only needs + consent gate completion.
    fields: ["needs", "privacy_consent"],
  },
];

function isFieldFilled(key: keyof ProfileBuilderState, value: string): boolean {
  const v = (value ?? "").trim();
  if (key.startsWith("is_") || key === "privacy_consent") {
    return v === "on";
  }
  if (key === "needs") {
    return v.length > 0;
  }
  return v.length > 0;
}

export function computeStepCompletion(
  state: ProfileBuilderState,
  stepId: number
): { filled: number; total: number } {
  const step = PROFILE_BUILDER_STEPS.find((s) => s.id === stepId);
  if (!step) return { filled: 0, total: 0 };

  if (stepId === 3) {
    let filled = 0;
    for (const key of step.fields) {
      if (isFieldFilled(key, state[key])) filled += 1;
    }
    const incomeFilled =
      isFieldFilled("household_income_annual", state.household_income_annual) ||
      isFieldFilled("income_bracket", state.income_bracket);
    if (incomeFilled) filled += 1;
    return { filled, total: step.fields.length + 1 };
  }

  let filled = 0;
  for (const key of step.fields) {
    if (isFieldFilled(key, state[key])) filled += 1;
  }
  return { filled, total: step.fields.length };
}

export function computeOverallCompletion(state: ProfileBuilderState): number {
  let sum = 0;
  for (const s of PROFILE_BUILDER_STEPS) {
    const { filled, total } = computeStepCompletion(state, s.id);
    if (total > 0) sum += filled / total;
  }
  return Math.round((sum / PROFILE_BUILDER_STEPS.length) * 100);
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
