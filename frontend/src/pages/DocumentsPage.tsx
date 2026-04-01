import { Link } from "react-router-dom";

export function DocumentsPage() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6">
      <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Document vault</h1>
      <p className="mt-3 text-slate-600 dark:text-slate-400">
        We&apos;re building a simple way to track which requirements you have ready and link out to official uploads.
        Full file storage isn&apos;t available yet — for now, use{" "}
        <Link to="/applications" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
          Applications
        </Link>{" "}
        to track saved programs and{" "}
        <Link to="/profile-builder" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
          your profile
        </Link>{" "}
        for documents you&apos;ve already declared.
      </p>
      <p className="mt-4 rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600 dark:border-slate-600 dark:bg-slate-800/50 dark:text-slate-300">
        <strong className="text-slate-800 dark:text-slate-100">Planned for a later release:</strong> optional uploads or
        checklist-only tracking, with cloud integrations (e.g. Google Drive) only after the core MVP is stable.
      </p>
    </div>
  );
}
