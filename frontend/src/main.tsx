import React from "react";
import ReactDOM from "react-dom/client";
import "@fontsource/inter/latin-400.css";
import "@fontsource/inter/latin-500.css";
import "@fontsource/inter/latin-600.css";
import "@fontsource/inter/latin-800.css";
import "@fontsource/montserrat/latin-900.css";
import App from "./App";
import { API_CONFIG_ERROR } from "./api/client";
import { loadDeferredFontWeights } from "./lib/deferredFonts";
import { initSentryAfterFirstPaint } from "./lib/sentry";
import "./index.css";

const rootEl = document.getElementById("root");

if (rootEl) {
  if (API_CONFIG_ERROR) {
    rootEl.innerHTML = `
      <div style="font-family: system-ui, sans-serif; max-width: 28rem; margin: 4rem auto; padding: 0 1rem; text-align: center; color: #0f172a;">
        <h1 style="font-size: 1.25rem; font-weight: 600; margin-bottom: 0.5rem;">Unable to start Iskonnect</h1>
        <p style="font-size: 0.875rem; color: #475569; line-height: 1.5;">${API_CONFIG_ERROR}</p>
      </div>
    `;
  } else {
    ReactDOM.createRoot(rootEl).render(
      <React.StrictMode>
        <App />
      </React.StrictMode>,
    );
    loadDeferredFontWeights();
    initSentryAfterFirstPaint();
  }
}
