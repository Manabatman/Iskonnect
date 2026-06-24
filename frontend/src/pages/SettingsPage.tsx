import { Link } from "react-router-dom";
import { useTheme } from "../contexts/ThemeContext";
import { useAuth } from "../contexts/AuthContext";
import { FEEDBACK_CATEGORIES, useFeedback } from "../components/FeedbackModal";

function emailToDisplayName(email: string): string {
  const local = email.split("@")[0] ?? "";
  if (!local) return "";
  return local
    .replace(/[._-]+/g, " ")
    .split(" ")
    .filter(Boolean)
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase())
    .join(" ");
}

function initialsFromEmail(email: string): string {
  const local = email.split("@")[0] ?? "";
  if (!local) return "?";
  const parts = local.replace(/[^a-zA-Z0-9]/g, " ").trim().split(/\s+/);
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }
  return local.slice(0, 2).toUpperCase();
}

function IconSun({ className }: { className?: string }) {
  return (
    <svg className={className} width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden>
      <path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2v2zm18 0h2v-2h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 21v2h2v-2h-2zm0-18V3h2v2h-2zm5.66 1.77l1.41-1.41-1.41-1.41-1.41 1.41 1.41 1.41zm-12.02 12.02l1.41-1.41-1.41-1.41-1.41 1.41 1.41 1.41zm12.02 0l1.41 1.41 1.41-1.41-1.41-1.41-1.41 1.41zM4.93 4.93l1.41 1.41 1.41-1.41-1.41-1.41-1.41 1.41z" />
    </svg>
  );
}

function IconMoon({ className }: { className?: string }) {
  return (
    <svg className={className} width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden>
      <path d="M12.34 2.02C6.59 1.82 2 6.42 2 12c0 5.52 4.48 10 10 10 3.71 0 6.93-2.02 8.66-5.02-8.49-.5-15.3-7.35-15.32-15.96z" />
    </svg>
  );
}

function IconMonitor({ className }: { className?: string }) {
  return (
    <svg className={className} width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden>
      <path d="M20 3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h4v2h8v-2h4c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 13H4V5h16v11z" />
    </svg>
  );
}

const themeOptions = [
  { id: "light" as const, label: "Light", Icon: IconSun },
  { id: "dark" as const, label: "Dark", Icon: IconMoon },
  { id: "system" as const, label: "System", Icon: IconMonitor },
];

function Card({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <section
      className={`rounded-2xl border border-slate-200 bg-white p-6 dark:border-slate-700 dark:bg-slate-800/50 ${className}`}
    >
      {children}
    </section>
  );
}

export function SettingsPage() {
  const { theme, setTheme } = useTheme();
  const { user } = useAuth();
  const { openFeedback } = useFeedback();

  const email = user?.email ?? "";
  const displayName = email ? emailToDisplayName(email) : "";
  const showNameEmpty = !displayName && !email;

  return (
    <section className="py-10">
      <div className="mx-auto max-w-2xl space-y-6 px-4">
        <header>
          <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Your Account</h1>
          <p className="mt-2 text-slate-600 dark:text-slate-400">Manage how Iskonnect works for you.</p>
        </header>

        <Card>
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Profile overview</h2>
          <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
            Your account and scholarship profile are linked.
          </p>
          <div className="mt-5 flex flex-col gap-4 sm:flex-row sm:items-center">
            <div
              className="flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-primary-100 text-lg font-bold text-primary-700 dark:bg-primary-900/40 dark:text-primary-300"
              aria-hidden
            >
              {email ? initialsFromEmail(email) : "?"}
            </div>
            <div className="min-w-0 flex-1">
              {showNameEmpty ? (
                <p className="italic text-slate-400 dark:text-slate-500">
                  Complete your profile to see your name here
                </p>
              ) : (
                <>
                  <p className="font-semibold text-slate-900 dark:text-slate-100">
                    {displayName || "Iskonnect member"}
                  </p>
                  {email ? (
                    <p className="mt-0.5 truncate text-sm text-slate-600 dark:text-slate-400">{email}</p>
                  ) : null}
                </>
              )}
            </div>
          </div>
          <p className="mt-4 text-xs italic text-slate-500 dark:text-slate-400">
            Your profile directly affects your match scores. Keep it up to date.
          </p>
          <Link
            to="/profile-builder"
            className="mt-4 inline-flex items-center rounded-xl bg-primary-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-primary-700"
          >
            Update Scholarship Profile →
          </Link>
        </Card>

        <Card>
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Display</h2>
          <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
            Choose how Iskonnect looks on your device.
          </p>
          <div className="mt-4 flex flex-wrap gap-2">
            {themeOptions.map(({ id, label, Icon }) => {
              const selected = theme === id;
              return (
                <button
                  key={id}
                  type="button"
                  onClick={() => setTheme(id)}
                  className={[
                    "inline-flex items-center gap-2 rounded-xl border px-4 py-2.5 text-sm font-medium transition",
                    selected
                      ? "border-primary-500 bg-primary-50 text-primary-800 ring-2 ring-primary-500 dark:border-primary-500 dark:bg-primary-900/30 dark:text-primary-200"
                      : "border-slate-200 bg-slate-50 text-slate-700 hover:bg-slate-100 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700",
                  ].join(" ")}
                >
                  <Icon className="opacity-90" />
                  {label}
                </button>
              );
            })}
          </div>
        </Card>

        <Card className="opacity-60">
          <div className="flex flex-wrap items-center gap-2">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Alerts</h2>
            <span className="rounded-full bg-highlight-100 px-2 py-0.5 text-xs font-semibold text-highlight-800 dark:bg-highlight-900/40 dark:text-highlight-200">
              Coming soon
            </span>
          </div>
          <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
            Notification preferences will be available in a future update.
          </p>
          <div className="pointer-events-none mt-5 space-y-4 cursor-not-allowed">
            <label className="flex cursor-not-allowed items-start justify-between gap-4">
              <span>
                <span className="block text-sm font-medium text-slate-900 dark:text-slate-100">
                  Scholarship deadline reminders
                </span>
                <span className="mt-0.5 block text-xs text-slate-500 dark:text-slate-400">
                  Get notified 2 weeks before a deadline closes
                </span>
              </span>
              <span
                className="relative inline-flex h-6 w-11 shrink-0 rounded-full bg-slate-200 dark:bg-slate-600"
                aria-hidden
              />
            </label>
            <label className="flex cursor-not-allowed items-start justify-between gap-4">
              <span>
                <span className="block text-sm font-medium text-slate-900 dark:text-slate-100">New match alerts</span>
                <span className="mt-0.5 block text-xs text-slate-500 dark:text-slate-400">
                  When a new scholarship matches your profile
                </span>
              </span>
              <span
                className="relative inline-flex h-6 w-11 shrink-0 rounded-full bg-slate-200 dark:bg-slate-600"
                aria-hidden
              />
            </label>
          </div>
        </Card>

        <Card>
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Privacy &amp; data</h2>
          <ul className="mt-4 space-y-2">
            <li>
              <Link to="/terms" className="text-sm font-medium text-primary-600 hover:underline dark:text-primary-400">
                Terms of Service
              </Link>
            </li>
            <li>
              <Link to="/privacy" className="text-sm font-medium text-primary-600 hover:underline dark:text-primary-400">
                Privacy Policy
              </Link>
            </li>
          </ul>
          <div className="mt-4 flex flex-wrap items-center gap-2">
            <button
              type="button"
              disabled
              className="cursor-not-allowed rounded-lg border border-slate-200 px-3 py-2 text-sm font-medium text-slate-400 opacity-70 dark:border-slate-600"
            >
              Download my data
            </button>
            <span className="text-xs font-medium text-slate-500 dark:text-slate-400">Coming soon</span>
          </div>

          <div className="mt-8 rounded-xl border border-danger-100 p-4 dark:border-danger-900/40">
            <h3 className="text-sm font-semibold text-danger-600 dark:text-danger-400">Delete account</h3>
            <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
              This removes your profile, matches, and saved scholarships permanently.
            </p>
            <button
              type="button"
              disabled
              className="mt-3 cursor-not-allowed rounded-lg border border-danger-200 bg-white px-3 py-2 text-sm font-semibold text-danger-400 opacity-70 dark:border-danger-800 dark:bg-slate-900 dark:text-danger-500"
            >
              Request deletion
            </button>
            <span className="ml-2 text-xs font-medium text-slate-500 dark:text-slate-400">Coming soon</span>
          </div>
        </Card>

        <Card>
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Help us improve</h2>
          <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">Found a bug? Have an idea? Tell us.</p>
          <div className="mt-4 grid grid-cols-1 gap-2 sm:grid-cols-3">
            {FEEDBACK_CATEGORIES.map(({ id, heading, subtext, Icon }) => (
              <button
                key={id}
                type="button"
                onClick={() => openFeedback(id)}
                className="flex flex-col items-start gap-1 rounded-xl border border-slate-200 bg-slate-50/80 p-3 text-left text-sm transition hover:border-primary-300 hover:bg-primary-50/40 dark:border-slate-600 dark:bg-slate-800/50 dark:hover:border-primary-600"
              >
                <Icon className="h-5 w-5 text-primary-600 dark:text-primary-400" />
                <span className="font-semibold text-slate-900 dark:text-slate-100">{heading}</span>
                <span className="text-xs text-slate-600 dark:text-slate-400">{subtext}</span>
              </button>
            ))}
          </div>
        </Card>

        <Card>
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">About</h2>
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">Iskonnect v1.5.0</p>
          <ul className="mt-4 flex flex-col gap-2 text-sm">
            <li>
              <Link to="/changelog" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
                Changelog
              </Link>
            </li>
            <li>
              <Link to="/about" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
                About
              </Link>
            </li>
            <li>
              <Link to="/how-it-works" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
                How it works
              </Link>
            </li>
            <li>
              <Link to="/transparency" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
                Transparency
              </Link>
            </li>
          </ul>
        </Card>

        <div>
          <Link
            to="/dashboard"
            className="inline-flex items-center text-sm font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400"
          >
            ← Back to Dashboard
          </Link>
        </div>
      </div>
    </section>
  );
}
