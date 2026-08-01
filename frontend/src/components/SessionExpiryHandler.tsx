import { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { AUTH_SESSION_EXPIRED_EVENT } from "../api/client";

/** Redirect to login with returnTo when refresh token fails (UX-15). */
export function SessionExpiryHandler() {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const onExpired = () => {
      if (location.pathname.startsWith("/login") || location.pathname.startsWith("/register")) return;
      navigate("/login", { replace: true, state: { from: location.pathname } });
    };
    window.addEventListener(AUTH_SESSION_EXPIRED_EVENT, onExpired);
    return () => window.removeEventListener(AUTH_SESSION_EXPIRED_EVENT, onExpired);
  }, [location.pathname, navigate]);

  return null;
}
