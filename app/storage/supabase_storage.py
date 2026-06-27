"""Upload and delete objects in Supabase Storage using the service role key."""

from __future__ import annotations

import logging
from urllib.parse import quote

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

CACHE_CONTROL = "public, max-age=31536000, immutable"


class StorageNotConfiguredError(RuntimeError):
    """Raised when SUPABASE_URL or service role key is missing."""


def _require_config() -> tuple[str, str, str]:
    base = (settings.supabase_url or "").strip().rstrip("/")
    key = (settings.supabase_service_role_key or "").strip()
    bucket = (settings.scholarship_image_bucket or "scholarship-images").strip()
    if not base or not key:
        raise StorageNotConfiguredError(
            "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set for image uploads"
        )
    return base, key, bucket


def public_object_url(object_path: str, bucket: str | None = None) -> str:
    """Build the public CDN URL for an object in a public bucket."""
    base, _, default_bucket = _require_config()
    b = bucket or default_bucket
    encoded = "/".join(quote(part, safe="") for part in object_path.split("/"))
    return f"{base}/storage/v1/object/public/{b}/{encoded}"


def upload_object(
    object_path: str,
    data: bytes,
    *,
    content_type: str = "image/webp",
    bucket: str | None = None,
    upsert: bool = True,
) -> str:
    """Upload bytes to Supabase Storage; returns public URL."""
    base, key, default_bucket = _require_config()
    b = bucket or default_bucket
    encoded = "/".join(quote(part, safe="") for part in object_path.split("/"))
    url = f"{base}/storage/v1/object/{b}/{encoded}"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": content_type,
        "Cache-Control": CACHE_CONTROL,
    }
    if upsert:
        headers["x-upsert"] = "true"
    with httpx.Client(timeout=30.0) as client:
        r = client.post(url, content=data, headers=headers)
        if r.status_code not in (200, 201):
            logger.error("storage_upload_failed path=%s status=%s body=%s", object_path, r.status_code, r.text[:500])
            r.raise_for_status()
    return public_object_url(object_path, b)


def delete_object(object_path: str, *, bucket: str | None = None) -> None:
    """Delete an object from Supabase Storage (best-effort)."""
    base, key, default_bucket = _require_config()
    b = bucket or default_bucket
    encoded = "/".join(quote(part, safe="") for part in object_path.split("/"))
    url = f"{base}/storage/v1/object/{b}/{encoded}"
    headers = {"Authorization": f"Bearer {key}"}
    with httpx.Client(timeout=30.0) as client:
        r = client.delete(url, headers=headers)
        if r.status_code not in (200, 204, 404):
            logger.warning("storage_delete_failed path=%s status=%s", object_path, r.status_code)


def storage_path_from_public_url(public_url: str | None) -> str | None:
    """Extract object path from a Supabase public URL, if it matches our bucket."""
    if not public_url:
        return None
    try:
        _, _, default_bucket = _require_config()
    except StorageNotConfiguredError:
        return None
    marker = f"/storage/v1/object/public/{default_bucket}/"
    idx = public_url.find(marker)
    if idx < 0:
        return None
    return public_url[idx + len(marker) :]
