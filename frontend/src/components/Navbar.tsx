import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { useTheme } from "../contexts/ThemeContext";

const navLinkClass = (active: boolean) =>
  [
    "text-sm transition focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 rounded px-1",
    active
      ? "font-medium text-primary-600 dark:text-primary-400"
      : "text-slate-600 hover:text-primary-600 dark:text-slate-400 dark:hover:text-primary-400",
  ].join(" ");

export function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { resolvedTheme } = useTheme();
  const path = location.pathname;
  const brandLogoSrc = resolvedTheme === "dark" ? "/images/logo-dark.svg" : "/images/logo.svg";

  const isActive = (to: string) => (to === "/" ? path === "/" : path === to || path.startsWith(`${to}/`));

  return (
    <header className="border-b border-slate-200 bg-white dark:border-slate-700 dark:bg-slate-800">
      <div className="mx-auto flex max-w-6xl flex-col gap-4 px-4 py-4 sm:flex-row sm:items-center sm:justify-between">
        <Link to="/" className="flex shrink-0 items-center gap-3">
          <img
            src={brandLogoSrc}
            alt=""
            className="h-10 w-10"
            width={40}
            height={40}
            onError={(e) => {
              (e.target as HTMLImageElement).src = "/images/logo.svg";
            }}
          />
          <span>
            <span className="block font-sans text-xl font-black uppercase tracking-[0.06em] text-primary-700 dark:text-primary-400 sm:text-2xl">
              ISKONNECT
            </span>
            <span className="block text-xs font-medium text-slate-500 dark:text-slate-400">
              Connecting Filipino Students to Opportunity
            </span>
          </span>
        </Link>

        <nav className="flex flex-wrap items-center gap-x-4 gap-y-2 sm:gap-x-5" aria-label="Primary">
          <Link to="/how-it-works" className={navLinkClass(isActive("/how-it-works"))}>
            How it works
          </Link>
          <Link to="/scholarships/search" className={navLinkClass(path.startsWith("/scholarships"))}>
            Scholarships
          </Link>
          <Link to="/transparency" className={navLinkClass(isActive("/transparency"))}>
            Transparency
          </Link>
        </nav>

        <div className="flex flex-wrap items-center gap-2 sm:justify-end">
          {user ? (
            <>
              <Link
                to="/dashboard"
                className={navLinkClass(path.startsWith("/dashboard"))}
              >
                Dashboard
              </Link>
              <span className="hidden text-sm text-slate-500 dark:text-slate-400 sm:inline max-w-[10rem] truncate" title={user.email}>
                {user.email}
              </span>
              <button
                type="button"
                onClick={() => {
                  logout();
                  navigate("/");
                }}
                className="text-sm text-slate-600 hover:text-primary-600 dark:text-slate-400 dark:hover:text-primary-400"
              >
                Log out
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="text-sm font-medium text-slate-600 hover:text-primary-600 dark:text-slate-400 dark:hover:text-primary-400"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="inline-flex items-center rounded-lg bg-primary-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-slate-800"
              >
                Get Started
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
