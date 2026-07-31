"""Tests for email validation helper."""

import pytest

from app.utils.email_validation import validate_email_format


def test_validate_email_format_accepts_valid():
    validate_email_format("user@gmail.com")


def test_validate_email_format_rejects_invalid():
    with pytest.raises(ValueError):
        validate_email_format("not-an-email")
