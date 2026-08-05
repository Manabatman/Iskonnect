import type { ReactNode } from "react";
import type { ErrorCopyEntry } from "../constants/errorCopy";

type StateMessageProps = {
  copy: ErrorCopyEntry;
  action?: ReactNode;
  className?: string;
};

/** Standard empty/error state — title, why, and next step (CONT-03). */
export function StateMessage({ copy, action, className = "" }: StateMessageProps) {
  return (
    <div className={`rounded-xl border border-slate-200 bg-white p-6 text-center dark:border-slate-700 dark:bg-slate-900 ${className}`}>
      <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">{copy.title}</h2>
      <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">{copy.message}</p>
      {action ? <div className="mt-4">{action}</div> : null}
    </div>
  );
}
