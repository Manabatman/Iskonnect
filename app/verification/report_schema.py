"""Import-ready schemas for ChatGPT verification report outputs."""

from __future__ import annotations

FIELD_CHANGES_COLUMNS: tuple[str, ...] = (
    "id",
    "field",
    "iskconnect_value",
    "official_value",
    "action",
    "change_reason",
    "closure_type",
    "confidence",
    "source_url",
    "evidence_snippet",
    "official_last_updated",
    "announcement_date",
    "verified_at",
)

CHANGE_REASONS: tuple[str, ...] = (
    "annual_cycle_update",
    "policy_revision",
    "provider_renamed_program",
    "application_portal_migrated",
    "website_redesign",
    "program_discontinued",
    "temporary_suspension",
    "eligibility_expansion",
    "eligibility_restriction",
    "typographical_correction",
    "unknown",
)

CLOSURE_TYPES: tuple[str, ...] = (
    "permanently_discontinued",
    "closed_for_this_cycle",
    "temporarily_unavailable",
    "unknown",
)

CONFIDENCE_LEVELS: tuple[str, ...] = (
    "verified",
    "partially_verified",
    "cannot_verify",
)

FIELD_CHANGE_ACTIONS: tuple[str, ...] = (
    "update",
    "confirm_unchanged",
    "archive",
    "flag_review",
)

NEW_SCHOLARSHIP_KEYS: tuple[str, ...] = (
    "title",
    "provider",
    "provider_type",
    "scholarship_type",
    "primary_link",
    "application_portal_url",
    "description",
    "eligible_levels",
    "eligible_regions",
    "priority_groups",
    "members_only",
    "application_open_date",
    "application_deadline",
    "cycle_type",
    "benefit_summary",
    "source_url",
    "evidence_snippet",
)

SCHEMA_CANDIDATE_KEYS: tuple[str, ...] = (
    "observed_rule",
    "example_scholarship_ids",
    "frequency_in_bundle",
    "current_workaround",
    "recommendation",
    "source_urls",
)

IMPORTANT_NOTE_KEYS: tuple[str, ...] = (
    "scholarship_id",
    "notes",
    "source_url",
)

SCHEMA_CANDIDATE_RECOMMENDATIONS: tuple[str, ...] = (
    "keep_free_text",
    "add_structured_field",
    "add_to_priority_groups",
)
