import { BookmarkButton } from "../BookmarkButton";
import { formatDateMedium } from "../../utils/formatDate";
import { trackOutboundClick } from "../../utils/trackOutboundClick";

interface ScholarshipDetailStickyBarProps {
  scholarshipId: number;
  title: string;
  link: string | null;
  lastVerifiedAt?: string | null;
}

/** Mobile sticky apply bar with save + freshness at the decision point (Wave 5 / M7). */
export function ScholarshipDetailStickyBar({
  scholarshipId,
  title,
  link,
  lastVerifiedAt,
}: ScholarshipDetailStickyBarProps) {
  const hasLink = Boolean(link?.trim().startsWith("http"));
  const verifiedLabel = lastVerifiedAt ? `Last verified ${formatDateMedium(lastVerifiedAt)}` : null;

  return (
    <div
      className="fixed inset-x-0 bottom-0 z-40 border-t border-slate-200 bg-white/95 px-4 py-3 shadow-[0_-4px_24px_rgba(15,23,42,0.08)] backdrop-blur-sm dark:border-slate-700 dark:bg-slate-900/95 md:hidden"
      style={{ paddingBottom: "max(0.75rem, env(safe-area-inset-bottom))" }}
      role="region"
      aria-label="Apply actions"
    >
      {verifiedLabel ? (
        <p className="mb-2 text-center text-xs text-slate-500 dark:text-slate-400">{verifiedLabel}</p>
      ) : null}
      <div className="flex items-center gap-2">
        <BookmarkButton scholarshipId={scholarshipId} variant="labeled" className="shrink-0" />
        {hasLink ? (
          <a
            href={link!}
            target="_blank"
            rel="noreferrer"
            onClick={() =>
              trackOutboundClick({
                scholarshipId,
                surface: "detail_sticky_bar",
                linkKind: "apply_official",
              })
            }
            className="focus-visible-ring min-h-[44px] flex-1 rounded-xl bg-primary-600 px-4 py-3 text-center text-sm font-semibold text-white shadow-md transition hover:bg-primary-700"
          >
            Apply on official site
          </a>
        ) : (
          <p className="flex-1 text-center text-xs text-slate-500 dark:text-slate-400">
            Official link unavailable for {title}
          </p>
        )}
      </div>
    </div>
  );
}
