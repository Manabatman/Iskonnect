import { NEEDS_CATEGORIES } from "../../constants/needsCategories";
import { AutocompleteInput } from "../AutocompleteInput";
import type { ProfileBuilderState } from "./profileBuilderState";
import type { StepProps } from "./PersonalInfoStep";
import { inputClass, labelClass } from "./profileBuilderConstants";

export function FieldOfStudyStep({ state, onChange }: StepProps) {
  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Field of Study and Skills</h2>
        <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
          What you want to study and what you have achieved outside class.
        </p>
      </div>

      <div className="rounded-lg border border-primary-200 bg-primary-50 px-3 py-2 text-sm text-primary-800 dark:border-primary-800 dark:bg-primary-900/20 dark:text-primary-200">
        List preferred courses — we match scholarships that support any of them.
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div className="sm:col-span-2">
          <label htmlFor="pb-field_of_study_broad" className={labelClass}>
            Field of study (broad)
          </label>
          <select
            id="pb-field_of_study_broad"
            value={state.field_of_study_broad}
            onChange={(e) => onChange("field_of_study_broad", e.target.value)}
            className={inputClass}
          >
            <option value="">Select</option>
            <optgroup label="STEM (Science, Technology, Engineering, Math)">
              <option value="STEM">STEM</option>
              <option value="Engineering">Engineering</option>
              <option value="IT">IT / Computer Science</option>
              <option value="Science">Natural Sciences</option>
              <option value="Mathematics">Mathematics / Statistics</option>
            </optgroup>
            <optgroup label="Other fields">
              <option value="Medical">Medical / Health Sciences</option>
              <option value="Business">Business / Accountancy</option>
              <option value="Education">Education</option>
              <option value="Agriculture">Agriculture / Forestry</option>
              <option value="Arts">Arts / Humanities</option>
            </optgroup>
          </select>
        </div>
        <div className="sm:col-span-2">
          <label htmlFor="pb-field_of_study_specific" className={labelClass}>
            Field of study (specific)
          </label>
          <input
            id="pb-field_of_study_specific"
            type="text"
            value={state.field_of_study_specific}
            onChange={(e) => onChange("field_of_study_specific", e.target.value)}
            className={inputClass}
            placeholder="e.g. BS Computer Science"
          />
        </div>
        <div className="sm:col-span-2">
          <span className={labelClass}>Preferred courses (up to 3)</span>
          <p className="mt-0.5 text-xs text-slate-500 dark:text-slate-400">
            Quick tags from our taxonomy: {NEEDS_CATEGORIES[0].tags.slice(0, 5).join(", ")}…
          </p>
          <div className="mt-2 space-y-2">
            <AutocompleteInput
              id="pb-preferred_course_1"
              name="preferred_course_1"
              value={state.preferred_course_1}
              onChange={(name, value) => onChange(name as keyof ProfileBuilderState, value)}
              endpoint="/api/v1/suggestions/courses"
              placeholder="Course 1 (e.g. BS Computer Science)"
              className={inputClass}
            />
            <AutocompleteInput
              id="pb-preferred_course_2"
              name="preferred_course_2"
              value={state.preferred_course_2}
              onChange={(name, value) => onChange(name as keyof ProfileBuilderState, value)}
              endpoint="/api/v1/suggestions/courses"
              placeholder="Course 2 (optional)"
              className={inputClass}
            />
            <AutocompleteInput
              id="pb-preferred_course_3"
              name="preferred_course_3"
              value={state.preferred_course_3}
              onChange={(name, value) => onChange(name as keyof ProfileBuilderState, value)}
              endpoint="/api/v1/suggestions/courses"
              placeholder="Course 3 (optional)"
              className={inputClass}
            />
          </div>
        </div>
        <div className="sm:col-span-2">
          <label htmlFor="pb-extracurriculars" className={labelClass}>
            Extracurriculars (comma-separated)
          </label>
          <input
            id="pb-extracurriculars"
            type="text"
            value={state.extracurriculars}
            onChange={(e) => onChange("extracurriculars", e.target.value)}
            className={inputClass}
            placeholder="e.g. Student Council, Science Club"
          />
        </div>
        <div className="sm:col-span-2">
          <label htmlFor="pb-awards" className={labelClass}>
            Awards (comma-separated)
          </label>
          <input
            id="pb-awards"
            type="text"
            value={state.awards}
            onChange={(e) => onChange("awards", e.target.value)}
            className={inputClass}
            placeholder="e.g. National Honor Society"
          />
        </div>
      </div>

      <div className="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-700 dark:border-slate-600 dark:bg-slate-800/50 dark:text-slate-300">
        Add a project or competition? Include it in awards or extracurriculars — it strengthens your profile.
      </div>
    </div>
  );
}
