"""Server-side image validation and WebP compression for scholarship uploads."""

from __future__ import annotations

import hashlib
import io
from typing import Tuple

from fastapi import HTTPException
from PIL import Image, ImageOps

ALLOWED_CONTENT_TYPES = frozenset({"image/jpeg", "image/png", "image/webp"})
MAX_DIMENSION = 1600
WEBP_QUALITY = 82


def compress_scholarship_image(raw: bytes, content_type: str, max_bytes: int) -> Tuple[bytes, str]:
    """
    Validate and compress an uploaded image to WebP.
    Returns (webp_bytes, content_hash_prefix).
    """
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported image type. Allowed: {', '.join(sorted(ALLOWED_CONTENT_TYPES))}",
        )
    if len(raw) > max_bytes:
        raise HTTPException(
            status_code=422,
            detail=f"Image too large (max {max_bytes // (1024 * 1024)} MB)",
        )
    try:
        img = Image.open(io.BytesIO(raw))
        img = ImageOps.exif_transpose(img)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")
        elif img.mode == "RGBA":
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        w, h = img.size
        if max(w, h) > MAX_DIMENSION:
            img.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.Resampling.LANCZOS)
        out = io.BytesIO()
        img.save(out, format="WEBP", quality=WEBP_QUALITY, method=4)
        webp = out.getvalue()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=422, detail="Invalid or corrupt image file") from exc

    digest = hashlib.sha256(webp).hexdigest()[:8]
    return webp, digest
