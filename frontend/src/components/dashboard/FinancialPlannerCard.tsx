import { useEffect, useMemo, useState } from "react";
import type { SavedScholarship } from "../../types";

type Props = {
  saved: SavedScholarship[];
  /** Merged onto the root card (e.g. h-full for grid stretch). */
  className?: string;
};

type TermStructure = "semester" | "trimester" | "custom";
type ExpenseModel = "weekly" | "monthly";

function parseMoney(s: string): number | null {
  const t = String(s).replace(/,/g, "").trim();
  if (t === "") return null;
  const n = Number(t);
  if (!Number.isFinite(n) || n < 0) return null;
  return n;
}

function numTermsFor(structure: TermStructure, custom: string): number {
  if (structure === "semester") return 2;
  if (structure === "trimester") return 3;
  const n = Number(custom.replace(/,/g, "").trim());
  if (!Number.isFinite(n) || n < 1) return 0;
  return Math.min(Math.floor(n), 12);
}

function cardRootClass(extra?: string) {
  return [
    "flex h-full min-h-0 flex-col rounded-2xl border border-emerald-200/80 bg-white p-6 shadow-sm dark:border-emerald-900/50 dark:bg-slate-800/80",
    extra,
  ]
    .filter(Boolean)
    .join(" ");
}

export function FinancialPlannerCard({ saved, className }: Props) {
  const [scholarshipId, setScholarshipId] = useState<string>(() => String(saved[0]?.scholarship_id ?? ""));
  const [tuitionPerTerm, setTuitionPerTerm] = useState("");
  const [termStructure, setTermStructure] = useState<TermStructure>("semester");
  const [customTerms, setCustomTerms] = useState("");
  const [expenseModel, setExpenseModel] = useState<ExpenseModel>("monthly");
  const [monthlyExpenses, setMonthlyExpenses] = useState("");
  const [weeklyExpenses, setWeeklyExpenses] = useState("");
  const [activeSchoolWeeks, setActiveSchoolWeeks] = useState("");

  useEffect(() => {
    if (saved.length === 0) {
      setScholarshipId("");
      return;
    }
    const stillSaved = saved.some((s) => String(s.scholarship_id) === scholarshipId);
    if (!stillSaved) {
      setScholarshipId(String(saved[0]?.scholarship_id ?? ""));
    }
  }, [saved, scholarshipId]);

  const selected = useMemo(() => {
    const id = Number(scholarshipId);
    return saved.find((s) => s.scholarship_id === id) ?? null;
  }, [saved, scholarshipId]);

  const sch = selected?.scholarship ?? (selected
    ? {
        title: selected.title ?? undefined,
        benefit_tuition: selected.benefit_tuition ?? undefined,
        benefit_allowance_monthly: selected.benefit_allowance_monthly ?? undefined,
        benefit_total_value: selected.benefit_total_value ?? undefined,
      }
    : undefined);

  const analysis = useMemo(() => {
    const tuitionN = parseMoney(tuitionPerTerm);
    const terms = numTermsFor(termStructure, customTerms);
    const monthlyN = parseMoney(monthlyExpenses);
    const weeklyN = parseMoney(weeklyExpenses);
    const weeksN = parseMoney(activeSchoolWeeks);

    const hasTuitionInput = tuitionPerTerm.trim() !== "";
    const hasLivingInputs =
      expenseModel === "monthly"
        ? monthlyExpenses.trim() !== ""
        : weeklyExpenses.trim() !== "" && activeSchoolWeeks.trim() !== "";

    if (!hasTuitionInput && !hasLivingInputs) {
      return {
        kind: "empty" as const,
        message: "Enter tuition per term and your living costs to see an annual estimate.",
      };
    }

    if (hasTuitionInput && tuitionN === null) {
      return { kind: "invalid" as const, message: "Enter a valid number for tuition per term (or clear the field)." };
    }

    if (termStructure === "custom" && terms === 0 && hasTuitionInput) {
      return {
        kind: "invalid" as const,
        message: "Enter a valid number of terms (1–12) for custom structure.",
      };
    }

    const tuitionAnnual = hasTuitionInput && tuitionN != null && terms > 0 ? tuitionN * terms : 0;

    let livingAnnual = 0;
    if (expenseModel === "monthly") {
      if (hasLivingInputs && monthlyN === null) {
        return { kind: "invalid" as const, message: "Enter a valid number for monthly expenses." };
      }
      if (monthlyN != null) livingAnnual = monthlyN * 12;
    } else {
      if (hasLivingInputs && (weeklyN === null || weeksN === null)) {
        return {
          kind: "invalid" as const,
          message: "Enter valid numbers for weekly expenses and active school weeks.",
        };
      }
      if (weeklyN != null && weeksN != null) livingAnnual = weeklyN * weeksN;
    }

    const tPart = tuitionAnnual;
    const lPart = livingAnnual;
    const annualNeed = tPart + lPart;

    const notes: string[] = [];
    let covered = 0;

    if (sch?.benefit_tuition) {
      if (terms > 0 && sch.benefit_total_value != null && sch.benefit_total_value > 0 && tuitionAnnual > 0) {
        const tuitionCov = Math.min(sch.benefit_total_value, tuitionAnnual);
        covered += tuitionCov;
        notes.push(
          `This scholarship may cover up to ₱${tuitionCov.toLocaleString("en-PH")} per year toward your estimated tuition (listed benefit ₱${sch.benefit_total_value.toLocaleString("en-PH")}; multi-year programs may cover more — confirm on the official page).`
        );
      } else if (tuitionAnnual > 0) {
        covered += tuitionAnnual;
        notes.push(
          "This scholarship includes tuition support but no fixed amount is listed — coverage assumed up to your entered annual tuition."
        );
      } else if (sch.benefit_total_value != null && sch.benefit_total_value > 0 && terms === 0) {
        notes.push(
          "This scholarship lists tuition support — set your term structure to estimate how much it may cover."
        );
      }
    }

    if (sch?.benefit_allowance_monthly != null && sch.benefit_allowance_monthly > 0) {
      const stip = sch.benefit_allowance_monthly * 12;
      covered += stip;
      notes.push(
        `Monthly allowance ₱${sch.benefit_allowance_monthly.toLocaleString("en-PH")} × 12 ≈ ₱${stip.toLocaleString("en-PH")} / year.`
      );
    }

    if (sch?.benefit_total_value != null && sch.benefit_total_value > 0 && !sch.benefit_tuition) {
      const cap = Math.min(sch.benefit_total_value, Math.max(0, annualNeed - covered));
      if (cap > 0) {
        covered += cap;
        notes.push(
          `Total scholarship benefit of up to ₱${cap.toLocaleString("en-PH")} applied toward remaining costs.`
        );
      }
    }

    if (notes.length === 0) {
      notes.push("No benefit amounts listed for this scholarship — check the official program page.");
    }

    const gap = Math.max(0, annualNeed - covered);
    let band: "full" | "partial" | "none";
    if (annualNeed <= 0) band = "none";
    else if (gap <= 0) band = "full";
    else if (covered <= 0) band = "none";
    else band = "partial";

    const bandLabel =
      band === "full"
        ? "Fully covered (by this estimate)"
        : band === "partial"
          ? "Partially covered"
          : "Not covered (by this estimate)";

    return {
      kind: "ok" as const,
      annualNeed,
      covered,
      gap,
      band,
      bandLabel,
      notes,
      terms,
      tuitionAnnual: tPart,
      livingAnnual: lPart,
    };
  }, [
    sch,
    tuitionPerTerm,
    termStructure,
    customTerms,
    expenseModel,
    monthlyExpenses,
    weeklyExpenses,
    activeSchoolWeeks,
  ]);

  if (saved.length === 0) {
    return (
      <div className={cardRootClass(className)}>
        <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">Financial Planner</h3>
        <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
          Save scholarships to compare your expected costs against what each program covers.
        </p>
      </div>
    );
  }

  return (
    <div className={cardRootClass(className)}>
      <div className="flex items-start gap-3">
        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-200">
          <span className="text-lg" aria-hidden>
            🧮
          </span>
        </div>
        <div>
          <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">Financial Planner</h3>
          <p className="text-sm text-slate-500 dark:text-slate-400">Your yearly cost vs what this scholarship covers</p>
        </div>
      </div>

      <label className="mt-4 block text-xs font-medium text-slate-600 dark:text-slate-400">Scholarship</label>
      <select
        value={scholarshipId}
        onChange={(e) => setScholarshipId(e.target.value)}
        className="mt-1 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm dark:border-slate-600 dark:bg-slate-900 dark:text-slate-100"
      >
        {saved.map((s) => (
          <option key={s.id} value={s.scholarship_id}>
            {s.title ?? s.scholarship?.title ?? `Scholarship #${s.scholarship_id}`}
          </option>
        ))}
      </select>

      <div className="mt-4 space-y-3">
        <div>
          <label className="text-xs font-medium text-slate-600 dark:text-slate-400">Academic structure</label>
          <div className="mt-1 flex flex-wrap gap-2">
            {(
              [
                ["semester", "Semester (2 terms)"],
                ["trimester", "Trimester (3 terms)"],
                ["custom", "Custom (# terms)"],
              ] as const
            ).map(([v, lab]) => (
              <button
                key={v}
                type="button"
                onClick={() => setTermStructure(v)}
                className={[
                  "rounded-lg border px-3 py-1.5 text-xs font-medium",
                  termStructure === v
                    ? "border-emerald-600 bg-emerald-50 text-emerald-900 dark:border-emerald-500 dark:bg-emerald-950 dark:text-emerald-50"
                    : "border-slate-300 text-slate-700 dark:border-slate-600 dark:text-slate-200",
                ].join(" ")}
              >
                {lab}
              </button>
            ))}
          </div>
          {termStructure === "custom" ? (
            <input
              type="text"
              inputMode="numeric"
              placeholder="Number of terms (e.g. 4)"
              value={customTerms}
              onChange={(e) => setCustomTerms(e.target.value)}
              className="mt-2 w-full max-w-xs rounded-xl border border-slate-300 px-3 py-2 text-sm dark:border-slate-600 dark:bg-slate-900 dark:text-slate-100"
            />
          ) : null}
        </div>

        <div>
          <label className="text-xs font-medium text-slate-600 dark:text-slate-400">Tuition per term (₱)</label>
          <div className="mt-1 flex rounded-xl border border-slate-300 dark:border-slate-600">
            <span className="flex items-center px-2 text-sm text-slate-500">₱</span>
            <input
              type="text"
              inputMode="decimal"
              placeholder=""
              value={tuitionPerTerm}
              onChange={(e) => setTuitionPerTerm(e.target.value)}
              className="w-full min-w-0 rounded-r-xl border-0 bg-transparent py-2 pr-3 text-sm outline-none dark:text-slate-100"
            />
          </div>
        </div>

        <div>
          <span className="text-xs font-medium text-slate-600 dark:text-slate-400">Living costs</span>
          <div className="mt-1 flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => setExpenseModel("monthly")}
              className={[
                "rounded-lg border px-3 py-1.5 text-xs font-medium",
                expenseModel === "monthly"
                  ? "border-emerald-600 bg-emerald-50 text-emerald-900 dark:border-emerald-500 dark:bg-emerald-950/40 dark:text-emerald-100"
                  : "border-slate-300 text-slate-700 dark:border-slate-600 dark:text-slate-300",
              ].join(" ")}
            >
              Monthly × 12
            </button>
            <button
              type="button"
              onClick={() => setExpenseModel("weekly")}
              className={[
                "rounded-lg border px-3 py-1.5 text-xs font-medium",
                expenseModel === "weekly"
                  ? "border-emerald-600 bg-emerald-50 text-emerald-900 dark:border-emerald-500 dark:bg-emerald-950/40 dark:text-emerald-100"
                  : "border-slate-300 text-slate-700 dark:border-slate-600 dark:text-slate-300",
              ].join(" ")}
            >
              Weekly × active school weeks
            </button>
          </div>
          {expenseModel === "monthly" ? (
            <div className="mt-2 flex rounded-xl border border-slate-300 dark:border-slate-600">
              <span className="flex items-center px-2 text-sm text-slate-500">₱</span>
              <input
                type="text"
                inputMode="decimal"
                placeholder="Monthly expenses"
                value={monthlyExpenses}
                onChange={(e) => setMonthlyExpenses(e.target.value)}
                className="w-full min-w-0 rounded-r-xl border-0 bg-transparent py-2 pr-3 text-sm outline-none dark:text-slate-100"
              />
            </div>
          ) : (
            <div className="mt-2 grid gap-2 sm:grid-cols-2">
              <div className="flex rounded-xl border border-slate-300 dark:border-slate-600">
                <span className="flex items-center px-2 text-sm text-slate-500">₱</span>
                <input
                  type="text"
                  inputMode="decimal"
                  placeholder="Weekly expenses"
                  value={weeklyExpenses}
                  onChange={(e) => setWeeklyExpenses(e.target.value)}
                  className="w-full min-w-0 rounded-r-xl border-0 bg-transparent py-2 pr-3 text-sm outline-none dark:text-slate-100"
                />
              </div>
              <input
                type="text"
                inputMode="numeric"
                placeholder="Active school weeks / year"
                value={activeSchoolWeeks}
                onChange={(e) => setActiveSchoolWeeks(e.target.value)}
                className="rounded-xl border border-slate-300 px-3 py-2 text-sm dark:border-slate-600 dark:bg-slate-900 dark:text-slate-100"
              />
            </div>
          )}
        </div>
      </div>

      <div className="mt-4 rounded-xl border border-slate-100 bg-slate-50 p-4 text-slate-800 dark:border-slate-600 dark:bg-slate-900/90 dark:text-slate-200">
        {analysis.kind === "empty" || analysis.kind === "invalid" ? (
          <p className="text-sm text-slate-700 dark:text-slate-300">{analysis.message}</p>
        ) : (
          <>
            <p className="text-xs font-semibold uppercase tracking-wide text-emerald-800 dark:text-emerald-200">
              {analysis.bandLabel}
            </p>
            <ul className="mt-2 space-y-1 text-sm text-slate-700 dark:text-slate-300">
              <li>
                Estimated annual need:{" "}
                <strong>₱{analysis.annualNeed.toLocaleString("en-PH")}</strong>
                {analysis.tuitionAnnual != null && analysis.tuitionAnnual > 0 ? (
                  <span className="text-slate-500">
                    {" "}
                    (tuition × {analysis.terms} term{analysis.terms === 1 ? "" : "s"}
                    {analysis.livingAnnual != null && analysis.livingAnnual > 0
                      ? ` + living ₱${analysis.livingAnnual.toLocaleString("en-PH")}`
                      : ""}
                    )
                  </span>
                ) : analysis.livingAnnual != null && analysis.livingAnnual > 0 ? (
                  <span className="text-slate-500"> (living only)</span>
                ) : null}
              </li>
              <li>
                What this scholarship covers: <strong>₱{analysis.covered.toLocaleString("en-PH")}</strong>
              </li>
              <li>
                What you may still need: <strong>₱{analysis.gap.toLocaleString("en-PH")}</strong>
              </li>
            </ul>
            <ul className="mt-3 list-inside list-disc text-xs text-slate-600 dark:text-slate-400">
              {analysis.notes.map((n) => (
                <li key={n}>{n}</li>
              ))}
            </ul>
          </>
        )}
        <p className="mt-3 border-t border-slate-200 pt-3 text-xs font-medium text-amber-900 dark:border-slate-600 dark:text-amber-200">
          This is an estimate based on your inputs. Actual costs and scholarship coverage may vary. Always confirm stipend
          rules, caps, and payment schedules on the official program page.
        </p>
      </div>
    </div>
  );
}
