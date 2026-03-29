import { type ReactNode } from "react";

export interface SplitLayoutProps {
  /** Left pane: scrollable list (e.g. scholarship list) */
  listPane: ReactNode;
  /** Right pane: detail / preview (sticky on desktop) */
  detailPane: ReactNode;
  /** Tailwind width class for the list column on large screens (default: `lg:w-[min(420px,40%)]`) */
  listWidthClassName?: string;
}

/**
 * Two-panel layout: list + detail. Desktop: side-by-side; mobile: stacked (list first).
 */
export function SplitLayout({
  listPane,
  detailPane,
  listWidthClassName = "lg:w-[min(420px,40%)]",
}: SplitLayoutProps) {
  return (
    <div className="flex min-h-[min(70vh,640px)] flex-col gap-4 lg:flex-row lg:items-start lg:gap-6">
      <div
        className={[
          "max-h-[min(50vh,480px)] lg:max-h-[calc(100vh-8rem)] lg:min-h-0",
          "shrink-0 overflow-y-auto rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-700 dark:bg-slate-800",
          listWidthClassName,
        ].join(" ")}
      >
        {listPane}
      </div>
      <div className="min-h-[min(40vh,320px)] min-w-0 flex-1 lg:sticky lg:top-16 lg:max-h-[calc(100vh-8rem)] lg:overflow-y-auto">
        <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-700 dark:bg-slate-800">
          {detailPane}
        </div>
      </div>
    </div>
  );
}
