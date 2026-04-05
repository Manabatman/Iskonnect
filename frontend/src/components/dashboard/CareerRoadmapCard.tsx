import { useCallback, useMemo, useState } from "react";
import { COURSE_CATEGORIES } from "../../data/courseCategories";
import { apiFetch } from "../../api/client";
import { useAuth } from "../../contexts/AuthContext";

function buildCareerQuery(course: string): string {
  return [
    `${course} Philippines curriculum subjects first year to fourth year`,
    "career paths job titles entry level Philippines salary range",
    "typical day at work responsibilities",
    "skills needed in industry not taught in university Philippines",
    "internship portfolio certifications employers want",
    "self assessment questions if unsure about career path",
    "alternative careers related degree downsides honest",
  ].join(" ");
}

type Props = {
  profileEducationLevel?: string;
};

export function CareerRoadmapCard({ profileEducationLevel }: Props) {
  const { authHeaders, user } = useAuth();
  const [openCat, setOpenCat] = useState<string | null>(COURSE_CATEGORIES[0]?.id ?? null);
  const [course, setCourse] = useState(COURSE_CATEGORIES[0]?.courses[0] ?? "BS Computer Science");
  const [aiText, setAiText] = useState<string | null>(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState<string | null>(null);

  const googleHref = useMemo(() => {
    return `https://www.google.com/search?q=${encodeURIComponent(buildCareerQuery(course))}`;
  }, [course]);

  const runAi = useCallback(async () => {
    if (!user) return;
    setAiLoading(true);
    setAiError(null);
    setAiText(null);
    try {
      const res = await apiFetch("/api/v1/ai/career-roadmap", {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({
          course: course.trim(),
          education_level: profileEducationLevel ?? null,
        }),
      });
      const data = await res.json().catch(() => null);
      if (!res.ok) {
        throw new Error((data as { detail?: string })?.detail ?? "AI request failed");
      }
      setAiText((data as { text?: string }).text ?? "");
    } catch (e) {
      setAiError(e instanceof Error ? e.message : "Could not load AI roadmap.");
    } finally {
      setAiLoading(false);
    }
  }, [user, authHeaders, course, profileEducationLevel]);

  return (
    <div className="rounded-2xl border border-violet-200/90 bg-gradient-to-br from-violet-50/90 to-white p-5 shadow-sm dark:border-violet-900/50 dark:from-violet-950/30 dark:to-slate-900/40">
      <div className="flex items-start gap-3">
        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-violet-600 text-white">
          <span className="text-lg" aria-hidden>
            🎓
          </span>
        </div>
        <div>
          <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">Career Roadmap Overview</h3>
          <p className="text-sm text-slate-500 dark:text-slate-400">Explore courses, roles, and expectations</p>
        </div>
      </div>
      <p className="mt-3 text-sm text-slate-700 dark:text-slate-300">
        Pick a course, then generate an AI roadmap (honest, Philippines-focused) or open a targeted Google search.
      </p>
      <div className="mt-4 space-y-2">
        {COURSE_CATEGORIES.map((cat) => {
          const open = openCat === cat.id;
          return (
            <div key={cat.id} className="rounded-xl border border-slate-200 dark:border-slate-600">
              <button
                type="button"
                onClick={() => setOpenCat(open ? null : cat.id)}
                className="flex w-full items-center justify-between px-3 py-2 text-left text-sm font-semibold text-slate-800 dark:text-slate-100"
              >
                {cat.label}
                <span className="text-slate-400">{open ? "▾" : "▸"}</span>
              </button>
              {open ? (
                <div className="border-t border-slate-100 px-2 py-2 dark:border-slate-700">
                  <div className="flex flex-wrap gap-1">
                    {cat.courses.map((c) => (
                      <button
                        key={c}
                        type="button"
                        onClick={() => setCourse(c)}
                        className={[
                          "rounded-lg px-2 py-1 text-xs font-medium transition",
                          c === course
                            ? "bg-violet-600 text-white"
                            : "bg-slate-100 text-slate-700 hover:bg-slate-200 dark:bg-slate-700 dark:text-slate-200",
                        ].join(" ")}
                      >
                        {c}
                      </button>
                    ))}
                  </div>
                </div>
              ) : null}
            </div>
          );
        })}
      </div>
      <p className="mt-3 text-xs text-slate-600 dark:text-slate-400">
        Selected: <strong>{course}</strong>
      </p>
      <div className="mt-3 flex flex-col gap-2 sm:flex-row">
        <button
          type="button"
          disabled={aiLoading || !user}
          onClick={() => void runAi()}
          className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-violet-600 px-4 py-3 text-sm font-bold text-white shadow hover:bg-violet-700 disabled:opacity-50"
        >
          {aiLoading ? "Generating…" : "Generate roadmap (AI)"}
        </button>
        <a
          href={googleHref}
          target="_blank"
          rel="noopener noreferrer"
          className="flex flex-1 items-center justify-center gap-2 rounded-xl border-2 border-violet-400 bg-white px-4 py-3 text-sm font-bold text-violet-900 hover:bg-violet-50 dark:border-violet-700 dark:bg-slate-800 dark:text-violet-100 dark:hover:bg-slate-700"
        >
          Search with Google
        </a>
      </div>
      {!user ? <p className="mt-2 text-xs text-slate-500">Sign in for AI roadmap (or use Google).</p> : null}

      {aiError ? (
        <p className="mt-3 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-800 dark:border-red-800 dark:bg-red-900/20 dark:text-red-200">
          {aiError} Try Google search or configure <code className="rounded bg-red-100 px-1 dark:bg-red-950">OPENAI_API_KEY</code> on the API.
        </p>
      ) : null}

      {aiText ? (
        <div className="mt-4 max-h-96 overflow-y-auto rounded-xl border border-violet-100 bg-white/90 p-3 text-sm text-slate-800 dark:border-violet-900/50 dark:bg-slate-900/60 dark:text-slate-200">
          <p className="whitespace-pre-wrap">{aiText}</p>
        </div>
      ) : null}
    </div>
  );
}
