import { Link } from "react-router-dom";

export function NotFoundPage() {
  return (
    <section className="py-24">
      <div className="mx-auto max-w-lg px-4 text-center">
        <h1 className="text-4xl font-bold text-slate-900 dark:text-slate-100">404</h1>
        <p className="mt-2 text-lg text-slate-600 dark:text-slate-400">Page not found</p>
        <Link
          to="/"
          className="mt-6 inline-block rounded-xl bg-primary-600 px-6 py-3 font-semibold text-white hover:bg-primary-700"
        >
          Back to home
        </Link>
      </div>
    </section>
  );
}
