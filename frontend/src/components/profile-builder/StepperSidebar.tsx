import { memo, useMemo } from "react";
import {
  PROFILE_BUILDER_STEPS,
  type ProfileBuilderState,
  computeOverallCompletion,
  computeStepCompletion,
} from "./profileBuilderState";

export interface StepperSidebarProps {
  currentStep: number;
  onStepClick: (step: number) => void;
  state: ProfileBuilderState;
}

function StepperSidebarInner({ currentStep, onStepClick, state }: StepperSidebarProps) {
  const overall = useMemo(() => computeOverallCompletion(state), [state]);
  const activeStep = PROFILE_BUILDER_STEPS.find((s) => s.id === currentStep);

  return (
    <div className="space-y-4">
      <div>
        <div className="mb-1 flex items-center justify-between text-xs font-medium text-slate-600 dark:text-slate-400">
          <span>Match quality</span>
          <span>{overall}%</span>
        </div>
        <div className="h-2 w-full overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700">
          <div
            className="h-full rounded-full bg-primary-600 transition-[width] duration-base ease-out-custom"
            style={{ width: `${overall}%` }}
          />
        </div>
      </div>

      {activeStep ? (
        <p className="rounded-lg border border-primary-200 bg-primary-50 px-3 py-2 text-xs text-primary-800 dark:border-primary-800 dark:bg-primary-900/20 dark:text-primary-200">
          {activeStep.unlockHint}
        </p>
      ) : null}

      <div className="flex gap-2 overflow-x-auto pb-1 lg:hidden" role="tablist" aria-label="Profile steps">
        {PROFILE_BUILDER_STEPS.map((s) => {
          const { filled, total } = computeStepCompletion(state, s.id);
          const done = total > 0 ? filled === total : false;
          const active = currentStep === s.id;
          return (
            <button
              key={s.id}
              type="button"
              role="tab"
              aria-selected={active}
              aria-current={active ? "step" : undefined}
              onClick={() => onStepClick(s.id)}
              className={[
                "shrink-0 rounded-full px-3 py-1.5 text-xs font-medium transition",
                active
                  ? "bg-primary-600 text-white shadow"
                  : done
                    ? "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-200"
                    : "bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-200",
              ].join(" ")}
            >
              {s.shortLabel}
            </button>
          );
        })}
      </div>

      <nav className="hidden space-y-2 lg:block" aria-label="Profile steps">
        {PROFILE_BUILDER_STEPS.map((s) => {
          const { filled, total } = computeStepCompletion(state, s.id);
          const done = total > 0 ? filled === total : false;
          const active = currentStep === s.id;
          return (
            <button
              key={s.id}
              type="button"
              aria-current={active ? "step" : undefined}
              onClick={() => onStepClick(s.id)}
              className={[
                "flex w-full items-center gap-3 rounded-xl border px-3 py-3 text-left transition",
                active
                  ? "border-primary-500 bg-primary-50 shadow-sm dark:border-primary-600 dark:bg-primary-900/25"
                  : "border-slate-200 bg-white hover:border-slate-300 dark:border-slate-700 dark:bg-slate-800/80 dark:hover:border-slate-600",
              ].join(" ")}
            >
              <span
                className={[
                  "flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-sm font-semibold",
                  done && !active
                    ? "bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300"
                    : active
                      ? "bg-primary-600 text-white"
                      : "bg-slate-100 text-slate-500 dark:bg-slate-700 dark:text-slate-400",
                ].join(" ")}
              >
                {done && !active ? (
                  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden>
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                ) : (
                  s.id
                )}
              </span>
              <span className="min-w-0 flex-1">
                <span className="block text-sm font-medium text-slate-900 dark:text-slate-100">{s.label}</span>
                <span className="text-xs text-slate-600 dark:text-slate-400">
                  {total > 0 ? `${filled}/${total} required` : "Optional — improves matches"}
                </span>
              </span>
            </button>
          );
        })}
      </nav>
    </div>
  );
}

export const StepperSidebar = memo(StepperSidebarInner);
