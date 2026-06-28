import { useEffect, useRef, useState } from "react";

const BUSY = "iskonnect-api-busy";
const IDLE = "iskonnect-api-idle";

/** Shown when API requests are in flight; debounced so fast local calls do not flicker. */
export function ApiWarmupBanner() {
  const [visible, setVisible] = useState(false);
  const showTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    const onBusy = () => {
      if (showTimer.current) clearTimeout(showTimer.current);
      showTimer.current = window.setTimeout(() => setVisible(true), 500);
    };
    const onIdle = () => {
      if (showTimer.current) {
        clearTimeout(showTimer.current);
        showTimer.current = null;
      }
      setVisible(false);
    };
    window.addEventListener(BUSY, onBusy);
    window.addEventListener(IDLE, onIdle);
    return () => {
      window.removeEventListener(BUSY, onBusy);
      window.removeEventListener(IDLE, onIdle);
      if (showTimer.current) clearTimeout(showTimer.current);
    };
  }, []);

  if (!visible) return null;

  return (
    <div
      className="pointer-events-none fixed bottom-0 left-0 right-0 z-[100] border-t border-primary-200 bg-primary-50/95 px-4 py-2 text-center text-sm text-primary-900 shadow-lg backdrop-blur dark:border-slate-600 dark:bg-slate-800/95 dark:text-slate-200"
      role="status"
      aria-live="polite"
    >
      Connecting to server… If this is your first visit after a while, waking the API can take up
      to 70 seconds — please wait.
    </div>
  );
}
