import type { ReactNode } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export function SchoolGuard({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth();
  if (loading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center text-slate-600 dark:text-slate-400">
        Loading…
      </div>
    );
  }
  if (user?.role !== "school_verifier") {
    return <Navigate to="/dashboard" replace />;
  }
  return <>{children}</>;
}
