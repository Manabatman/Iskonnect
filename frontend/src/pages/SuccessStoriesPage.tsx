import { Link } from "react-router-dom";

export function SuccessStoriesPage() {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-2xl px-4 text-center">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Success stories</h1>
        <p className="mt-4 text-slate-600 dark:text-slate-400">
          We are collecting real stories from Filipino students who found scholarships through Iskonnect.
          Check back soon — or share your experience through the feedback option in your dashboard.
        </p>
        <div className="mt-10 rounded-2xl border border-dashed border-slate-300 bg-slate-50/80 p-8 dark:border-slate-600 dark:bg-slate-800/40">
          <p className="text-sm text-slate-500 dark:text-slate-400">Stories coming soon</p>
        </div>
        <p className="mt-10 text-sm text-slate-500 dark:text-slate-400">
          <Link to="/register" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
            Get started
          </Link>{" "}
          to build your profile and find programs matched to you.
        </p>
      </div>
    </section>
  );
}
