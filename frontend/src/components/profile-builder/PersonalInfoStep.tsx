import type { ProfileBuilderState } from "./profileBuilderState";
import { inputClass, labelClass } from "./profileBuilderConstants";

export interface StepProps {
  state: ProfileBuilderState;
  onChange: (field: keyof ProfileBuilderState, value: string) => void;
}

export function PersonalInfoStep({ state, onChange }: StepProps) {
  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Personal Info</h2>
        <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
          Basic details we use to identify your profile and contact you.
        </p>
      </div>

      <div className="rounded-lg border border-primary-200 bg-primary-50 px-3 py-2 text-sm text-primary-800 dark:border-primary-800 dark:bg-primary-900/20 dark:text-primary-200">
        Add a working email so you do not miss scholarship updates.
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label htmlFor="pb-full_name" className={labelClass}>
            Full name
          </label>
          <input
            id="pb-full_name"
            type="text"
            value={state.full_name}
            onChange={(e) => onChange("full_name", e.target.value)}
            className={inputClass}
            placeholder="e.g. Maria Santos"
            autoComplete="name"
          />
        </div>
        <div>
          <label htmlFor="pb-email" className={labelClass}>
            Email
          </label>
          <input
            id="pb-email"
            type="email"
            value={state.email}
            onChange={(e) => onChange("email", e.target.value)}
            className={inputClass}
            placeholder="maria@example.com"
            autoComplete="email"
          />
        </div>
        <div>
          <label htmlFor="pb-gender" className={labelClass}>
            Gender
          </label>
          <select
            id="pb-gender"
            value={state.gender}
            onChange={(e) => onChange("gender", e.target.value)}
            className={inputClass}
          >
            <option value="">Select</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
        </div>
        <div>
          <label htmlFor="pb-age" className={labelClass}>
            Age
          </label>
          <input
            id="pb-age"
            type="number"
            min={13}
            max={120}
            value={state.age}
            onChange={(e) => onChange("age", e.target.value)}
            className={inputClass}
            placeholder="18"
          />
        </div>
      </div>
    </div>
  );
}
