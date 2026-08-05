"""Profile-options field taxonomy contract (DATA-04 / B8)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
from app.taxonomy.psced_fields import (
    LEGACY_BROAD_DISCIPLINES,
    PSCED_BROAD_DISCIPLINES,
    build_fields_of_study_options,
)


def test_profile_options_includes_fields_of_study():
    client = TestClient(app)
    resp = client.get("/api/v1/suggestions/profile-options")
    assert resp.status_code == 200
    body = resp.json()
    assert "fields_of_study" in body
    groups = body["fields_of_study"]
    assert isinstance(groups, list) and groups

    api_values = {
        opt["value"]
        for group in groups
        for opt in group.get("options", [])
        if isinstance(opt, dict) and opt.get("value")
    }
    for broad in LEGACY_BROAD_DISCIPLINES:
        assert broad in api_values


def test_profile_options_fields_match_backend_builder():
    client = TestClient(app)
    resp = client.get("/api/v1/suggestions/profile-options")
    assert resp.status_code == 200
    assert resp.json()["fields_of_study"] == build_fields_of_study_options()


def test_broad_discipline_labels_present():
    groups = build_fields_of_study_options()
    broad_group = next(g for g in groups if g.get("label") == "Broad disciplines")
    labels = {opt["label"] for opt in broad_group["options"]}
    assert PSCED_BROAD_DISCIPLINES["Law"] in labels
    assert PSCED_BROAD_DISCIPLINES["Architecture"] in labels
