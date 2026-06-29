import { Link } from "react-router-dom";
import { BackNavLink } from "../components/BackNavLink";

const reasons = [
  {
    title: "They never heard about it",
    problem:
      "Scholarships are announced on different government portals, university sites, LGU Facebook pages, and foundation newsletters—often with no single place to search.",
    solution:
      "ISKONNECT brings programs from CHED, DOST-SEI, TESDA, LGUs, universities, and private foundations into one catalog you can browse and match against your profile.",
  },
  {
    title: "They missed the deadline",
    problem:
      "Application windows can be short. By the time a student finds a program, the deadline may already have passed.",
    solution:
      "Your scholarship plan shows what's open now, what's opening soon, and what's expected to reopen—so you can prepare before the rush.",
  },
  {
    title: "They weren't eligible yet",
    problem:
      "Many programs require a specific grade level, GWA, or course. Students often discover a scholarship only after they've already missed the window to qualify.",
    solution:
      "ISKONNECT flags future eligibility—scholarships you might qualify for later—so you can plan ahead instead of learning about them too late.",
  },
  {
    title: "They didn't have time to prepare",
    problem:
      "Gathering documents, essays, and certificates takes weeks. Starting at the last minute means incomplete applications.",
    solution:
      "Document checklists, preparation reminders, and early visibility into upcoming cycles give you time to get ready before applications open.",
  },
  {
    title: "The information was confusing or outdated",
    problem:
      "Deadlines change, links break, and requirements differ between cycles. It's hard to know what still applies.",
    solution:
      "We verify listings against official sources, show when information was last checked, and link you to the provider's site so you can confirm details yourself.",
  },
] as const;

export function WhyIskonnectPage() {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Why ISKONNECT exists</h1>
        <p className="mt-3 text-base leading-relaxed text-slate-600 dark:text-slate-400">
          Filipino students deserve a fair shot at scholarships—not just those who already know where to look. ISKONNECT
          was built because too many qualified students miss opportunities they could have reached.
        </p>

        <div className="mt-10 rounded-xl border border-primary-200 bg-primary-50/60 p-6 dark:border-primary-800 dark:bg-primary-950/30">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Our mission</h2>
          <p className="mt-2 leading-relaxed text-slate-700 dark:text-slate-300">
            Help Filipino students discover scholarships they qualify for—today, soon, or in the future—and give them
            enough time and clarity to apply with confidence.
          </p>
        </div>

        <div className="mt-12 space-y-10">
          <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-100">
            Five reasons students miss scholarships
          </h2>
          {reasons.map((item, i) => (
            <article key={item.title} className="border-l-4 border-primary-500 pl-5">
              <p className="text-xs font-semibold uppercase tracking-wide text-primary-600 dark:text-primary-400">
                Reason {i + 1}
              </p>
              <h3 className="mt-1 text-lg font-semibold text-slate-900 dark:text-slate-100">{item.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">{item.problem}</p>
              <p className="mt-3 text-sm leading-relaxed text-slate-700 dark:text-slate-300">
                <span className="font-medium text-emerald-700 dark:text-emerald-400">How ISKONNECT helps: </span>
                {item.solution}
              </p>
            </article>
          ))}
        </div>

        <div className="mt-12 rounded-xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800/80">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Ready to start?</h2>
          <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">
            Build your profile once and see your scholarship plan—matches you can apply for now, programs to prepare for,
            and opportunities to watch for next cycle.
          </p>
          <div className="mt-4 flex flex-wrap gap-3">
            <Link
              to="/register"
              className="rounded-lg bg-primary-600 px-4 py-2 text-sm font-semibold text-white hover:bg-primary-700"
            >
              Create free account
            </Link>
            <Link
              to="/how-we-verify"
              className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 dark:border-slate-600 dark:text-slate-200 dark:hover:bg-slate-700"
            >
              How we verify scholarships
            </Link>
          </div>
        </div>

        <div className="mt-12">
          <BackNavLink />
        </div>
      </div>
    </section>
  );
}
