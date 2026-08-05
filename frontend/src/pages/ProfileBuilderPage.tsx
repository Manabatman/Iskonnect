import { useCallback, useEffect, useMemo, useReducer, useRef, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { apiFetch } from "../api/client";
import { ConsentRequiredModal } from "../components/ConsentRequiredModal";
import { SplitLayout } from "../components/layout/SplitLayout";
import { EducationStep } from "../components/profile-builder/EducationStep";
import { EligibilityGoalsStep } from "../components/profile-builder/EligibilityGoalsStep";
import { FieldOfStudyStep } from "../components/profile-builder/FieldOfStudyStep";
import { LocationBackgroundStep } from "../components/profile-builder/LocationBackgroundStep";
import { PersonalInfoStep } from "../components/profile-builder/PersonalInfoStep";
import {
  DRAFT_KEY,
  INITIAL_STATE,
  clearProfileDraft,
  mergeProfileDrafts,
  parseDraftFromStorage,
  validateProfileBuilderStep,
  type ProfileBuilderState,
  profileBuilderReducer,
} from "../components/profile-builder/profileBuilderState";
import { StepperSidebar } from "../components/profile-builder/StepperSidebar";
import { SuccessModal } from "@/components/ui/success-modal";
import { AUTH_USER_CHANGED_EVENT, type AuthUserChangedDetail, useAuth } from "../contexts/AuthContext";
import { buildStudentProfileFromBuilderState } from "../utils/studentProfilePayload";
import { parseApiDetail } from "../utils/apiErrors";
import { profileToInitialValues } from "../utils/profileDraft";
import { validateEmail } from "../utils/validateEmail";

const SAVE_DEBOUNCE_MS = 400;
const TOTAL_STEPS = 5;

const STEP_SLUG_TO_NUMBER: Record<string, number> = {
  personal: 1,
  education: 2,
  location: 3,
  field: 4,
  goals: 5,
};

function initFromStorage(): ProfileBuilderState {
  try {
    const raw = localStorage.getItem(DRAFT_KEY);
    const draft = parseDraftFromStorage(raw);
    if (draft && Object.keys(draft).length > 0) {
      return profileBuilderReducer(INITIAL_STATE, { type: "LOAD_DRAFT", draft });
    }
  } catch {
    /* ignore */
  }
  return INITIAL_STATE;
}

export function ProfileBuilderPage() {
  const { user, authHeaders, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [state, dispatch] = useReducer(profileBuilderReducer, INITIAL_STATE, initFromStorage);
  const [currentStep, setCurrentStep] = useState(1);
  const [serverLoading, setServerLoading] = useState(false);
  const [saveLoading, setSaveLoading] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [stepError, setStepError] = useState<string | null>(null);
  const [consentModalOpen, setConsentModalOpen] = useState(false);
  const [successModalOpen, setSuccessModalOpen] = useState(false);
  const saveTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const hadProfileOnLoadRef = useRef(false);
  const redirectTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    const onAuthChange = (event: Event) => {
      const detail = (event as CustomEvent<AuthUserChangedDetail>).detail;
      const prev = detail?.previousUserId ?? null;
      const next = detail?.userId ?? null;
      // Anonymous → authenticated: keep local draft; server merge runs in profiles/me effect.
      if (prev === null && next !== null) return;
      if (next === null || (prev !== null && prev !== next)) {
        clearProfileDraft();
        dispatch({ type: "RESET" });
        setCurrentStep(1);
      }
    };
    window.addEventListener(AUTH_USER_CHANGED_EVENT, onAuthChange);
    return () => window.removeEventListener(AUTH_USER_CHANGED_EVENT, onAuthChange);
  }, []);

  useEffect(() => {
    if (authLoading || !user) return;
    let cancelled = false;
    setServerLoading(true);
    apiFetch("/api/v1/profiles/me", { headers: authHeaders() })
      .then((r) => {
        if (r.status === 404) return null;
        return r.ok ? r.json() : null;
      })
      .then((row: unknown) => {
        if (cancelled || !row || typeof row !== "object") return;
        if ("id" in row && row.id != null) {
          hadProfileOnLoadRef.current = true;
        }
        const serverFlat = profileToInitialValues(row as { id?: number; [key: string]: unknown });
        const localDraft = parseDraftFromStorage(localStorage.getItem(DRAFT_KEY)) ?? {};
        const merged = mergeProfileDrafts(localDraft, serverFlat);
        dispatch({ type: "LOAD_DRAFT", draft: merged });
      })
      .catch(() => {
        /* keep local draft */
      })
      .finally(() => {
        if (!cancelled) setServerLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [user, authLoading, authHeaders]);

  useEffect(() => {
    const stepSlug = searchParams.get("step");
    if (!stepSlug) return;
    const stepNum = STEP_SLUG_TO_NUMBER[stepSlug];
    if (stepNum >= 1 && stepNum <= TOTAL_STEPS) {
      setCurrentStep(stepNum);
    }
  }, [searchParams]);

  const emailPrefilledRef = useRef(false);
  useEffect(() => {
    const onAuthChange = () => {
      emailPrefilledRef.current = false;
    };
    window.addEventListener(AUTH_USER_CHANGED_EVENT, onAuthChange);
    return () => window.removeEventListener(AUTH_USER_CHANGED_EVENT, onAuthChange);
  }, []);

  useEffect(() => {
    if (authLoading || serverLoading || !user?.email) return;
    if (emailPrefilledRef.current) return;
    if (!state.email.trim()) {
      dispatch({ type: "SET_FIELD", field: "email", value: user.email });
      emailPrefilledRef.current = true;
    }
  }, [user?.email, authLoading, serverLoading, state.email]);

  useEffect(() => {
    if (saveTimeoutRef.current) clearTimeout(saveTimeoutRef.current);
    saveTimeoutRef.current = setTimeout(() => {
      try {
        const payload: Record<string, string> = {};
        (Object.keys(INITIAL_STATE) as (keyof ProfileBuilderState)[]).forEach((k) => {
          payload[k] = state[k];
        });
        localStorage.setItem(DRAFT_KEY, JSON.stringify(payload));
      } catch {
        /* quota */
      }
    }, SAVE_DEBOUNCE_MS);
    return () => {
      if (saveTimeoutRef.current) clearTimeout(saveTimeoutRef.current);
    };
  }, [state]);

  const onChange = useCallback((field: keyof ProfileBuilderState, value: string) => {
    dispatch({ type: "SET_FIELD", field, value });
  }, []);

  const goNext = () => {
    const validationError = validateProfileBuilderStep(currentStep, state, validateEmail);
    if (validationError) {
      setStepError(validationError);
      return;
    }
    setStepError(null);
    setCurrentStep((s) => Math.min(TOTAL_STEPS, s + 1));
  };
  const goBack = () => {
    setStepError(null);
    setCurrentStep((s) => Math.max(1, s - 1));
  };

  const stepContent = useMemo(() => {
    switch (currentStep) {
      case 1:
        return <PersonalInfoStep state={state} onChange={onChange} />;
      case 2:
        return <EducationStep state={state} onChange={onChange} />;
      case 3:
        return <LocationBackgroundStep state={state} onChange={onChange} />;
      case 4:
        return <FieldOfStudyStep state={state} onChange={onChange} />;
      case 5:
        return <EligibilityGoalsStep state={state} onChange={onChange} />;
      default:
        return null;
    }
  }, [currentStep, state, onChange]);

  useEffect(() => {
    return () => {
      if (redirectTimeoutRef.current) clearTimeout(redirectTimeoutRef.current);
    };
  }, []);

  const saveToServer = useCallback(async () => {
    setSaveError(null);
    if (!user) {
      navigate("/login", { state: { from: "/profile-builder" } });
      return;
    }
    if (state.privacy_consent !== "on") {
      setConsentModalOpen(true);
      return;
    }
    if (!state.full_name?.trim() || state.full_name.trim().length < 2) {
      setSaveError("Please enter your full name (at least 2 characters).");
      return;
    }
    if (!state.email?.trim()) {
      setSaveError("Please enter a valid email address.");
      return;
    }
    const emailCheck = validateEmail(state.email);
    if (!emailCheck.valid) {
      setSaveError(emailCheck.message ?? "Please enter a valid email address.");
      return;
    }
    if (!state.region?.trim()) {
      setSaveError("Please select your region before saving.");
      return;
    }
    setSaveLoading(true);
    try {
      const profile = buildStudentProfileFromBuilderState(state);
      const headers: Record<string, string> = { "Content-Type": "application/json", ...authHeaders() };
      const res = await apiFetch("/api/v1/profiles", {
        method: "POST",
        headers,
        body: JSON.stringify(profile),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(parseApiDetail(data?.detail, "Unable to save profile"));
      }
      clearProfileDraft();
      hadProfileOnLoadRef.current = true;
      setSuccessModalOpen(true);
      redirectTimeoutRef.current = setTimeout(() => {
        navigate("/scholarships/search", { replace: true });
      }, 1200);
    } catch (e) {
      setSaveError(e instanceof Error ? e.message : "Save failed");
    } finally {
      setSaveLoading(false);
    }
  }, [user, navigate, state, authHeaders, currentStep]);

  return (
    <section className="px-4 py-6 sm:px-6 lg:py-8" aria-labelledby="profile-builder-title">
      <div className="mx-auto max-w-7xl">
        <div className="mb-6 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h1 id="profile-builder-title" className="text-2xl font-semibold text-slate-900 dark:text-slate-100">
              Complete Your Profile
            </h1>
            <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
              Guided steps. Your progress saves automatically to this device
              {user ? " and can be synced to your account." : "."}
            </p>
            {!user ? (
              <p className="mt-2 text-sm text-amber-800 dark:text-amber-200">
                <Link to="/login" className="font-medium underline">
                  Sign in
                </Link>{" "}
                to load and save your profile to the server.
              </p>
            ) : null}
            {serverLoading ? (
              <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">Loading profile from server…</p>
            ) : null}
          </div>
          <Link
            to="/settings"
            className="text-sm font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400"
          >
            Account settings
          </Link>
        </div>

        {saveError ? (
          <p className="mb-4 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-900 dark:border-red-800 dark:bg-red-950/50 dark:text-red-100" role="alert">
            {saveError}
          </p>
        ) : null}
        {stepError ? (
          <p className="mb-4 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-900 dark:border-amber-800 dark:bg-amber-950/50 dark:text-amber-100" role="alert">
            {stepError}
          </p>
        ) : null}

        <SplitLayout
          listWidthClassName="lg:w-[min(280px,30%)]"
          listPane={<StepperSidebar currentStep={currentStep} onStepClick={setCurrentStep} state={state} />}
          detailPane={
            <div className="flex min-h-0 flex-col">
              <div className="min-h-0 flex-1">{stepContent}</div>
              <div className="mt-8 flex flex-col gap-3 border-t border-slate-200 pt-6 dark:border-slate-700 sm:flex-row sm:justify-between">
                <button
                  type="button"
                  onClick={goBack}
                  disabled={currentStep <= 1}
                  className="rounded-lg border border-slate-300 bg-white px-4 py-3 text-sm font-medium text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700"
                >
                  Back
                </button>
                <div className="flex flex-col gap-3 sm:ml-auto sm:flex-row sm:items-center">
                  {currentStep < TOTAL_STEPS ? (
                    <button
                      type="button"
                      onClick={goNext}
                      className="rounded-lg bg-primary-600 px-5 py-3 text-sm font-semibold text-white shadow transition hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-slate-800"
                    >
                      Next
                    </button>
                  ) : (
                    <>
                      <button
                        type="button"
                        onClick={saveToServer}
                        disabled={saveLoading}
                        className="rounded-lg bg-primary-600 px-5 py-3 text-sm font-semibold text-white shadow transition hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-60 dark:focus:ring-offset-slate-800"
                      >
                        {saveLoading ? "Saving…" : "Save Profile"}
                      </button>
                    </>
                  )}
                </div>
              </div>
            </div>
          }
        />
      </div>
      <ConsentRequiredModal
        open={consentModalOpen}
        onOpenChange={setConsentModalOpen}
        onGoToConsent={() => {
          setCurrentStep(5);
          window.setTimeout(() => {
            document.getElementById("privacy-consent-checkbox")?.focus();
          }, 150);
        }}
      />
      <SuccessModal
        open={successModalOpen}
        onOpenChange={setSuccessModalOpen}
        title="Profile saved"
        description="Your profile is ready. Taking you to Scholarships to explore matches."
        actionLabel="Go to Scholarships"
        onAction={() => navigate("/scholarships/search", { replace: true })}
      />
    </section>
  );
}
