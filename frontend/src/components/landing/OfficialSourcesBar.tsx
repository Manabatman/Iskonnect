import { officialSources } from "./landingData";
import { Reveal } from "./Reveal";

export function OfficialSourcesBar() {
  return (
    <section className="border-b border-slate-200 bg-white py-10 dark:border-slate-800 dark:bg-slate-950" data-testid="landing-sources">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <Reveal>
          <div className="flex flex-col items-center gap-4">
            <p className="text-sm font-semibold uppercase tracking-wider text-slate-600 dark:text-slate-300">
              Programs sourced from official providers
            </p>
            <ul className="flex flex-wrap items-center justify-center gap-2.5">
              {officialSources.map((name) => (
                <li
                  key={name}
                  className="inline-flex items-center gap-1.5 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200"
                >
                  <span aria-hidden className="h-1.5 w-1.5 rounded-full bg-primary-500" />
                  {name}
                </li>
              ))}
            </ul>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
