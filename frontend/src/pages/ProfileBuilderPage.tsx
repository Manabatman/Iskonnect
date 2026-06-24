import { useCallback, useEffect, useMemo, useReducer, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiFetch } from "../api/client";
import { SplitLayout } from "../components/layout/SplitLayout";
import { EducationStep } from "../components/profile-builder/EducationStep";
import { EligibilityGoalsStep } from "../components/profile-builder/EligibilityGoalsStep";
import { FieldOfStudyStep } from "../components/profile-builder/FieldOfStudyStep";
import { LocationBackgroundStep } from "../components/profile-builder/LocationBackgroundStep";
import { PersonalInfoStep } from "../components/profile-builder/PersonalInfoStep";
import {
  DRAFT_KEY,
  INITIAL_STATE,
  type ProfileBuilderState,
  parseDraftFromStorage,
  profileBuilderReducer,
} from "../components/profile-builder/profileBuilderState";
import { StepperSidebar } from "../components/profile-builder/StepperSidebar";
import { useAuth } from "../contexts/AuthContext";
import { buildStudentProfileFromBuilderState } from "../utils/studentProfilePayload";
import { profileToInitialValues } from "../utils/profileDraft";

const SAVE_DEBOUNCE_MS = 400;
const TOTAL_STEPS = 5;

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
  const [state, dispatch] = useReducer(profileBuilderReducer, INITIAL_STATE, initFromStorage);
  const [currentStep, setCurrentStep] = useState(1);
  const [serverLoading, setServerLoading] = useState(false);
  const [saveLoading, setSaveLoading] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [saveOk, setSaveOk] = useState<string | null>(null);
  const saveTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

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
        const flat = profileToInitialValues(row as { id?: number; [key: string]: unknown });
        dispatch({ type: "LOAD_DRAFT", draft: flat });
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

  const goNext = () => setCurrentStep((s) => Math.min(TOTAL_STEPS, s + 1));
  const goBack = () => setCurrentStep((s) => Math.max(1, s - 1));

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

  const saveToServer = useCallback(async () => {
    setSaveError(null);
    setSaveOk(null);
    if (!user) {
      navigate("/login", { state: { from: "/profile-builder" } });
      return;
    }
    if (state.privacy_consent !== "on") {
      setSaveError("Please confirm the privacy consent checkbox before saving your profile.");
      return;
    }
    if (!state.full_name?.trim() || state.full_name.trim().length < 2) {
      setSaveError("Please enter your full name (at least 2 characters).");
      return;
    }
    if (!state.email?.trim() || !state.email.includes("@")) {
      setSaveError("Please enter a valid email address.");
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
        throw new Error(data?.detail ?? "Unable to save profile");
      }
      setSaveOk("Profile saved to your account.");
    } catch (e) {
      setSaveError(e instanceof Error ? e.message : "Save failed");
    } finally {
      setSaveLoading(false);
    }
  }, [user, navigate, state, authHeaders]);

  return (
    <section className="px-4 py-6 sm:px-6 lg:py-8" aria-labelledby="profile-builder-title">
      <div className="mx-auto max-w-7xl">
        <div className="mb-6 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h1 id="profile-builder-title" className="text-2xl font-semibold text-slate-900 dark:text-slate-100">
              Complete Your Profile
            </h1>
            <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
              Guided steps — your progress saves automatically to this device
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

        {saveOk ? (
          <p className="mb-4 rounded-lg border border-green-200 bg-green-50 px-3 py-2 text-sm text-green-900 dark:border-green-800 dark:bg-green-950/50 dark:text-green-100">
            {saveOk}
          </p>
        ) : null}
        {saveError ? (
          <p className="mb-4 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-900 dark:border-red-800 dark:bg-red-950/50 dark:text-red-100">
            {saveError}
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
                  className="rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm font-medium text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700"
                >
                  Back
                </button>
                <div className="flex flex-col gap-3 sm:ml-auto sm:flex-row sm:items-center">
                  {currentStep < TOTAL_STEPS ? (
                    <button
                      type="button"
                      onClick={goNext}
                      className="rounded-lg bg-primary-600 px-5 py-2.5 text-sm font-semibold text-white shadow transition hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-slate-800"
                    >
                      Next
                    </button>
                  ) : (
                    <>
                      <button
                        type="button"
                        onClick={saveToServer}
                        disabled={saveLoading}
                        className="rounded-lg bg-primary-600 px-5 py-2.5 text-sm font-semibold text-white shadow transition hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-60 dark:focus:ring-offset-slate-800"
                      >
                        {saveLoading ? "Saving…" : "Save Profile"}
                      </button>
                      <p className="text-sm text-slate-600 dark:text-slate-400">
                        Or run matches from your{" "}
                        <Link to="/dashboard" className="font-medium text-primary-600 dark:text-primary-400">
                          dashboard
                        </Link>
                        .
                      </p>
                    </>
                  )}
                </div>
              </div>
            </div>
          }
        />
      </div>
    </section>
  );
}
