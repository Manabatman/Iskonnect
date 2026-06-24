import type { ReactElement } from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";
export interface DashboardSidebarProps {
  collapsed: boolean;
  onToggleCollapse: () => void;
  mobileOpen: boolean;
  onMobileClose: () => void;
}

type NavItem = {
  to: string;
  label: string;
  match: (path: string) => boolean;
  icon: (props: { className?: string }) => ReactElement;
};

const navItems: NavItem[] = [
  {
    to: "/dashboard",
    label: "Dashboard",
    match: (path: string) => path === "/dashboard",
    icon: IconLayoutDashboard,
  },
  {
    to: "/scholarships/search",
    label: "Search scholarships",
    match: (path: string) => path.startsWith("/scholarships/search"),
    icon: IconSearch,
  },
  {
    to: "/applications",
    label: "Applications",
    match: (path: string) => path.startsWith("/applications"),
    icon: IconFileText,
  },
  {
    to: "/documents",
    label: "Documents",
    match: (path: string) => path.startsWith("/documents"),
    icon: IconClipboard,
  },
  {
    to: "/profile-builder",
    label: "Profile",
    match: (path: string) => path.startsWith("/profile-builder"),
    icon: IconUser,
  },
  {
    to: "/settings",
    label: "Account Settings",
    match: (path: string) => path.startsWith("/settings"),
    icon: IconSettings,
  },
];

function IconLayoutDashboard({ className }: { className?: string }) {
  return (
    <svg className={className} width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"
        fill="currentColor"
      />
    </svg>
  );
}

function IconSearch({ className }: { className?: string }) {
  return (
    <svg className={className} width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0016 9.5 6.5 6.5 0 109.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"
        fill="currentColor"
      />
    </svg>
  );
}

function IconClipboard({ className }: { className?: string }) {
  return (
    <svg className={className} width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9h6m-6 4h6"
        stroke="currentColor"
        strokeWidth={1.75}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function IconFileText({ className }: { className?: string }) {
  return (
    <svg className={className} width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"
        fill="currentColor"
      />
    </svg>
  );
}

function IconUser({ className }: { className?: string }) {
  return (
    <svg className={className} width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
        fill="currentColor"
      />
    </svg>
  );
}

function IconSettings({ className }: { className?: string }) {
  return (
    <svg className={className} width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M19.14 12.94c.04-.31.06-.63.06-.94 0-.31-.02-.63-.06-.94l2.03-1.58a.49.49 0 00.12-.61l-1.92-3.32a.488.488 0 00-.6-.22l-2.39.96c-.52-.4-1.08-.73-1.69-.98l-.36-2.54a.484.484 0 00-.49-.42h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.61.25-1.17.59-1.69.98l-2.39-.96c-.22-.08-.47 0-.6.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.04.31-.06.63-.06.94s.02.63.06.94l-2.03 1.58a.49.49 0 00-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.52.4 1.08.73 1.69.98l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.61-.25 1.17-.59 1.69-.98l2.39.96c.22.08.47 0 .6-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"
        fill="currentColor"
      />
    </svg>
  );
}

function IconChevronLeft({ className }: { className?: string }) {
  return (
    <svg className={className} width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z" fill="currentColor" />
    </svg>
  );
}

export function DashboardSidebar({
  collapsed,
  onToggleCollapse,
  mobileOpen,
  onMobileClose,
}: DashboardSidebarProps) {
  const location = useLocation();
  const path = location.pathname;
  const { user } = useAuth();

  return (
    <>
      {mobileOpen ? (
        <button
          type="button"
          className="fixed inset-0 z-30 bg-slate-900/40 backdrop-blur-sm lg:hidden"
          aria-label="Close navigation menu"
          onClick={onMobileClose}
        />
      ) : null}

      <aside
        className={[
          "fixed inset-y-0 left-0 z-40 flex flex-col border-r border-slate-200 bg-white shadow-lg transition-all duration-200 dark:border-slate-700 dark:bg-slate-800",
          collapsed ? "w-16" : "w-64",
          mobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0",
        ].join(" ")}
      >
        <div
          className={[
            "flex h-16 shrink-0 items-center border-b border-slate-200 px-3 dark:border-slate-700",
            collapsed ? "justify-center" : "justify-between gap-2",
          ].join(" ")}
        >
          {collapsed ? (
            <Link
              to="/dashboard"
              className="flex h-10 w-10 items-center justify-center rounded-lg text-lg font-bold text-primary-700 dark:text-primary-400"
              title="Iskonnect dashboard"
            >
              I
            </Link>
          ) : (
            <Link to="/dashboard" className="min-w-0 flex-1 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-slate-800">
              <span className="block truncate text-lg font-bold text-primary-700 dark:text-primary-400">
                Iskonnect
              </span>
              <span className="block truncate text-xs text-slate-500 dark:text-slate-400">
                Student dashboard
              </span>
            </Link>
          )}
          <button
            type="button"
            onClick={onToggleCollapse}
            className="hidden h-9 w-9 shrink-0 items-center justify-center rounded-lg text-slate-500 transition hover:bg-slate-100 hover:text-slate-800 dark:hover:bg-slate-700 dark:hover:text-slate-200 lg:flex"
            aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
            title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          >
            <IconChevronLeft
              className={["transition-transform", collapsed ? "rotate-180" : ""].join(" ")}
            />
          </button>
        </div>

        <nav className="flex-1 space-y-1 overflow-y-auto p-2 pb-0" aria-label="Dashboard navigation">
          {navItems.map((item) => {
            const active = item.match(path);
            const Icon = item.icon;
            return (
              <Link
                key={item.to}
                to={item.to}
                onClick={onMobileClose}
                aria-current={active ? "page" : undefined}
                className={[
                  "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition",
                  active
                    ? "bg-primary-50 text-primary-700 shadow-sm dark:bg-primary-900/30 dark:text-primary-300"
                    : "text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-700/80",
                  collapsed ? "justify-center px-2" : "",
                ].join(" ")}
                title={collapsed ? item.label : undefined}
              >
                <Icon className="shrink-0 opacity-90" />
                {!collapsed ? <span className="truncate">{item.label}</span> : null}
              </Link>
            );
          })}
        </nav>

        {user?.role === "admin" || user?.role === "sponsor" || user?.role === "school_verifier" ? (
          <div className="mt-auto space-y-1 border-t border-slate-200 p-2 dark:border-slate-700">
            {user?.role === "sponsor" ? (
              <Link
                to="/sponsor"
                onClick={onMobileClose}
                className={[
                  "flex items-center gap-3 rounded-xl px-3 py-2 text-sm font-medium transition",
                  path.startsWith("/sponsor")
                    ? "bg-primary-50 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300"
                    : "text-slate-500 hover:bg-slate-100 hover:text-slate-800 dark:text-slate-400 dark:hover:bg-slate-700/80 dark:hover:text-slate-200",
                  collapsed ? "justify-center px-2" : "",
                ].join(" ")}
                title={collapsed ? "Sponsor" : undefined}
              >
                <span className="flex h-5 w-5 shrink-0 items-center justify-center text-xs font-bold" aria-hidden>
                  S
                </span>
                {!collapsed ? <span>Sponsor</span> : null}
              </Link>
            ) : null}
            {user?.role === "school_verifier" ? (
              <Link
                to="/school"
                onClick={onMobileClose}
                className={[
                  "flex items-center gap-3 rounded-xl px-3 py-2 text-sm font-medium transition",
                  path.startsWith("/school")
                    ? "bg-primary-50 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300"
                    : "text-slate-500 hover:bg-slate-100 hover:text-slate-800 dark:text-slate-400 dark:hover:bg-slate-700/80 dark:hover:text-slate-200",
                  collapsed ? "justify-center px-2" : "",
                ].join(" ")}
                title={collapsed ? "School" : undefined}
              >
                <span className="flex h-5 w-5 shrink-0 items-center justify-center text-xs font-bold" aria-hidden>
                  V
                </span>
                {!collapsed ? <span>School verify</span> : null}
              </Link>
            ) : null}
            {user?.role === "admin" ? (
              <Link
                to="/admin"
                onClick={onMobileClose}
                className={[
                  "flex items-center gap-3 rounded-xl px-3 py-2 text-sm font-medium transition",
                  path.startsWith("/admin")
                    ? "bg-primary-50 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300"
                    : "text-slate-500 hover:bg-slate-100 hover:text-slate-800 dark:text-slate-400 dark:hover:bg-slate-700/80 dark:hover:text-slate-200",
                  collapsed ? "justify-center px-2" : "",
                ].join(" ")}
                title={collapsed ? "Admin" : undefined}
              >
                <span className="flex h-5 w-5 shrink-0 items-center justify-center text-xs font-bold" aria-hidden>
                  A
                </span>
                {!collapsed ? <span>Admin</span> : null}
              </Link>
            ) : null}
          </div>
        ) : null}
      </aside>
    </>
  );
}
