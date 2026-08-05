import { lazy, Suspense, useEffect } from "react";
import { BrowserRouter, Routes, Route, useLocation, Navigate } from "react-router-dom";
import { ThemeProvider } from "./contexts/ThemeContext";
import { AuthProvider } from "./contexts/AuthContext";
import { SavedScholarshipsProvider } from "./contexts/SavedScholarshipsContext";
import { LandingPage } from "./pages/LandingPage";
import { PublicLayout, PublicShell } from "./components/layout/PublicLayout";
import { DashboardLayout } from "./components/layout/DashboardLayout";
import { AdaptiveSearchLayout } from "./components/layout/AdaptiveSearchLayout";
import { FeedbackProvider } from "./components/FeedbackModal";
import { AdminGuard } from "./components/AdminGuard";
import { SponsorGuard } from "./components/SponsorGuard";
import { SchoolGuard } from "./components/SchoolGuard";
import { OfflineIndicator } from "./components/OfflineIndicator";
import { SessionExpiryHandler } from "./components/SessionExpiryHandler";
import { ApiWarmupBanner } from "./components/ApiWarmupBanner";
import { ErrorBoundary } from "./components/ErrorBoundary";
import { RouteFallbackSkeleton } from "./components/LoadingSkeletons";
import { ScrollToTop } from "./components/ScrollToTop";
import { BackToTopButton } from "./components/BackToTopButton";
import { Toaster } from "@/components/ui/sonner";

const LoginPage = lazy(() => import("./pages/LoginPage").then((m) => ({ default: m.LoginPage })));
const RegisterPage = lazy(() => import("./pages/RegisterPage").then((m) => ({ default: m.RegisterPage })));
const ForgotPasswordPage = lazy(() =>
  import("./pages/ForgotPasswordPage").then((m) => ({ default: m.ForgotPasswordPage }))
);
const ResetPasswordPage = lazy(() =>
  import("./pages/ResetPasswordPage").then((m) => ({ default: m.ResetPasswordPage }))
);
const VerifyEmailPage = lazy(() => import("./pages/VerifyEmailPage").then((m) => ({ default: m.VerifyEmailPage })));

const AboutPage = lazy(() => import("./pages/AboutPage").then((m) => ({ default: m.AboutPage })));
const TermsPage = lazy(() => import("./pages/TermsPage").then((m) => ({ default: m.TermsPage })));
const PrivacyPage = lazy(() => import("./pages/PrivacyPage").then((m) => ({ default: m.PrivacyPage })));
const ChangelogPage = lazy(() => import("./pages/ChangelogPage").then((m) => ({ default: m.ChangelogPage })));
const NotFoundPage = lazy(() => import("./pages/NotFoundPage").then((m) => ({ default: m.NotFoundPage })));
const HowItWorksPage = lazy(() => import("./pages/HowItWorksPage").then((m) => ({ default: m.HowItWorksPage })));
const HowMatchingWorksPage = lazy(() =>
  import("./pages/HowMatchingWorksPage").then((m) => ({ default: m.HowMatchingWorksPage }))
);
const VerificationPage = lazy(() =>
  import("./pages/VerificationPage").then((m) => ({ default: m.VerificationPage }))
);
const ContactPage = lazy(() => import("./pages/ContactPage").then((m) => ({ default: m.ContactPage })));
const OpportunityComingSoonPage = lazy(() =>
  import("./pages/OpportunityComingSoonPage").then((m) => ({ default: m.OpportunityComingSoonPage }))
);
const ScholarshipStatusPage = lazy(() =>
  import("./pages/ScholarshipStatusPage").then((m) => ({ default: m.ScholarshipStatusPage }))
);
const FaqPage = lazy(() => import("./pages/FaqPage").then((m) => ({ default: m.FaqPage })));
const DesignSystemPage = lazy(() =>
  import("./pages/DesignSystemPage").then((m) => ({ default: m.DesignSystemPage }))
);

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
const ProfileBuilderPage = lazy(() =>
  import("./pages/ProfileBuilderPage").then((m) => ({ default: m.ProfileBuilderPage }))
);
const SponsorPortalPage = lazy(() =>
  import("./pages/SponsorPortalPage").then((m) => ({ default: m.SponsorPortalPage }))
);
const SchoolPortalPage = lazy(() =>
  import("./pages/SchoolPortalPage").then((m) => ({ default: m.SchoolPortalPage }))
);
const OpportunityPlannerPage = lazy(() =>
  import("./pages/OpportunityPlannerPage").then((m) => ({ default: m.OpportunityPlannerPage }))
);
const OrganizationPage = lazy(() =>
  import("./pages/OrganizationPage").then((m) => ({ default: m.OrganizationPage }))
);

function RouteFallback() {
  return <RouteFallbackSkeleton />;
}

/** Scroll to in-page anchors when navigating to /path#section (e.g. /how-it-works#verification). */
function ScrollToHashElement() {
  const { pathname, hash } = useLocation();

  useEffect(() => {
    if (!hash) return;
    const id = decodeURIComponent(hash.slice(1));
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [pathname, hash]);

  return null;
}

function AppRoutes() {
  return (
    <Suspense fallback={<RouteFallback />}>
      <Routes>
        <Route element={<PublicLayout />}>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
          <Route path="/reset-password" element={<ResetPasswordPage />} />
          <Route path="/verify-email" element={<VerifyEmailPage />} />
          <Route path="/how-it-works" element={<HowItWorksPage />} />
          <Route path="/how-matching-works" element={<HowMatchingWorksPage />} />
          <Route path="/how-we-verify" element={<VerificationPage />} />
          <Route path="/transparency" element={<Navigate to="/how-matching-works" replace />} />
          <Route path="/match-methodology" element={<Navigate to="/how-matching-works#methodology" replace />} />
          <Route path="/why-iskonnect" element={<Navigate to="/how-matching-works#why" replace />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="/opportunities/:typeSlug" element={<OpportunityComingSoonPage />} />
          <Route path="/scholarship-status" element={<ScholarshipStatusPage />} />
          <Route path="/faq" element={<FaqPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/terms" element={<TermsPage />} />
          <Route path="/privacy" element={<PrivacyPage />} />
          <Route path="/changelog" element={<ChangelogPage />} />
          <Route path="/design-system" element={<DesignSystemPage />} />
          <Route path="/organizations/:slug" element={<OrganizationPage />} />
        </Route>

        <Route
          path="/scholarships/search"
          element={
            <AdaptiveSearchLayout>
              <ScholarshipSearchPage />
            </AdaptiveSearchLayout>
          }
        />

        <Route
          path="/scholarship/:id"
          element={
            <PublicShell>
              <Suspense fallback={<RouteFallback />}>
                <ScholarshipDetailPage />
              </Suspense>
            </PublicShell>
          }
        />

        <Route element={<DashboardLayout />}>
          <Route path="/dashboard" element={<ProfileDashboard />} />
          <Route path="/planner/:profileId" element={<OpportunityPlannerPage />} />
          <Route path="/match/:profileId" element={<MatchResultsPage />} />
          <Route path="/match-compare" element={<MatchComparisonPage />} />
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
          <ScrollToTop />
          <ScrollToHashElement />          <AuthProvider>
            <SavedScholarshipsProvider>
              <FeedbackProvider>
                <SessionExpiryHandler />
                <AppRoutes />
                <OfflineIndicator />
                <ApiWarmupBanner />
                <BackToTopButton />
                <Toaster richColors closeButton position="top-center" />              </FeedbackProvider>
            </SavedScholarshipsProvider>
          </AuthProvider>
        </BrowserRouter>
      </ErrorBoundary>
    </ThemeProvider>
  );
}
