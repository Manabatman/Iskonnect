import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ThemeProvider } from "./contexts/ThemeContext";
import { AuthProvider } from "./contexts/AuthContext";
import { SavedScholarshipsProvider } from "./contexts/SavedScholarshipsContext";
import { MatchResultsPage } from "./pages/MatchResultsPage";
import { ScholarshipDetailPage } from "./pages/ScholarshipDetailPage";
import { AboutPage } from "./pages/AboutPage";
import { TermsPage } from "./pages/TermsPage";
import { PrivacyPage } from "./pages/PrivacyPage";
import { SettingsPage } from "./pages/SettingsPage";
import { ChangelogPage } from "./pages/ChangelogPage";
import { AdminPage } from "./pages/AdminPage";
import { AdminAnalyticsPage } from "./pages/AdminAnalyticsPage";
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/RegisterPage";
import { ProfileDashboard } from "./pages/ProfileDashboard";
import { MatchComparisonPage } from "./pages/MatchComparisonPage";
import { ScholarshipList } from "./components/ScholarshipList";
import { ScholarshipSearchPage } from "./pages/ScholarshipSearchPage";
import { NotFoundPage } from "./pages/NotFoundPage";
import { ApplicationsPage } from "./pages/ApplicationsPage";
import { DocumentsPage } from "./pages/DocumentsPage";
import { OpportunityBrowserPage } from "./pages/OpportunityBrowserPage";
import { ProfileBuilderPage } from "./pages/ProfileBuilderPage";
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
import { SponsorPortalPage } from "./pages/SponsorPortalPage";
import { SchoolPortalPage } from "./pages/SchoolPortalPage";

function AppRoutes() {
  return (
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
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <AuthProvider>
          <SavedScholarshipsProvider>
            <FeedbackProvider>
              <AppRoutes />
            </FeedbackProvider>
          </SavedScholarshipsProvider>
        </AuthProvider>
      </BrowserRouter>
    </ThemeProvider>
  );
}
