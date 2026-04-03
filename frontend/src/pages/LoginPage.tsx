import { FormEvent, useEffect, useState, useCallback } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { AuthDirectionalOverlay } from "../components/visual/DirectionalImageOverlays";
import { useAuth } from "../contexts/AuthContext";

const AUTH_PANEL_PRIMARY = "/images/auth/login-illustration.jpg";
const AUTH_PANEL_FALLBACK = "/images/hero/hero-1.svg";

function safeReturnPath(from: unknown): string | null {
  if (typeof from !== "string" || !from.startsWith("/")) return null;
  if (from.startsWith("//")) return null;
  return from;
}

export function LoginPage() {
  const { login, user, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const returnTo = safeReturnPath((location.state as { from?: string } | null)?.from);

  useEffect(() => {
    if (!authLoading && user) {
      navigate(returnTo ?? "/dashboard", { replace: true });
    }
  }, [authLoading, user, navigate, returnTo]);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [authPanelSrc, setAuthPanelSrc] = useState(AUTH_PANEL_PRIMARY);
  const [brandLogoSrc, setBrandLogoSrc] = useState("/images/logo.png");

  const handleBrandLogoError = useCallback(() => {
    setBrandLogoSrc("/images/logo.svg");
  }, []);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(email, password);
      navigate(returnTo ?? "/dashboard", { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-[calc(100vh-4rem)] flex-col md:flex-row">
      {/* Left — visual + trust copy (no testimonials) */}
      <div className="relative hidden min-h-[280px] flex-1 md:block md:min-h-0">
        <img
          src={authPanelSrc}
          alt=""
          decoding="async"
          loading="lazy"
          onError={() => setAuthPanelSrc((s) => (s === AUTH_PANEL_PRIMARY ? AUTH_PANEL_FALLBACK : s))}
          className="absolute inset-0 h-full w-full object-cover"
        />
        <AuthDirectionalOverlay />
        <div className="relative z-10 flex h-full min-h-[420px] flex-col justify-end p-8 lg:p-12">
          <img
            src={brandLogoSrc}
            alt="ISKONNECT"
            width={40}
            height={40}
            onError={handleBrandLogoError}
            className="absolute left-8 top-8 h-10 w-10 lg:left-12 lg:top-12"
          />
          <p className="max-w-md text-lg font-medium leading-relaxed text-white lg:text-xl">
            Built for Filipino students navigating scholarships and programs — with transparency,
            clarity, and control.
          </p>
        </div>
      </div>

      {/* Right — form */}
      <div className="flex flex-1 items-center justify-center bg-slate-50 px-4 py-12 dark:bg-slate-950 md:py-0">
        <div className="glass w-full max-w-md rounded-2xl p-8 shadow-xl dark:bg-slate-800/70">
          <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Welcome back</h2>
          <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">Sign in to continue your scholarship journey.</p>
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
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                Password
              </label>
              <input
                id="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mt-1 w-full rounded-xl border border-slate-300 bg-white/80 px-3 py-2.5 text-slate-900 backdrop-blur dark:border-slate-600 dark:bg-slate-900/50 dark:text-slate-100"
                autoComplete="current-password"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-2xl bg-primary-600 px-4 py-3 font-semibold text-white shadow-lg shadow-primary-600/20 transition hover:bg-primary-700 disabled:opacity-70"
            >
              {loading ? "Signing in…" : "Sign in"}
            </button>
          </form>
          <p className="mt-6 text-center text-sm text-slate-600 dark:text-slate-400">
            Don&apos;t have an account?{" "}
            <Link to="/register" className="font-semibold text-primary-600 hover:text-primary-700 dark:text-primary-400">
              Register
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
