import { useEffect, useState } from "react";
import { useFeedback } from "./FeedbackModal";

function IconChat({ className }: { className?: string }) {
  return (
    <svg className={className} width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"
        fill="currentColor"
      />
    </svg>
  );
}

export function FeedbackButton() {
  const { openFeedback } = useFeedback();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const t = window.setTimeout(() => setVisible(true), 50);
    return () => window.clearTimeout(t);
  }, []);

  if (!visible) {
    return null;
  }

  return (
    <button
      type="button"
      onClick={() => openFeedback(null)}
      className="fixed bottom-6 right-6 z-50 flex items-center gap-2 rounded-full bg-primary-600 px-4 py-3 text-sm font-semibold text-white shadow-lg transition-all duration-200 hover:scale-105 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:ring-offset-2 dark:focus:ring-offset-slate-900"
      aria-label="Share feedback"
    >
      <IconChat className="shrink-0" />
      <span>Share Feedback</span>
    </button>
  );
}
