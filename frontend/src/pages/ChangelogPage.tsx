import { CHANGELOG_VERSIONS, type ChangelogItem } from "../data/changelog";
import { BackNavLink } from "../components/BackNavLink";

function ItemList({ heading, items }: { heading: string; items: ChangelogItem[] }) {
  if (!items.length) return null;
  return (
    <div className="mt-6">
      <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">{heading}</h3>
      <ul className="mt-3 space-y-4">
        {items.map((item) => (
          <li key={item.title}>
            <p className="font-medium text-slate-900 dark:text-slate-100">{item.title}</p>
            <p className="mt-1 text-sm leading-relaxed text-slate-600 dark:text-slate-400">{item.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export function ChangelogPage() {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Changelog</h1>
        <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
          What changed in Iskonnect. We keep notes practical and honest—this is an MVP that grows with feedback.
        </p>

        <div className="mt-10 space-y-10">
          {CHANGELOG_VERSIONS.map((release) => (
            <article
              key={release.version}
              className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800/80"
            >
              <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1 border-b border-slate-100 pb-4 dark:border-slate-700">
                <span className="rounded-md bg-primary-100 px-2.5 py-1 text-sm font-semibold text-primary-800 dark:bg-primary-900/40 dark:text-primary-200">
                  v{release.version}
                </span>
                <span className="text-sm text-slate-500 dark:text-slate-400">{release.date}</span>
              </div>
              <h2 className="mt-4 text-xl font-semibold text-slate-900 dark:text-slate-100">{release.title}</h2>
              <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">{release.summary}</p>

              <ItemList heading="Fixes" items={release.fixes ?? []} />
              <ItemList heading="Improvements" items={release.improvements ?? []} />
              <ItemList heading="Behind the scenes" items={release.behindTheScenes ?? []} />
            </article>
          ))}
        </div>

        <div className="mt-12">
          <BackNavLink />
        </div>
      </div>
    </section>
  );
}
