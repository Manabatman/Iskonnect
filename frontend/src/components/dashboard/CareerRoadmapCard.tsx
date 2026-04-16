import { useEffect, useMemo, useState } from "react";
import { EDUCATION_LEVELS } from "../../constants/profileOptions";
import { buildGoogleAiModeSearchUrl } from "../../utils/googleAiModeSearch";

function CompassIcon({ className }: { className?: string }) {
  return (
    <svg className={className} xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <circle cx="12" cy="12" r="10" />
      <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76" />
    </svg>
  );
}

function SparklesIcon({ className }: { className?: string }) {
  return (
    <svg className={className} xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z" />
    </svg>
  );
}

type CareerRoadmapCardProps = {
  /** Pre-fill from profile: education_level (same DB field as "target level" in UI). */
  defaultEducationLevel?: string;
  className?: string;
};

const ROADMAP_TIPS = [
  "Try both a job title (e.g. “civil engineer”) and a field (e.g. “renewable energy”) to compare AI summaries.",
  "Salary figures in AI answers are estimates — verify with Payscale, JobStreet, or industry reports.",
  "Use your target education level so the roadmap matches scholarships you’re aiming for.",
  "Bookmark useful links from the AI answer into your Applications or notes.",
];

/**
 * Long-form query so Google AI Mode returns a rich career overview (PH context).
 */
export function buildCareerRoadmapQuery(career: string, educationLevel: string): string {
  const job = career.trim() || "undecided career path";
  const level = educationLevel.trim() || "a Filipino student";
  return (
    `career roadmap for ${job} in the Philippines for ${level} including realistic job roles, ` +
    `day-to-day tasks, required technical and soft skills, entry-level requirements, ` +
    `salary range in PHP, career progression from entry to senior, common struggles in the field, ` +
    `and recommended courses or certifications`
  );
}

export function CareerRoadmapCard({ defaultEducationLevel, className }: CareerRoadmapCardProps) {
  const [careerInterest, setCareerInterest] = useState("");
  const [educationLevel, setEducationLevel] = useState(defaultEducationLevel ?? "");

  useEffect(() => {
    if (defaultEducationLevel) setEducationLevel(defaultEducationLevel);
  }, [defaultEducationLevel]);

  const aiModeHref = useMemo(() => {
    const q = buildCareerRoadmapQuery(careerInterest, educationLevel);
    return buildGoogleAiModeSearchUrl(q);
  }, [careerInterest, educationLevel]);

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
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-violet-100 text-violet-800 dark:bg-violet-950/50 dark:text-violet-200">
          <CompassIcon className="h-5 w-5" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Career Roadmap</h3>
          <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
            Explore careers in Google&apos;s AI Mode — one synthesized answer with roles, skills, salaries
            (Philippines), and next steps. Opens in a new tab.
          </p>
        </div>
      </div>

      <div className="space-y-3">
        <label htmlFor="crm-career" className="block text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
          Career or field you&apos;re curious about
        </label>
        <input
          id="crm-career"
          type="text"
          value={careerInterest}
          onChange={(e) => setCareerInterest(e.target.value)}
          placeholder="e.g. software engineer, nurse, teacher, undecided"
          className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 shadow-inner focus:border-violet-400 focus:outline-none focus:ring-2 focus:ring-violet-200 dark:border-slate-600 dark:bg-slate-900 dark:text-slate-100 dark:focus:border-violet-500 dark:focus:ring-violet-800"
        />

        <label htmlFor="crm-edu" className="block text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
          Your target education level (for scholarship context)
        </label>
        <select
          id="crm-edu"
          value={educationLevel}
          onChange={(e) => setEducationLevel(e.target.value)}
          className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 shadow-inner focus:border-violet-400 focus:outline-none focus:ring-2 focus:ring-violet-200 dark:border-slate-600 dark:bg-slate-900 dark:text-slate-100 dark:focus:border-violet-500 dark:focus:ring-violet-800"
        >
          {EDUCATION_LEVELS.map((opt) => (
            <option key={opt.value || "empty"} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>

        <a
          href={aiModeHref}
          target="_blank"
          rel="noreferrer"
          className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-violet-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-violet-700"
        >
          <SparklesIcon className="h-4 w-4" />
          Explore with AI
        </a>
        <p className="text-xs text-slate-500 dark:text-slate-400">
          Opens Google AI Mode in a new tab. We don&apos;t track your searches.
        </p>
      </div>

      <div className="mt-auto rounded-xl border border-slate-100 bg-slate-50 p-4 dark:border-slate-600 dark:bg-slate-900/80">
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-600 dark:text-slate-300">Quick tips</p>
        <ul className="mt-2 list-disc space-y-1 pl-4 text-sm text-slate-800 dark:text-slate-200">
          {ROADMAP_TIPS.map((tip) => (
            <li key={tip}>{tip}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
