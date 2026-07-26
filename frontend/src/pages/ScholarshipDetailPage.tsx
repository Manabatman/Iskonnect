import { useEffect, useMemo, useRef, useState } from "react";
import { Link, useParams, useNavigate, useLocation, useSearchParams } from "react-router-dom";
import { apiFetch } from "../api/client";
import { useAuth } from "../contexts/AuthContext";
import { FinancialPlannerCard } from "../components/dashboard/FinancialPlannerCard";
import {
  EligibilityRequirementsList,
  QualificationStatusBadge,
  VerificationBadge,
} from "../components/QualificationStatusBadge";
import { normalizeScholarshipRegions } from "../utils/normalizeLocation";
import { formatDateMedium } from "../utils/formatDate";
import { formatDeadlineDisplay, formatOpenDateDisplay } from "../utils/formatDeadline";
import { FreshnessChipRow, freshnessFromScholarship } from "../components/FreshnessChip";
import { LifecycleStatusBadge } from "../components/LifecycleStatusBadge";
import { TrustCard } from "../components/TrustCard";
import type { FieldEvidence, QualificationStatus, SavedScholarship, ScholarshipEligibilityDetail, ScholarshipVersionHistoryItem } from "../types";

const DOCUMENT_LABELS: Record<string, string> = {
  ITR: "Income Tax Return",
  BIRTH_CERT: "Birth Certificate",
  GOOD_MORAL: "Good Moral Certificate",
  TOR: "Transcript of Records",
  FORM_137: "Form 137 / School Records",
  BARANGAY_CERT: "Barangay Certificate",
  SKETCH_HOME: "Sketch of Home Location",
  ESSAY: "Application Essay",
  OFW_DOCS: "OFW POEA/DMW Records",
  "4PS_CERT": "4Ps/Listahanan Certificate",
};

interface ScholarshipDetail {
  id: number;
  title: string;
  provider: string;
  description: string;
  link: string | null;
  provider_type?: string | null;
  scholarship_type?: string | null;
  eligible_levels?: string[];
  eligible_regions?: string[];
  eligible_cities?: string[];
  eligible_school_types?: string[];
  eligible_courses_psced?: string[];
  max_income_threshold?: number | null;
  min_gwa_normalized?: number | null;
  min_age?: number | null;
  max_age?: number | null;
  benefit_tuition?: boolean;
  benefit_allowance_monthly?: number | null;
  benefit_books?: boolean;
  benefit_total_value?: number | null;
  required_documents?: string[];
  has_qualifying_exam?: boolean;
  has_interview?: boolean;
  has_essay_requirement?: boolean;
  has_return_service?: boolean;
  application_deadline?: string | null;
  deadline_precision?: string | null;
  deadline_note?: string | null;
  application_open_date?: string | null;
  next_review_date?: string | null;
  field_evidence?: FieldEvidence[];
  completeness_label?: string | null;
  academic_year_target?: string | null;
  image_url?: string | null;
  image_alt?: string | null;
  data_status?: string | null;
  application_status?: string | null;
  link_status?: string | null;
  verification_source?: string | null;
  confidence_score?: number | null;
  last_verified_at?: string | null;
  verification_badge?: string | null;
  verification_badge_label?: string | null;
  verification_source_label?: string | null;
  verification_date_label?: string | null;
  completeness_signal?: string | null;
  qualification_status?: QualificationStatus | string;
  qualifying_requirements?: string[];
  missing_requirements?: string[];
  eligibility_confidence?: string | null;
}

const ISSUE_TYPES = [
  { value: "broken_link", label: "Broken link" },
  { value: "wrong_deadline", label: "Incorrect deadline" },
  { value: "outdated_info", label: "Outdated information" },
  { value: "other", label: "Other" },
];

export function ScholarshipDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const [searchParams] = useSearchParams();
  const profileIdFromQuery = searchParams.get("profile_id");
  const { authHeaders, user } = useAuth();
  const requirementsRef = useRef<HTMLDivElement>(null);
  const eligibilityRef = useRef<HTMLDivElement>(null);
  const [requirementsHighlight, setRequirementsHighlight] = useState(false);
  const [scholarship, setScholarship] = useState<ScholarshipDetail | null>(null);
  const [eligibilityDetail, setEligibilityDetail] = useState<ScholarshipEligibilityDetail | null>(null);
  const [history, setHistory] = useState<ScholarshipVersionHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showReport, setShowReport] = useState(false);
  const [issueType, setIssueType] = useState("broken_link");
  const [reportDesc, setReportDesc] = useState("");
  const [reportSubmitting, setReportSubmitting] = useState(false);
  const [reportMsg, setReportMsg] = useState<string | null>(null);
  const [reportError, setReportError] = useState(false);
  const [profileId, setProfileId] = useState<number | null>(null);

  useEffect(() => {
    if (profileIdFromQuery) {
      setProfileId(Number(profileIdFromQuery));
      return;
    }
    if (!user) {
      setProfileId(null);
      return;
    }
    let cancelled = false;
    apiFetch("/api/v1/profiles/me", { headers: authHeaders() })
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (!cancelled && data?.id) setProfileId(Number(data.id));
      })
      .catch(() => {
        if (!cancelled) setProfileId(null);
      });
    return () => {
      cancelled = true;
    };
  }, [user, authHeaders, profileIdFromQuery]);

  useEffect(() => {
    if (!id) {
      setLoading(false);
      setError("Invalid scholarship");
      return;
    }
    let cancelled = false;
    setLoading(true);
    setError(null);
    const qs = profileId ? `?profile_id=${profileId}` : "";
    apiFetch(`/api/v1/scholarships/${id}${qs}`, { headers: authHeaders() })
      .then((res) => {
        if (!res.ok) throw new Error("Scholarship not found");
        return res.json();
      })
      .then((data) => {
        if (!cancelled) setScholarship(data);
      })
      .catch((err) => {
        if (!cancelled) setError(err instanceof Error ? err.message : "Something went wrong");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [id, profileId, authHeaders]);

  useEffect(() => {
    if (!id || !profileId) {
      setEligibilityDetail(null);
      return;
    }
    let cancelled = false;
    apiFetch(`/api/v1/scholarships/${id}/eligibility?profile_id=${profileId}`, { headers: authHeaders() })
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (!cancelled && data) setEligibilityDetail(data as ScholarshipEligibilityDetail);
      })
      .catch(() => {
        if (!cancelled) setEligibilityDetail(null);
      });
    return () => {
      cancelled = true;
    };
  }, [id, profileId, authHeaders]);

  useEffect(() => {
    if (!id) return;
    let cancelled = false;
    apiFetch(`/api/v1/scholarships/${id}/history`)
      .then((res) => (res.ok ? res.json() : []))
      .then((data) => {
        if (!cancelled) setHistory(Array.isArray(data) ? data : []);
      })
      .catch(() => {
        if (!cancelled) setHistory([]);
      });
    return () => {
      cancelled = true;
    };
  }, [id]);

  const plannerSaved = useMemo((): SavedScholarship[] => {
    if (!scholarship) return [];
    return [
      {
        id: scholarship.id,
        scholarship_id: scholarship.id,
        created_at: new Date().toISOString(),
        title: scholarship.title,
        provider: scholarship.provider,
        benefit_tuition: scholarship.benefit_tuition,
        benefit_allowance_monthly: scholarship.benefit_allowance_monthly,
        benefit_total_value: scholarship.benefit_total_value,
      },
    ];
  }, [scholarship]);

  useEffect(() => {
    if (!scholarship) return;
    const hash = location.hash.replace("#", "");
    const el =
      hash === "eligibility"
        ? eligibilityRef.current
        : hash === "requirements"
          ? requirementsRef.current
          : null;
    if (!el) return;
    const scrollTimer = window.setTimeout(() => {
      el.scrollIntoView({ behavior: "smooth", block: "center" });
      if (hash === "requirements") setRequirementsHighlight(true);
    }, 100);
    const unhighlightTimer =
      hash === "requirements" ? window.setTimeout(() => setRequirementsHighlight(false), 2900) : undefined;
    return () => {
      window.clearTimeout(scrollTimer);
      if (unhighlightTimer != null) window.clearTimeout(unhighlightTimer);
    };
  }, [scholarship, location.hash, id]);

  if (loading) {
    return (
      <section className="py-12">
        <div className="mx-auto max-w-3xl px-4">
          <div className="animate-pulse rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-12">
            <div className="h-8 w-3/4 rounded bg-slate-200 dark:bg-slate-700" />
            <div className="mt-6 h-4 w-full rounded bg-slate-100 dark:bg-slate-700" />
            <div className="mt-2 h-4 w-5/6 rounded bg-slate-100 dark:bg-slate-700" />
          </div>
        </div>
      </section>
    );
  }

  if (error || !scholarship) {
    return (
      <section className="py-12">
        <div className="mx-auto max-w-3xl px-4">
          <div className="rounded-xl border border-red-200 bg-red-50 p-8 text-center">
            <p className="text-red-700">{error || "Scholarship not found"}</p>
            <button
              type="button"
              onClick={() => navigate(-1)}
              className="mt-4 rounded-lg bg-primary-600 px-4 py-2 text-white hover:bg-primary-700"
            >
              Go back
            </button>
          </div>
        </div>
      </section>
    );
  }

  const regions = normalizeScholarshipRegions(scholarship.eligible_regions ?? [], scholarship.provider);
  const isNationwide = regions.length === 0 && !(scholarship.eligible_cities?.length);
  const hasLink = scholarship.link && scholarship.link.trim().startsWith("http");
  const activeQualification =
    eligibilityDetail?.qualification_status ?? scholarship.qualification_status;
  const activeQualifying =
    eligibilityDetail?.qualifying_requirements ?? scholarship.qualifying_requirements;
  const activeMissing =
    eligibilityDetail?.missing_requirements ?? scholarship.missing_requirements;
  const activeConfidence =
    eligibilityDetail?.eligibility_confidence ?? scholarship.eligibility_confidence;

  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <button
          type="button"
          onClick={() => navigate(-1)}
          className="mb-6 inline-flex items-center text-sm font-medium text-primary-600 hover:text-primary-700"
        >
          ← Back to results
        </button>

        <article className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-8 shadow-md">
          <div
            className="mb-6 rounded-lg border border-primary-200 bg-primary-50/80 px-4 py-3 text-sm leading-relaxed text-primary-900 dark:border-primary-800 dark:bg-primary-950/40 dark:text-primary-100"
            role="note"
          >
            <p className="font-medium">Always confirm on the official provider&apos;s site</p>
            <p className="mt-1 text-primary-800/90 dark:text-primary-200/90">
              Deadlines, income ceilings, and document requirements can change without notice. Before you apply, verify
              every detail on the scholarship provider&apos;s website.{" "}
              <Link to="/how-we-verify" className="font-medium underline hover:text-primary-700 dark:hover:text-primary-300">
                How we verify
              </Link>
              {" · "}
              <Link
                to="/scholarship-status"
                className="font-medium underline hover:text-primary-700 dark:hover:text-primary-300"
              >
                Status guide
              </Link>
            </p>
          </div>

          <div className="mb-6">
            <div className="flex flex-wrap gap-2">
              <LifecycleStatusBadge
                application_status={scholarship.application_status}
                data_status={scholarship.data_status}
              />
              {scholarship.provider_type && (
                <span className="rounded bg-slate-100 dark:bg-slate-700 px-2 py-0.5 text-xs font-medium text-slate-600 dark:text-slate-400">
                  {scholarship.provider_type}
                </span>
              )}
              {scholarship.scholarship_type && (
                <span className="rounded bg-slate-100 dark:bg-slate-700 px-2 py-0.5 text-xs font-medium text-slate-600 dark:text-slate-400">
                  {scholarship.scholarship_type}
                </span>
              )}
              {scholarship.link_status === "broken" ? (
                <span className="rounded bg-amber-100 dark:bg-amber-900/50 px-2 py-0.5 text-xs font-medium text-amber-900 dark:text-amber-200">
                  Link issue
                </span>
              ) : null}
              <FreshnessChipRow chips={freshnessFromScholarship(scholarship)} />
              <VerificationBadge
                badge={scholarship.verification_badge}
                label={scholarship.verification_badge_label}
              />
              {scholarship.verification_date_label ? (
                <span className="rounded bg-slate-100 px-2 py-0.5 text-xs text-slate-600 dark:bg-slate-700 dark:text-slate-300">
                  {scholarship.verification_date_label}
                </span>
              ) : null}
              {scholarship.completeness_signal ? (
                <span className="rounded bg-slate-100 px-2 py-0.5 text-xs text-slate-600 dark:bg-slate-700 dark:text-slate-300">
                  {scholarship.completeness_signal}
                </span>
              ) : null}
            </div>
            {activeQualification ? (
              <div
                ref={eligibilityRef}
                id="eligibility"
                className="mt-4 scroll-mt-24 rounded-lg border border-slate-200 bg-slate-50/80 p-4 dark:border-slate-600 dark:bg-slate-900/40 md:scroll-mt-28"
              >
                <div className="flex flex-wrap items-center gap-2">
                  <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                    {eligibilityDetail?.passes_for_matching === false
                      ? "Why you don't match"
                      : "Why you match"}
                  </h2>
                  <QualificationStatusBadge status={activeQualification} />
                </div>
                {activeConfidence ? (
                  <p className="mt-2 text-xs text-slate-600 dark:text-slate-400">
                    Confidence: {String(activeConfidence).replace(/_/g, " ")}
                  </p>
                ) : null}
                <EligibilityRequirementsList qualifying={activeQualifying} missing={activeMissing} />
                {!profileId ? (
                  <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">
                    <Link to="/login" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
                      Sign in
                    </Link>{" "}
                    and complete your profile to see personalized eligibility.
                  </p>
                ) : null}
              </div>
            ) : null}
            {scholarship.image_url ? (
              <img
                src={scholarship.image_url}
                alt={scholarship.image_alt?.trim() || scholarship.title}
                className="mt-4 h-48 w-full rounded-xl object-cover"
                loading="lazy"
              />
            ) : (
              <p className="mt-4 text-xs text-slate-500">No banner image assigned yet.</p>
            )}
            <h1 className="mt-2 text-2xl font-bold text-slate-900 dark:text-slate-100">{scholarship.title}</h1>
            <p className="mt-1 text-slate-600 dark:text-slate-400">{scholarship.provider}</p>
          </div>

          {scholarship.description && (
            <div className="mb-8">
              <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">Overview</h2>
              <p className="mt-2 text-slate-700 dark:text-slate-300">{scholarship.description}</p>
            </div>
          )}

          <div className="mb-8">
            <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">Eligibility Summary</h2>
            <ul className="mt-2 space-y-1 text-sm text-slate-700 dark:text-slate-300">
              {scholarship.eligible_levels?.length ? (
                <li>Education level: {scholarship.eligible_levels.join(", ")}</li>
              ) : null}
              {scholarship.eligible_school_types?.length ? (
                <li>School type: {scholarship.eligible_school_types.join(", ")}</li>
              ) : null}
              {scholarship.eligible_courses_psced?.length ? (
                <li>Field of study: {scholarship.eligible_courses_psced.join(", ")}</li>
              ) : null}
              {scholarship.min_gwa_normalized != null && (
                <li>Minimum GWA: {scholarship.min_gwa_normalized}%</li>
              )}
              {scholarship.max_income_threshold != null && (
                <li>Income ceiling: PHP {scholarship.max_income_threshold.toLocaleString()}/year</li>
              )}
              {(scholarship.min_age != null || scholarship.max_age != null) && (
                <li>
                  Age: {scholarship.min_age != null ? `Min ${scholarship.min_age}` : ""}
                  {scholarship.min_age != null && scholarship.max_age != null && " • "}
                  {scholarship.max_age != null ? `Max ${scholarship.max_age}` : ""}
                </li>
              )}
              {isNationwide ? (
                <li>Region: Nationwide</li>
              ) : scholarship.eligible_cities?.length ? (
                <li>City: {scholarship.eligible_cities.join(", ")}</li>
              ) : regions.length ? (
                <li>Region: {regions.join(", ")}</li>
              ) : null}
            </ul>
          </div>

          <div className="mb-8">
            <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">Benefits</h2>
            <ul className="mt-2 space-y-1 text-sm text-slate-700 dark:text-slate-300">
              {scholarship.benefit_tuition && <li>Tuition coverage</li>}
              {scholarship.benefit_allowance_monthly != null && scholarship.benefit_allowance_monthly > 0 && (
                <li>Monthly allowance: ₱{scholarship.benefit_allowance_monthly.toLocaleString()}</li>
              )}
              {scholarship.benefit_books && <li>Books allowance</li>}
              {scholarship.benefit_total_value != null && scholarship.benefit_total_value > 0 && (
                <li className="font-medium text-primary-700 dark:text-primary-400">
                  Total value: up to ₱{scholarship.benefit_total_value.toLocaleString()}/year
                </li>
              )}
              {!scholarship.benefit_tuition &&
                !scholarship.benefit_allowance_monthly &&
                !scholarship.benefit_books &&
                (!scholarship.benefit_total_value || scholarship.benefit_total_value === 0) && (
                  <li className="text-slate-500 dark:text-slate-400">See official website for details</li>
                )}
            </ul>
          </div>

          <div
            ref={requirementsRef}
            id="requirements"
            className={[
              "mb-8 scroll-mt-24 rounded-xl p-4 transition-[box-shadow,background-color] duration-500 md:scroll-mt-28",
              requirementsHighlight
                ? "bg-primary-50/90 shadow-[0_0_0_3px_rgba(59,130,246,0.45)] dark:bg-primary-950/50 dark:shadow-[0_0_0_3px_rgba(96,165,250,0.35)]"
                : "",
            ].join(" ")}
          >
            <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">Requirements</h2>
            <ul className="mt-2 space-y-1 text-sm text-slate-700 dark:text-slate-300">
              {scholarship.has_qualifying_exam && <li>Qualifying exam</li>}
              {scholarship.has_interview && <li>Interview</li>}
              {scholarship.has_essay_requirement && <li>Application essay</li>}
              {scholarship.has_return_service && <li>Return service obligation</li>}
            </ul>
            {scholarship.required_documents && scholarship.required_documents.length > 0 && (
              <div className="mt-3">
                <h3 className="text-xs font-medium text-slate-600 dark:text-slate-400">Documents required</h3>
                <ul className="mt-1 space-y-0.5 text-sm text-slate-700 dark:text-slate-300">
                  {scholarship.required_documents.map((doc, i) => (
                    <li key={doc ?? `doc-${i}`}>
                      {DOCUMENT_LABELS[String(doc ?? "")] ||
                        String(doc ?? "").replace(/_/g, " ") ||
                        "—"}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          <TrustCard
            fieldEvidence={scholarship.field_evidence}
            nextReviewDate={scholarship.next_review_date}
            verificationBadge={scholarship.verification_badge}
            verificationBadgeLabel={scholarship.verification_badge_label}
            completenessLabel={scholarship.completeness_label}
            lastReviewedLabel={scholarship.verification_date_label}
            verificationSourceLabel={scholarship.verification_source_label}
            className="mb-8"
          />

          <div className="mb-8">
            <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">Timeline</h2>
            <ul className="mt-2 space-y-1 text-sm text-slate-700 dark:text-slate-300">
              {scholarship.application_open_date ? (
                <li>
                  {formatOpenDateDisplay(
                    scholarship.application_open_date,
                    scholarship.deadline_precision,
                    scholarship.deadline_note
                  )}
                </li>
              ) : null}
              {scholarship.application_deadline || scholarship.deadline_precision ? (
                <li>
                  {formatDeadlineDisplay(
                    scholarship.application_deadline,
                    scholarship.deadline_precision,
                    scholarship.deadline_note,
                    scholarship.last_verified_at
                  )}
                </li>
              ) : null}
              {scholarship.academic_year_target && (
                <li>Academic year: {scholarship.academic_year_target}</li>
              )}
              {!scholarship.application_open_date &&
                !scholarship.application_deadline &&
                !scholarship.deadline_precision &&
                !scholarship.academic_year_target && (
                  <li className="text-slate-500 dark:text-slate-400">Check official website for dates</li>
                )}
            </ul>
          </div>

          {history.length > 0 ? (
            <div className="mb-8">
              <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                Change history
              </h2>
              <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                Field-level updates we have recorded for this listing.
              </p>
              <ul className="mt-3 space-y-2 text-sm">
                {history.slice(0, 8).map((item) => (
                  <li
                    key={item.version_number}
                    className="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 dark:border-slate-600 dark:bg-slate-900/40"
                  >
                    <p className="font-medium text-slate-800 dark:text-slate-200">
                      Version {item.version_number}
                      {item.changed_at ? (
                        <span className="ml-2 font-normal text-slate-500 dark:text-slate-400">
                          · {formatDateMedium(item.changed_at)}
                        </span>
                      ) : null}
                    </p>
                    <ul className="mt-1 list-inside list-disc text-xs text-slate-600 dark:text-slate-400">
                      {Object.keys(item.changes)
                        .slice(0, 5)
                        .map((key) => (
                          <li key={key}>{key.replace(/_/g, " ")}</li>
                        ))}
                    </ul>
                  </li>
                ))}
              </ul>
            </div>
          ) : null}

          {(scholarship.benefit_tuition ||
            (scholarship.benefit_allowance_monthly != null && scholarship.benefit_allowance_monthly > 0) ||
            (scholarship.benefit_total_value != null && scholarship.benefit_total_value > 0)) && (
            <div className="mb-8">
              <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                Financial planning
              </h2>
              <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                Estimate how this scholarship could offset tuition and living costs.
              </p>
              <div className="mt-3">
                <FinancialPlannerCard saved={plannerSaved} />
              </div>
            </div>
          )}

          <div className="border-t border-slate-200 dark:border-slate-700 pt-6">
            <div className="mb-4 flex flex-wrap items-center gap-3">
              <button
                type="button"
                onClick={() => {
                  setReportMsg(null);
                  setShowReport(true);
                }}
                className="rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 px-4 py-2 text-sm font-medium text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700"
              >
                Report an issue
              </button>
            </div>
            {showReport ? (
              <div
                className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
                role="dialog"
                aria-modal="true"
                aria-labelledby="report-issue-title"
              >
                <div className="w-full max-w-md rounded-xl border border-slate-200 bg-white p-6 shadow-xl dark:border-slate-600 dark:bg-slate-800">
                  <h2 id="report-issue-title" className="text-lg font-semibold text-slate-900 dark:text-slate-100">
                    Report an issue
                  </h2>
                  <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
                    Help us keep scholarship data accurate. Reports are reviewed by admins.
                  </p>
                  <label className="mt-4 block text-sm font-medium text-slate-700 dark:text-slate-300">Issue type</label>
                  <select
                    value={issueType}
                    onChange={(e) => setIssueType(e.target.value)}
                    className="mt-1 w-full rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 px-3 py-2 text-sm"
                  >
                    {ISSUE_TYPES.map((t) => (
                      <option key={t.value} value={t.value}>
                        {t.label}
                      </option>
                    ))}
                  </select>
                  <label className="mt-3 block text-sm font-medium text-slate-700 dark:text-slate-300">
                    Details (optional)
                  </label>
                  <textarea
                    value={reportDesc}
                    onChange={(e) => setReportDesc(e.target.value)}
                    rows={3}
                    className="mt-1 w-full rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 px-3 py-2 text-sm"
                    placeholder="Describe the problem…"
                  />
                  {reportMsg ? (
                    <p
                      className={
                        reportError
                          ? "mt-2 text-sm text-red-600 dark:text-red-400"
                          : "mt-2 text-sm text-green-700 dark:text-green-400"
                      }
                    >
                      {reportMsg}
                    </p>
                  ) : null}
                  <div className="mt-4 flex justify-end gap-2">
                    <button
                      type="button"
                      onClick={() => setShowReport(false)}
                      className="rounded-lg px-4 py-2 text-sm text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-700"
                    >
                      Cancel
                    </button>
                    <button
                      type="button"
                      disabled={reportSubmitting}
                      onClick={async () => {
                        if (!id) return;
                        setReportSubmitting(true);
                        setReportMsg(null);
                        setReportError(false);
                        try {
                          const res = await apiFetch("/api/v1/reports", {
                            method: "POST",
                            headers: {
                              ...authHeaders(),
                              "Content-Type": "application/json",
                            },
                            body: JSON.stringify({
                              scholarship_id: Number(id),
                              issue_type: issueType,
                              description: reportDesc.trim() || undefined,
                            }),
                          });
                          if (!res.ok) {
                            const err = await res.json().catch(() => ({}));
                            throw new Error((err as { detail?: string }).detail || "Could not submit report");
                          }
                          setReportMsg("Thank you — your report was submitted.");
                          setReportDesc("");
                          setReportError(false);
                        } catch (e) {
                          setReportError(true);
                          setReportMsg(e instanceof Error ? e.message : "Failed to submit");
                        } finally {
                          setReportSubmitting(false);
                        }
                      }}
                      className="rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-50"
                    >
                      {reportSubmitting ? "Submitting…" : "Submit"}
                    </button>
                  </div>
                </div>
              </div>
            ) : null}
            <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">Apply</h2>
            <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
              Applications are submitted through the official scholarship provider website.
            </p>
            {hasLink ? (
              <a
                href={scholarship.link!}
                target="_blank"
                rel="noreferrer"
                className="mt-4 inline-block rounded-lg bg-primary-600 px-6 py-3 font-semibold text-white shadow transition hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
              >
                Apply Now →
              </a>
            ) : (
              <p className="mt-4 text-sm text-slate-500 dark:text-slate-400">Official link not available. Search for the provider online.</p>
            )}
          </div>
        </article>
      </div>
    </section>
  );
}
