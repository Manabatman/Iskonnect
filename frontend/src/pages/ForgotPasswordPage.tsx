import { FormEvent, useState } from "react";
import { Link } from "react-router-dom";
import { apiFetch } from "../api/client";
import { validateEmail } from "../utils/validateEmail";

export function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    setMessage(null);
    const emailCheck = validateEmail(email);
    if (!emailCheck.valid) {
      setError(emailCheck.message ?? "Enter a valid email address.");
      return;
    }
    setLoading(true);
    try {
      const res = await apiFetch("/api/v1/auth/forgot-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error((data as { detail?: string }).detail ?? "Request failed");
      }
      setMessage("If that email exists, reset instructions have been sent. Check your inbox.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Request failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center bg-slate-50 px-4 py-12 dark:bg-slate-950">
      <div className="glass w-full max-w-md rounded-2xl p-8 shadow-xl dark:bg-slate-800/70">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Forgot password</h2>
        <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
          Enter your email and we&apos;ll send a link to reset your password.
        </p>
        <form onSubmit={handleSubmit} className="mt-8 space-y-4">
          {error && (
            <div className="rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700 dark:border-red-800 dark:bg-red-900/30 dark:text-red-300" role="alert">
              {error}
            </div>
          )}
          {message && (
            <div className="rounded-xl border border-green-200 bg-green-50 px-3 py-2 text-sm text-green-800 dark:border-green-800 dark:bg-green-900/30 dark:text-green-300" role="status">
              {message}
            </div>
          )}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-slate-700 dark:text-slate-300">
              Email
            </label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 w-full rounded-xl border border-slate-300 bg-white/80 px-3 py-2.5 text-slate-900 backdrop-blur dark:border-slate-600 dark:bg-slate-900/50 dark:text-slate-100"
              placeholder="you@example.com"
              autoComplete="email"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-2xl bg-primary-600 px-4 py-3 font-semibold text-white shadow-lg shadow-primary-600/20 transition hover:bg-primary-700 disabled:opacity-70"
          >
            {loading ? "Sending…" : "Send reset link"}
          </button>
        </form>
        <p className="mt-6 text-center text-sm text-slate-600 dark:text-slate-400">
          <Link to="/login" className="font-semibold text-primary-600 hover:text-primary-700 dark:text-primary-400">
            Back to sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
