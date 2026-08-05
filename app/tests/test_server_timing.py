"""Tests for Server-Timing header formatting."""

from starlette.responses import Response

from app.utils.server_timing import ServerTiming


def test_server_timing_header_format():
    timing = ServerTiming()
    timing.record("db_lookup", 12.345)
    timing.record("bcrypt", 180.5, desc="password verify")
    assert timing.header_value() == (
        'db-lookup;dur=12.35, bcrypt;dur=180.50;desc="password verify"'
    )


def test_server_timing_measure_context():
    timing = ServerTiming()
    with timing.measure("token_issue"):
        pass
    assert len(timing.metrics) == 1
    assert timing.metrics[0][0] == "token_issue"
    assert timing.metrics[0][1] >= 0


def test_server_timing_attach_merges_existing():
    response = Response()
    response.headers["Server-Timing"] = "cdn;dur=1.00"
    timing = ServerTiming()
    timing.record("app", 5.0)
    timing.attach(response)
    assert response.headers["Server-Timing"] == "cdn;dur=1.00, app;dur=5.00"
