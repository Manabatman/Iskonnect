import { useEffect, useRef, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";

export interface DashboardTopbarProps {
  onOpenMobileSidebar: () => void;
}

function titleForPath(pathname: string): string {
  if (pathname === "/dashboard") return "Dashboard";
  if (pathname.startsWith("/opportunities")) return "Opportunities";
  if (pathname.startsWith("/scholarships/search")) return "Scholarship search";
  if (pathname.startsWith("/scholarships")) return "Scholarships";
  if (pathname.startsWith("/scholarship/")) return "Scholarship";
  if (pathname.startsWith("/applications")) return "Applications";
  if (pathname.startsWith("/documents")) return "Documents";
  if (pathname.startsWith("/profile-builder")) return "Profile builder";
  if (pathname.startsWith("/settings")) return "Account settings";
  if (pathname.startsWith("/match-compare")) return "Compare matches";
  if (pathname.startsWith("/match/")) return "Match results";
  if (pathname.startsWith("/admin")) return "Admin";
  return "Dashboard";
}

function IconMenu({ className }: { className?: string }) {
  return (
    <svg className={className} width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z" fill="currentColor" />
    </svg>
  );
}

function IconBell({ className }: { className?: string }) {
  return (
    <svg className={className} width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.89 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"
        fill="currentColor"
      />
    </svg>
  );
}

function IconChevronDown({ className }: { className?: string }) {
  return (
    <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path d="M7 10l5 5 5-5z" fill="currentColor" />
    </svg>
  );
}

export function DashboardTopbar({ onOpenMobileSidebar }: DashboardTopbarProps) {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  const pageTitle = titleForPath(location.pathname);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setMenuOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <header className="sticky top-0 z-20 flex h-16 shrink-0 items-center gap-3 border-b border-slate-200 bg-white/95 px-3 shadow-sm backdrop-blur dark:border-slate-700 dark:bg-slate-800/95 sm:px-4">
      <button
        type="button"
        className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg text-slate-600 transition hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-700 lg:hidden"
        onClick={onOpenMobileSidebar}
        aria-label="Open navigation menu"
      >
        <IconMenu />
      </button>

      <div className="min-w-0 flex-1">
        <p className="truncate text-xs font-medium uppercase tracking-wide text-slate-500 dark:text-slate-400">
          ISKONNECT
        </p>
        <h1 className="truncate text-lg font-semibold text-slate-900 dark:text-slate-100">{pageTitle}</h1>
      </div>

      <div className="hidden max-w-md flex-1 sm:block md:max-w-lg lg:max-w-xl">
        <label htmlFor="dashboard-global-search" className="sr-only">
          Search
        </label>
        <input
          id="dashboard-global-search"
          type="search"
          placeholder="Search scholarships, schools…"
          readOnly
          className="w-full rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-600 placeholder:text-slate-400 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/30 dark:border-slate-600 dark:bg-slate-900/50 dark:text-slate-200 dark:placeholder:text-slate-500"
          aria-describedby="search-soon-hint"
        />
        <span id="search-soon-hint" className="sr-only">
          Global search coming soon
        </span>
      </div>

      <div className="flex shrink-0 items-center gap-1 sm:gap-2">
        <button
          type="button"
          className="flex h-10 w-10 items-center justify-center rounded-lg text-slate-500 transition hover:bg-slate-100 hover:text-slate-800 dark:text-slate-400 dark:hover:bg-slate-700 dark:hover:text-slate-100"
          aria-label="Notifications"
        >
          <IconBell />
        </button>

        <div className="relative" ref={menuRef}>
          <button
            type="button"
            onClick={() => setMenuOpen((o) => !o)}
            className="flex max-w-[12rem] items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 py-1.5 pl-2 pr-2 text-left transition hover:bg-slate-100 dark:border-slate-600 dark:bg-slate-900/40 dark:hover:bg-slate-700"
            aria-expanded={menuOpen}
            aria-haspopup="true"
          >
            <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary-100 text-sm font-semibold text-primary-800 dark:bg-primary-900/50 dark:text-primary-200">
              {user?.email?.[0]?.toUpperCase() ?? "?"}
            </span>
            <span className="hidden min-w-0 flex-1 sm:block">
              <span className="block truncate text-xs font-medium text-slate-900 dark:text-slate-100">
                {user?.email ?? "Account"}
              </span>
            </span>
            <IconChevronDown className="shrink-0 text-slate-500" />
          </button>

          {menuOpen ? (
            <div
              className="absolute right-0 mt-2 w-56 rounded-xl border border-slate-200 bg-white py-1 shadow-lg dark:border-slate-600 dark:bg-slate-800"
              role="menu"
            >
              <div className="border-b border-slate-100 px-3 py-2 dark:border-slate-700">
                <p className="truncate text-xs text-slate-500 dark:text-slate-400">Signed in as</p>
                <p className="truncate text-sm font-medium text-slate-900 dark:text-slate-100">{user?.email}</p>
              </div>
              <Link
                to="/settings"
                className="block px-3 py-2 text-sm text-slate-700 hover:bg-slate-50 dark:text-slate-200 dark:hover:bg-slate-700"
                role="menuitem"
                onClick={() => setMenuOpen(false)}
              >
                Profile settings
              </Link>
              <button
                type="button"
                className="w-full px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 dark:text-slate-200 dark:hover:bg-slate-700"
                role="menuitem"
                onClick={() => {
                  setMenuOpen(false);
                  logout();
                  navigate("/");
                }}
              >
                Log out
              </button>
            </div>
          ) : null}
        </div>
      </div>
    </header>
  );
}
