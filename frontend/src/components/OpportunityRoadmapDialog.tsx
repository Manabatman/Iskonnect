import * as Dialog from "@radix-ui/react-dialog";
import { Link } from "react-router-dom";
import { OPPORTUNITY_TYPES } from "../constants/opportunityTypes";

export interface OpportunityRoadmapDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function OpportunityRoadmapDialog({ open, onOpenChange }: OpportunityRoadmapDialogProps) {
  const comingSoon = OPPORTUNITY_TYPES.filter((t) => !t.available);

  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />
        <Dialog.Content
          className="fixed left-1/2 top-1/2 z-50 flex max-h-[85vh] w-[min(100%-2rem,42rem)] -translate-x-1/2 -translate-y-1/2 flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-xl focus:outline-none dark:border-slate-700 dark:bg-slate-900"
          aria-describedby="roadmap-dialog-desc"
        >
          <div className="border-b border-slate-200 px-6 py-4 dark:border-slate-700">
            <Dialog.Title className="text-lg font-semibold text-slate-900 dark:text-slate-100">
              Explore what&apos;s coming
            </Dialog.Title>
            <Dialog.Description id="roadmap-dialog-desc" className="mt-1 text-sm text-slate-600 dark:text-slate-400">
              ISKONNECT is becoming a unified student opportunity platform. Scholarships are fully supported during
              public beta; these types are on the roadmap.
            </Dialog.Description>
          </div>
          <div className="flex-1 overflow-y-auto px-6 py-4">
            <ul className="grid grid-cols-1 gap-3 sm:grid-cols-2">
              {comingSoon.map((t) => (
                <li key={t.slug}>
                  <Link
                    to={`/opportunities/${t.slug}`}
                    onClick={() => onOpenChange(false)}
                    className="group block rounded-xl border border-slate-200 bg-slate-50/80 p-3 transition hover:border-primary-300 hover:bg-primary-50/50 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 dark:border-slate-600 dark:bg-slate-800/60 dark:hover:border-primary-700 dark:hover:bg-primary-950/30"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <span className="text-sm font-semibold text-slate-900 group-hover:text-primary-700 dark:text-slate-100 dark:group-hover:text-primary-300">
                        {t.label}
                      </span>
                      <span className="shrink-0 rounded bg-slate-200 px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-slate-600 dark:bg-slate-700 dark:text-slate-300">
                        Soon
                      </span>
                    </div>
                    <p className="mt-1 text-xs leading-relaxed text-slate-600 dark:text-slate-400">{t.description}</p>
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          <div className="border-t border-slate-200 px-6 py-4 dark:border-slate-700">
            <Dialog.Close className="rounded-lg bg-primary-600 px-4 py-2 text-sm font-semibold text-white hover:bg-primary-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500">
              Back to search
            </Dialog.Close>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
