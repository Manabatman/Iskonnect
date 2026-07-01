import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { apiFetch } from "../api/client";
import { useDebounce } from "../hooks/useDebounce";
import { PHILIPPINE_REGIONS } from "../constants/regions";
import type { ScholarshipSearchFilters } from "../types";

/** Fallback when /search/filters fails or returns no levels */
const FALLBACK_EDUCATION_LEVELS = [
  "Senior High School",
  "College",
  "Graduate",
  "TVET",
] as const;

const INCOME_OPTIONS: { label: string; value: number }[] = [
  { label: "Any", value: -1 },
  { label: "Below ₱250K", value: 250_000 },
  { label: "₱250K - ₱400K", value: 400_000 },
  { label: "₱400K - ₱500K", value: 500_000 },
  { label: "Above ₱500K", value: 500_001 },
];

interface ScholarshipFilterOptions {
  providers: string[];
  education_levels: string[];
  regions: string[];
  fields_of_study: string[];
}

interface ScholarshipSearchFiltersProps {
  filters: ScholarshipSearchFilters;
  onChange: (filters: ScholarshipSearchFilters) => void;
}

const TIMING_LABELS: Record<string, string> = {
  open_now: "Open now",
  opening_soon: "Opening soon",
  expected_reopen: "Expected to reopen",
  closed: "Closed",
  previous_cycle: "Past cycle",
  needs_verification: "Needs verification",
  archived: "No longer offered",
};

const LIFE_STAGE_LABELS: Record<string, string> = {
  high_school: "High school",
  college: "College",
  graduate: "Graduate",
  tvet: "TVET",
};

export function describeActiveFilters(filters: ScholarshipSearchFilters): string[] {
  const labels: string[] = [];
  if (filters.region) labels.push(`Region: ${filters.region}`);
  if (filters.education_level) labels.push(`Level: ${filters.education_level}`);
  if (filters.life_stage) labels.push(`Stage: ${LIFE_STAGE_LABELS[filters.life_stage] ?? filters.life_stage}`);
  if (filters.timing) labels.push(`Timing: ${TIMING_LABELS[filters.timing] ?? filters.timing}`);
  if (filters.field) labels.push(`Study area: ${filters.field}`);
  if (filters.school) labels.push(`School: ${filters.school}`);
  if (filters.provider) labels.push(`Provider: ${filters.provider}`);
  if (filters.max_income != null && filters.max_income >= 0) {
    const incomeLabel = INCOME_OPTIONS.find((o) => o.value === filters.max_income)?.label;
    labels.push(`Income: ${incomeLabel ?? `≤ ₱${filters.max_income.toLocaleString()}`}`);
  }
  if (filters.include_archived) labels.push("Including archived");
  return labels;
}

export function ScholarshipSearchFilters({ filters, onChange }: ScholarshipSearchFiltersProps) {
  const [filterOptions, setFilterOptions] = useState<ScholarshipFilterOptions>({
    providers: [],
    education_levels: [],
    regions: [],
    fields_of_study: [],
  });
  const [providerInput, setProviderInput] = useState(filters.provider ?? "");

  useEffect(() => {
    setProviderInput(filters.provider ?? "");
  }, [filters.provider]);
  const [providerSuggestions, setProviderSuggestions] = useState<string[]>([]);
  const [providerOpen, setProviderOpen] = useState(false);
  const providerInputRef = useRef<HTMLInputElement>(null);
  const debouncedProvider = useDebounce(providerInput, 200);

  const educationLevelOptions = useMemo(() => {
    const fromApi = filterOptions.education_levels.filter(Boolean);
    const merged = new Set<string>([...fromApi, ...FALLBACK_EDUCATION_LEVELS]);
    return Array.from(merged).sort((a, b) => a.localeCompare(b));
  }, [filterOptions.education_levels]);

  useEffect(() => {
    let cancelled = false;
    apiFetch("/api/v1/scholarships/search/filters")
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (!cancelled && data) {
          setFilterOptions({
            providers: data.providers ?? [],
            education_levels: data.education_levels ?? [],
            regions: data.regions ?? [],
            fields_of_study: data.fields_of_study ?? [],
          });
        }
      })
      .catch(() => {});
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (!debouncedProvider.trim()) {
      setProviderSuggestions([]);
      return;
    }
    const q = debouncedProvider.toLowerCase();
    const matches = filterOptions.providers.filter((p) =>
      p.toLowerCase().includes(q)
    );
    setProviderSuggestions(matches.slice(0, 10));
    setProviderOpen(true);
  }, [debouncedProvider, filterOptions.providers]);

  useEffect(() => {
    const trimmed = debouncedProvider.trim() || undefined;
    if (trimmed === (filters.provider ?? undefined)) return;
    onChange({ ...filters, provider: trimmed });
  }, [debouncedProvider, filters, onChange]);

  const updateFilter = useCallback(
    <K extends keyof ScholarshipSearchFilters>(key: K, value: ScholarshipSearchFilters[K]) => {
      onChange({ ...filters, [key]: value });
    },
    [filters, onChange]
  );

  const handleClearAll = useCallback(() => {
    setProviderInput("");
    onChange({});
  }, [onChange]);

  const hasActiveFilters =
    filters.region ||
    filters.field ||
    filters.education_level ||
    filters.provider ||
    filters.school ||
    filters.timing ||
    filters.life_stage ||
    filters.include_closed ||
    (filters.max_income != null && filters.max_income >= 0);

  const selectClassName =
    "mt-1 w-full min-h-[44px] rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 px-3 py-3 text-base sm:text-sm text-slate-900 dark:text-slate-100 outline-none transition focus:ring-2 focus:ring-primary-200 focus:border-primary-500";
  const inputClassName =
    "mt-1 w-full min-h-[44px] rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 px-3 py-3 text-base sm:text-sm text-slate-900 dark:text-slate-100 outline-none transition focus:ring-2 focus:ring-primary-200 focus:border-primary-500";

  return (
    <aside className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-4 shadow-md">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-600 dark:text-slate-400">
          Filters
        </h3>
        {hasActiveFilters && (
          <button
            type="button"
            onClick={handleClearAll}
            className="text-xs font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400"
          >
            Clear all
          </button>
        )}
      </div>

      <div className="space-y-4">
        <div>
          <label htmlFor="filter-region" className="block text-sm font-medium text-slate-700 dark:text-slate-300">
            Region
          </label>
          <select
            id="filter-region"
            value={filters.region ?? ""}
            onChange={(e) => updateFilter("region", e.target.value || undefined)}
            className={selectClassName}
          >
            <option value="">All regions</option>
            {PHILIPPINE_REGIONS.map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="filter-education" className="block text-sm font-medium text-slate-700 dark:text-slate-300">
            Education Level
          </label>
          <select
            id="filter-education"
            value={filters.education_level ?? ""}
            onChange={(e) => updateFilter("education_level", e.target.value || undefined)}
            className={selectClassName}
          >
            <option value="">All levels</option>
            {educationLevelOptions.map((l) => (
              <option key={l} value={l}>
                {l}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="filter-life-stage" className="block text-sm font-medium text-slate-700 dark:text-slate-300">
            Life stage
          </label>
          <select
            id="filter-life-stage"
            value={filters.life_stage ?? ""}
            onChange={(e) => updateFilter("life_stage", e.target.value || undefined)}
            className={selectClassName}
          >
            <option value="">Any stage</option>
            <option value="high_school">High school</option>
            <option value="college">College</option>
            <option value="graduate">Graduate</option>
            <option value="tvet">TVET</option>
          </select>
        </div>

        <div>
          <label htmlFor="filter-timing" className="block text-sm font-medium text-slate-700 dark:text-slate-300">
            When to apply
          </label>
          <select
            id="filter-timing"
            value={filters.timing ?? ""}
            onChange={(e) => updateFilter("timing", e.target.value || undefined)}
            className={selectClassName}
          >
            <option value="">Any timing</option>
            <option value="open_now">Open now</option>
            <option value="opening_soon">Opening soon</option>
            <option value="expected_reopen">Expected to reopen</option>
            <option value="closed">Closed</option>
            <option value="previous_cycle">Past cycle</option>
            <option value="needs_verification">Needs verification</option>
            <option value="archived">No longer offered</option>
          </select>
        </div>

        <label className="flex min-h-[44px] items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
          <input
            type="checkbox"
            checked={!!filters.include_archived}
            onChange={(e) => updateFilter("include_archived", e.target.checked || undefined)}
            className="h-5 w-5 rounded border-slate-300 text-primary-600 focus:ring-primary-500"
          />
          Include archived programs
        </label>

        <div>
          <label htmlFor="filter-field" className="block text-sm font-medium text-slate-700 dark:text-slate-300">
            Study area
          </label>
          <input
            id="filter-field"
            type="text"
            value={filters.field ?? ""}
            onChange={(e) => updateFilter("field", e.target.value || undefined)}
            placeholder="e.g. Engineering, STEM"
            className={inputClassName}
          />
        </div>

        <div>
          <label htmlFor="filter-school" className="block text-sm font-medium text-slate-700 dark:text-slate-300">
            School / university
          </label>
          <input
            id="filter-school"
            type="text"
            value={filters.school ?? ""}
            onChange={(e) => updateFilter("school", e.target.value || undefined)}
            placeholder="e.g. UP, Ateneo, state university"
            className={inputClassName}
          />
        </div>

        <div>
          <label htmlFor="filter-income" className="block text-sm font-medium text-slate-700 dark:text-slate-300">
            Max Household Income
          </label>
          <select
            id="filter-income"
            value={
              filters.max_income != null && filters.max_income >= 0
                ? filters.max_income
                : ""
            }
            onChange={(e) => {
              const v = e.target.value;
              updateFilter("max_income", v === "" ? undefined : Number(v));
            }}
            className={selectClassName}
          >
            {INCOME_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value === -1 ? "" : opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>

        <div className="relative">
          <label htmlFor="filter-provider" className="block text-sm font-medium text-slate-700 dark:text-slate-300">
            Scholarship Provider
          </label>
          <input
            ref={providerInputRef}
            id="filter-provider"
            type="text"
            value={providerInput}
            onChange={(e) => setProviderInput(e.target.value)}
            onFocus={() => providerInput && setProviderOpen(true)}
            onBlur={() => {
              setTimeout(() => setProviderOpen(false), 150);
            }}
            placeholder="e.g. DOST, CHED"
            className={inputClassName}
          />
          {providerOpen && providerSuggestions.length > 0 && (
            <ul
              className="absolute z-50 mt-1 max-h-48 w-full overflow-auto rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-800 py-1 shadow-lg"
              role="listbox"
            >
              {providerSuggestions.map((p) => (
                <li
                  key={p}
                  role="option"
                  className="cursor-pointer px-3 py-2 text-sm text-slate-900 dark:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-700"
                  onMouseDown={(e) => {
                    e.preventDefault();
                    setProviderInput(p);
                    updateFilter("provider", p);
                    setProviderOpen(false);
                  }}
                >
                  {p}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </aside>
  );
}
