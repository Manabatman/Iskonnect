import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { LandingMotionProvider } from "../components/landing/LandingMotionProvider";
import { BenefitsSection } from "../components/landing/BenefitsSection";
import { FaqSection } from "../components/landing/FaqSection";
import { FinalCtaSection } from "../components/landing/FinalCtaSection";
import { HeroSection } from "../components/landing/HeroSection";
import { MiniProfileWizard } from "../components/landing/MiniProfileWizard";
import { HowItWorksSection } from "../components/landing/HowItWorksSection";
import { OfficialSourcesBar } from "../components/landing/OfficialSourcesBar";
import { ProblemSection } from "../components/landing/ProblemSection";
import { TrustSection } from "../components/landing/TrustSection";

export function LandingPage() {
  const { user, loading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!loading && user) {
      navigate("/dashboard", { replace: true });
    }
  }, [loading, user, navigate]);

  if (loading) {
    return (
      <div className="flex min-h-[50vh] items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="h-10 w-10 animate-spin rounded-full border-2 border-primary-500 border-t-transparent" />
          <p className="text-sm text-slate-500 dark:text-slate-400">Loading…</p>
        </div>
      </div>
    );
  }

  if (user) {
    return null;
  }

  return (
    <LandingMotionProvider>
      <div className="overflow-hidden">
        <HeroSection />
        <MiniProfileWizard />
        <OfficialSourcesBar />
        <ProblemSection />
        <HowItWorksSection />
        <TrustSection />
        <BenefitsSection />
        <FaqSection />
        <FinalCtaSection />
      </div>
    </LandingMotionProvider>
  );
}
