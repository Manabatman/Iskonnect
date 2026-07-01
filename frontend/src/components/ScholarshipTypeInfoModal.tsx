import * as Dialog from "@radix-ui/react-dialog";
import { getScholarshipTypeGuide } from "../data/scholarshipTypeGuide";

interface ScholarshipTypeInfoModalProps {
  scholarshipType: string | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function ScholarshipTypeInfoModal({
  scholarshipType,
  open,
  onOpenChange,
}: ScholarshipTypeInfoModalProps) {
  const guide = getScholarshipTypeGuide(scholarshipType);
  if (!guide) return null;

  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 z-[100] bg-black/40 backdrop-blur-sm data-[state=open]:animate-overlayFade data-[state=closed]:animate-overlayFadeOut" />
        <Dialog.Content
          className="fixed inset-0 z-[101] flex max-h-full w-full items-center justify-center p-4 outline-none data-[state=open]:animate-matchDialogIn data-[state=closed]:animate-matchDialogOut sm:p-6"
          aria-describedby="scholarship-type-modal-desc"
        >
          <div className="max-h-[85vh] w-full max-w-md overflow-y-auto rounded-2xl border border-slate-200 bg-white p-6 shadow-xl dark:border-slate-700 dark:bg-slate-900">
            <Dialog.Title className="text-lg font-bold text-slate-900 dark:text-slate-100">
              {guide.title}
            </Dialog.Title>
            <Dialog.Description id="scholarship-type-modal-desc" className="mt-3 text-sm leading-relaxed text-slate-700 dark:text-slate-300">
              {guide.summary}
            </Dialog.Description>
            {guide.examples.length > 0 ? (
              <div className="mt-4">
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                  Examples
                </p>
                <ul className="mt-2 list-disc space-y-1.5 pl-5 text-sm text-slate-600 dark:text-slate-400">
                  {guide.examples.map((example) => (
                    <li key={example}>{example}</li>
                  ))}
                </ul>
              </div>
            ) : null}
            <div className="mt-6 flex justify-end">
              <Dialog.Close className="rounded-xl bg-primary-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-primary-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 dark:focus-visible:ring-offset-slate-900">
                Got it
              </Dialog.Close>
            </div>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
