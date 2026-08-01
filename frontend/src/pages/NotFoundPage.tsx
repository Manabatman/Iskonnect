import { Link } from "react-router-dom";
import { StateMessage } from "../components/StateMessage";
import { ERROR_COPY } from "../constants/errorCopy";

export function NotFoundPage() {
  return (
    <section className="py-24">
      <div className="mx-auto max-w-lg px-4">
        <StateMessage
          copy={ERROR_COPY.not_found}
          action={
            <div className="flex flex-col items-center gap-3 sm:flex-row sm:justify-center">
              <Link
                to="/"
                className="inline-flex rounded-xl bg-primary-600 px-6 py-3 font-semibold text-white hover:bg-primary-700"
              >
                Back to home
              </Link>
              <Link
                to="/scholarships/search"
                className="inline-flex rounded-xl border border-slate-300 px-6 py-3 font-semibold text-slate-700 hover:bg-slate-50 dark:border-slate-600 dark:text-slate-200 dark:hover:bg-slate-800"
              >
                Search scholarships
              </Link>
            </div>
          }
        />
      </div>
    </section>
  );
}
