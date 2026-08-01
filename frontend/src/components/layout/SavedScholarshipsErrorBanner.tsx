import { useSavedScholarships } from "../../contexts/SavedScholarshipsContext";

export function SavedScholarshipsErrorBanner() {
  const { error, clearError } = useSavedScholarships();
  if (!error) return null;
  return (
    <div
      role="status"
      className="border-b border-slate-200 bg-slate-100 px-4 py-2 text-sm text-slate-800 dark:border-slate-700 dark:bg-slate-800/80 dark:text-slate-200"
    >
      <div className="mx-auto flex max-w-7xl items-start justify-between gap-3">
        <p className="min-w-0 flex-1">{error}</p>
        <button
          type="button"
          onClick={clearError}
          className="shrink-0 rounded-md border border-slate-300 bg-white px-2 py-1 text-xs font-medium hover:bg-slate-50 dark:border-slate-600 dark:bg-slate-900 dark:hover:bg-slate-700"
        >
          Dismiss
        </button>
      </div>
    </div>
  );
}
