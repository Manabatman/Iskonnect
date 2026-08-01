import { Component, type ErrorInfo, type ReactNode } from "react";
import { captureSentryException, isSentryConfigured } from "../lib/sentry";
import { ERROR_COPY } from "../constants/errorCopy";

interface Props {
  children: ReactNode;
}

interface State {
  error: Error | null;
}

const sentryEnabled = isSentryConfigured();

/**
 * Catches render errors in child trees so one bad page does not white-screen the whole app.
 */
export class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  override componentDidCatch(error: Error, info: ErrorInfo) {
    if (!import.meta.env.PROD) {
      console.error("[ErrorBoundary]", error, info.componentStack);
    }
    if (sentryEnabled) {
      void captureSentryException(error, { componentStack: info.componentStack });
    }
  }

  override render() {
    if (this.state.error) {
      return (
        <div className="mx-auto max-w-lg px-4 py-16 text-center">
          <h1 className="text-xl font-semibold text-slate-900 dark:text-slate-100">
            {ERROR_COPY.generic.title}
          </h1>
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
            {ERROR_COPY.generic.message}
          </p>
          <button
            type="button"
            className="mt-6 rounded-xl bg-primary-600 px-4 py-2 text-sm font-semibold text-white hover:bg-primary-700"
            onClick={() => this.setState({ error: null })}
          >
            {ERROR_COPY.generic.recoveryAction}
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
