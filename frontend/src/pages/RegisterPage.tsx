import { FormEvent, useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { AuthDirectionalOverlay } from "../components/visual/DirectionalImageOverlays";
import { getPostAuthPath, useAuth } from "../contexts/AuthContext";
import { safeReturnPath } from "../utils/returnPath";
import { validateEmail } from "../utils/validateEmail";

const AUTH_PANEL_PRIMARY = "/images/auth/register-illustration.jpg";
const AUTH_PANEL_FALLBACK = "/images/hero/hero-2.svg";

export function RegisterPage() {
  const { register, user, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const returnTo = safeReturnPath((location.state as { from?: string } | null)?.from);

  useEffect(() => {
    if (!authLoading && user) {
      navigate(getPostAuthPath(user, returnTo), { replace: true });
    }
  }, [authLoading, user, navigate, returnTo]);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [authPanelSrc, setAuthPanelSrc] = useState(AUTH_PANEL_PRIMARY);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    if (password.length < 10) {
      setError("Password must be at least 10 characters");
      return;
    }
    const emailCheck = validateEmail(email);
    if (!emailCheck.valid) {
      setError(emailCheck.message ?? "Enter a valid email address.");
      return;
    }
    setLoading(true);
    try {
      const authUser = await register(email, password);
      navigate(getPostAuthPath(authUser, returnTo), { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-[calc(100vh-4rem)] flex-col md:flex-row">
      <div className="relative hidden min-h-[280px] flex-1 md:block md:min-h-0">
        <img
          src={authPanelSrc}
          alt=""
          width={800}
          height={600}
          decoding="async"
          loading="lazy"
          onError={() => setAuthPanelSrc((s) => (s === AUTH_PANEL_PRIMARY ? AUTH_PANEL_FALLBACK : s))}
          className="absolute inset-0 h-full w-full object-cover"
        />
        <AuthDirectionalOverlay />
        <div className="relative z-10 flex h-full min-h-[420px] flex-col justify-end p-8 lg:p-12">
          <p className="max-w-md text-lg font-medium leading-relaxed text-white lg:text-xl">
            Build your profile once — match to scholarships from government, universities, and private foundations across the Philippines.
          </p>
        </div>
      </div>

      <div className="flex flex-1 items-center justify-center bg-slate-50 px-4 py-12 dark:bg-slate-950 md:py-0">
        <div className="glass w-full max-w-md rounded-2xl p-8 shadow-xl dark:bg-slate-800/70">
          <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Create your account</h2>
          <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">Start matching in minutes — it&apos;s free.</p>
          <form onSubmit={handleSubmit} className="mt-8 space-y-4">
            {error && (
              <div
                className="rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700 dark:border-red-800 dark:bg-red-900/30 dark:text-red-300"
                role="alert"
              >
                {error}
              </div>
            )}
            <div>
              <label htmlFor="reg-email" className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                Email
              </label>
              <input
                id="reg-email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-1 w-full rounded-xl border border-slate-300 bg-white/80 px-3 py-2.5 text-slate-900 backdrop-blur dark:border-slate-600 dark:bg-slate-900/50 dark:text-slate-100"
                placeholder="you@example.com"
                autoComplete="email"
              />
            </div>
            <div>
              <label htmlFor="reg-password" className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                Password
              </label>
              <input
                id="reg-password"
                type="password"
                required
                minLength={10}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mt-1 w-full rounded-xl border border-slate-300 bg-white/80 px-3 py-2.5 text-slate-900 backdrop-blur dark:border-slate-600 dark:bg-slate-900/50 dark:text-slate-100"
                placeholder="At least 10 characters"
                autoComplete="new-password"
              />
              <p className="mt-0.5 text-xs text-slate-500 dark:text-slate-400">Minimum 10 characters</p>
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-2xl bg-primary-600 px-4 py-3 font-semibold text-white shadow-lg shadow-primary-600/20 transition hover:bg-primary-700 disabled:opacity-70"
            >
              {loading ? "Creating account…" : "Register"}
            </button>
          </form>
          <p className="mt-6 text-center text-sm text-slate-600 dark:text-slate-400">
            Already have an account?{" "}
            <Link to="/login" className="font-semibold text-primary-600 hover:text-primary-700 dark:text-primary-400">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
