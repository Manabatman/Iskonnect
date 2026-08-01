import { Link } from "react-router-dom";
import type { FieldEvidence } from "../types";
import { formatDateMedium } from "../utils/formatDate";
import { trackOutboundClick } from "../utils/trackOutboundClick";

const FIELD_LABELS: Record<string, string> = {
  application_deadline: "Application deadline",
  application_open_date: "Application open date",
  max_income_threshold: "Income ceiling",
  min_gwa_normalized: "Minimum GWA",
  required_documents: "Required documents",
  benefit_total_value: "Benefit value",
  link: "Official link",
};

function fieldLabel(key: string): string {
  return FIELD_LABELS[key] ?? key.replace(/_/g, " ");
}

function confidenceTone(badge?: string | null): string {
  switch (badge) {
    case "verified":
      return "bg-emerald-100 text-emerald-900 dark:bg-emerald-900/40 dark:text-emerald-100";
    case "partially_verified":
      return "bg-amber-100 text-amber-900 dark:bg-amber-900/40 dark:text-amber-100";
    default:
      return "bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-200";
  }
}

export interface TrustCardProps {
  scholarshipId?: number;
  fieldEvidence?: FieldEvidence[] | null;
  nextReviewDate?: string | null;
  verificationBadge?: string | null;
  verificationBadgeLabel?: string | null;
  completenessLabel?: string | null;
  lastReviewedLabel?: string | null;
  verificationSourceLabel?: string | null;
  className?: string;
}

export function TrustCard({
  scholarshipId,
  fieldEvidence,
  nextReviewDate,
  verificationBadge,
  verificationBadgeLabel,
  completenessLabel,
  lastReviewedLabel,
  verificationSourceLabel,
  className = "",
}: TrustCardProps) {
  const evidence = fieldEvidence ?? [];
  const hasContent =
    evidence.length > 0 ||
    nextReviewDate ||
    verificationBadgeLabel ||
    completenessLabel ||
    lastReviewedLabel;

  if (!hasContent) return null;

  const confidenceReason =
    completenessLabel ||
    lastReviewedLabel ||
    (verificationSourceLabel ? `Source: ${verificationSourceLabel}` : null);

  return (
    <section
      className={`rounded-xl border border-slate-200 bg-slate-50/80 p-5 dark:border-slate-600 dark:bg-slate-900/40 ${className}`}
      aria-labelledby="trust-card-heading"
    >
      <h2 id="trust-card-heading" className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
        Data trust &amp; sources
      </h2>

      <div className="mt-3 flex flex-wrap items-center gap-2">
        {verificationBadgeLabel ? (
          <span className={`rounded-full px-2.5 py-0.5 text-xs font-semibold ${confidenceTone(verificationBadge)}`}>
            {verificationBadgeLabel}
          </span>
        ) : null}
        {confidenceReason ? (
          <span className="text-xs text-slate-600 dark:text-slate-400">{confidenceReason}</span>
        ) : null}
      </div>

      {nextReviewDate ? (
        <p className="mt-2 text-sm text-slate-700 dark:text-slate-300">
          Next scheduled review: {formatDateMedium(nextReviewDate)}
        </p>
      ) : null}

      {evidence.length > 0 ? (
        <div className="mt-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
            Field evidence
          </p>
          <ul className="mt-2 space-y-3">
            {evidence.map((row) => (
              <li
                key={row.id}
                className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm dark:border-slate-600 dark:bg-slate-800"
              >
                <p className="font-medium text-slate-900 dark:text-slate-100">{fieldLabel(row.field_key)}</p>
                {row.value_snapshot ? (
                  <p className="mt-0.5 text-slate-600 dark:text-slate-400">{row.value_snapshot}</p>
                ) : null}
                {row.evidence_snippet ? (
                  <p className="mt-1 text-xs italic text-slate-500 dark:text-slate-400">&ldquo;{row.evidence_snippet}&rdquo;</p>
                ) : null}
                <div className="mt-1 flex flex-wrap gap-x-3 gap-y-1 text-xs text-slate-500 dark:text-slate-400">
                  {row.source_url ? (
                    <a
                      href={row.source_url}
                      target="_blank"
                      rel="noreferrer"
                      onClick={() => {
                        if (scholarshipId != null) {
                          trackOutboundClick({
                            scholarshipId,
                            surface: "trust_source",
                            linkKind: "view_source",
                          });
                        }
                      }}
                      className="font-medium text-primary-600 hover:underline dark:text-primary-400"
                    >
                      View source
                    </a>
                  ) : null}
                  {row.retrieved_at ? <span>Retrieved {formatDateMedium(row.retrieved_at)}</span> : null}
                </div>
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      <p className="mt-4 text-xs text-slate-500 dark:text-slate-400">
        We cite official sources where available.{" "}
        <Link to="/how-we-verify" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
          How we verify
        </Link>
      </p>
    </section>
  );
}
