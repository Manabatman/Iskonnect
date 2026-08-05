import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { BackNavLink } from "../components/BackNavLink";
import { scoringFactors } from "../components/landing/landingData";

const factors = [
  {
    name: "Academic Performance",
    weight: 30,
    description: "How your grades compare to the scholarship's minimum GWA requirement.",
    tip: "Keep your GWA updated. Even a decimal point can change your score.",
  },
  {
    name: "Financial Need",
    weight: 28,
    description:
      "How well your household income fits the program's financial eligibility range (for need-sensitive programs).",
    tip: "Make sure your household income in your profile is accurate and current.",
  },
  {
    name: "Field of Study",
    weight: 22,
    description: "Whether your intended course matches what the scholarship is designed to fund.",
    tip: "Add all your possible course interests, not just your first choice.",
  },
  {
    name: "Location Match",
    weight: 10,
    description:
      "Whether your region, city, or province fits the scholarship's geographic rules (when the program has location limits).",
    tip: "Be as specific as possible. City-level data scores higher than region-level.",
  },
  {
    name: "Priority Group",
    weight: 10,
    description:
      "Whether you belong to groups the scholarship actively supports, like PWD, 4Ps, or IP.",
    tip: "Declare any applicable groups in your profile. This is part of the weighted score, not a separate override.",
  },
] as const;

const factorRationale: Record<string, { why: string; examples: string }> = {
  "Academic Performance": {
    why: "Most Philippine scholarships set a minimum GWA or grade requirement. Academic fit is the most common hard gate after education level.",
    examples: "CHED merit programs, university honors scholarships, DOST-SEI science scholarships with GWA floors.",
  },
  "Financial Need": {
    why: "Many government and LGU programs exist specifically to support students from lower-income households. Need-sensitive programs should rank higher when your profile reflects genuine financial need.",
    examples: "4Ps-linked grants, TESDA livelihood scholarships, LGU educational assistance for indigent students.",
  },
  "Field of Study": {
    why: "Scholarships often target specific courses: STEM, education, agriculture, or health sciences. Aligning your declared field with program intent helps you find programs you can actually use.",
    examples: "DOST-SEI priority S&T courses, CHED priority programs, industry-sponsored engineering scholarships.",
  },
  "Location Match": {
    why: "Regional and LGU scholarships are geographically restricted by design. Location weighting surfaces programs meant for your area without hiding nationwide opportunities.",
    examples: "Provincial LGU grants, regional CHED allocations, city-specific university scholarships.",
  },
  "Priority Group": {
    why: "Philippine scholarship policy often recognizes equity groups: PWD, indigenous peoples, solo parents, 4Ps beneficiaries, and others. This factor reflects documented priority-group eligibility without overriding hard rules.",
    examples: "RA 7277 (PWD), IP education programs, solo-parent educational assistance, 4Ps-aligned grants.",
  },
};

const whyReasons = [
  {
    title: "They never heard about it",
    problem:
      "Scholarships are announced on different government portals, university sites, LGU Facebook pages, and foundation newsletters, often with no single place to search.",
    solution:
      "ISKONNECT brings programs from CHED, DOST-SEI, TESDA, LGUs, universities, and private foundations into one catalog you can browse and match against your profile.",
  },
  {
    title: "They missed the deadline",
    problem: "Application windows can be short. By the time a student finds a program, the deadline may already have passed.",
    solution:
      "Your scholarship plan shows what's open now, what's opening soon, and what's expected to reopen, so you can prepare before the rush.",
  },
  {
    title: "They weren't eligible yet",
    problem:
      "Many programs require a specific grade level, GWA, or course. Students often discover a scholarship only after they've already missed the window to qualify.",
    solution:
      "ISKONNECT flags future eligibility: scholarships you might qualify for later, so you can plan ahead instead of learning about them too late.",
  },
  {
    title: "They didn't have time to prepare",
    problem: "Gathering documents, essays, and certificates takes weeks. Starting at the last minute means incomplete applications.",
    solution:
      "Document checklists, preparation reminders, and early visibility into upcoming cycles give you time to get ready before applications open.",
  },
  {
    title: "The information was confusing or outdated",
    problem: "Deadlines change, links break, and requirements differ between cycles. It's hard to know what still applies.",
    solution:
      "We verify scholarships against official sources, show when information was last checked, and link you to the provider's site so you can confirm details yourself.",
  },
] as const;

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
        className="h-full rounded-full bg-primary-500 transition-[width] duration-reveal ease-out-custom dark:bg-primary-400"
        style={{ width: visible ? `${widthPercent}%` : "0%" }}
      />
    </div>
  );
}

export function HowMatchingWorksPage() {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-600 dark:text-primary-400">
          How matching works
        </p>
        <h1 className="mt-2 text-3xl font-bold text-slate-900 dark:text-slate-100">
          How ISKONNECT matches you to scholarships
        </h1>
        <p className="mt-4 text-lg leading-relaxed text-slate-600 dark:text-slate-400">
          Your match score measures eligibility fit, not your odds of winning. This page explains why ISKONNECT exists,
          how scores are built, and what we cannot see.
        </p>

        <div className="mt-8 rounded-2xl border border-primary-200 bg-primary-50 p-6 shadow-sm dark:border-primary-800 dark:bg-slate-900">
          <p className="text-sm leading-relaxed text-slate-900 dark:text-slate-100">
            <strong className="font-semibold text-primary-900 dark:text-primary-200">
              A high match score means strong eligibility fit, not a guarantee of acceptance.
            </strong>{" "}
            Providers may consider interviews, essays, quotas, and other factors ISKONNECT cannot see. Use scores to
            prioritize where to invest your time, not as a prediction of outcome.
          </p>
        </div>

        <div id="why" className="mt-12 scroll-mt-24 space-y-6">
          <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-100">Why ISKONNECT exists</h2>
          <p className="text-sm leading-relaxed text-slate-700 dark:text-slate-300">
            Filipino students deserve a fair shot at scholarships, not just those who already know where to look.
            ISKONNECT was built because too many qualified students miss opportunities they could have reached.
          </p>
          <div className="rounded-xl border border-primary-200 bg-primary-50/60 p-5 dark:border-primary-800 dark:bg-primary-950/30">
            <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Our mission</h3>
            <p className="mt-2 text-sm leading-relaxed text-slate-700 dark:text-slate-300">
              Help Filipino students discover scholarships they qualify for today, soon, or in the future, and give
              them enough time and clarity to apply with confidence.
            </p>
          </div>
          <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
            Five reasons students miss scholarships
          </h3>
          <div className="space-y-8">
            {whyReasons.map((item, i) => (
              <article key={item.title} className="border-l-4 border-primary-500 pl-5">
                <p className="text-xs font-semibold uppercase tracking-wide text-primary-600 dark:text-primary-400">
                  Reason {i + 1}
                </p>
                <h4 className="mt-1 text-base font-semibold text-slate-900 dark:text-slate-100">{item.title}</h4>
                <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">{item.problem}</p>
                <p className="mt-3 text-sm leading-relaxed text-slate-700 dark:text-slate-300">
                  <span className="font-medium text-emerald-700 dark:text-emerald-400">How ISKONNECT helps: </span>
                  {item.solution}
                </p>
              </article>
            ))}
          </div>
        </div>

        <div id="score-ranges" className="mt-12 scroll-mt-24">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">What the numbers mean</h2>
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

        <div id="factors" className="mt-12 scroll-mt-24">
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
                  <span className="font-medium">Tip: </span>
                  {f.tip}
                </p>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-12 space-y-4 text-slate-700 dark:text-slate-300">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">How the final number is calculated</h2>
          <p className="text-sm leading-relaxed">
            Each factor is scored between 0 and 1 based on your profile data. The five scores are weighted and combined
            into a number from 0 to 100. If a scholarship has no field or location restriction, that part is left out and
            the other weights are scaled so the total still makes sense.
          </p>
          <p className="text-sm leading-relaxed">
            Document readiness (uploaded vs. required documents) is shown on your scholarship and documents pages. It is{" "}
            <strong className="font-semibold">not</strong> part of this match score, so your fit rank reflects program
            rules, not how many files you have uploaded yet.
          </p>
        </div>

        <div id="methodology" className="mt-12 scroll-mt-24 space-y-4">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Weighting philosophy</h2>
          <p className="text-sm leading-relaxed text-slate-700 dark:text-slate-300">
            Weights reflect how often each dimension appears as a decisive eligibility rule across Philippine scholarship
            programs. Academic performance and financial need together account for most of the score because they are the
            most common published gates. Field of study and location matter when programs are course- or region-specific.
            Priority groups receive a smaller but meaningful share because they apply to targeted equity programs, not
            every scholarship.
          </p>
          <div className="mt-6 space-y-4">
            {scoringFactors.map((factor) => {
              const detail = factorRationale[factor.name];
              return (
                <article
                  key={factor.name}
                  className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800/80"
                >
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <h3 className="font-semibold text-slate-900 dark:text-slate-100">{factor.name}</h3>
                    <span className="rounded-full bg-primary-100 px-3 py-0.5 text-xs font-semibold text-primary-800 dark:bg-primary-900/50 dark:text-primary-200">
                      {factor.weight}% of score
                    </span>
                  </div>
                  {detail ? (
                    <>
                      <p className="mt-3 text-sm leading-relaxed text-slate-700 dark:text-slate-300">
                        <strong className="font-medium text-slate-900 dark:text-slate-100">Why it exists: </strong>
                        {detail.why}
                      </p>
                      <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">
                        <strong className="font-medium text-slate-800 dark:text-slate-200">Examples: </strong>
                        {detail.examples}
                      </p>
                    </>
                  ) : null}
                </article>
              );
            })}
          </div>
        </div>

        <div className="mt-12 space-y-4">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Fairness commitments</h2>
          <ul className="list-disc space-y-2 pl-5 text-sm leading-relaxed text-slate-700 dark:text-slate-300">
            <li>Hard eligibility rules are applied before scoring. Programs you clearly cannot qualify for are filtered out.</li>
            <li>Merit-only programs do not penalize students for income data; need-based programs weight financial fit appropriately.</li>
            <li>Priority-group scoring reflects published program criteria, not assumptions about your background.</li>
            <li>Scores are explainable: every match shows which factors helped or held you back.</li>
          </ul>
        </div>

        <div className="mt-12 rounded-2xl border border-amber-200 bg-amber-50 p-6 dark:border-amber-800 dark:bg-amber-950/30">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Current limitations</h2>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm leading-relaxed text-slate-700 dark:text-slate-300">
            <li>We cannot see essay quality, interviews, or provider-internal quotas.</li>
            <li>Some scholarships publish incomplete criteria; we flag those as needing verification.</li>
            <li>Document readiness is tracked separately. It does not change your eligibility fit score.</li>
            <li>Weights are calibrated for Philippine undergraduate and TVET programs; graduate-specific rules are still expanding.</li>
          </ul>
        </div>

        <div className="mt-12 space-y-4">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Future improvements</h2>
          <ul className="list-disc space-y-2 pl-5 text-sm leading-relaxed text-slate-700 dark:text-slate-300">
            <li>Community feedback loops to refine weights as we learn which factors students find most useful.</li>
            <li>More granular course alignment using PSCED taxonomy updates.</li>
            <li>Transparent changelogs whenever scoring policy versions change.</li>
            <li>Separate scoring profiles for merit-heavy vs. need-heavy program families where appropriate.</li>
          </ul>
        </div>

        <div className="mt-12 rounded-2xl border border-slate-200 bg-slate-50 p-6 shadow-sm dark:border-slate-600 dark:bg-slate-900">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Why your score might change</h2>
          <p className="mt-2 text-sm leading-relaxed text-slate-700 dark:text-slate-300">
            Scores are recalculated every time you update your profile, when an administrator adjusts program weights for a
            new cycle, or when new scholarship data is published. This is intentional. It keeps results accurate as your
            situation and available programs evolve.
          </p>
        </div>

        <div className="mt-12 grid gap-4 sm:grid-cols-2">
          <Link
            to="/how-we-verify"
            className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:border-primary-300 dark:border-slate-700 dark:bg-slate-800/80"
          >
            <h3 className="font-semibold text-slate-900 group-hover:text-primary-700 dark:text-slate-100">How we verify</h3>
            <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
              Sources, freshness labels, and our review process.
            </p>
          </Link>
          <Link
            to="/scholarship-status"
            className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:border-primary-300 dark:border-slate-700 dark:bg-slate-800/80"
          >
            <h3 className="font-semibold text-slate-900 group-hover:text-primary-700 dark:text-slate-100">
              Scholarship status guide
            </h3>
            <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
              What labels like Open now and Needs verification mean.
            </p>
          </Link>
        </div>

        <div className="mt-12">
          <BackNavLink />
        </div>
      </div>
    </section>
  );
}
