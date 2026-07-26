import type { ProfileBuilderState } from "../components/profile-builder/profileBuilderState";
import type { StudentProfile } from "../types";

/** Build API payload from profile builder state (POST /api/v1/profiles). */
export function buildStudentProfileFromBuilderState(state: ProfileBuilderState): StudentProfile {
  const trim = (k: keyof ProfileBuilderState) => {
    const v = state[k]?.trim();
    return v || undefined;
  };
  const getNum = (k: keyof ProfileBuilderState) => {
    const v = state[k]?.trim();
    if (!v) return undefined;
    const n = Number(v);
    return Number.isNaN(n) ? undefined : n;
  };
  const getBool = (k: keyof ProfileBuilderState) => state[k] === "on";
  const getList = (raw: string) =>
    raw
      .split(",")
      .map((n) => n.trim())
      .filter(Boolean);

  const preferredCourses = [trim("preferred_course_1"), trim("preferred_course_2"), trim("preferred_course_3")].filter(
    (c): c is string => Boolean(c)
  );

  return {
    full_name: state.full_name,
    email: state.email,
    age: getNum("age"),
    region: trim("region"),
    school: trim("school"),
    needs: getList(state.needs),
    education_level: trim("education_level"),
    gender: trim("gender"),
    enrollment_status: trim("enrollment_status"),
    current_year_level: getNum("current_year_level"),
    current_academic_stage: trim("current_academic_stage"),
    target_academic_year: trim("target_academic_year"),
    province: trim("province"),
    city_municipality: trim("city_municipality"),
    barangay: trim("barangay"),
    school_type: trim("school_type"),
    target_school: trim("target_school"),
    gwa_raw: trim("gwa_raw"),
    gwa_scale: trim("gwa_scale"),
    field_of_study_broad: trim("field_of_study_broad"),
    field_of_study_specific: preferredCourses[0] ?? trim("field_of_study_specific"),
    preferred_courses: preferredCourses,
    extracurriculars: getList(state.extracurriculars),
    awards: getList(state.awards),
    household_income_annual: getNum("household_income_annual"),
    income_bracket: trim("income_bracket"),
    is_underprivileged: getBool("is_underprivileged"),
    is_pwd: getBool("is_pwd"),
    is_indigenous_people: getBool("is_indigenous_people"),
    is_solo_parent_dependent: getBool("is_solo_parent_dependent"),
    is_ofw_dependent: getBool("is_ofw_dependent"),
    is_farmer_fisher_dependent: getBool("is_farmer_fisher_dependent"),
    is_4ps_listahanan: getBool("is_4ps_listahanan"),
    is_military_dependent: getBool("is_military_dependent"),
    is_uniformed_service_dependent: getBool("is_uniformed_service_dependent"),
    is_gsis_dependent: getBool("is_gsis_dependent"),
    is_sss_dependent: getBool("is_sss_dependent"),
    parent_occupation: trim("parent_occupation"),
    privacy_consent: getBool("privacy_consent"),
    privacy_consent_version: "ra10173-v1",
  };
}
