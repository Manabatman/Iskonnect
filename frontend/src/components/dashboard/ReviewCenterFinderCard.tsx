import { useMemo, useState } from "react";
import { buildGoogleAiModeSearchUrl } from "../../utils/googleAiModeSearch";

function MapPinIcon({ className }: { className?: string }) {
  return (
    <svg className={className} xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z" />
      <circle cx="12" cy="10" r="3" />
    </svg>
  );
}

function SearchIcon({ className }: { className?: string }) {
  return (
    <svg className={className} xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <circle cx="11" cy="11" r="8" />
      <path d="m21 21-4.3-4.3" />
    </svg>
  );
}

type ReviewCenterFinderCardProps = {
  defaultLocation?: string;
  className?: string;
};

const EXAM_TYPES = [
  "UPCAT",
  "DCAT",
  "ACET",
  "NMAT",
  "LET",
  "Civil Service",
  "PRC",
  "LAW",
  "Med School",
] as const;

const QUICK_TIPS = [
  "Check passing rates and recent student feedback before enrolling.",
  "Compare fees — typical range is ₱5k–₱25k depending on program length.",
  "Ask about schedule options: weekend, daily, or online/hybrid.",
  "Verify accreditation, materials included, and mock exam frequency.",
];

/** Rich query for Google AI Mode (udm=50) so answers cover fees, schedules, reviews, etc. */
function buildReviewCenterAiModeQuery(location: string, examFocus?: string | null): string {
  const loc = location.trim() || "Philippines";
  const exam = examFocus?.trim();
  if (exam) {
    return (
      `${exam} review center near ${loc} Philippines price range tuition fee passing rate ` +
      `schedule options online or face to face teaching style and student reviews`
    );
  }
  return (
    `best review centers for college entrance exams near ${loc} Philippines comparing fees ` +
    `schedule passing rates and student reviews`
  );
}

export function ReviewCenterFinderCard({ defaultLocation, className }: ReviewCenterFinderCardProps) {
  const [location, setLocation] = useState(defaultLocation ?? "");
  const [selectedExam, setSelectedExam] = useState<string | null>(null);

  const googleHref = useMemo(
    () => buildGoogleAiModeSearchUrl(buildReviewCenterAiModeQuery(location, selectedExam)),
    [location, selectedExam],
  );

  return (
    <div
      className={[
        "flex h-full min-h-0 flex-col rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800",
        className,
      ]
        .filter(Boolean)
        .join(" ")}
    >
      <div className="mb-4 flex items-start gap-3">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-200">
          <MapPinIcon className="h-5 w-5" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Review Center Finder</h3>
          <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
            Find nearby review centers in Google&apos;s AI Mode — synthesized answers with fees,
            schedules, and reviews. Pick an exam type, then open in a new tab.
          </p>
        </div>
      </div>

      <div className="space-y-3">
        <label className="block text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
          City / region
        </label>
        <div className="flex flex-col gap-2 sm:flex-row">
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="e.g., Quezon City, Cebu, Davao"
            className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 shadow-inner focus:border-sky-400 focus:outline-none focus:ring-2 focus:ring-sky-200 dark:border-slate-600 dark:bg-slate-900 dark:text-slate-100 dark:focus:border-sky-500 dark:focus:ring-sky-800"
          />
          <a
            href={googleHref}
            target="_blank"
            rel="noreferrer"
            className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-sky-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-sky-700 sm:w-auto sm:min-w-[200px]"
          >
            <SearchIcon className="h-4 w-4" />
            Open in Google AI Mode
          </a>
        </div>
        <p className="text-xs text-slate-500 dark:text-slate-400">
          Opens Google AI Mode in a new tab. We don&apos;t track your searches.
        </p>
      </div>

      <div className="mt-5">
        <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
          Common exam types
        </p>
        <div className="flex flex-wrap gap-2">
          {EXAM_TYPES.map((exam) => {
            const active = selectedExam === exam;
            return (
              <button
                key={exam}
                type="button"
                onClick={() => setSelectedExam(active ? null : exam)}
                className={`rounded-full border px-3 py-1 text-xs font-semibold transition ${
                  active
                    ? "border-sky-600 bg-sky-50 text-sky-800 dark:border-sky-500 dark:bg-sky-950/50 dark:text-sky-200"
                    : "border-slate-200 bg-slate-50 text-slate-700 hover:border-slate-300 dark:border-slate-600 dark:bg-slate-700 dark:text-slate-200 dark:hover:border-slate-500"
                }`}
              >
                {exam}
              </button>
            );
          })}
        </div>
        <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">
          Your query includes fees, passing rates, online vs face-to-face, and reviews for better AI
          answers.
        </p>
      </div>

      <div className="mt-auto rounded-xl border border-slate-100 bg-slate-50 p-4 dark:border-slate-600 dark:bg-slate-900/80">
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-600 dark:text-slate-300">Quick tips</p>
        <ul className="mt-2 list-disc space-y-1 pl-4 text-sm text-slate-800 dark:text-slate-200">
          {QUICK_TIPS.map((tip) => (
            <li key={tip}>{tip}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
