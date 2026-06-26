import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

type Props = {
  className?: string;
};

/** Context-aware back link — dashboard when signed in, home when logged out. */
export function BackNavLink({ className }: Props) {
  const { user } = useAuth();
  const to = user ? "/dashboard" : "/";
  const label = user ? "Back to Dashboard" : "Back to home";

  return (
    <Link
      to={to}
      className={
        className ??
        "inline-flex items-center text-sm font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300"
      }
    >
      ← {label}
    </Link>
  );
}
