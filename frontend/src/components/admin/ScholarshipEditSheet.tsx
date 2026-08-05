import { useEffect, useState, type ReactNode } from "react";
import { apiFetch } from "../../api/client";
import type { ScholarshipInfo } from "../../types";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";

type ScholarshipRecord = Record<string, unknown>;

export type ScholarshipFormValues = {
  title: string;
  provider: string;
  link: string;
  description: string;
  application_deadline: string;
  application_open_date: string;
  deadline_note: string;
  eligible_levels: string;
  regions: string;
  max_income_threshold: string;
  min_gwa_normalized: string;
  benefit_tuition: boolean;
  benefit_allowance_monthly: string;
  benefit_total_value: string;
};

const EMPTY_FORM: ScholarshipFormValues = {
  title: "",
  provider: "",
  link: "",
  description: "",
  application_deadline: "",
  application_open_date: "",
  deadline_note: "",
  eligible_levels: "",
  regions: "",
  max_income_threshold: "",
  min_gwa_normalized: "",
  benefit_tuition: false,
  benefit_allowance_monthly: "",
  benefit_total_value: "",
};

const SCHOLARSHIP_PUT_KEYS = [
  "title",
  "provider",
  "source",
  "countries",
  "regions",
  "min_age",
  "max_age",
  "needs_tags",
  "level",
  "link",
  "description",
  "provider_type",
  "scholarship_type",
  "eligible_levels",
  "eligible_regions",
  "eligible_cities",
  "residency_required",
  "eligible_school_types",
  "eligible_schools",
  "eligible_school_systems",
  "eligible_school_categories",
  "eligible_year_levels",
  "eligible_enrollment_status",
  "eligible_courses_psced",
  "eligible_courses_specific",
  "citizenship_required",
  "max_income_threshold",
  "min_gwa_normalized",
  "priority_groups",
  "members_only",
  "preferred_extracurriculars",
  "preferred_awards",
  "benefit_tuition",
  "benefit_allowance_monthly",
  "benefit_books",
  "benefit_miscellaneous",
  "benefit_total_value",
  "required_documents",
  "has_qualifying_exam",
  "has_interview",
  "has_essay_requirement",
  "has_return_service",
  "application_deadline",
  "deadline_precision",
  "deadline_note",
  "deadline_source_url",
  "application_open_date",
  "academic_year_target",
  "cycle_type",
  "last_open_date",
  "last_close_date",
  "is_active",
  "image_url",
  "image_alt",
  "opportunity_type",
  "type_attributes",
  "organization_id",
  "editorial_state",
] as const;

const RESPONSE_ONLY_KEYS = new Set([
  "id",
  "freshness_chips",
  "field_evidence",
  "preparation",
  "verification_badge",
  "verification_badge_label",
  "verification_source_label",
  "last_reviewed_label",
  "verification_date_label",
  "predicted_next_open",
  "completeness_label",
  "completeness_tier",
  "completeness_signal",
  "qualification_status",
  "qualifying_requirements",
  "missing_requirements",
  "eligibility_confidence",
  "requirements",
  "unverified_requirements",
  "provider_display",
  "data_completeness_score",
  "confidence_score",
  "link_status",
  "data_status",
  "application_status",
  "verification_source",
  "last_verified_at",
  "link_last_checked_at",
  "link_failure_count",
  "next_review_date",
]);

function toDateInputValue(value: unknown): string {
  if (value == null || value === "") return "";
  const s = String(value);
  return s.length >= 10 ? s.slice(0, 10) : s;
}

function joinList(value: unknown): string {
  if (Array.isArray(value)) return value.filter(Boolean).join(", ");
  if (typeof value === "string" && value.trim()) return value;
  return "";
}

function parseCommaList(raw: string): string[] {
  return raw
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
}

function parseOptionalInt(raw: string): number | null {
  const trimmed = raw.trim();
  if (!trimmed) return null;
  const n = Number(trimmed);
  return Number.isFinite(n) ? Math.round(n) : null;
}

function parseOptionalFloat(raw: string): number | null {
  const trimmed = raw.trim();
  if (!trimmed) return null;
  const n = Number(trimmed);
  return Number.isFinite(n) ? n : null;
}

function parseOptionalDate(raw: string): string | null {
  const trimmed = raw.trim();
  return trimmed || null;
}

function recordToForm(record: ScholarshipRecord): ScholarshipFormValues {
  const regions =
    joinList(record.eligible_regions) || joinList(record.regions);

  return {
    title: String(record.title ?? ""),
    provider: String(record.provider ?? ""),
    link: String(record.link ?? ""),
    description: String(record.description ?? ""),
    application_deadline: toDateInputValue(record.application_deadline),
    application_open_date: toDateInputValue(record.application_open_date),
    deadline_note: String(record.deadline_note ?? ""),
    eligible_levels: joinList(record.eligible_levels),
    regions,
    max_income_threshold:
      record.max_income_threshold != null ? String(record.max_income_threshold) : "",
    min_gwa_normalized:
      record.min_gwa_normalized != null ? String(record.min_gwa_normalized) : "",
    benefit_tuition: Boolean(record.benefit_tuition),
    benefit_allowance_monthly:
      record.benefit_allowance_monthly != null
        ? String(record.benefit_allowance_monthly)
        : "",
    benefit_total_value:
      record.benefit_total_value != null ? String(record.benefit_total_value) : "",
  };
}

function pickPutPayload(record: ScholarshipRecord): ScholarshipRecord {
  const out: ScholarshipRecord = {};
  for (const key of SCHOLARSHIP_PUT_KEYS) {
    if (key in record && record[key] !== undefined) {
      out[key] = record[key];
    }
  }
  return out;
}

function formToPutOverrides(form: ScholarshipFormValues): ScholarshipRecord {
  const regions = parseCommaList(form.regions);
  return {
    title: form.title.trim(),
    provider: form.provider.trim() || null,
    link: form.link.trim() || null,
    description: form.description.trim() || null,
    application_deadline: parseOptionalDate(form.application_deadline),
    application_open_date: parseOptionalDate(form.application_open_date),
    deadline_note: form.deadline_note.trim() || null,
    eligible_levels: parseCommaList(form.eligible_levels),
    regions,
    eligible_regions: regions,
    max_income_threshold: parseOptionalInt(form.max_income_threshold),
    min_gwa_normalized: parseOptionalFloat(form.min_gwa_normalized),
    benefit_tuition: form.benefit_tuition,
    benefit_allowance_monthly: parseOptionalInt(form.benefit_allowance_monthly),
    benefit_total_value: parseOptionalInt(form.benefit_total_value),
  };
}

function stripResponseOnly(record: ScholarshipRecord): ScholarshipRecord {
  const out: ScholarshipRecord = { ...record };
  for (const key of RESPONSE_ONLY_KEYS) {
    delete out[key];
  }
  return out;
}

async function loadScholarshipRecord(
  scholarshipId: number,
  rowFallback: ScholarshipInfo | undefined,
  authHeaders: () => Record<string, string>,
): Promise<ScholarshipRecord> {
  try {
    const res = await apiFetch(`/api/v1/scholarships/${scholarshipId}`, {
      headers: authHeaders(),
    });
    if (res.ok) {
      return (await res.json()) as ScholarshipRecord;
    }
  } catch {
    // fall through to row fallback
  }
  if (rowFallback) {
    return { ...rowFallback } as ScholarshipRecord;
  }
  throw new Error("Could not load scholarship record");
}

type ScholarshipEditSheetProps = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  scholarshipId: number | null;
  rowFallback?: ScholarshipInfo;
  authHeaders: () => Record<string, string>;
  onSaved: () => void;
  onError: (message: string) => void;
};

function FormSection({ title, children }: { title: string; children: ReactNode }) {
  return (
    <fieldset className="space-y-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-700 dark:bg-slate-900">
      <legend className="px-1 text-sm font-semibold text-slate-900 dark:text-slate-100">
        {title}
      </legend>
      {children}
    </fieldset>
  );
}

function FieldLabel({ htmlFor, children }: { htmlFor: string; children: ReactNode }) {
  return (
    <label htmlFor={htmlFor} className="mb-1 block text-xs font-medium text-slate-600 dark:text-slate-400">
      {children}
    </label>
  );
}

const inputClass =
  "w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm dark:border-slate-600 dark:bg-slate-900";

export function ScholarshipEditSheet({
  open,
  onOpenChange,
  scholarshipId,
  rowFallback,
  authHeaders,
  onSaved,
  onError,
}: ScholarshipEditSheetProps) {
  const [form, setForm] = useState<ScholarshipFormValues>(EMPTY_FORM);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [baseRecord, setBaseRecord] = useState<ScholarshipRecord | null>(null);

  useEffect(() => {
    if (!open || scholarshipId == null) {
      setForm(EMPTY_FORM);
      setBaseRecord(null);
      return;
    }

    let cancelled = false;
    setLoading(true);
    setForm(EMPTY_FORM);
    setBaseRecord(null);

    void loadScholarshipRecord(scholarshipId, rowFallback, authHeaders)
      .then((record) => {
        if (cancelled) return;
        setBaseRecord(record);
        setForm(recordToForm(record));
      })
      .catch((e) => {
        if (cancelled) return;
        onError(e instanceof Error ? e.message : "Failed to load scholarship");
        onOpenChange(false);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [open, scholarshipId, rowFallback, authHeaders, onError, onOpenChange]);

  const updateForm = <K extends keyof ScholarshipFormValues>(key: K, value: ScholarshipFormValues[K]) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const handleSave = async () => {
    if (scholarshipId == null || !baseRecord) return;
    if (!form.title.trim()) {
      onError("Title is required");
      return;
    }

    setSaving(true);
    try {
      let record = stripResponseOnly(baseRecord);
      try {
        const res = await apiFetch(`/api/v1/scholarships/${scholarshipId}`, {
          headers: authHeaders(),
        });
        if (res.ok) {
          record = stripResponseOnly((await res.json()) as ScholarshipRecord);
        }
      } catch {
        // use cached base record
      }

      const merged = {
        ...pickPutPayload(record),
        ...formToPutOverrides(form),
        source: (record.source as string | undefined) ?? "manual",
      };

      const res = await apiFetch(`/api/v1/scholarships/${scholarshipId}`, {
        method: "PUT",
        headers: { ...authHeaders(), "Content-Type": "application/json" },
        body: JSON.stringify(merged),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(
          typeof data?.detail === "string"
            ? data.detail
            : Array.isArray(data?.detail)
              ? data.detail.map((d: { msg?: string }) => d.msg).filter(Boolean).join("; ")
              : "Save failed",
        );
      }
      onOpenChange(false);
      onSaved();
    } catch (e) {
      onError(e instanceof Error ? e.message : "Save failed");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent side="right" className="w-full max-w-lg overflow-y-auto sm:max-w-2xl">
        <SheetHeader>
          <SheetTitle>Edit scholarship</SheetTitle>
          <SheetDescription>
            {scholarshipId != null ? `Scholarship #${scholarshipId}` : "Update catalog record"}
          </SheetDescription>
        </SheetHeader>

        {loading ? (
          <p className="mt-6 text-sm text-slate-500">Loading scholarship…</p>
        ) : (
          <div className="mt-6 space-y-4 pb-8">
            <FormSection title="Basics">
              <div>
                <FieldLabel htmlFor="sch-title">Title</FieldLabel>
                <input
                  id="sch-title"
                  className={inputClass}
                  value={form.title}
                  onChange={(e) => updateForm("title", e.target.value)}
                  required
                />
              </div>
              <div>
                <FieldLabel htmlFor="sch-provider">Provider</FieldLabel>
                <input
                  id="sch-provider"
                  className={inputClass}
                  value={form.provider}
                  onChange={(e) => updateForm("provider", e.target.value)}
                />
              </div>
              <div>
                <FieldLabel htmlFor="sch-link">Application link</FieldLabel>
                <input
                  id="sch-link"
                  type="url"
                  className={inputClass}
                  value={form.link}
                  onChange={(e) => updateForm("link", e.target.value)}
                />
              </div>
              <div>
                <FieldLabel htmlFor="sch-description">Description</FieldLabel>
                <textarea
                  id="sch-description"
                  rows={4}
                  className={inputClass}
                  value={form.description}
                  onChange={(e) => updateForm("description", e.target.value)}
                />
              </div>
            </FormSection>

            <FormSection title="Timeline">
              <div className="grid gap-3 sm:grid-cols-2">
                <div>
                  <FieldLabel htmlFor="sch-open-date">Application open date</FieldLabel>
                  <input
                    id="sch-open-date"
                    type="date"
                    className={inputClass}
                    value={form.application_open_date}
                    onChange={(e) => updateForm("application_open_date", e.target.value)}
                  />
                </div>
                <div>
                  <FieldLabel htmlFor="sch-deadline">Application deadline</FieldLabel>
                  <input
                    id="sch-deadline"
                    type="date"
                    className={inputClass}
                    value={form.application_deadline}
                    onChange={(e) => updateForm("application_deadline", e.target.value)}
                  />
                </div>
              </div>
              <div>
                <FieldLabel htmlFor="sch-deadline-note">Deadline note</FieldLabel>
                <input
                  id="sch-deadline-note"
                  className={inputClass}
                  placeholder="e.g. Rolling until funds are exhausted"
                  value={form.deadline_note}
                  onChange={(e) => updateForm("deadline_note", e.target.value)}
                />
              </div>
            </FormSection>

            <FormSection title="Eligibility">
              <div>
                <FieldLabel htmlFor="sch-levels">Eligible levels (comma-separated)</FieldLabel>
                <input
                  id="sch-levels"
                  className={inputClass}
                  placeholder="College, TVET, Graduate"
                  value={form.eligible_levels}
                  onChange={(e) => updateForm("eligible_levels", e.target.value)}
                />
              </div>
              <div>
                <FieldLabel htmlFor="sch-regions">Regions (comma-separated)</FieldLabel>
                <input
                  id="sch-regions"
                  className={inputClass}
                  placeholder="Region IV-A - CALABARZON, Nationwide"
                  value={form.regions}
                  onChange={(e) => updateForm("regions", e.target.value)}
                />
              </div>
              <div className="grid gap-3 sm:grid-cols-2">
                <div>
                  <FieldLabel htmlFor="sch-income">Max income threshold (PHP/year)</FieldLabel>
                  <input
                    id="sch-income"
                    type="number"
                    min={0}
                    className={inputClass}
                    value={form.max_income_threshold}
                    onChange={(e) => updateForm("max_income_threshold", e.target.value)}
                  />
                </div>
                <div>
                  <FieldLabel htmlFor="sch-gwa">Min GWA normalized (%)</FieldLabel>
                  <input
                    id="sch-gwa"
                    type="number"
                    min={0}
                    max={100}
                    step={0.1}
                    className={inputClass}
                    value={form.min_gwa_normalized}
                    onChange={(e) => updateForm("min_gwa_normalized", e.target.value)}
                  />
                </div>
              </div>
            </FormSection>

            <FormSection title="Benefits">
              <label className="flex items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  checked={form.benefit_tuition}
                  onChange={(e) => updateForm("benefit_tuition", e.target.checked)}
                />
                Covers tuition
              </label>
              <div className="grid gap-3 sm:grid-cols-2">
                <div>
                  <FieldLabel htmlFor="sch-allowance">Monthly allowance (PHP)</FieldLabel>
                  <input
                    id="sch-allowance"
                    type="number"
                    min={0}
                    className={inputClass}
                    value={form.benefit_allowance_monthly}
                    onChange={(e) => updateForm("benefit_allowance_monthly", e.target.value)}
                  />
                </div>
                <div>
                  <FieldLabel htmlFor="sch-total-value">Total benefit value (PHP)</FieldLabel>
                  <input
                    id="sch-total-value"
                    type="number"
                    min={0}
                    className={inputClass}
                    value={form.benefit_total_value}
                    onChange={(e) => updateForm("benefit_total_value", e.target.value)}
                  />
                </div>
              </div>
            </FormSection>

            <div className="flex gap-2 pt-2">
              <button
                type="button"
                disabled={saving || loading}
                onClick={() => void handleSave()}
                className="rounded-xl bg-primary-600 px-4 py-2 text-sm font-semibold text-white hover:bg-primary-700 disabled:opacity-50"
              >
                {saving ? "Saving…" : "Save changes"}
              </button>
              <button
                type="button"
                disabled={saving}
                onClick={() => onOpenChange(false)}
                className="rounded-lg border border-slate-300 px-4 py-2 text-sm dark:border-slate-600"
              >
                Cancel
              </button>
            </div>
          </div>
        )}
      </SheetContent>
    </Sheet>
  );
}
