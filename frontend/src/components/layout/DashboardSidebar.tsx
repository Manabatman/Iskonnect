import { Link, useLocation } from "react-router-dom";

export interface DashboardSidebarProps {
  collapsed: boolean;
  onToggleCollapse: () => void;
  mobileOpen: boolean;
  onMobileClose: () => void;
}

const navItems = [
  {
    to: "/dashboard",
    label: "Dashboard",
    match: (path: string) => path === "/dashboard",
    icon: IconLayoutDashboard,
  },
  {
    to: "/opportunities",
    label: "Opportunities",
    match: (path: string) => path.startsWith("/opportunities"),
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
    icon: IconFolderOpen,
  },
  {
    to: "/profile-builder",
    label: "Profile",
    match: (path: string) => path.startsWith("/profile-builder"),
    icon: IconUser,
  },
] as const;

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

function IconFolderOpen({ className }: { className?: string }) {
  return (
    <svg className={className} width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 12H4V8h16v10z"
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
              title="ISKONNECT dashboard"
            >
              I
            </Link>
          ) : (
            <Link to="/dashboard" className="min-w-0 flex-1 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-slate-800">
              <span className="block truncate text-lg font-bold text-primary-700 dark:text-primary-400">
                ISKONNECT
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

        <div className="mt-auto border-t border-slate-200 p-2 dark:border-slate-700">
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
        </div>
      </aside>
    </>
  );
}
