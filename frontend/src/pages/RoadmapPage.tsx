import { Link } from "react-router-dom";
import { BackNavLink } from "../components/BackNavLink";
import {
  ROADMAP_COLUMN_LABELS,
  ROADMAP_DISCLAIMER,
  ROADMAP_ITEMS,
  type RoadmapColumn,
} from "../data/roadmap";

const COLUMN_ORDER: RoadmapColumn[] = ["planned", "in_progress", "shipped"];

export function RoadmapPage() {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-5xl px-4">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Product roadmap</h1>
        <p className="mt-3 max-w-3xl text-base leading-relaxed text-slate-600 dark:text-slate-400">
          {ROADMAP_DISCLAIMER}
        </p>
        <div className="mt-10 grid gap-6 md:grid-cols-3">
          {COLUMN_ORDER.map((column) => (
            <section
              key={column}
              className="rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-700 dark:bg-slate-900"
            >
              <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                {ROADMAP_COLUMN_LABELS[column]}
              </h2>
              <ul className="mt-3 space-y-2">
                {ROADMAP_ITEMS.filter((item) => item.column === column).map((item) => (
                  <li
                    key={item.id}
                    className="rounded-lg border border-slate-100 bg-slate-50 px-3 py-2 text-sm text-slate-800 dark:border-slate-800 dark:bg-slate-950/40 dark:text-slate-200"
                  >
                    {item.title}
                  </li>
                ))}
              </ul>
            </section>
          ))}
        </div>
        <p className="mt-8 text-sm text-slate-600 dark:text-slate-400">
          Have an idea?{" "}
          <Link to="/settings" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
            Send feedback from Settings
          </Link>
          .
        </p>
        <div className="mt-12">
          <BackNavLink />
        </div>
      </div>
    </section>
  );
}
