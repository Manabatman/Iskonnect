import { Link } from "react-router-dom";

export function TransparencyPage() {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-600 dark:text-primary-400">Transparency</p>
        <h1 className="mt-2 text-3xl font-bold text-slate-900 dark:text-slate-100">How your match score is built</h1>
        <p className="mt-4 text-lg text-slate-600 dark:text-slate-400">
          See exactly why you qualify. ISKONNECT uses a deterministic pipeline: hard eligibility filters first, then weighted
          scoring.
        </p>

        <div className="mt-10 space-y-8 text-slate-700 dark:text-slate-300">
          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">1. Hard filters (must pass)</h2>
            <p className="mt-2">
              Scholarships that fail any required rule—such as region, education level, income ceiling, minimum GPA, or
              course alignment—are not shown. Scoring only runs on programs you can actually qualify for.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">2. What goes into the score</h2>
            <ul className="mt-3 list-inside list-disc space-y-1">
              <li>Academic performance (GWA / GPA where applicable)</li>
              <li>Household income and need indicators</li>
              <li>Field of study alignment with the program</li>
              <li>Geographic fit (region / city vs program rules)</li>
              <li>Equity and priority groups (e.g. 4Ps, IP, PWD) when declared</li>
            </ul>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Example breakdown (illustrative)</h2>
            <div className="mt-3 overflow-hidden rounded-xl border border-slate-200 dark:border-slate-600">
              <table className="w-full text-sm">
                <thead className="bg-slate-100 dark:bg-slate-800">
                  <tr>
                    <th className="px-3 py-2 text-left font-medium">Factor</th>
                    <th className="px-3 py-2 text-left font-medium">Sample weight</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 dark:divide-slate-700">
                  <tr>
                    <td className="px-3 py-2">Academic</td>
                    <td className="px-3 py-2">30%</td>
                  </tr>
                  <tr>
                    <td className="px-3 py-2">Income / need</td>
                    <td className="px-3 py-2">28%</td>
                  </tr>
                  <tr>
                    <td className="px-3 py-2">Field alignment</td>
                    <td className="px-3 py-2">22%</td>
                  </tr>
                  <tr>
                    <td className="px-3 py-2">Geographic</td>
                    <td className="px-3 py-2">10%</td>
                  </tr>
                  <tr>
                    <td className="px-3 py-2">Equity priority</td>
                    <td className="px-3 py-2">10%</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
              Actual weights may be tuned by administrators; always check the explanation on your match results page.
            </p>
          </section>
        </div>

        <div className="mt-12">
          <Link
            to="/register"
            className="inline-flex rounded-xl bg-primary-600 px-6 py-3 font-semibold text-white hover:bg-primary-700"
          >
            Get Started
          </Link>
        </div>
      </div>
    </section>
  );
}
