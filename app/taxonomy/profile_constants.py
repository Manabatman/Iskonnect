"""Profile builder option constants (mirrors frontend profileOptions.ts)."""

from __future__ import annotations

EDUCATION_LEVELS: list[dict[str, str]] = [
    {"value": "Grade 11", "label": "Grade 11"},
    {"value": "Grade 12", "label": "Grade 12"},
    {"value": "High School", "label": "High School"},
    {"value": "College", "label": "College"},
    {"value": "TVET", "label": "TVET"},
    {"value": "Graduate", "label": "Graduate"},
]

ACADEMIC_STAGES: list[dict[str, str]] = [
    {"value": "Junior HS", "label": "Junior High School"},
    {"value": "Senior HS", "label": "Senior High School"},
    {"value": "Undergraduate", "label": "College Undergraduate"},
    {"value": "Postgraduate", "label": "Postgraduate"},
    {"value": "TVET", "label": "TVET"},
    {"value": "ALS", "label": "ALS Completer"},
]

SCHOOL_TYPES: list[dict[str, str]] = [
    {"value": "Public", "label": "Public"},
    {"value": "Private", "label": "Private"},
]

GWA_SCALES: list[dict[str, str]] = [
    {"value": "percentage", "label": "Percentage (0-100)"},
    {"value": "5.0_scale", "label": "5.0 Scale (1.0 highest)"},
    {"value": "4.0_scale", "label": "4.0 Scale (4.0 highest)"},
]

ENROLLMENT_STATUSES: list[dict[str, str]] = [
    {"value": "enrolled", "label": "Currently enrolled"},
    {"value": "incoming_freshman", "label": "Incoming freshman"},
    {"value": "transferee", "label": "Transferee"},
    {"value": "returning", "label": "Returning student"},
    {"value": "graduating", "label": "Graduating this year"},
    {"value": "on_leave", "label": "On leave / LOA"},
]

YEAR_LEVELS: list[dict[str, str | int]] = [
    {"value": 11, "label": "Grade 11"},
    {"value": 12, "label": "Grade 12"},
    {"value": 1, "label": "College 1st Year"},
    {"value": 2, "label": "College 2nd Year"},
    {"value": 3, "label": "College 3rd Year"},
    {"value": 4, "label": "College 4th Year"},
    {"value": 5, "label": "College 5th Year+"},
]

CITIZENSHIP_OPTIONS: list[dict[str, str]] = [
    {"value": "Filipino", "label": "Filipino"},
    {"value": "Dual Citizen", "label": "Dual Citizen"},
    {"value": "Foreign National", "label": "Foreign National"},
]

EMPLOYMENT_STATUSES: list[dict[str, str]] = [
    {"value": "none", "label": "Not employed"},
    {"value": "part-time", "label": "Employed part-time"},
    {"value": "full-time", "label": "Employed full-time"},
    {"value": "self-employed", "label": "Self-employed"},
]

ATHLETE_LEVELS: list[dict[str, str]] = [
    {"value": "", "label": "Not an athlete"},
    {"value": "club", "label": "Club / intramural"},
    {"value": "varsity", "label": "Varsity / university team"},
    {"value": "regional", "label": "Regional team"},
    {"value": "national", "label": "National team"},
]

DEADLINE_PRECISION_LABELS: dict[str, str] = {
    "exact": "Exact date",
    "estimated": "Estimated date",
    "rolling": "Rolling admissions",
    "not_announced": "Deadline not announced",
}
