import { beforeEach, describe, expect, it, vi } from "vitest";
import {
  DRAFT_KEY,
  INITIAL_STATE,
  clearProfileDraft,
  computeOverallCompletion,
  computeStepCompletion,
  type ProfileBuilderState,
} from "./profileBuilderState";

function filledState(overrides: Partial<ProfileBuilderState> = {}): ProfileBuilderState {
  return {
    ...INITIAL_STATE,
    full_name: "Maria Santos",
    email: "maria@example.com",
    age: "18",
    gender: "female",
    education_level: "College / University",
    current_academic_stage: "1st Year",
    target_academic_year: "2026-2027",
    school: "Sample University",
    school_type: "public",
    gwa_raw: "1.5",
    gwa_scale: "5.0",
    region: "NCR",
    province: "Metro Manila",
    city_municipality: "Quezon City",
    household_income_annual: "200000",
    field_of_study_broad: "STEM",
    field_of_study_specific: "Engineering",
    preferred_course_1: "Civil Engineering",
    needs: "tuition",
    privacy_consent: "on",
    ...overrides,
  };
}

describe("profile completion", () => {
  it("100% when all save-required fields are filled", () => {
    const state = filledState();
    expect(computeOverallCompletion(state)).toBe(100);
  });

  it("does not require enrollment_status or parent_occupation for 100%", () => {
    const state = filledState({ enrollment_status: "", current_year_level: "", parent_occupation: "" });
    expect(computeOverallCompletion(state)).toBe(100);
  });

  it("step 3 tracks region only for required fields", () => {
    const withRegion = filledState({ province: "", city_municipality: "", household_income_annual: "", income_bracket: "" });
    expect(computeStepCompletion(withRegion, 3)).toEqual({ filled: 1, total: 1 });
  });
});

describe("clearProfileDraft", () => {
  const store: Record<string, string> = {};

  beforeEach(() => {
    Object.keys(store).forEach((k) => delete store[k]);
    vi.stubGlobal("localStorage", {
      getItem: (key: string) => store[key] ?? null,
      setItem: (key: string, value: string) => {
        store[key] = value;
      },
      removeItem: (key: string) => {
        delete store[key];
      },
    });
  });

  it("removes the device-local profile draft from localStorage", () => {
    localStorage.setItem(DRAFT_KEY, JSON.stringify({ full_name: "Previous User" }));
    clearProfileDraft();
    expect(localStorage.getItem(DRAFT_KEY)).toBeNull();
  });
});
