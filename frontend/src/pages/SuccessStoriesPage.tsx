import { Link } from "react-router-dom";

const placeholders = [
  {
    name: "Maria S.",
    location: "Visayas",
    school: "State university",
    program: "Regional STEM grant (placeholder)",
    quote: "Having one profile and clear match reasons saved me weeks of guessing which programs fit.",
    initials: "MS",
  },
  {
    name: "Juan R.",
    location: "Metro Manila",
    school: "City college",
    program: "Need-based aid (placeholder)",
    quote: "I could focus on applications instead of hunting every website separately.",
    initials: "JR",
  },
  {
    name: "Alex T.",
    location: "Mindanao",
    school: "Provincial university",
    program: "LGU-supported scholarship (placeholder)",
    quote: "The deadline reminders helped me submit on time.",
    initials: "AT",
  },
] as const;

export function SuccessStoriesPage() {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-5xl px-4">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Success stories</h1>
        <p className="mt-2 text-slate-600 dark:text-slate-400">
          Stories will be updated as students share their experiences. Below are illustrative placeholders.
        </p>

        <div className="mt-10 grid gap-6 md:grid-cols-3">
          {placeholders.map((s) => (
            <blockquote
              key={s.name}
              className="glass flex flex-col rounded-2xl p-6 shadow-md transition hover:-translate-y-0.5 hover:shadow-lg"
            >
              <div className="flex items-start gap-3">
                <div
                  className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-primary-500 to-primary-700 text-sm font-bold text-white"
                  aria-hidden
                >
                  {s.initials}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <p className="font-semibold text-slate-900 dark:text-slate-100">{s.name}</p>
                    <span className="rounded-full bg-slate-200/80 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-slate-600 dark:bg-slate-600/50 dark:text-slate-300">
                      Sample story
                    </span>
                  </div>
                  <p className="text-xs text-slate-500 dark:text-slate-400">{s.location}</p>
                  <p className="text-xs text-slate-400">{s.school}</p>
                </div>
              </div>
              <p className="mt-4 text-sm italic leading-relaxed text-slate-700 dark:text-slate-300">
                &ldquo;{s.quote}&rdquo;
              </p>
              <p className="mt-3 text-xs text-slate-400">{s.program}</p>
            </blockquote>
          ))}
        </div>

        <p className="mt-10 text-center text-sm text-slate-500 dark:text-slate-400">
          <Link to="/register" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
            Get started
          </Link>{" "}
          to build your profile and find programs matched to you.
        </p>
      </div>
    </section>
  );
}
