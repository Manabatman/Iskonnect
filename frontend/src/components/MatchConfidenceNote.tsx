import { Link } from "react-router-dom";
import { cn } from "@/lib/utils";

/** Two-sentence non-guarantee copy — match-explanation surfaces only (TRUST-04 / D-08). */
export const MATCH_CONFIDENCE_EXPLANATION = [
  "Scholarship providers make the final selection.",
  "Meeting eligibility does not guarantee acceptance.",
] as const;

interface MatchConfidenceNoteProps {
  className?: string;
  showMethodologyLink?: boolean;
}

export function MatchConfidenceNote({
  className,
  showMethodologyLink = true,
}: MatchConfidenceNoteProps) {
  return (
    <div
      className={cn("space-y-1 text-sm leading-relaxed text-slate-600 dark:text-slate-400", className)}
      role="note"
    >
      <p>{MATCH_CONFIDENCE_EXPLANATION[0]}</p>
      <p>{MATCH_CONFIDENCE_EXPLANATION[1]}</p>
      {showMethodologyLink ? (
        <p className="pt-1">
          <Link
            to="/how-matching-works"
            className="font-medium text-primary-600 underline-offset-2 hover:underline dark:text-primary-400"
          >
            Learn how matching works
          </Link>
        </p>
      ) : null}
    </div>
  );
}
