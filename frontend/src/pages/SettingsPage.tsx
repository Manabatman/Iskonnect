import { Link } from "react-router-dom";
import { useCallback, useEffect, useState } from "react";
import { useTheme } from "../contexts/ThemeContext";
import { useAuth } from "../contexts/AuthContext";
import { apiFetch } from "../api/client";
import { FEEDBACK_CATEGORIES, useFeedback } from "../components/FeedbackModal";
import { DeleteAccountModal } from "../components/DeleteAccountModal";
import { APP_RELEASE_DATE, APP_RELEASE_LABEL, APP_VERSION } from "../data/changelog";

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

function Toggle({
  checked,
  disabled,
  onChange,
  label,
}: {
  checked: boolean;
  disabled?: boolean;
  onChange: (next: boolean) => void;
  label: string;
}) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      aria-label={label}
      disabled={disabled}
      onClick={() => onChange(!checked)}
      className={[
        "relative inline-flex h-6 w-11 shrink-0 rounded-full transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500",
        disabled ? "cursor-not-allowed opacity-50" : "cursor-pointer",
        checked ? "bg-primary-600" : "bg-slate-200 dark:bg-slate-600",
      ].join(" ")}
    >
      <span
        className={[
          "pointer-events-none inline-block h-5 w-5 translate-y-0.5 rounded-full bg-white shadow transition",
          checked ? "translate-x-5" : "translate-x-0.5",
        ].join(" ")}
      />
    </button>
  );
}

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
  const { user, authHeaders } = useAuth();
  const { openFeedback } = useFeedback();
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [notifyDeadline, setNotifyDeadline] = useState(true);
  const [notifyNewMatch, setNotifyNewMatch] = useState(true);
  const [prefsLoading, setPrefsLoading] = useState(true);
  const [prefsSaving, setPrefsSaving] = useState(false);
  const [prefsError, setPrefsError] = useState<string | null>(null);
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);

  const savePref = useCallback(
    async (patch: { notify_deadline_reminders?: boolean; notify_new_matches?: boolean }) => {
      setPrefsSaving(true);
      setPrefsError(null);
      try {
        const res = await apiFetch("/api/v1/settings/notifications", {
          method: "PATCH",
          headers: { "Content-Type": "application/json", ...authHeaders() },
          body: JSON.stringify(patch),
        });
        if (!res.ok) throw new Error("Could not save notification settings");
        const data = (await res.json()) as {
          notify_deadline_reminders: boolean;
          notify_new_matches: boolean;
          notifications_globally_enabled: boolean;
        };
        setNotifyDeadline(data.notify_deadline_reminders);
        setNotifyNewMatch(data.notify_new_matches);
        setNotificationsEnabled(data.notifications_globally_enabled);
      } catch (e) {
        setPrefsError(e instanceof Error ? e.message : "Could not save settings");
      } finally {
        setPrefsSaving(false);
      }
    },
    [authHeaders]
  );

  useEffect(() => {
    if (!user) {
      setPrefsLoading(false);
      return;
    }
    let cancelled = false;
    setPrefsLoading(true);
    apiFetch("/api/v1/settings/notifications", { headers: authHeaders() })
      .then(async (res) => {
        if (!res.ok) return null;
        return res.json();
      })
      .then((data) => {
        if (cancelled || !data) return;
        setNotifyDeadline(Boolean(data.notify_deadline_reminders));
        setNotifyNewMatch(Boolean(data.notify_new_matches));
        setNotificationsEnabled(Boolean(data.notifications_globally_enabled));
      })
      .catch(() => {
        if (!cancelled) setPrefsError("Could not load notification settings");
      })
      .finally(() => {
        if (!cancelled) setPrefsLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [user, authHeaders]);

  const alertsActive = notifyDeadline || notifyNewMatch;

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
            Update Your Profile →
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

        <Card>
          <div className="flex flex-wrap items-center gap-2">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Alerts</h2>
            <span
              className={[
                "rounded-full px-2 py-0.5 text-xs font-semibold",
                alertsActive
                  ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-200"
                  : "bg-slate-200 text-slate-600 dark:bg-slate-700 dark:text-slate-300",
              ].join(" ")}
            >
              {alertsActive ? "Active" : "Off"}
            </span>
            {prefsSaving ? (
              <span className="text-xs text-slate-500 dark:text-slate-400">Saving…</span>
            ) : null}
          </div>
          <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
            Control in-app alerts for saved scholarships and strong new matches. Turning these off stops new
            notifications; it does not delete past ones.
          </p>
          {!notificationsEnabled ? (
            <p className="mt-2 text-sm text-amber-700 dark:text-amber-300">
              Notifications are disabled on this server (ENABLE_NOTIFICATIONS=false).
            </p>
          ) : null}
          {prefsError ? <p className="mt-2 text-sm text-red-600 dark:text-red-400">{prefsError}</p> : null}
          <div className="mt-5 space-y-4">
            <label className="flex items-start justify-between gap-4">
              <span>
                <span className="block text-sm font-medium text-slate-900 dark:text-slate-100">
                  Scholarship deadline reminders
                </span>
                <span className="mt-0.5 block text-xs text-slate-500 dark:text-slate-400">
                  In-app alert when a saved scholarship deadline is within 7 days
                </span>
              </span>
              <Toggle
                label="Scholarship deadline reminders"
                checked={notifyDeadline}
                disabled={prefsLoading || prefsSaving || !notificationsEnabled}
                onChange={(next) => {
                  setNotifyDeadline(next);
                  void savePref({ notify_deadline_reminders: next });
                }}
              />
            </label>
            <label className="flex items-start justify-between gap-4">
              <span>
                <span className="block text-sm font-medium text-slate-900 dark:text-slate-100">New match alerts</span>
                <span className="mt-0.5 block text-xs text-slate-500 dark:text-slate-400">
                  In-app alert when a new strong match appears after you run matching
                </span>
              </span>
              <Toggle
                label="New match alerts"
                checked={notifyNewMatch}
                disabled={prefsLoading || prefsSaving || !notificationsEnabled}
                onChange={(next) => {
                  setNotifyNewMatch(next);
                  void savePref({ notify_new_matches: next });
                }}
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
              Permanently removes your profile, match history, saved scholarships, and applications. Product feedback you
              submitted may be kept anonymously.
            </p>
            <button
              type="button"
              onClick={() => setDeleteModalOpen(true)}
              className="mt-3 rounded-lg border border-danger-200 bg-white px-3 py-2 text-sm font-semibold text-danger-600 hover:bg-danger-50 dark:border-danger-800 dark:bg-slate-900 dark:text-danger-400 dark:hover:bg-danger-950/30"
            >
              Delete account
            </button>
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
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
            Iskonnect {APP_RELEASE_LABEL} · v{APP_VERSION} · {APP_RELEASE_DATE}
          </p>
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
        {email ? (
          <DeleteAccountModal open={deleteModalOpen} onOpenChange={setDeleteModalOpen} userEmail={email} />
        ) : null}
      </div>
    </section>
  );
}
