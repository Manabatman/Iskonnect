"""Staging import warns on unknown provider strings."""

from app.utils.import_validation import validate_import_row


def test_unknown_provider_warning():
    row = {
        "title": "New Grant",
        "provider": "Totally New Agency",
        "link": "https://example.com/new",
        "eligible_levels": ["College"],
    }
    result = validate_import_row(row, known_org_names={"ched", "dost"})
    assert result["status"] == "new"
    assert "unknown_provider" in result["warnings"]


def test_known_provider_no_warning():
    row = {
        "title": "Known Grant",
        "provider": "CHED",
        "link": "https://example.com/known",
        "eligible_levels": ["College"],
    }
    result = validate_import_row(row, known_org_names={"ched"})
    assert "unknown_provider" not in result.get("warnings", [])
