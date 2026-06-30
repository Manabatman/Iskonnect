"""Tests for authoritative application_status computation."""

from datetime import date, timedelta

import pytest

from app.utils.application_status import (
    ARCHIVED,
    CLOSED,
    EXPECTED_REOPEN,
    NEEDS_VERIFICATION,
    OPEN,
    PREVIOUS_CYCLE,
    compute_application_status,
)


def _row(**kwargs):
    base = {
        "is_active": True,
        "data_status": "active",
        "application_deadline": None,
        "application_open_date": None,
        "cycle_type": None,
        "last_open_date": None,
        "last_close_date": None,
        "academic_year_target": None,
    }
    base.update(kwargs)
    return base


def test_archived_when_inactive():
    assert compute_application_status(_row(is_active=False)) == ARCHIVED


def test_needs_verification_from_data_status():
    assert compute_application_status(_row(data_status="needs_review")) == NEEDS_VERIFICATION


def test_open_when_active_no_deadline():
    assert compute_application_status(_row()) == OPEN


def test_closed_when_deadline_passed_no_cycle():
    past = date.today() - timedelta(days=1)
    assert compute_application_status(_row(application_deadline=past)) == CLOSED


def test_expected_reopen_when_deadline_passed_with_cycle():
    past = date.today() - timedelta(days=30)
    last_open = date.today() - timedelta(days=400)
    assert (
        compute_application_status(
            _row(
                application_deadline=past,
                cycle_type="annual",
                last_open_date=last_open,
            )
        )
        == EXPECTED_REOPEN
    )


def test_previous_cycle_when_expired_with_history_no_prediction():
    assert (
        compute_application_status(
            _row(
                data_status="expired",
                academic_year_target="AY 2024-2025",
            )
        )
        == PREVIOUS_CYCLE
    )


def test_future_open_date_still_open_lifecycle():
    future_open = date.today() + timedelta(days=14)
    assert compute_application_status(_row(application_open_date=future_open)) == OPEN
