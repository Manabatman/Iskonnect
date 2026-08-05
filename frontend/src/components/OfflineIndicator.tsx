import { useEffect, useState } from "react";
import { ERROR_COPY } from "../constants/errorCopy";

/** Global offline banner — distinct from ApiWarmupBanner cold-start (UX-16). */
export function OfflineIndicator() {
  const [offline, setOffline] = useState(() =>
    typeof navigator !== "undefined" ? !navigator.onLine : false,
  );

  useEffect(() => {
    const onOffline = () => setOffline(true);
    const onOnline = () => setOffline(false);
    window.addEventListener("offline", onOffline);
    window.addEventListener("online", onOnline);
    return () => {
      window.removeEventListener("offline", onOffline);
      window.removeEventListener("online", onOnline);
    };
  }, []);

  if (!offline) return null;

  return (
    <div
      role="status"
      className="border-b border-amber-200 bg-amber-50 px-4 py-2 text-center text-sm text-amber-900 dark:border-amber-800 dark:bg-amber-950/80 dark:text-amber-100"
    >
      {ERROR_COPY.offline.title} — {ERROR_COPY.offline.message}
    </div>
  );
}
