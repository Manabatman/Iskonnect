import * as Dialog from "@radix-ui/react-dialog";
import { X } from "lucide-react";
import { OpportunityJourneyTimeline } from "./OpportunityJourneyTimeline";

export interface OpportunityRoadmapDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function OpportunityRoadmapDialog({ open, onOpenChange }: OpportunityRoadmapDialogProps) {
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm data-[state=open]:animate-overlayFade data-[state=closed]:animate-overlayFadeOut" />
        <Dialog.Content
          className="glass fixed left-1/2 top-1/2 z-50 flex max-h-[85vh] w-[min(100%-2rem,42rem)] -translate-x-1/2 -translate-y-1/2 flex-col overflow-hidden rounded-2xl border border-slate-200/80 shadow-xl focus:outline-none dark:border-slate-700/80"
          aria-describedby="roadmap-dialog-desc"
        >
          <div className="border-b border-slate-200/80 px-6 py-4 dark:border-slate-700/80">
            <div className="flex items-start justify-between gap-3">
              <div>
                <Dialog.Title className="text-lg font-semibold text-slate-900 dark:text-slate-100">
                  Your opportunity journey
                </Dialog.Title>
                <Dialog.Description id="roadmap-dialog-desc" className="mt-1 text-sm text-slate-600 dark:text-slate-400">
                  ISKONNECT is building one place for every student opportunity, starting with scholarships.
                </Dialog.Description>
              </div>
              <Dialog.Close
                className="focus-visible-ring rounded-lg p-1 text-slate-500 hover:bg-slate-100 hover:text-slate-800 dark:hover:bg-slate-800 dark:hover:text-slate-200"
                aria-label="Close"
              >
                <X className="size-5" aria-hidden />
              </Dialog.Close>
            </div>
          </div>
          <div className="flex-1 overflow-y-auto px-6 py-4">
            <OpportunityJourneyTimeline linkItems compact />
          </div>
          <div className="border-t border-slate-200/80 px-6 py-4 dark:border-slate-700/80">
            <Dialog.Close className="inline-flex min-h-11 items-center rounded-xl bg-primary-600 px-4 py-2 text-sm font-semibold text-white hover:bg-primary-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500">
              Back to search
            </Dialog.Close>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
