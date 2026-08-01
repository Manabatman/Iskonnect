import { useId, useState, type ReactNode } from "react";
import { GLOSSARY, type GlossaryTermKey } from "../constants/glossary";

type GlossaryTermProps = {
  term: GlossaryTermKey;
  /** Visible label; defaults to the glossary term. */
  children?: ReactNode;
  className?: string;
};

/**
 * Inline term with an accessible definition — button + popover (not title-only).
 */
export function GlossaryTerm({ term, children, className = "" }: GlossaryTermProps) {
  const entry = GLOSSARY[term];
  const tagalog = "tagalog" in entry ? entry.tagalog : undefined;
  const [open, setOpen] = useState(false);
  const definitionId = useId();
  const label = children ?? entry.term;

  return (
    <span className={`relative inline ${className}`}>
      <button
        type="button"
        className="inline border-b border-dotted border-current font-inherit text-inherit underline-offset-2 hover:text-primary-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-1 dark:hover:text-primary-300"
        aria-expanded={open}
        aria-describedby={open ? definitionId : undefined}
        onClick={() => setOpen((v) => !v)}
        onBlur={(e) => {
          if (!e.currentTarget.parentElement?.contains(e.relatedTarget as Node | null)) {
            setOpen(false);
          }
        }}
      >
        {label}
        <span className="sr-only"> — what does {entry.term} mean?</span>
      </button>
      {open ? (
        <span
          id={definitionId}
          role="tooltip"
          className="absolute left-0 top-full z-50 mt-1 block w-[min(18rem,calc(100vw-2rem))] rounded-lg border border-slate-200 bg-white px-3 py-2 text-left text-xs font-normal normal-case tracking-normal text-slate-700 shadow-lg dark:border-slate-600 dark:bg-slate-800 dark:text-slate-200"
        >
          <span className="font-semibold text-slate-900 dark:text-slate-100">{entry.term}: </span>
          {entry.definition}
          {tagalog ? (
            <span className="mt-1 block text-slate-600 dark:text-slate-400">{tagalog}</span>
          ) : null}
        </span>
      ) : null}
    </span>
  );
}
