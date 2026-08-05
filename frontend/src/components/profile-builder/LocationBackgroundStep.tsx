import { INCOME_BRACKETS } from "../../constants/needsCategories";
import { PHILIPPINE_REGIONS } from "../../constants/regions";
import { AutocompleteInput } from "../AutocompleteInput";
import type { ProfileBuilderState } from "./profileBuilderState";
import type { StepProps } from "./PersonalInfoStep";
import { inputClass, labelClass, fieldHintClass } from "./profileBuilderConstants";

export function LocationBackgroundStep({ state, onChange }: StepProps) {
  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Location and Background</h2>
        <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
          Regional programs and income-based aid use this information.
        </p>
      </div>

      <div className="rounded-lg border border-primary-200 bg-primary-50 px-3 py-2 text-sm text-primary-800 dark:border-primary-800 dark:bg-primary-900/20 dark:text-primary-200">
        Many scholarships are region-specific — pick the region where you currently reside.
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label htmlFor="pb-region" className={labelClass}>
            Region
          </label>
          <p className={fieldHintClass}>Where you currently live — many programs are region-locked.</p>
          <select
            id="pb-region"
            value={state.region}
            onChange={(e) => onChange("region", e.target.value)}
            className={inputClass}
          >
            <option value="">Select your region</option>
            {PHILIPPINE_REGIONS.map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))}
          </select>
        </div>
        <div>
          <AutocompleteInput
            id="pb-province"
            name="province"
            label="Province"
            value={state.province}
            onChange={(name, value) => onChange(name as keyof ProfileBuilderState, value)}
            endpoint="/api/v1/suggestions/provinces"
            extraParams={state.region ? { region: state.region } : {}}
            placeholder="e.g. Metro Manila"
            className={inputClass}
          />
        </div>
        <div>
          <label htmlFor="pb-city_municipality" className={labelClass}>
            City / Municipality
          </label>
          <input
            id="pb-city_municipality"
            type="text"
            value={state.city_municipality}
            onChange={(e) => onChange("city_municipality", e.target.value)}
            className={inputClass}
            placeholder="e.g. Quezon City"
          />
        </div>
        <div>
          <label htmlFor="pb-barangay" className={labelClass}>
            Barangay
          </label>
          <input
            id="pb-barangay"
            type="text"
            value={state.barangay}
            onChange={(e) => onChange("barangay", e.target.value)}
            className={inputClass}
            placeholder="Optional"
          />
        </div>
        <div>
          <label htmlFor="pb-household_income_annual" className={labelClass}>
            Household income (PHP/year)
          </label>
          <p className={fieldHintClass}>Annual family income — used for need-based income ceilings.</p>
          <input
            id="pb-household_income_annual"
            type="number"
            min={0}
            value={state.household_income_annual}
            onChange={(e) => onChange("household_income_annual", e.target.value)}
            className={inputClass}
            placeholder="e.g. 180000"
          />
        </div>
        <div>
          <label htmlFor="pb-income_bracket" className={labelClass}>
            Income bracket (if unsure)
          </label>
          <select
            id="pb-income_bracket"
            value={state.income_bracket}
            onChange={(e) => onChange("income_bracket", e.target.value)}
            className={inputClass}
          >
            <option value="">Select</option>
            {INCOME_BRACKETS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>
        <div className="sm:col-span-2">
          <label htmlFor="pb-parent_occupation" className={labelClass}>
            Parent occupation (optional)
          </label>
          <input
            id="pb-parent_occupation"
            type="text"
            value={state.parent_occupation}
            onChange={(e) => onChange("parent_occupation", e.target.value)}
            className={inputClass}
            placeholder="e.g. GSIS member, OFW"
          />
        </div>
      </div>
    </div>
  );
}
