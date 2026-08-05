import { useNavigate } from "react-router-dom";
import { ChevronLeft } from "lucide-react";
import { useAuth } from "../contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { cn, MIN_TOUCH_TARGET_CLASS } from "@/lib/utils";

type Props = {
  className?: string;
};

/** Context-aware back link — dashboard when signed in, home when logged out. */
export function BackNavLink({ className }: Props) {
  const { user } = useAuth();
  const navigate = useNavigate();
  const to = user ? "/dashboard" : "/";
  const label = user ? "Back to Dashboard" : "Back to home";

  return (
    <Button
      type="button"
      variant="ghost"
      className={cn(MIN_TOUCH_TARGET_CLASS, className)}
      onClick={() => navigate(to)}
    >
      <ChevronLeft className="size-4" aria-hidden />
      {label}
    </Button>
  );
}
