import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { BackNavLink } from "../components/BackNavLink";
const factors = [
  {
    name: "Academic Performance",
    weight: 30,
    description: "How your grades compare to the scholarship's minimum GWA requirement.",
    tip: "Keep your GWA updated — even a decimal point can change your score.",
  },
  {
    name: "Financial Need",
    weight: 28,
    description: "How well your household income fits the program's financial eligibility range (for need-sensitive programs).",
    tip: "Make sure your household income in your profile is accurate and current.",
  },
  {
    name: "Field of Study",
    weight: 22,
    description: "Whether your intended course matches what the scholarship is designed to fund.",
    tip: "Add all your possible course interests — not just your first choice.",
  },
  {
    name: "Location Match",
    weight: 10,
    description: "Whether your region, city, or province fits the scholarship's geographic rules (when the program has location limits).",
    tip: "Be as specific as possible — city-level data scores higher than region-level.",
  },
  {
    name: "Priority Group",
    weight: 10,
    description: "Whether you belong to groups the scholarship actively supports, like PWD, 4Ps, or IP.",
    tip: "Declare any applicable groups in your profile. This is part of the weighted score, not a separate override.",
  },
] as const;

/** Accent = colored top border; body uses neutral surfaces for readable light + dark contrast. */
const scoreRanges = [
  {
    range: "0–49",
    label: "Poor fit",
    desc: "Your profile doesn't closely match this program's criteria",
    accent: "border-t-4 border-t-red-600 dark:border-t-red-400",
  },
  {
    range: "50–74",
    label: "Moderate fit",
    desc: "You meet some criteria but not all",
    accent: "border-t-4 border-t-amber-600 dark:border-t-amber-400",
  },
  {
    range: "75–89",
    label: "Strong fit",
    desc: "Your profile closely matches this program",
    accent: "border-t-4 border-t-emerald-600 dark:border-t-emerald-400",
  },
  {
    range: "90–100",
    label: "Excellent fit",
    desc: "Your profile is an exceptionally strong match",
    accent: "border-t-4 border-t-primary-600 dark:border-t-primary-400",
  },
] as const;

function WeightBar({ widthPercent }: { widthPercent: number }) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const obs = new IntersectionObserver(
      ([entry]) => {
        if (entry?.isIntersecting) setVisible(true);
      },
      { threshold: 0.2 }
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  return (
    <div ref={ref} className="mt-3 h-1.5 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-700">
      <div
        className="h-full rounded-full bg-primary-500 transition-[width] duration-700 ease-out dark:bg-primary-400"
        style={{ width: visible ? `${widthPercent}%` : "0%" }}
      />
    </div>
  );
}

export function TransparencyPage() {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-600 dark:text-primary-400">Transparency</p>
        <h1 className="mt-2 text-3xl font-bold text-slate-900 dark:text-slate-100">How your match score is built</h1>
        <p className="mt-4 text-lg text-slate-600 dark:text-slate-400">
          Your score measures fit — not your chances of winning. Here&apos;s exactly what goes into it.
        </p>

        <div className="mt-8 rounded-2xl border border-primary-200 bg-primary-50 p-6 shadow-sm dark:border-primary-800 dark:bg-slate-900 dark:shadow-none">
          <p className="text-sm leading-relaxed text-slate-900 dark:text-slate-100">
            <strong className="font-semibold text-primary-900 dark:text-primary-200">Your match score is a measure of eligibility fit, not a prediction of acceptance.</strong>{" "}
            A score of 85 means your profile strongly matches this program&apos;s criteria. It does{" "}
            <strong className="font-semibold">not</strong> mean you have an 85% chance of receiving the scholarship.
          </p>
        </div>

        <div className="mt-10">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
            Trust &amp; status resources
          </h2>
          <div className="mt-3 grid gap-4 sm:grid-cols-2">
            <Link
              to="/how-we-verify"
              className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:border-primary-300 hover:shadow-md dark:border-slate-700 dark:bg-slate-800/80 dark:hover:border-primary-600"
            >
              <h3 className="font-semibold text-slate-900 group-hover:text-primary-700 dark:text-slate-100 dark:group-hover:text-primary-400">
                How we verify
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">
                Learn how ISKONNECT checks scholarship listings against official sources and what our freshness labels mean.
              </p>
            </Link>
            <Link
              to="/scholarship-status"
              className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:border-primary-300 hover:shadow-md dark:border-slate-700 dark:bg-slate-800/80 dark:hover:border-primary-600"
            >
              <h3 className="font-semibold text-slate-900 group-hover:text-primary-700 dark:text-slate-100 dark:group-hover:text-primary-400">
                Scholarship status guide
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">
                Understand labels like Open now, Closed, Past cycle, and Needs verification—and what to do next.
              </p>
            </Link>
          </div>
        </div>

        <div className="mt-10">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
            What the numbers mean
          </h2>
          <div className="mt-3 grid grid-cols-2 gap-3 lg:grid-cols-4">
            {scoreRanges.map((s) => (
              <div
                key={s.range}
                className={`rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-600 dark:bg-slate-900 ${s.accent}`}
              >
                <p className="text-xs font-bold uppercase tracking-wide text-slate-500 dark:text-slate-400">{s.range}</p>
                <p className="mt-1 font-semibold text-slate-900 dark:text-slate-50">{s.label}</p>
                <p className="mt-2 text-xs leading-snug text-slate-600 dark:text-slate-300">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-12">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">What goes into your score</h2>
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
            Each part below has a weight. Together they form your match score after you pass eligibility checks.
          </p>
          <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
            {factors.map((f) => (
              <div
                key={f.name}
                className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800/80"
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <h3 className="font-semibold text-slate-900 dark:text-slate-100">{f.name}</h3>
                  <span className="rounded-full bg-primary-100 px-2 py-0.5 text-xs font-semibold text-primary-800 dark:bg-primary-900/50 dark:text-primary-200">
                    {f.weight}%
                  </span>
                </div>
                <WeightBar widthPercent={f.weight} />
                <p className="mt-3 text-sm text-slate-600 dark:text-slate-400">{f.description}</p>
                <p className="mt-2 text-sm text-primary-600 dark:text-primary-400">
                  <span aria-hidden>→ </span>
                  {f.tip}
                </p>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-12 space-y-4 text-slate-700 dark:text-slate-300">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">How the final number is calculated</h2>
          <p className="text-sm leading-relaxed">
            Each factor is scored between 0 and 1 based on your profile data. The five scores are weighted and combined into a
            number from 0 to 100. If a scholarship has no field or location restriction, that part is left out and the other
            weights are scaled so the total still makes sense.
          </p>
          <p className="text-sm leading-relaxed">
            Document readiness (uploaded vs. required documents) is shown on your scholarship and documents pages — it is{" "}
            <strong className="font-semibold">not</strong> part of this match score, so your fit rank reflects program rules,
            not how many files you have uploaded yet.
          </p>
        </div>

        <div className="mt-10 rounded-2xl border border-slate-200 bg-slate-50 p-6 shadow-sm dark:border-slate-600 dark:bg-slate-900">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Scholarship data you can trust</h2>
          <p className="mt-2 text-sm leading-relaxed text-slate-700 dark:text-slate-300">
            Match scores tell you how well you fit a program&apos;s rules. Freshness and status labels tell you how current
            the listing is. Use the trust resources above to learn what each label means—and always confirm details on the
            official provider&apos;s site before applying.
          </p>
        </div>

        <div className="mt-10 rounded-2xl border border-slate-200 bg-slate-50 p-6 shadow-sm dark:border-slate-600 dark:bg-slate-900">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Why your score might change</h2>
          <p className="mt-2 text-sm leading-relaxed text-slate-700 dark:text-slate-300">
            Scores are recalculated every time you update your profile, when an administrator adjusts program weights for a new
            cycle, or when new scholarship data is published. This is intentional — it keeps results accurate as your situation
            and available programs evolve.
          </p>
        </div>

        <div className="mt-12">
          <BackNavLink />
        </div>
      </div>
    </section>
  );
}
