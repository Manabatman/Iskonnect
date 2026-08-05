import { useId, useState, type ReactNode } from "react";
import { ChevronDown } from "lucide-react";
import type { StatusGuideEntry } from "../utils/scholarshipStatus";
import { cn } from "@/lib/utils";

interface StatusGuideAccordionProps {
  items: Array<{
    id: string;
    label: string;
    shortDescription: string;
    entry: StatusGuideEntry;
    icon: ReactNode;
    badge?: ReactNode;
  }>;
}

export function StatusGuideAccordion({ items }: StatusGuideAccordionProps) {
  const baseId = useId();
  const [openId, setOpenId] = useState<string | null>(null);

  return (
    <div className="space-y-2">
      {items.map(({ id, label, shortDescription, entry, icon, badge }) => {
        const isOpen = openId === id;
        const panelId = `${baseId}-${id}-panel`;
        const buttonId = `${baseId}-${id}-button`;
        return (
          <article
            key={id}
            id={id}
            className="scroll-mt-24 rounded-xl border border-slate-200 bg-white dark:border-slate-700 dark:bg-slate-800/80"
          >
            <button
              id={buttonId}
              type="button"
              className="flex w-full items-start gap-3 px-4 py-4 text-left focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-inset"
              aria-expanded={isOpen}
              aria-controls={panelId}
              onClick={() => setOpenId(isOpen ? null : id)}
            >
              <span className="mt-0.5 shrink-0 text-primary-600 dark:text-primary-400" aria-hidden>
                {icon}
              </span>
              <span className="min-w-0 flex-1">
                <span className="flex flex-wrap items-center gap-2">
                  <span className="font-semibold text-slate-900 dark:text-slate-100">{label}</span>
                  {badge}
                </span>
                <span className="mt-1 block text-sm leading-relaxed text-slate-600 dark:text-slate-400">
                  {shortDescription}
                </span>
              </span>
              <ChevronDown
                className={cn(
                  "mt-1 h-5 w-5 shrink-0 text-slate-500 transition-transform dark:text-slate-400",
                  isOpen && "rotate-180"
                )}
                aria-hidden
              />
            </button>
            <div
              id={panelId}
              role="region"
              aria-labelledby={buttonId}
              hidden={!isOpen}
              className="border-t border-slate-200 px-4 py-4 dark:border-slate-700"
            >
              <p className="text-sm leading-relaxed text-slate-700 dark:text-slate-300">
                <span className="font-medium text-slate-900 dark:text-slate-100">What to do: </span>
                {entry.whatToDo}
              </p>
            </div>
          </article>
        );
      })}
    </div>
  );
}
