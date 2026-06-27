import { officialSources } from "./landingData";
import { Reveal } from "./Reveal";

export function OfficialSourcesBar() {
  return (
    <section className="border-b border-slate-200 bg-white py-8 dark:border-slate-800 dark:bg-slate-950">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <Reveal>
          <div className="flex flex-col items-center gap-3">
            <p className="text-xs font-medium uppercase tracking-wider text-slate-500 dark:text-slate-400">
              Programs sourced from official providers
            </p>
            <ul className="flex flex-wrap items-center justify-center gap-2">
              {officialSources.map((name) => (
                <li
                  key={name}
                  className="inline-flex items-center gap-1.5 rounded-full border border-slate-200 bg-white px-3.5 py-1.5 text-sm font-medium text-slate-700 shadow-sm dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200"
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
