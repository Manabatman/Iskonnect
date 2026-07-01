import { Link } from "react-router-dom";
import { BackNavLink } from "../components/BackNavLink";
import { scoringFactors } from "../components/landing/landingData";

const factorRationale: Record<
  string,
  { why: string; examples: string }
> = {
  "Academic Performance": {
    why: "Most Philippine scholarships set a minimum GWA or grade requirement. Academic fit is the most common hard gate after education level.",
    examples: "CHED merit programs, university honors scholarships, DOST-SEI science scholarships with GWA floors.",
  },
  "Financial Need": {
    why: "Many government and LGU programs exist specifically to support students from lower-income households. Need-sensitive programs should rank higher when your profile reflects genuine financial need.",
    examples: "4Ps-linked grants, TESDA livelihood scholarships, LGU educational assistance for indigent students.",
  },
  "Field of Study": {
    why: "Scholarships often target specific courses—STEM, education, agriculture, or health sciences. Aligning your declared field with program intent helps you find programs you can actually use.",
    examples: "DOST-SEI priority S&T courses, CHED priority programs, industry-sponsored engineering scholarships.",
  },
  "Location Match": {
    why: "Regional and LGU scholarships are geographically restricted by design. Location weighting surfaces programs meant for your area without hiding nationwide opportunities.",
    examples: "Provincial LGU grants, regional CHED allocations, city-specific university scholarships.",
  },
  "Priority Group": {
    why: "Philippine scholarship policy often recognizes equity groups—PWD, indigenous peoples, solo parents, 4Ps beneficiaries, and others. This factor reflects documented priority-group eligibility without overriding hard rules.",
    examples: "RA 7277 (PWD), IP education programs, solo-parent educational assistance, 4Ps-aligned grants.",
  },
};

export function MatchMethodologyPage() {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-600 dark:text-primary-400">
          Match methodology
        </p>
        <h1 className="mt-2 text-3xl font-bold text-slate-900 dark:text-slate-100">
          Why your match score is weighted this way
        </h1>
        <p className="mt-4 text-lg leading-relaxed text-slate-600 dark:text-slate-400">
          ISKONNECT scores measure how well your profile fits a scholarship&apos;s published rules—not your odds of winning.
          This page explains the research thinking behind each factor, how we balance fairness, and what we plan to improve.
        </p>

        <div className="mt-8 rounded-2xl border border-primary-200 bg-primary-50 p-6 shadow-sm dark:border-primary-800 dark:bg-slate-900">
          <p className="text-sm leading-relaxed text-slate-900 dark:text-slate-100">
            <strong className="font-semibold text-primary-900 dark:text-primary-200">
              A high match score means strong eligibility fit, not a guarantee of acceptance.
            </strong>{" "}
            Providers may consider interviews, essays, quotas, and other factors ISKONNECT cannot see. Use scores to
            prioritize where to invest your time—not as a prediction of outcome.
          </p>
        </div>

        <div className="mt-10 space-y-4">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Weighting philosophy</h2>
          <p className="text-sm leading-relaxed text-slate-700 dark:text-slate-300">
            Weights reflect how often each dimension appears as a decisive eligibility rule across Philippine scholarship
            programs. Academic performance and financial need together account for most of the score because they are the
            most common published gates. Field of study and location matter when programs are course- or region-specific.
            Priority groups receive a smaller but meaningful share because they apply to targeted equity programs—not
            every listing.
          </p>
          <p className="text-sm leading-relaxed text-slate-700 dark:text-slate-300">
            When a scholarship has no geographic or field restriction, that factor is excluded and the remaining weights are
            renormalized so the total still reflects a fair comparison.
          </p>
        </div>

        <div className="mt-10">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Factor-by-factor rationale</h2>
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
                    <span className="rounded-full bg-primary-100 px-2.5 py-0.5 text-xs font-semibold text-primary-800 dark:bg-primary-900/50 dark:text-primary-200">
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

        <div className="mt-10 space-y-4">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Fairness commitments</h2>
          <ul className="list-disc space-y-2 pl-5 text-sm leading-relaxed text-slate-700 dark:text-slate-300">
            <li>Hard eligibility rules are applied before scoring—programs you clearly cannot qualify for are filtered out.</li>
            <li>Merit-only programs do not penalize students for income data; need-based programs weight financial fit appropriately.</li>
            <li>Priority-group scoring reflects published program criteria, not assumptions about your background.</li>
            <li>Scores are explainable: every match shows which factors helped or held you back.</li>
          </ul>
        </div>

        <div className="mt-10 rounded-2xl border border-amber-200 bg-amber-50 p-6 dark:border-amber-800 dark:bg-amber-950/30">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Current limitations</h2>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm leading-relaxed text-slate-700 dark:text-slate-300">
            <li>We cannot see essay quality, interviews, or provider-internal quotas.</li>
            <li>Some scholarships publish incomplete criteria; we flag those as needing verification.</li>
            <li>Document readiness is tracked separately—it does not change your eligibility fit score.</li>
            <li>Weights are calibrated for Philippine undergraduate and TVET programs; graduate-specific rules are still expanding.</li>
          </ul>
        </div>

        <div className="mt-10 space-y-4">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Future improvements</h2>
          <ul className="list-disc space-y-2 pl-5 text-sm leading-relaxed text-slate-700 dark:text-slate-300">
            <li>Community feedback loops to refine weights as we learn which factors students find most useful.</li>
            <li>More granular course alignment using PSCED taxonomy updates.</li>
            <li>Transparent changelogs whenever scoring policy versions change.</li>
            <li>Separate scoring profiles for merit-heavy vs. need-heavy program families where appropriate.</li>
          </ul>
        </div>

        <div className="mt-10 rounded-2xl border border-slate-200 bg-slate-50 p-6 dark:border-slate-600 dark:bg-slate-900">
          <p className="text-sm leading-relaxed text-slate-700 dark:text-slate-300">
            For the technical breakdown of each factor and score ranges, see{" "}
            <Link to="/transparency" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
              How your match score is built
            </Link>
            .
          </p>
        </div>

        <div className="mt-12">
          <BackNavLink />
        </div>
      </div>
    </section>
  );
}
