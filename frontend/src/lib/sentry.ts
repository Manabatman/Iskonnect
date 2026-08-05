type SentryModule = typeof import("@sentry/react");

let initPromise: Promise<SentryModule | null> | null = null;

function readSentryEnv() {
  const env = (import.meta as unknown as {
    env?: {
      VITE_SENTRY_DSN?: string;
      VITE_SENTRY_ENVIRONMENT?: string;
      VITE_SENTRY_RELEASE?: string;
      MODE?: string;
    };
  }).env;
  return {
    dsn: env?.VITE_SENTRY_DSN,
    environment: env?.VITE_SENTRY_ENVIRONMENT ?? env?.MODE ?? "development",
    release: env?.VITE_SENTRY_RELEASE,
  };
}

/** Defer Sentry until after first paint so the landing bundle stays off the critical path. */
export function initSentryAfterFirstPaint(): Promise<SentryModule | null> {
  const { dsn, environment, release } = readSentryEnv();
  if (!dsn) return Promise.resolve(null);
  if (initPromise) return initPromise;

  initPromise = new Promise((resolve) => {
    const run = async () => {
      const Sentry = await import("@sentry/react");
      Sentry.init({
        dsn,
        integrations: [Sentry.browserTracingIntegration()],
        tracesSampleRate: 0.1,
        environment,
        release,
      });
      resolve(Sentry);
    };

    if (typeof window.requestAnimationFrame === "function") {
      window.requestAnimationFrame(() => {
        window.requestAnimationFrame(() => {
          void run();
        });
      });
    } else {
      window.setTimeout(() => void run(), 0);
    }
  });

  return initPromise;
}

export function isSentryConfigured(): boolean {
  return Boolean(readSentryEnv().dsn);
}

export async function captureSentryException(
  error: Error,
  context?: { componentStack?: string | null | undefined },
): Promise<void> {
  if (!isSentryConfigured()) return;
  const Sentry = await initSentryAfterFirstPaint();
  if (!Sentry) return;
  Sentry.captureException(error, {
    contexts: context?.componentStack
      ? { react: { componentStack: context.componentStack } }
      : undefined,
  });
}
