import { Link } from "react-router-dom";
import * as Dialog from "@radix-ui/react-dialog";
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import { apiFetch } from "../api/client";
import { useAuth } from "../contexts/AuthContext";
import { validateEmail } from "../utils/validateEmail";

export type FeedbackCategory = "bug" | "suggestion" | "experience";

const MAX_CHARS = 500;
const COUNTER_THRESHOLD = Math.floor(MAX_CHARS * 0.8);

const CATEGORY_COPY: Record<
  FeedbackCategory,
  { prompt: string; placeholder: string }
> = {
  bug: {
    prompt: "What happened, and what did you expect instead?",
    placeholder:
      "e.g. The match results didn't load after I saved my profile.",
  },
  suggestion: {
    prompt: "What would you like to see in Iskonnect?",
    placeholder: "e.g. I wish I could filter scholarships by deadline.",
  },
  experience: {
    prompt: "Tell us your story — we'd love to hear it.",
    placeholder:
      "e.g. Iskonnect helped me find the scholarship I'm currently using to pay for college.",
  },
};

interface FeedbackContextValue {
  openFeedback: (category?: FeedbackCategory | null) => void;
}

const FeedbackContext = createContext<FeedbackContextValue | null>(null);

export function useFeedback() {
  const ctx = useContext(FeedbackContext);
  if (!ctx) throw new Error("useFeedback must be used within FeedbackProvider");
  return ctx;
}

function IconWarning({ className }: { className?: string }) {
  return (
    <svg className={className} width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"
        fill="currentColor"
      />
    </svg>
  );
}

function IconLightbulb({ className }: { className?: string }) {
  return (
    <svg className={className} width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M9 21c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-1H9v1zm3-19C8.14 2 5 5.14 5 9c0 2.38 1.19 4.47 3 5.74V17c0 .55.45 1 1 1h6c.55 0 1-.45 1-1v-2.26c1.81-1.27 3-3.36 3-5.74 0-3.86-3.14-7-7-7zm2.85 11.1l-.85.6V16h-4v-2.3l-.85-.6A4.997 4.997 0 017 9c0-2.76 2.24-5 5-5s5 2.24 5 5c0 1.63-.8 3.16-2.15 4.1z"
        fill="currentColor"
      />
    </svg>
  );
}

function IconHeart({ className }: { className?: string }) {
  return (
    <svg className={className} width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
        fill="currentColor"
      />
    </svg>
  );
}

const CATEGORIES: {
  id: FeedbackCategory;
  heading: string;
  subtext: string;
  Icon: typeof IconWarning;
}[] = [
  {
    id: "bug",
    heading: "Something's broken",
    subtext: "A feature isn't working as expected",
    Icon: IconWarning,
  },
  {
    id: "suggestion",
    heading: "I have an idea",
    subtext: "A way to make Iskonnect better",
    Icon: IconLightbulb,
  },
  {
    id: "experience",
    heading: "Share your story",
    subtext: "How Iskonnect helped you",
    Icon: IconHeart,
  },
];

interface FeedbackModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  initialCategory: FeedbackCategory | null;
}

export function FeedbackModal({ open, onOpenChange, initialCategory }: FeedbackModalProps) {
  const { authHeaders } = useAuth();
  const [step, setStep] = useState<1 | 2>(1);
  const [category, setCategory] = useState<FeedbackCategory | null>(null);
  const [message, setMessage] = useState("");
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  useEffect(() => {
    if (!open) return;
    setSubmitted(false);
    setSubmitting(false);
    setSubmitError(null);
    setMessage("");
    setEmail("");
    if (initialCategory) {
      setStep(2);
      setCategory(initialCategory);
    } else {
      setStep(1);
      setCategory(null);
    }
  }, [open, initialCategory]);

  const handleSubmit = async () => {
    if (!category || !message.trim()) return;
    if (email.trim()) {
      const emailCheck = validateEmail(email);
      if (!emailCheck.valid) {
        setSubmitError(emailCheck.message ?? "Enter a valid email address.");
        return;
      }
    }
    setSubmitting(true);
    setSubmitError(null);
    try {
      const res = await apiFetch("/api/v1/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({
          category,
          message: message.trim(),
          contact_email: email.trim() || undefined,
        }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => null);
        throw new Error(err?.detail ?? "Could not send feedback");
      }
      setSubmitted(true);
    } catch (e) {
      setSubmitted(false);
      setSubmitError(e instanceof Error ? e.message : "Could not send feedback");
    } finally {
      setSubmitting(false);
    }
  };

  const copy =
    category != null ? CATEGORY_COPY[category] : { prompt: "", placeholder: "" };

  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 z-[100] bg-black/40 backdrop-blur-sm data-[state=open]:animate-overlayFade data-[state=closed]:animate-overlayFadeOut dark:bg-black/60" />
        <Dialog.Content
          className="fixed inset-0 z-[101] flex max-h-full w-full items-center justify-center p-4 outline-none data-[state=open]:animate-matchDialogIn data-[state=closed]:animate-matchDialogOut sm:p-6"
          aria-describedby="feedback-modal-desc"
        >
          <div className="flex max-h-[90vh] w-full max-w-lg flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-2xl dark:border-slate-700 dark:bg-slate-900">
            <div className="flex items-start justify-between gap-3 border-b border-slate-200 px-5 py-4 dark:border-slate-700">
              <div className="min-w-0">
                <Dialog.Title className="text-lg font-bold text-slate-900 dark:text-slate-100">
                  Share feedback
                </Dialog.Title>
                <Dialog.Description
                  id="feedback-modal-desc"
                  className="mt-1 text-sm text-slate-600 dark:text-slate-400"
                >
                  Help us improve Iskonnect. Your message goes straight to our team.
                </Dialog.Description>
              </div>
              <Dialog.Close
                type="button"
                className="shrink-0 rounded-lg p-2 text-slate-500 transition hover:bg-slate-100 hover:text-slate-800 focus:outline-none focus:ring-2 focus:ring-primary-500 dark:hover:bg-slate-800 dark:hover:text-slate-200"
                aria-label="Close"
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </Dialog.Close>
            </div>

            <div className="min-h-0 flex-1 overflow-y-auto px-5 py-5">
              {submitted ? (
                <div className="py-4 text-center">
                  <p className="text-lg font-semibold text-slate-900 dark:text-slate-100">
                    Thank you for helping us improve
                  </p>
                  <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
                    Your feedback was received. We read every message and triage suggestions on our{" "}
                    <Link to="/roadmap" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
                      public roadmap
                    </Link>
                    .
                  </p>
                  <Dialog.Close asChild>
                    <button
                      type="button"
                      className="mt-6 inline-flex rounded-xl bg-primary-600 px-6 py-2.5 text-sm font-semibold text-white hover:bg-primary-700"
                    >
                      Back to Iskonnect
                    </button>
                  </Dialog.Close>
                </div>
              ) : step === 1 ? (
                <div className="space-y-3">
                  <p className="text-sm font-medium text-slate-700 dark:text-slate-300">
                    What would you like to share?
                  </p>
                  <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
                    {CATEGORIES.map(({ id, heading, subtext, Icon }) => (
                      <button
                        key={id}
                        type="button"
                        onClick={() => {
                          setCategory(id);
                          setStep(2);
                        }}
                        className="flex flex-col items-start gap-2 rounded-xl border border-slate-200 bg-slate-50/80 p-4 text-left transition hover:border-primary-300 hover:bg-primary-50/50 dark:border-slate-600 dark:bg-slate-800/50 dark:hover:border-primary-600 dark:hover:bg-primary-950/30"
                      >
                        <Icon className="text-primary-600 dark:text-primary-400" />
                        <span className="text-sm font-semibold text-slate-900 dark:text-slate-100">{heading}</span>
                        <span className="text-xs text-slate-600 dark:text-slate-400">{subtext}</span>
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  {submitError ? (
                    <p className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-800 dark:border-red-800 dark:bg-red-900/30 dark:text-red-200">
                      {submitError}
                    </p>
                  ) : null}
                  {category ? (
                    <>
                      <div>
                        <label htmlFor="feedback-message" className="text-sm font-medium text-slate-900 dark:text-slate-100">
                          {copy.prompt}
                        </label>
                        <textarea
                          id="feedback-message"
                          value={message}
                          onChange={(e) => setMessage(e.target.value.slice(0, MAX_CHARS))}
                          placeholder={copy.placeholder}
                          rows={5}
                          className="mt-2 min-h-[120px] w-full resize-y rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 placeholder:text-slate-400 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/30 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-100"
                        />
                        {message.length >= COUNTER_THRESHOLD ? (
                          <p className="mt-1 text-right text-xs text-slate-500 dark:text-slate-400">
                            {message.length} / {MAX_CHARS}
                          </p>
                        ) : null}
                      </div>
                      <div>
                        <label htmlFor="feedback-email" className="text-sm font-medium text-slate-900 dark:text-slate-100">
                          Your email (optional)
                        </label>
                        <input
                          id="feedback-email"
                          type="email"
                          value={email}
                          onChange={(e) => setEmail(e.target.value)}
                          placeholder="We'll only use this to follow up on your report"
                          className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 placeholder:text-slate-400 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/30 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-100"
                          autoComplete="email"
                        />
                        <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">We never share your email.</p>
                      </div>
                    </>
                  ) : null}
                </div>
              )}
            </div>

            {!submitted && step === 2 ? (
              <div className="flex flex-wrap items-center justify-between gap-3 border-t border-slate-200 px-5 py-4 dark:border-slate-700">
                <button
                  type="button"
                  onClick={() => {
                    setStep(1);
                    setCategory(null);
                    setMessage("");
                  }}
                  className="rounded-lg px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
                >
                  ← Back
                </button>
                <button
                  type="button"
                  disabled={!message.trim() || submitting}
                  onClick={handleSubmit}
                  className="rounded-xl bg-primary-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-primary-700 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {submitting ? "Sending…" : "Send Feedback"}
                </button>
              </div>
            ) : null}
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}

export function FeedbackProvider({ children }: { children: ReactNode }) {
  const [open, setOpen] = useState(false);
  const [initialCategory, setInitialCategory] = useState<FeedbackCategory | null>(null);

  const openFeedback = useCallback((category?: FeedbackCategory | null) => {
    setInitialCategory(category ?? null);
    setOpen(true);
  }, []);

  const handleOpenChange = useCallback((next: boolean) => {
    setOpen(next);
    if (!next) {
      window.setTimeout(() => setInitialCategory(null), 0);
    }
  }, []);

  return (
    <FeedbackContext.Provider value={{ openFeedback }}>
      {children}
      <FeedbackModal open={open} onOpenChange={handleOpenChange} initialCategory={initialCategory} />
    </FeedbackContext.Provider>
  );
}

export { CATEGORIES as FEEDBACK_CATEGORIES };
