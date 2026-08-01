import { Link } from "react-router-dom";
import { cn } from "@/lib/utils";

export const MATCH_CONFIDENCE_COMPACT =
  "ISKONNECT estimate — the provider decides who is accepted.";

export const MATCH_CONFIDENCE_FULL =
  "This score reflects how well your profile fits the listed requirements. It is not a guarantee of funding or acceptance — always verify on the official provider site.";

interface MatchConfidenceNoteProps {
  variant?: "compact" | "full";
  className?: string;
  showMethodologyLink?: boolean;
}

/** Shared non-guarantee copy for match scores and qualification badges (TRUST-04). */
export function MatchConfidenceNote({
  variant = "compact",
  className,
  showMethodologyLink = variant === "full",
}: MatchConfidenceNoteProps) {
  const text = variant === "full" ? MATCH_CONFIDENCE_FULL : MATCH_CONFIDENCE_COMPACT;

  return (
    <p
      className={cn(
        "text-slate-600 dark:text-slate-400",
        variant === "compact" ? "text-[11px] leading-snug" : "text-xs leading-relaxed",
        className
      )}
      role="note"
    >
      {text}{" "}
      {showMethodologyLink ? (
        <Link
          to="/how-matching-works"
          className="font-medium text-primary-600 underline-offset-2 hover:underline dark:text-primary-400"
        >
          How we match
        </Link>
      ) : null}
    </p>
  );
}
