import { type ReactNode, useState } from "react";
import { useAuth } from "../../contexts/AuthContext";
import { SkipLink } from "../a11y/SkipLink";
import { ErrorBoundary } from "../ErrorBoundary";
import { SavedScholarshipsErrorBanner } from "./SavedScholarshipsErrorBanner";
import { PublicShell } from "./PublicLayout";
import { DashboardSidebar } from "./DashboardSidebar";
import { DashboardTopbar } from "./DashboardTopbar";
import { BottomNav } from "./BottomNav";
import { FeedbackButton } from "../FeedbackButton";
import { AuthShellSkeleton } from "../LoadingSkeletons";

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
    return <AuthShellSkeleton />;
  }

  if (user) {
    return (
      <div className="min-h-screen bg-background text-foreground pb-[env(safe-area-inset-bottom)]">
        <SkipLink />
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
              "flex min-h-screen flex-col transition-[padding] duration-base",
              sidebarCollapsed ? "lg:pl-16" : "lg:pl-sidebar",
            ].join(" ")}
          >
            <DashboardTopbar onOpenMobileSidebar={() => setMobileSidebarOpen(true)} />
            <main id="main-content" className="flex-1 overflow-auto pb-bottom-nav lg:pb-0">
              <ErrorBoundary>{children}</ErrorBoundary>
            </main>
          </div>
          <BottomNav />
          <FeedbackButton />
        </ErrorBoundary>
      </div>
    );
  }

  return <PublicShell>{children}</PublicShell>;
}
