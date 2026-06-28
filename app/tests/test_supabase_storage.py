"""Unit tests for Supabase Storage client helpers."""

from unittest.mock import MagicMock, patch

import pytest

from app.storage import supabase_storage


def test_normalize_supabase_base_strips_rest_v1_suffix():
    assert (
        supabase_storage._normalize_supabase_base("https://proj.supabase.co/rest/v1")
        == "https://proj.supabase.co"
    )
    assert supabase_storage._normalize_supabase_base("https://proj.supabase.co/") == "https://proj.supabase.co"


def test_upload_object_sends_apikey_and_uses_storage_path(monkeypatch):
    monkeypatch.setattr(supabase_storage.settings, "supabase_url", "https://proj.supabase.co/rest/v1")
    monkeypatch.setattr(supabase_storage.settings, "supabase_service_role_key", "service-role-key")
    monkeypatch.setattr(supabase_storage.settings, "scholarship_image_bucket", "scholarship-images")

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_client = MagicMock()
    mock_client.post.return_value = mock_response
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)

    with patch("app.storage.supabase_storage.httpx.Client", return_value=mock_client):
        url = supabase_storage.upload_object("12/abcd.webp", b"webp-bytes", content_type="image/webp")

    mock_client.post.assert_called_once()
    call_url, = [mock_client.post.call_args[0][0]]
    headers = mock_client.post.call_args[1]["headers"]
    assert call_url == "https://proj.supabase.co/storage/v1/object/scholarship-images/12/abcd.webp"
    assert headers["Authorization"] == "Bearer service-role-key"
    assert headers["apikey"] == "service-role-key"
    assert headers["x-upsert"] == "true"
    assert url == "https://proj.supabase.co/storage/v1/object/public/scholarship-images/12/abcd.webp"


def test_upload_object_requires_config(monkeypatch):
    monkeypatch.setattr(supabase_storage.settings, "supabase_url", None)
    monkeypatch.setattr(supabase_storage.settings, "supabase_service_role_key", None)
    with pytest.raises(supabase_storage.StorageNotConfiguredError):
        supabase_storage.upload_object("1/x.webp", b"x")
