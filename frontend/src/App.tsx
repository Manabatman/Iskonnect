import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "./contexts/ThemeContext";
import { AuthProvider } from "./contexts/AuthContext";
import { MatchResultsPage } from "./pages/MatchResultsPage";
import { ScholarshipDetailPage } from "./pages/ScholarshipDetailPage";
import { AboutPage } from "./pages/AboutPage";
import { TermsPage } from "./pages/TermsPage";
import { PrivacyPage } from "./pages/PrivacyPage";
import { SettingsPage } from "./pages/SettingsPage";
import { ChangelogPage } from "./pages/ChangelogPage";
import { AdminPage } from "./pages/AdminPage";
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
import { PublicLayout, PublicShell } from "./components/layout/PublicLayout";
import { DashboardLayout } from "./components/layout/DashboardLayout";

function AppRoutes() {
  return (
    <Routes>
      <Route element={<PublicLayout />}>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/terms" element={<TermsPage />} />
        <Route path="/privacy" element={<PrivacyPage />} />
        <Route path="/changelog" element={<ChangelogPage />} />
      </Route>

      <Route element={<DashboardLayout />}>
        <Route path="/dashboard" element={<ProfileDashboard />} />
        <Route path="/match/:profileId" element={<MatchResultsPage />} />
        <Route path="/match-compare" element={<MatchComparisonPage />} />
        <Route path="/scholarship/:id" element={<ScholarshipDetailPage />} />
        <Route path="/opportunities" element={<OpportunityBrowserPage />} />
        <Route path="/scholarships/search" element={<ScholarshipSearchPage />} />
        <Route path="/scholarships" element={<ScholarshipList />} />
        <Route path="/profile-builder" element={<ProfileBuilderPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/admin" element={<AdminPage />} />
        <Route path="/applications" element={<ApplicationsPage />} />
        <Route path="/documents" element={<DocumentsPage />} />
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
          <AppRoutes />
        </AuthProvider>
      </BrowserRouter>
    </ThemeProvider>
  );
}
