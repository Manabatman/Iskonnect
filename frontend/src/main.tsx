import React from "react";
import ReactDOM from "react-dom/client";
import "@fontsource/inter/latin-400.css";
import "@fontsource/inter/latin-500.css";
import "@fontsource/inter/latin-600.css";
import "@fontsource/russo-one/latin-400.css";
import App from "./App";
import { loadDeferredFontWeights } from "./lib/deferredFonts";
import { initSentryAfterFirstPaint } from "./lib/sentry";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

loadDeferredFontWeights();
initSentryAfterFirstPaint();
