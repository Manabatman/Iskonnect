import { defineConfig, type Plugin } from "vite";
import react from "@vitejs/plugin-react-swc";
import { VitePWA } from "vite-plugin-pwa";
import path from "node:path";

/** Preload latin critical woff2 assets emitted at build time (C6 LCP/CLS). */
function injectCriticalFontPreloads(): Plugin {
  return {
    name: "inject-critical-font-preloads",
    transformIndexHtml: {
      order: "post",
      handler(html, ctx) {
        const bundle = ctx.bundle;
        if (!bundle) return html;

        const preloads = Object.keys(bundle)
          .filter(
            (fileName) =>
              fileName.endsWith(".woff2") &&
              (/inter-latin-(400|500|600)-normal/.test(fileName) ||
                /russo-one-latin-400-normal/.test(fileName)),
          )
          .map((fileName) => {
            const href = `/${fileName.replace(/\\/g, "/")}`;
            return `<link rel="preload" href="${href}" as="font" type="font/woff2" crossorigin>`;
          });

        if (!preloads.length) return html;
        return html.replace("</head>", `    ${preloads.join("\n    ")}\n  </head>`);
      },
    },
  };
}

export default defineConfig({
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (!id.includes("node_modules")) return;
          if (id.includes("@sentry")) return "sentry";
          if (id.includes("framer-motion")) return "framer-motion";
          if (id.includes("@radix-ui")) return "radix";
          return "vendor";
        },
      },
    },
  },
  plugins: [
    react(),
    injectCriticalFontPreloads(),
    VitePWA({
      registerType: "autoUpdate",
      injectRegister: "script-defer",
      includeAssets: ["images/logo-light.png", "images/logo-dark.png"],
      manifest: false,
      workbox: {
        globPatterns: ["**/*.{js,css,html,ico,svg,png,woff2}"],
        maximumFileSizeToCacheInBytes: 5 * 1024 * 1024,
        navigateFallbackDenylist: [/^\/api\//],
        runtimeCaching: [
          {
            urlPattern: ({ url }) => url.pathname.startsWith("/api/v1/auth"),
            handler: "NetworkOnly",
          },
          {
            urlPattern: ({ url }) => url.pathname.startsWith("/api/v1/profiles"),
            handler: "NetworkOnly",
          },
          {
            urlPattern: ({ url }) => url.pathname.startsWith("/api/v1/applications"),
            handler: "NetworkOnly",
          },
          {
            urlPattern: ({ url }) => url.pathname.startsWith("/api/v1/match-runs"),
            handler: "NetworkOnly",
          },
          {
            urlPattern: ({ url }) => url.pathname.startsWith("/api/v1/plan"),
            handler: "NetworkOnly",
          },
          {
            urlPattern: ({ url }) => url.pathname.startsWith("/api/v1/scholarships"),
            handler: "NetworkFirst",
            options: {
              cacheName: "iskonnect-scholarship-catalog",
              networkTimeoutSeconds: 8,
              expiration: { maxEntries: 32, maxAgeSeconds: 60 * 60 * 24 },
            },
          },
        ],
      },
    }),
  ],
  server: {
    port: 5173,
    strictPort: true,
  },
  test: {
    environment: "jsdom",
    setupFiles: "./src/test/setup.ts",
    globals: true,
    exclude: ["**/node_modules/**", "**/dist/**", "e2e/**"],
    coverage: {
      provider: "v8",
      reporter: ["text", "text-summary"],
      // QA-03 baseline (A8, 2026-08-01): floor of measured `npm test -- --coverage`.
      // Override: see docs/engineering/reports/QA-03-report.md (R-15 §22).
      thresholds: {
        lines: 14,
        functions: 30,
        statements: 14,
        branches: 42,
      },
    },
  },
});
