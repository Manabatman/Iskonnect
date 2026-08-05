import { useState } from "react";
import { Link } from "react-router-dom";
import { ChevronDown, ChevronUp } from "lucide-react";
import { formatDateMedium } from "../utils/formatDate";
import { trackOutboundClick } from "../utils/trackOutboundClick";

export type StudentVerificationStatus = "verified" | "needs_review" | "archived";

export interface VerificationStripProps {
  scholarshipId?: number;
  status?: StudentVerificationStatus | string | null;
  label?: string | null;
  message?: string | null;
  lastVerifiedAt?: string | null;
  officialWebsite?: string | null;
  officialWebsiteHost?: string | null;
  verificationSourceLabel?: string | null;
  linkStatus?: string | null;
  className?: string;
}

function statusTone(status: string): string {
  switch (status) {
    case "verified":
      return "bg-emerald-100 text-emerald-900 dark:bg-emerald-900/40 dark:text-emerald-100";
    case "archived":
      return "bg-slate-200 text-slate-700 dark:bg-slate-700 dark:text-slate-200";
    default:
      return "bg-amber-100 text-amber-900 dark:bg-amber-900/40 dark:text-amber-100";
  }
}

export function VerificationStrip({
  scholarshipId,
  status = "needs_review",
  label,
  message,
  lastVerifiedAt,
  officialWebsite,
  officialWebsiteHost,
  verificationSourceLabel,
  linkStatus,
  className = "",
}: VerificationStripProps) {
  const [expanded, setExpanded] = useState(false);
  const resolvedStatus = (status || "needs_review") as string;
  const displayLabel = label || (resolvedStatus === "verified" ? "Verified" : resolvedStatus === "archived" ? "Archived" : "Needs Review");

  return (
    <section
      className={`rounded-xl border border-slate-200 bg-slate-50/80 p-5 dark:border-slate-600 dark:bg-slate-900/40 ${className}`}
      aria-labelledby="verification-strip-heading"
    >
      <h2 id="verification-strip-heading" className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
        Verification
      </h2>

      <div className="mt-3 flex flex-wrap items-center gap-2">
        <span className={`rounded-full px-3 py-0.5 text-xs font-semibold ${statusTone(resolvedStatus)}`}>
          {displayLabel}
        </span>
      </div>

      {message ? (
        <p className="mt-2 text-sm text-slate-700 dark:text-slate-300">{message}</p>
      ) : null}

      {lastVerifiedAt ? (
        <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
          Last verified {formatDateMedium(lastVerifiedAt)}
        </p>
      ) : null}

      {officialWebsite ? (
        <p className="mt-2 text-sm text-slate-700 dark:text-slate-300">
          Official source{" "}
          <a
            href={officialWebsite}
            target="_blank"
            rel="noreferrer"
            onClick={() => {
              if (scholarshipId != null) {
                trackOutboundClick({
                  scholarshipId,
                  surface: "verification_strip",
                  linkKind: "official_website",
                });
              }
            }}
            className="font-medium text-primary-600 hover:underline dark:text-primary-400"
          >
            {officialWebsiteHost || officialWebsite}
          </a>
        </p>
      ) : null}

      <p className="mt-3 text-xs text-slate-500 dark:text-slate-400">
        Always confirm details on the official website before applying.
      </p>

      <button
        type="button"
        onClick={() => setExpanded((v) => !v)}
        className="mt-3 flex items-center gap-1 text-xs font-medium text-primary-600 hover:underline dark:text-primary-400"
        aria-expanded={expanded}
      >
        {expanded ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
        How was this information verified?
      </button>

      {expanded ? (
        <div className="mt-2 space-y-1 border-t border-slate-200 pt-3 text-xs text-slate-600 dark:border-slate-600 dark:text-slate-400">
          {verificationSourceLabel ? <p>Method: {verificationSourceLabel}</p> : null}
          {linkStatus ? <p>Link status: {linkStatus}</p> : null}
          {lastVerifiedAt ? <p>Last verified: {formatDateMedium(lastVerifiedAt)}</p> : null}
          {officialWebsite ? (
            <p>
              Official website:{" "}
              <a href={officialWebsite} target="_blank" rel="noreferrer" className="text-primary-600 hover:underline dark:text-primary-400">
                {officialWebsiteHost || officialWebsite}
              </a>
            </p>
          ) : null}
        </div>
      ) : null}

      <p className="mt-3 text-xs text-slate-500 dark:text-slate-400">
        Information is regularly reviewed against official sources.{" "}
        <Link to="/how-we-verify" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
          How we verify
        </Link>
      </p>
    </section>
  );
}
