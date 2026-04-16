import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ThemeProvider } from "./contexts/ThemeContext";
import { AuthProvider } from "./contexts/AuthContext";
import { SavedScholarshipsProvider } from "./contexts/SavedScholarshipsContext";
import { AboutPage } from "./pages/AboutPage";
import { TermsPage } from "./pages/TermsPage";
import { PrivacyPage } from "./pages/PrivacyPage";
import { ChangelogPage } from "./pages/ChangelogPage";
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/RegisterPage";
import { ScholarshipList } from "./components/ScholarshipList";
import { NotFoundPage } from "./pages/NotFoundPage";
import { LandingPage } from "./pages/LandingPage";
import { HowItWorksPage } from "./pages/HowItWorksPage";
import { TransparencyPage } from "./pages/TransparencyPage";
import { SuccessStoriesPage } from "./pages/SuccessStoriesPage";
import { PublicLayout, PublicShell } from "./components/layout/PublicLayout";
import { DashboardLayout } from "./components/layout/DashboardLayout";
import { AdaptiveSearchLayout } from "./components/layout/AdaptiveSearchLayout";
import { FeedbackProvider } from "./components/FeedbackModal";
import { ENABLE_OPPORTUNITIES } from "./config/featureFlags";
import { AdminGuard } from "./components/AdminGuard";
import { SponsorGuard } from "./components/SponsorGuard";
import { SchoolGuard } from "./components/SchoolGuard";
import { ApiWarmupBanner } from "./components/ApiWarmupBanner";
import { ErrorBoundary } from "./components/ErrorBoundary";

const MatchResultsPage = lazy(() =>
  import("./pages/MatchResultsPage").then((m) => ({ default: m.MatchResultsPage }))
);
const ScholarshipDetailPage = lazy(() =>
  import("./pages/ScholarshipDetailPage").then((m) => ({ default: m.ScholarshipDetailPage }))
);
const SettingsPage = lazy(() => import("./pages/SettingsPage").then((m) => ({ default: m.SettingsPage })));
const AdminPage = lazy(() => import("./pages/AdminPage").then((m) => ({ default: m.AdminPage })));
const AdminAnalyticsPage = lazy(() =>
  import("./pages/AdminAnalyticsPage").then((m) => ({ default: m.AdminAnalyticsPage }))
);
const ProfileDashboard = lazy(() =>
  import("./pages/ProfileDashboard").then((m) => ({ default: m.ProfileDashboard }))
);
const MatchComparisonPage = lazy(() =>
  import("./pages/MatchComparisonPage").then((m) => ({ default: m.MatchComparisonPage }))
);
const ScholarshipSearchPage = lazy(() =>
  import("./pages/ScholarshipSearchPage").then((m) => ({ default: m.ScholarshipSearchPage }))
);
const ApplicationsPage = lazy(() =>
  import("./pages/ApplicationsPage").then((m) => ({ default: m.ApplicationsPage }))
);
const DocumentsPage = lazy(() => import("./pages/DocumentsPage").then((m) => ({ default: m.DocumentsPage })));
const OpportunityBrowserPage = lazy(() =>
  import("./pages/OpportunityBrowserPage").then((m) => ({ default: m.OpportunityBrowserPage }))
);
const ProfileBuilderPage = lazy(() =>
  import("./pages/ProfileBuilderPage").then((m) => ({ default: m.ProfileBuilderPage }))
);
const SponsorPortalPage = lazy(() =>
  import("./pages/SponsorPortalPage").then((m) => ({ default: m.SponsorPortalPage }))
);
const SchoolPortalPage = lazy(() =>
  import("./pages/SchoolPortalPage").then((m) => ({ default: m.SchoolPortalPage }))
);

function RouteFallback() {
  return (
    <div className="flex min-h-[40vh] items-center justify-center px-4 text-sm text-slate-600 dark:text-slate-400">
      Loading…
    </div>
  );
}

function AppRoutes() {
  return (
    <Suspense fallback={<RouteFallback />}>
      <Routes>
        <Route element={<PublicLayout />}>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/how-it-works" element={<HowItWorksPage />} />
          <Route path="/transparency" element={<TransparencyPage />} />
          <Route path="/success-stories" element={<SuccessStoriesPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/terms" element={<TermsPage />} />
          <Route path="/privacy" element={<PrivacyPage />} />
          <Route path="/changelog" element={<ChangelogPage />} />
        </Route>

        <Route
          path="/scholarships/search"
          element={
            <AdaptiveSearchLayout>
              <ScholarshipSearchPage />
            </AdaptiveSearchLayout>
          }
        />

        <Route element={<DashboardLayout />}>
          <Route path="/dashboard" element={<ProfileDashboard />} />
          <Route path="/match/:profileId" element={<MatchResultsPage />} />
          <Route path="/match-compare" element={<MatchComparisonPage />} />
          <Route path="/scholarship/:id" element={<ScholarshipDetailPage />} />
          <Route
            path="/opportunities"
            element={
              ENABLE_OPPORTUNITIES ? (
                <OpportunityBrowserPage />
              ) : (
                <Navigate to="/dashboard" replace />
              )
            }
          />
          <Route path="/scholarships" element={<ScholarshipList />} />
          <Route path="/profile-builder" element={<ProfileBuilderPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route
            path="/admin"
            element={
              <AdminGuard>
                <AdminPage />
              </AdminGuard>
            }
          />
          <Route
            path="/admin/analytics"
            element={
              <AdminGuard>
                <AdminAnalyticsPage />
              </AdminGuard>
            }
          />
          <Route path="/applications" element={<ApplicationsPage />} />
          <Route path="/documents" element={<DocumentsPage />} />
          <Route
            path="/sponsor"
            element={
              <SponsorGuard>
                <SponsorPortalPage />
              </SponsorGuard>
            }
          />
          <Route
            path="/school"
            element={
              <SchoolGuard>
                <SchoolPortalPage />
              </SchoolGuard>
            }
          />
        </Route>

        <Route
          path="*"
          element={
            <PublicShell>
              <NotFoundPage />
            </PublicShell>
          }
        />
      </Routes>
    </Suspense>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <ErrorBoundary>
        <BrowserRouter>
          <AuthProvider>
            <SavedScholarshipsProvider>
              <FeedbackProvider>
                <AppRoutes />
                <ApiWarmupBanner />
              </FeedbackProvider>
            </SavedScholarshipsProvider>
          </AuthProvider>
        </BrowserRouter>
      </ErrorBoundary>
    </ThemeProvider>
  );
}
