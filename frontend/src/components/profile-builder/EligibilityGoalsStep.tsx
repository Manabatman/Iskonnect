import { useCallback, useMemo } from "react";
import { EQUITY_GROUPS, NEEDS_CATEGORIES } from "../../constants/needsCategories";
import { NeedsCategoryAccordion } from "../NeedsCategoryAccordion";
import { SelectedChips } from "../SelectedChips";
import type { ProfileBuilderState } from "./profileBuilderState";
import { EQUITY_FLAG_MAP, labelClass } from "./profileBuilderConstants";

export interface EligibilityStepProps {
  state: ProfileBuilderState;
  onChange: (field: keyof ProfileBuilderState, value: string) => void;
}

export function EligibilityGoalsStep({ state, onChange }: EligibilityStepProps) {
  const selectedNeeds = useMemo(
    () =>
      (state.needs ?? "")
        .split(",")
        .map((n) => n.trim())
        .filter(Boolean),
    [state.needs]
  );

  const toggleNeed = useCallback(
    (tag: string) => {
      const next = selectedNeeds.includes(tag)
        ? selectedNeeds.filter((t) => t !== tag)
        : [...selectedNeeds, tag];
      onChange("needs", next.join(", "));
    },
    [selectedNeeds, onChange]
  );

  const toggleEquity = useCallback(
    (flagName: keyof ProfileBuilderState) => {
      const current = state[flagName] === "on";
      onChange(flagName, current ? "" : "on");
    },
    [state, onChange]
  );

  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Eligibility and Goals</h2>
        <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
          Tags and priority groups help us surface the right aid programs.
        </p>
      </div>

      <div className="rounded-lg border border-primary-200 bg-primary-50 px-3 py-2 text-sm text-primary-800 dark:border-primary-800 dark:bg-primary-900/20 dark:text-primary-200">
        Select any categories that describe your situation — you can update these anytime.
      </div>

      <div>
        <label className={labelClass}>Needs / interests</label>
        <div className="mt-2 space-y-3">
          <SelectedChips
            selected={selectedNeeds}
            onRemove={toggleNeed}
            emptyMessage="Expand a category below to select needs"
          />
          <NeedsCategoryAccordion categories={NEEDS_CATEGORIES} selected={selectedNeeds} onToggle={toggleNeed} />
        </div>
      </div>

      <div>
        <span className={labelClass}>Priority groups (RA-based)</span>
        <div className="mt-2 flex flex-wrap gap-2">
          {EQUITY_GROUPS[0].tags.map((tag) => {
            const flagName = (EQUITY_FLAG_MAP[tag.id] ?? tag.id) as keyof ProfileBuilderState;
            const isChecked = state[flagName] === "on";
            return (
              <label
                key={tag.id}
                className="flex cursor-pointer items-center gap-2 rounded-full border border-slate-200 px-3 py-1.5 text-sm hover:bg-slate-50 dark:border-slate-700 dark:hover:bg-slate-700"
              >
                <input
                  type="checkbox"
                  checked={isChecked}
                  onChange={() => toggleEquity(flagName)}
                  className="rounded border-slate-300 text-primary-600 focus:ring-primary-500"
                />
                <span>{tag.label}</span>
              </label>
            );
          })}
        </div>
        <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">
          Select if you belong to any priority group for scholarship matching.
        </p>
      </div>
    </div>
  );
}
