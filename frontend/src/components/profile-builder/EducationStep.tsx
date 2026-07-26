import { useEffect, useState } from "react";
import { AutocompleteInput } from "../AutocompleteInput";
import type { ProfileBuilderState } from "./profileBuilderState";
import {
  ACADEMIC_STAGES,
  EDUCATION_LEVELS,
  ENROLLMENT_STATUSES,
  GWA_SCALES,
  SCHOOL_TYPES,
  YEAR_LEVELS,
  inputClass,
  labelClass,
} from "./profileBuilderConstants";
import { apiFetch } from "../../api/client";
import type { StepProps } from "./PersonalInfoStep";

type ProfileOption = { value: string; label: string };

function normalizeOptions(raw: unknown, fallback: readonly ProfileOption[]): ProfileOption[] {
  if (!Array.isArray(raw)) return [...fallback];
  const mapped = raw
    .map((item) => {
      if (!item || typeof item !== "object") return null;
      const row = item as { value?: string | number; label?: string };
      if (row.value == null || row.label == null) return null;
      return { value: String(row.value), label: String(row.label) };
    })
    .filter((x): x is ProfileOption => x != null);
  return mapped.length > 0 ? mapped : [...fallback];
}

export function EducationStep({ state, onChange }: StepProps) {
  const [enrollmentOptions, setEnrollmentOptions] = useState<ProfileOption[]>([...ENROLLMENT_STATUSES]);
  const [yearLevelOptions, setYearLevelOptions] = useState<ProfileOption[]>([...YEAR_LEVELS]);

  useEffect(() => {
    let cancelled = false;
    apiFetch("/api/v1/suggestions/profile-options")
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (cancelled || !data) return;
        setEnrollmentOptions(
          normalizeOptions(
            (data as { enrollment_statuses?: unknown }).enrollment_statuses,
            ENROLLMENT_STATUSES
          )
        );
        const rawLevels = (data as { year_levels?: unknown }).year_levels;
        if (Array.isArray(rawLevels)) {
          const levels = rawLevels
            .map((item) => {
              if (!item || typeof item !== "object") return null;
              const row = item as { value?: string | number; label?: string };
              if (row.value == null || !row.label) return null;
              return { value: String(row.value), label: row.label };
            })
            .filter((x): x is ProfileOption => x != null);
          if (levels.length > 0) {
            setYearLevelOptions([{ value: "", label: "Select year level" }, ...levels]);
          }
        }
      })
      .catch(() => {
        /* keep local defaults */
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Education</h2>
        <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
          Where you study and how you are performing academically.
        </p>
      </div>

      <div className="rounded-lg border border-primary-200 bg-primary-50 px-3 py-2 text-sm text-primary-800 dark:border-primary-800 dark:bg-primary-900/20 dark:text-primary-200">
        Adding your GWA lets us check merit-based scholarships.
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label htmlFor="pb-current_academic_stage" className={labelClass}>
            Current academic stage
          </label>
          <select
            id="pb-current_academic_stage"
            value={state.current_academic_stage}
            onChange={(e) => onChange("current_academic_stage", e.target.value)}
            className={inputClass}
          >
            {ACADEMIC_STAGES.map((opt) => (
              <option key={opt.value || "empty"} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="pb-enrollment_status" className={labelClass}>
            Enrollment status
          </label>
          <select
            id="pb-enrollment_status"
            value={state.enrollment_status}
            onChange={(e) => onChange("enrollment_status", e.target.value)}
            className={inputClass}
          >
            {enrollmentOptions.map((opt) => (
              <option key={opt.value || "empty-enrollment"} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="pb-current_year_level" className={labelClass}>
            Current year level
          </label>
          <select
            id="pb-current_year_level"
            value={state.current_year_level}
            onChange={(e) => onChange("current_year_level", e.target.value)}
            className={inputClass}
          >
            {yearLevelOptions.map((opt) => (
              <option key={opt.value || "empty-year"} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="pb-education_level" className={labelClass}>
            Target education level for scholarship
          </label>
          <p className="mb-1 text-xs text-slate-500 dark:text-slate-400">
            The level you want scholarships for — can differ from your current academic stage above.
          </p>
          <select
            id="pb-education_level"
            value={state.education_level}
            onChange={(e) => onChange("education_level", e.target.value)}
            className={inputClass}
          >
            {EDUCATION_LEVELS.map((opt) => (
              <option key={opt.value || "empty"} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="pb-target_academic_year" className={labelClass}>
            Target academic year
          </label>
          <input
            id="pb-target_academic_year"
            type="text"
            value={state.target_academic_year}
            onChange={(e) => onChange("target_academic_year", e.target.value)}
            className={inputClass}
            placeholder="e.g. 2026-2027"
          />
        </div>
        <div>
          <AutocompleteInput
            id="pb-school"
            name="school"
            label="School"
            value={state.school}
            onChange={(name, value) => onChange(name as keyof ProfileBuilderState, value)}
            endpoint="/api/v1/suggestions/schools"
            placeholder="Current or target school"
            className={inputClass}
          />
        </div>
        <div>
          <label htmlFor="pb-school_type" className={labelClass}>
            School type
          </label>
          <select
            id="pb-school_type"
            value={state.school_type}
            onChange={(e) => onChange("school_type", e.target.value)}
            className={inputClass}
          >
            {SCHOOL_TYPES.map((opt) => (
              <option key={opt.value || "empty"} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>
        <div>
          <AutocompleteInput
            id="pb-target_school"
            name="target_school"
            label="Target university (optional)"
            value={state.target_school}
            onChange={(name, value) => onChange(name as keyof ProfileBuilderState, value)}
            endpoint="/api/v1/suggestions/schools"
            placeholder="e.g. UP Diliman"
            className={inputClass}
          />
        </div>
        <div>
          <label htmlFor="pb-gwa_raw" className={labelClass}>
            GWA / Grade
          </label>
          <input
            id="pb-gwa_raw"
            type="text"
            value={state.gwa_raw}
            onChange={(e) => onChange("gwa_raw", e.target.value)}
            className={inputClass}
            placeholder="e.g. 95 or 1.25"
          />
        </div>
        <div>
          <label htmlFor="pb-gwa_scale" className={labelClass}>
            Grading scale
          </label>
          <select
            id="pb-gwa_scale"
            value={state.gwa_scale}
            onChange={(e) => onChange("gwa_scale", e.target.value)}
            className={inputClass}
          >
            {GWA_SCALES.map((opt) => (
              <option key={opt.value || "empty"} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
}
