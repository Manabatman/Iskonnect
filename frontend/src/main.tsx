import React from "react";
import ReactDOM from "react-dom/client";
import * as Sentry from "@sentry/react";
import "@fontsource/inter/400.css";
import "@fontsource/inter/500.css";
import "@fontsource/inter/600.css";
import "@fontsource/inter/700.css";
import "@fontsource/russo-one/400.css";
import App from "./App";
import "./index.css";

const sentryDsn = (import.meta as unknown as { env?: { VITE_SENTRY_DSN?: string; MODE?: string } }).env
  ?.VITE_SENTRY_DSN;
const sentryEnv =
  (import.meta as unknown as { env?: { VITE_SENTRY_ENVIRONMENT?: string; MODE?: string } }).env
    ?.VITE_SENTRY_ENVIRONMENT ??
  (import.meta as unknown as { env?: { MODE?: string } }).env?.MODE ??
  "development";
const sentryRelease = (import.meta as unknown as { env?: { VITE_SENTRY_RELEASE?: string } }).env
  ?.VITE_SENTRY_RELEASE;

if (sentryDsn) {
  Sentry.init({
    dsn: sentryDsn,
    integrations: [Sentry.browserTracingIntegration()],
    tracesSampleRate: 0.1,
    environment: sentryEnv,
    release: sentryRelease,
  });
}

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
