import { type ReactNode } from "react";
import { Outlet } from "react-router-dom";
import { Navbar } from "../Navbar";
import { Footer } from "../Footer";
import { ErrorBoundary } from "../ErrorBoundary";

interface PublicShellProps {
  children: ReactNode;
}

/**
 * Shared shell: Navbar + main + Footer. Use with Outlet via PublicLayout, or wrap a single page (e.g. 404).
 */
export function PublicShell({ children }: PublicShellProps) {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 dark:bg-slate-900 dark:text-slate-100">
      <Navbar />
      <main className="bg-slate-50 dark:bg-slate-900">
        <ErrorBoundary>{children}</ErrorBoundary>
      </main>
      <Footer />
    </div>
  );
}

export function PublicLayout() {
  return (
    <PublicShell>
      <Outlet />
    </PublicShell>
  );
}
