import { useState } from "react";
import { useAuth } from "../contexts/AuthContext";
import { useSavedScholarships } from "../contexts/SavedScholarshipsContext";

interface BookmarkButtonProps {
  scholarshipId: number;
  className?: string;
  onClick?: (e: React.MouseEvent) => void;
  /** icon = compact heart-style control; labeled = Save/Saved text with bookmark icon */
  variant?: "icon" | "labeled";
}

function BookmarkIcon({ filled, className }: { filled: boolean; className?: string }) {
  if (filled) {
    return (
      <svg className={className} fill="currentColor" viewBox="0 0 24 24" aria-hidden>
        <path d="M6 2a2 2 0 00-2 2v18l8-4.5L20 22V4a2 2 0 00-2-2H6z" />
      </svg>
    );
  }
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden>
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M6 2a2 2 0 012-2h8a2 2 0 012 2v18l-8-4.5L6 22V4z"
      />
    </svg>
  );
}

export function BookmarkButton({
  scholarshipId,
  className = "",
  onClick,
  variant = "icon",
}: BookmarkButtonProps) {
  const { user } = useAuth();
  const { isSaved, toggleSave } = useSavedScholarships();
  const [toggling, setToggling] = useState(false);

  const saved = isSaved(scholarshipId);
  const label = saved ? "Saved" : "Save";

  const handleClick = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    onClick?.(e);
    if (!user || toggling) return;
    setToggling(true);
    try {
      await toggleSave(scholarshipId);
    } finally {
      setToggling(false);
    }
  };

  const baseIconClass = variant === "labeled" ? "h-4 w-4 shrink-0" : "h-5 w-5";

  if (!user) {
    if (variant === "labeled") {
      return (
        <button
          type="button"
          onClick={handleClick}
          title="Log in to save"
          className={`inline-flex items-center gap-1.5 rounded-lg border border-slate-300 px-3 py-1.5 text-xs font-semibold text-slate-500 dark:border-slate-600 dark:text-slate-400 ${className}`}
          aria-label="Save scholarship (log in required)"
        >
          <BookmarkIcon filled={false} className={baseIconClass} />
          Save
        </button>
      );
    }
    return (
      <button
        type="button"
        onClick={handleClick}
        title="Log in to save"
        className={`rounded p-1.5 text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700 dark:text-slate-500 ${className}`}
        aria-label="Save scholarship (log in required)"
      >
        <BookmarkIcon filled={false} className={baseIconClass} />
      </button>
    );
  }

  if (variant === "labeled") {
    return (
      <button
        type="button"
        onClick={handleClick}
        disabled={toggling}
        title={saved ? "Remove from saved" : "Save scholarship"}
        className={`inline-flex items-center gap-1.5 rounded-lg border px-3 py-1.5 text-xs font-semibold transition disabled:opacity-50 ${
          saved
            ? "border-primary-300 bg-primary-50 text-primary-800 dark:border-primary-700 dark:bg-primary-950/40 dark:text-primary-200"
            : "border-slate-300 text-slate-700 hover:bg-slate-50 dark:border-slate-600 dark:text-slate-200 dark:hover:bg-slate-800"
        } ${className}`}
        aria-label={saved ? "Remove from saved" : "Save scholarship"}
        aria-pressed={saved}
      >
        <BookmarkIcon filled={saved} className={baseIconClass} />
        {label}
      </button>
    );
  }

  return (
    <button
      type="button"
      onClick={handleClick}
      disabled={toggling}
      title={saved ? "Remove from saved" : "Save scholarship"}
      className={`rounded p-1.5 transition ${
        saved
          ? "text-primary-600 dark:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/30"
          : "text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700 hover:text-slate-600 dark:hover:text-slate-300"
      } disabled:opacity-50 ${className}`}
      aria-label={saved ? "Remove from saved" : "Save scholarship"}
      aria-pressed={saved}
    >
      <BookmarkIcon filled={saved} className={baseIconClass} />
    </button>
  );
}
