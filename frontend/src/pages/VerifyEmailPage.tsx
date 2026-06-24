import { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { apiFetch } from "../api/client";

export function VerifyEmailPage() {
  const [searchParams] = useSearchParams();
  const token = useMemo(() => searchParams.get("token")?.trim() ?? "", [searchParams]);
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const [message, setMessage] = useState("Verifying your email…");

  useEffect(() => {
    if (!token) {
      setStatus("error");
      setMessage("Missing verification token. Use the link from your registration email.");
      return;
    }
    let cancelled = false;
    (async () => {
      try {
        const res = await apiFetch("/api/v1/auth/verify-email", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ token }),
        });
        const data = await res.json().catch(() => ({}));
        if (cancelled) return;
        if (!res.ok) {
          setStatus("error");
          setMessage((data as { detail?: string }).detail ?? "Verification failed");
          return;
        }
        setStatus("success");
        setMessage("Email verified. You can sign in and start matching scholarships.");
      } catch {
        if (!cancelled) {
          setStatus("error");
          setMessage("Unable to reach the server. Try again later.");
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [token]);

  return (
    <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center bg-slate-50 px-4 py-12 dark:bg-slate-950">
      <div className="glass w-full max-w-md rounded-2xl p-8 shadow-xl dark:bg-slate-800/70 text-center">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Email verification</h2>
        <p
          className={`mt-6 text-sm ${
            status === "error"
              ? "text-red-700 dark:text-red-300"
              : status === "success"
                ? "text-green-800 dark:text-green-300"
                : "text-slate-600 dark:text-slate-400"
          }`}
          role={status === "loading" ? "status" : undefined}
        >
          {message}
        </p>
        {status !== "loading" && (
          <p className="mt-8">
            <Link
              to="/login"
              className="inline-block rounded-2xl bg-primary-600 px-6 py-3 font-semibold text-white shadow-lg shadow-primary-600/20 transition hover:bg-primary-700"
            >
              Sign in
            </Link>
          </p>
        )}
      </div>
    </div>
  );
}
