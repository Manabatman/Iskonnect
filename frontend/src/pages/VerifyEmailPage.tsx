import { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { apiFetch } from "../api/client";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";

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

        {status === "loading" && (
          <p className="mt-6 text-sm text-slate-600 dark:text-slate-400" role="status">
            {message}
          </p>
        )}

        {status === "success" && (
          <Alert className="mt-6 border-green-200 bg-green-50 text-left dark:border-green-900 dark:bg-green-950/40">
            <AlertDescription className="text-green-800 dark:text-green-300">{message}</AlertDescription>
          </Alert>
        )}

        {status === "error" && (
          <Alert variant="destructive" className="mt-6 text-left">
            <AlertDescription>{message}</AlertDescription>
          </Alert>
        )}

        {status !== "loading" && (
          <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:justify-center">
            <Button asChild size="lg">
              <Link to="/login">Sign in</Link>
            </Button>
            {status === "error" && (
              <Button asChild variant="outline" size="lg">
                <Link to="/register">Create account</Link>
              </Button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
