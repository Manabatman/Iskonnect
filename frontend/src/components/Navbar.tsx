import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { Menu, X } from "lucide-react";
import { useAuth } from "../contexts/AuthContext";
import { useTheme } from "../contexts/ThemeContext";
import { brandLogoSrc, BRAND_LOGO_NAV_CLASS, BRAND_LOGO_NAV_HEIGHT, BRAND_LOGO_NAV_WIDTH, LOGO_LIGHT_SRC } from "../lib/brandLogo";

const navLinkClass = (active: boolean) =>
  [
    "text-sm transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 rounded px-1",
    active
      ? "font-medium text-primary-600 dark:text-primary-400"
      : "text-slate-600 hover:text-primary-600 dark:text-slate-400 dark:hover:text-primary-400",
  ].join(" ");

const primaryNavClass =
  "inline-flex items-center rounded-xl bg-primary-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-primary-700 active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 dark:focus-visible:ring-offset-slate-900";

export function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { resolvedTheme } = useTheme();
  const path = location.pathname;
  const logoSrc = brandLogoSrc(resolvedTheme);

  const [mobileOpen, setMobileOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    setMobileOpen(false);
  }, [path]);

  const isActive = (to: string) => (to === "/" ? path === "/" : path === to || path.startsWith(`${to}/`));

  const navLinks = (
    <>
      <Link to="/how-it-works" className={navLinkClass(isActive("/how-it-works"))}>
        How it works
      </Link>
      <Link to="/scholarships/search" className={navLinkClass(path.startsWith("/scholarships"))}>
        Scholarships
      </Link>
      <Link to="/transparency" className={navLinkClass(isActive("/transparency"))}>
        Transparency
      </Link>
    </>
  );

  const authLinks = user ? (
    <>
      <Link to="/dashboard" className={navLinkClass(path.startsWith("/dashboard"))}>
        Dashboard
      </Link>
      <span
        className="hidden max-w-[10rem] truncate text-sm text-slate-500 dark:text-slate-400 sm:inline"
        title={user.email}
      >
        {user.email}
      </span>
      <button
        type="button"
        onClick={() => {
          logout();
          navigate("/");
        }}
        className="text-sm text-slate-600 hover:text-primary-600 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 dark:text-slate-400 dark:hover:text-primary-400"
      >
        Log out
      </button>
    </>
  ) : (
    <>
      <Link
        to="/login"
        className="text-sm font-medium text-slate-600 hover:text-primary-600 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 dark:text-slate-400 dark:hover:text-primary-400"
      >
        Login
      </Link>
      <Link to="/register" className={primaryNavClass}>
        Get Started
      </Link>
    </>
  );

  return (
    <header
      className={`sticky top-0 z-40 border-b transition-colors duration-200 ${
        scrolled
          ? "border-slate-200/80 bg-white/80 shadow-sm backdrop-blur-md dark:border-slate-700/80 dark:bg-slate-900/80"
          : "border-transparent bg-white/70 backdrop-blur-sm dark:bg-slate-900/70"
      }`}
    >
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3 sm:px-6 sm:py-4">
        <Link to="/" className="flex shrink-0 items-center gap-3">
          <img
            src={logoSrc}
            alt=""
            className={BRAND_LOGO_NAV_CLASS}
            width={BRAND_LOGO_NAV_WIDTH}
            height={BRAND_LOGO_NAV_HEIGHT}
            onError={(e) => {
              (e.target as HTMLImageElement).src = LOGO_LIGHT_SRC;
            }}
          />
          <span>
            <span className="block font-sans text-xl font-black uppercase tracking-[0.06em] text-primary-700 dark:text-primary-400 sm:text-2xl">
              Iskonnect
            </span>
            <span className="hidden text-xs font-medium text-slate-500 dark:text-slate-400 sm:block">
              Connecting Filipino Students to Opportunity
            </span>
          </span>
        </Link>

        <nav className="hidden items-center gap-x-5 md:flex" aria-label="Primary">
          {navLinks}
        </nav>

        <div className="hidden items-center gap-3 md:flex">{authLinks}</div>

        <button
          type="button"
          className="inline-flex items-center justify-center rounded-lg p-2 text-slate-600 hover:bg-slate-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 md:hidden dark:text-slate-300 dark:hover:bg-slate-800"
          aria-expanded={mobileOpen}
          aria-controls="mobile-nav"
          onClick={() => setMobileOpen((open) => !open)}
        >
          <span className="sr-only">{mobileOpen ? "Close menu" : "Open menu"}</span>
          {mobileOpen ? <X className="h-6 w-6" aria-hidden /> : <Menu className="h-6 w-6" aria-hidden />}
        </button>
      </div>

      {mobileOpen ? (
        <div
          id="mobile-nav"
          className="border-t border-slate-200 bg-white/95 px-4 py-4 backdrop-blur-md md:hidden dark:border-slate-700 dark:bg-slate-900/95"
        >
          <nav className="flex flex-col gap-3" aria-label="Mobile primary">
            {navLinks}
            <div className="mt-2 flex flex-col gap-3 border-t border-slate-200 pt-4 dark:border-slate-700">
              {authLinks}
            </div>
          </nav>
        </div>
      ) : null}
    </header>
  );
}
