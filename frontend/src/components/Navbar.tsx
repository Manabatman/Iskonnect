import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { Menu, X } from "lucide-react";
import { useAuth } from "../contexts/AuthContext";
import { useTheme } from "../contexts/ThemeContext";
import { MIN_TOUCH_TARGET_CLASS } from "@/lib/utils";
import { brandLogoSrc, BRAND_LOGO_NAV_CLASS, BRAND_LOGO_NAV_HEIGHT, BRAND_LOGO_NAV_WIDTH, LOGO_LIGHT_SRC } from "../lib/brandLogo";

const desktopNavLinkClass = (active: boolean) =>
  [
    "text-sm transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 rounded px-1",
    active
      ? "font-medium text-primary-600 dark:text-primary-400"
      : "text-slate-600 hover:text-primary-600 dark:text-slate-400 dark:hover:text-primary-400",
  ].join(" ");

const mobileNavLinkClass = (active: boolean) =>
  [
    "rounded-xl px-3 py-3 text-sm font-medium transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2",
    active
      ? "bg-primary-50 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300"
      : "text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800",
  ].join(" ");

const primaryNavClass =
  "inline-flex items-center justify-center rounded-xl bg-primary-600 px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-primary-700 active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 dark:focus-visible:ring-offset-slate-900";

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

  useEffect(() => {
    if (!mobileOpen) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = prev;
    };
  }, [mobileOpen]);

  const isActive = (to: string) => (to === "/" ? path === "/" : path === to || path.startsWith(`${to}/`));

  const desktopNavLinks = (
    <>
      <Link to="/" className={desktopNavLinkClass(isActive("/"))}>
        Home
      </Link>
      <Link to="/scholarships/search" className={desktopNavLinkClass(path.startsWith("/scholarships"))}>
        Scholarships
      </Link>
      <Link
        to="/how-it-works"
        className={desktopNavLinkClass(isActive("/how-it-works") || isActive("/transparency") || isActive("/match-methodology"))}
      >
        Trust & matching
      </Link>
    </>
  );

  const mobileNavLinks = (
    <>
      <Link to="/" className={mobileNavLinkClass(isActive("/"))} onClick={() => setMobileOpen(false)}>
        Home
      </Link>
      <Link
        to="/scholarships/search"
        className={mobileNavLinkClass(path.startsWith("/scholarships"))}
        onClick={() => setMobileOpen(false)}
      >
        Scholarships
      </Link>
      <Link
        to="/how-it-works"
        className={mobileNavLinkClass(isActive("/how-it-works") || isActive("/transparency") || isActive("/match-methodology"))}
        onClick={() => setMobileOpen(false)}
      >
        Trust & matching
      </Link>
    </>
  );

  const desktopAuthLinks = user ? (
    <>
      <Link to="/dashboard" className={desktopNavLinkClass(path.startsWith("/dashboard"))}>
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

  const mobileAuthLinks = user ? (
    <>
      <Link to="/dashboard" className={mobileNavLinkClass(path.startsWith("/dashboard"))} onClick={() => setMobileOpen(false)}>
        Dashboard
      </Link>
      <span className="truncate px-3 text-sm text-slate-500 dark:text-slate-400" title={user.email}>
        {user.email}
      </span>
      <button
        type="button"
        onClick={() => {
          logout();
          navigate("/");
          setMobileOpen(false);
        }}
        className={`${mobileNavLinkClass(false)} w-full text-left`}
      >
        Log out
      </button>
    </>
  ) : (
    <>
      <Link to="/login" className={mobileNavLinkClass(false)} onClick={() => setMobileOpen(false)}>
        Login
      </Link>
      <Link to="/register" className={`${primaryNavClass} w-full`} onClick={() => setMobileOpen(false)}>
        Get Started
      </Link>
    </>
  );

  return (
    <>
      <header
        className={`sticky top-0 z-40 border-b transition-colors duration-200 ${
          scrolled
            ? "border-slate-200 bg-white shadow-sm dark:border-slate-700 dark:bg-slate-900"
            : "border-slate-200/80 bg-white dark:border-slate-800 dark:bg-slate-900"
        }`}
      >
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-2 sm:px-6 sm:py-2.5">
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
              <span className="block font-brand text-xl font-black tracking-tight text-primary-700 dark:text-primary-400 sm:text-2xl">
                Iskonnect
              </span>
              <span className="hidden text-xs font-medium text-slate-500 dark:text-slate-400 sm:block">
                Connecting Filipino Students to Opportunity
              </span>
            </span>
          </Link>

          <nav className="hidden items-center gap-x-5 md:flex" aria-label="Primary">
            {desktopNavLinks}
          </nav>

          <div className="hidden items-center gap-3 md:flex">{desktopAuthLinks}</div>

          <button
            type="button"
            className={`inline-flex size-11 items-center justify-center rounded-lg text-slate-600 hover:bg-slate-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 md:hidden dark:text-slate-300 dark:hover:bg-slate-800 ${MIN_TOUCH_TARGET_CLASS}`}
            aria-expanded={mobileOpen}
            aria-controls="mobile-nav"
            onClick={() => setMobileOpen((open) => !open)}
          >
            <span className="sr-only">{mobileOpen ? "Close menu" : "Open menu"}</span>
            {mobileOpen ? <X className="h-6 w-6" aria-hidden /> : <Menu className="h-6 w-6" aria-hidden />}
          </button>
        </div>
      </header>

      {mobileOpen ? (
        <button
          type="button"
          className="fixed inset-0 z-40 bg-slate-900/40 backdrop-blur-sm md:hidden"
          aria-label="Close navigation menu"
          onClick={() => setMobileOpen(false)}
        />
      ) : null}

      <aside
        id="mobile-nav"
        className={[
          "fixed inset-y-0 left-0 z-50 flex w-72 max-w-[85vw] flex-col border-r border-slate-200 bg-white shadow-xl transition-transform duration-200 dark:border-slate-700 dark:bg-slate-900 md:hidden",
          mobileOpen ? "translate-x-0" : "-translate-x-full pointer-events-none",
        ].join(" ")}
        aria-hidden={!mobileOpen}
      >
        <div className="flex h-16 items-center justify-between border-b border-slate-200 px-4 dark:border-slate-700">
          <Link to="/" className="flex items-center gap-2" onClick={() => setMobileOpen(false)}>
            <img
              src={logoSrc}
              alt=""
              className="h-8 w-8 object-contain"
              onError={(e) => {
                (e.target as HTMLImageElement).src = LOGO_LIGHT_SRC;
              }}
            />
            <span className="font-brand text-lg font-black tracking-tight text-primary-700 dark:text-primary-400">
              Iskonnect
            </span>
          </Link>
          <button
            type="button"
            className={`inline-flex size-11 items-center justify-center rounded-lg text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800 ${MIN_TOUCH_TARGET_CLASS}`}
            onClick={() => setMobileOpen(false)}
            aria-label="Close menu"
          >
            <X className="h-6 w-6" aria-hidden />
          </button>
        </div>

        <nav className="flex flex-1 flex-col gap-1 overflow-y-auto p-3" aria-label="Mobile primary">
          {mobileNavLinks}
          <div className="mt-3 flex flex-col gap-1 border-t border-slate-200 pt-3 dark:border-slate-700">{mobileAuthLinks}</div>
        </nav>
      </aside>
    </>
  );
}
