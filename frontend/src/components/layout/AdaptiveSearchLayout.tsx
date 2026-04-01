import { type ReactNode, useState } from "react";
import { useAuth } from "../../contexts/AuthContext";
import { useSavedScholarships } from "../../contexts/SavedScholarshipsContext";
import { ErrorBoundary } from "../ErrorBoundary";
import { PublicShell } from "./PublicLayout";
import { DashboardSidebar } from "./DashboardSidebar";
import { DashboardTopbar } from "./DashboardTopbar";

function SavedScholarshipsErrorBanner() {
  const { error, clearError } = useSavedScholarships();
  if (!error) return null;
  return (
    <div
      role="status"
      className="border-b border-slate-200 bg-slate-100 px-4 py-2 text-sm text-slate-800 dark:border-slate-700 dark:bg-slate-800/80 dark:text-slate-200"
    >
      <div className="mx-auto flex max-w-7xl items-start justify-between gap-3">
        <p className="min-w-0 flex-1">{error}</p>
        <button
          type="button"
          onClick={clearError}
          className="shrink-0 rounded-md border border-slate-300 bg-white px-2 py-1 text-xs font-medium hover:bg-slate-50 dark:border-slate-600 dark:bg-slate-900 dark:hover:bg-slate-700"
        >
          Dismiss
        </button>
      </div>
    </div>
  );
}

interface AdaptiveSearchLayoutProps {
  children: ReactNode;
}

/**
 * Search page shell: dashboard layout when logged in, public shell when not.
 * Does not redirect unauthenticated users (search stays public).
 */
export function AdaptiveSearchLayout({ children }: AdaptiveSearchLayoutProps) {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);
  const { authError, clearAuthError, user, loading: authLoading } = useAuth();

  if (authLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50 text-slate-600 dark:bg-slate-900 dark:text-slate-300">
        <div className="flex flex-col items-center gap-3">
          <div className="h-10 w-10 animate-spin rounded-full border-2 border-primary-500 border-t-transparent" />
          <p className="text-sm">Loading…</p>
        </div>
      </div>
    );
  }

  if (user) {
    return (
      <div className="min-h-screen bg-slate-50 text-slate-900 dark:bg-slate-900 dark:text-slate-100">
        {authError ? (
          <div
            role="alert"
            className="border-b border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-900 dark:border-amber-800 dark:bg-amber-950/80 dark:text-amber-100"
          >
            <div className="mx-auto flex max-w-7xl items-start justify-between gap-3">
              <p className="min-w-0 flex-1">{authError}</p>
              <button
                type="button"
                onClick={clearAuthError}
                className="shrink-0 rounded-md border border-amber-300 bg-white px-2 py-1 text-xs font-medium text-amber-900 hover:bg-amber-100 dark:border-amber-700 dark:bg-amber-900 dark:text-amber-100 dark:hover:bg-amber-800"
              >
                Dismiss
              </button>
            </div>
          </div>
        ) : null}
        <ErrorBoundary>
          <SavedScholarshipsErrorBanner />
          <DashboardSidebar
            collapsed={sidebarCollapsed}
            onToggleCollapse={() => setSidebarCollapsed((c) => !c)}
            mobileOpen={mobileSidebarOpen}
            onMobileClose={() => setMobileSidebarOpen(false)}
          />
          <div
            className={[
              "flex min-h-screen flex-col transition-[padding] duration-200",
              sidebarCollapsed ? "lg:pl-16" : "lg:pl-64",
            ].join(" ")}
          >
            <DashboardTopbar onOpenMobileSidebar={() => setMobileSidebarOpen(true)} />
            <div className="flex-1 overflow-auto">
              <ErrorBoundary>{children}</ErrorBoundary>
            </div>
          </div>
        </ErrorBoundary>
      </div>
    );
  }

  return <PublicShell>{children}</PublicShell>;
}
