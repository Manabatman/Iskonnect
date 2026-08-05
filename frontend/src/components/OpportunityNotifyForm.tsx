import { useState } from "react";
import { apiFetch } from "../api/client";
import { validateEmail } from "../utils/validateEmail";

interface OpportunityNotifyFormProps {
  opportunitySlug: string;
  opportunityLabel: string;
}

/** Email capture for upcoming opportunity verticals (Wave 6). */
export function OpportunityNotifyForm({ opportunitySlug, opportunityLabel }: OpportunityNotifyFormProps) {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "done" | "error">("idle");
  const [message, setMessage] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = email.trim();
    const check = validateEmail(trimmed);
    if (!check.valid) {
      setStatus("error");
      setMessage(check.message ?? "Enter a valid email address.");
      return;
    }
    setStatus("loading");
    setMessage(null);
    try {
      const res = await apiFetch("/api/v1/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          category: "opportunity_notify",
          message: `Notify when ${opportunityLabel} launches (${opportunitySlug}).`,
          contact_email: trimmed,
        }),
      });
      if (!res.ok) throw new Error("Could not save your request.");
      setStatus("done");
      setMessage("You're on the list — we'll email you when this launches.");
      setEmail("");
    } catch (err) {
      setStatus("error");
      setMessage(err instanceof Error ? err.message : "Something went wrong. Try again.");
    }
  };

  return (
    <form onSubmit={(e) => void handleSubmit(e)} className="space-y-3">
      <label htmlFor="opportunity-notify-email" className="block text-sm font-medium text-slate-800 dark:text-slate-200">
        Get notified when {opportunityLabel} launches
      </label>
      <div className="flex flex-col gap-2 sm:flex-row">
        <input
          id="opportunity-notify-email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@school.edu.ph"
          disabled={status === "loading" || status === "done"}
          className="focus-visible-ring min-h-[44px] flex-1 rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm dark:border-slate-600 dark:bg-slate-900"
          autoComplete="email"
        />
        <button
          type="submit"
          disabled={status === "loading" || status === "done"}
          className="focus-visible-ring min-h-[44px] shrink-0 rounded-xl bg-primary-600 px-5 py-2 text-sm font-semibold text-white hover:bg-primary-700 disabled:opacity-60"
        >
          {status === "loading" ? "Saving…" : "Notify me"}
        </button>
      </div>
      {message ? (
        <p
          className={`text-sm ${status === "error" ? "text-red-700 dark:text-red-300" : "text-emerald-800 dark:text-emerald-200"}`}
          role={status === "error" ? "alert" : "status"}
        >
          {message}
        </p>
      ) : null}
    </form>
  );
}
