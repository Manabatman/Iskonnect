import { Link } from "react-router-dom";

export function SuccessStoriesPage() {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-2xl px-4 text-center">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Student outcomes</h1>
        <p className="mt-4 text-slate-600 dark:text-slate-400">
          We don&apos;t publish student outcome stories yet. ISKONNECT is still building its catalog and verification
          process — we&apos;d rather be honest about that than imply results we haven&apos;t verified.
        </p>
        <div className="mt-10 rounded-2xl border border-dashed border-slate-300 bg-slate-50/80 p-8 dark:border-slate-600 dark:bg-slate-800/40">
          <p className="text-sm text-slate-600 dark:text-slate-300">
            If you used ISKONNECT to find a scholarship, you can share feedback from your dashboard settings — we read
            every message, but we won&apos;t quote you as a &ldquo;success story&rdquo; without explicit consent.
          </p>
        </div>
        <p className="mt-10 text-sm text-slate-500 dark:text-slate-400">
          <Link to="/register" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
            Get started
          </Link>{" "}
          to build your profile and see which programs you can check against today.
        </p>
      </div>
    </section>
  );
}
