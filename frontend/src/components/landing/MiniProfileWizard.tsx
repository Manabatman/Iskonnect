import { useCallback, useState } from "react";
import { Link } from "react-router-dom";
import { apiFetch } from "../../api/client";
import type { MatchResult } from "../../types";
import { ScholarshipCardV2 } from "../ScholarshipCardV2";
import { primaryButtonClass } from "./Section";

const EDUCATION_LEVELS = ["Grade 12", "College", "TVET", "Graduate"];
const REGIONS = ["NCR", "Region IV-A - CALABARZON", "Region III - Central Luzon", "Region VII - Central Visayas"];
const FIELDS = ["Engineering", "Education", "Business", "Health", "Agriculture"];

export function MiniProfileWizard() {
  const [educationLevel, setEducationLevel] = useState("College");
  const [region, setRegion] = useState("NCR");
  const [field, setField] = useState("Engineering");
  const [loading, setLoading] = useState(false);
  const [matches, setMatches] = useState<MatchResult[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [ran, setRan] = useState(false);

  const runPreview = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams({
        education_level: educationLevel,
        region,
        field_of_study_broad: field,
        limit: "4",
      });
      const res = await apiFetch(`/api/v1/profiles/sample-matches?${params}`);
      if (!res.ok) throw new Error("Could not load preview matches");
      const data = (await res.json()) as { sample_matches?: MatchResult[] };
      setMatches(data.sample_matches ?? []);
      setRan(true);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Preview failed");
      setMatches([]);
    } finally {
      setLoading(false);
    }
  }, [educationLevel, region, field]);

  return (
    <section className="border-b border-slate-200 bg-slate-50 py-16 dark:border-slate-800 dark:bg-slate-900/50">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white sm:text-3xl">
            Preview scholarship matching
          </h2>
          <p className="mt-2 text-slate-600 dark:text-slate-400">
            See how ISKONNECT evaluates eligibility from our verified scholarship database—create a free account
            for full personalized matching.
          </p>
        </div>

        <div className="mx-auto mt-8 max-w-3xl rounded-2xl border border-slate-200 bg-white p-6 shadow-lg dark:border-slate-700 dark:bg-slate-800">
          <div className="grid gap-4 sm:grid-cols-3">
            <label className="block text-sm">
              <span className="font-medium text-slate-700 dark:text-slate-300">Education level</span>
              <select
                value={educationLevel}
                onChange={(e) => setEducationLevel(e.target.value)}
                className="mt-1 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 dark:border-slate-600 dark:bg-slate-900"
              >
                {EDUCATION_LEVELS.map((l) => (
                  <option key={l} value={l}>
                    {l}
                  </option>
                ))}
              </select>
            </label>
            <label className="block text-sm">
              <span className="font-medium text-slate-700 dark:text-slate-300">Region</span>
              <select
                value={region}
                onChange={(e) => setRegion(e.target.value)}
                className="mt-1 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 dark:border-slate-600 dark:bg-slate-900"
              >
                {REGIONS.map((r) => (
                  <option key={r} value={r}>
                    {r}
                  </option>
                ))}
              </select>
            </label>
            <label className="block text-sm">
              <span className="font-medium text-slate-700 dark:text-slate-300">Field of study</span>
              <select
                value={field}
                onChange={(e) => setField(e.target.value)}
                className="mt-1 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 dark:border-slate-600 dark:bg-slate-900"
              >
                {FIELDS.map((f) => (
                  <option key={f} value={f}>
                    {f}
                  </option>
                ))}
              </select>
            </label>
          </div>
          <button
            type="button"
            onClick={() => void runPreview()}
            disabled={loading}
            className={`${primaryButtonClass} mt-6 w-full sm:w-auto`}
          >
            {loading ? "Matching…" : "Show my matches"}
          </button>
          {error ? <p className="mt-3 text-sm text-red-600 dark:text-red-400">{error}</p> : null}
        </div>

        {ran ? (
          <div className="mt-10">
            {matches.length === 0 ? (
              <p className="text-center text-slate-600 dark:text-slate-400">
                No matches yet — complete a full profile for better results.
              </p>
            ) : (
              <div className="grid gap-6 md:grid-cols-2">
                {matches.map((m) => (
                  <ScholarshipCardV2 key={m.id} scholarship={m} />
                ))}
              </div>
            )}
            <p className="mt-8 text-center text-sm text-slate-600 dark:text-slate-400">
              Preview only.{" "}
              <Link to="/register" className="font-semibold text-primary-600 hover:underline dark:text-primary-400">
                Create a free account
              </Link>{" "}
              for full personalized matching with explainable eligibility.
            </p>
          </div>
        ) : null}

        <div className="mt-10 flex flex-wrap justify-center gap-2">
          {EDUCATION_LEVELS.map((level) => (
            <Link
              key={level}
              to={`/scholarships/search?education_level=${encodeURIComponent(level)}`}
              className="rounded-full border border-slate-300 bg-white px-4 py-1.5 text-sm font-medium text-slate-700 hover:border-primary-400 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-200"
            >
              Browse {level}
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
