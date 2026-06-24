"""
HTTP HEAD link health check for scholarship URLs.
Run: python -m app.jobs.link_checker
Requires ENABLE_LINK_CHECKER=true
"""

from __future__ import annotations

import logging
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any

from app.config import settings
from app.db import SessionLocal
from app import models

logger = logging.getLogger(__name__)

HEAD_TIMEOUT_SEC = 10
REQUEST_GAP_SEC = 1.0


def _head_status(url: str) -> tuple[bool, str]:
    """Return (success, reason_tag)."""
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Iskonnect-LinkChecker/1.0"})
        with urllib.request.urlopen(req, timeout=HEAD_TIMEOUT_SEC) as resp:
            code = getattr(resp, "status", resp.getcode())
            return (200 <= int(code) < 400, "ok")
    except urllib.error.HTTPError as e:
        code = e.code
        if 200 <= int(code) < 400:
            return True, "ok"
        return False, f"http_{code}"
    except urllib.error.URLError as e:
        return False, f"url_error:{e.reason!s}"
    except Exception as e:
        return False, f"error:{e!s}"


def run_link_check() -> dict[str, Any]:
    if not settings.enable_link_checker:
        logger.warning("link_checker_skipped enable_link_checker=false")
        return {"skipped": True, "reason": "ENABLE_LINK_CHECKER is false"}

    db = SessionLocal()
    stats = {"checked": 0, "ok": 0, "failed": 0, "broken": 0}
    try:
        rows = (
            db.query(models.Scholarship)
            .filter(
                models.Scholarship.is_active != False,  # noqa: E712
                models.Scholarship.link.isnot(None),
                models.Scholarship.link != "",
            )
            .all()
        )
        for s in rows:
            url = (s.link or "").strip()
            if not url.startswith(("http://", "https://")):
                continue
            time.sleep(REQUEST_GAP_SEC)
            ok, _tag = _head_status(url)
            stats["checked"] += 1
            ts = datetime.now(timezone.utc)
            s.link_last_checked_at = ts
            if ok:
                stats["ok"] += 1
                s.link_status = "ok"
                s.link_failure_count = 0
            else:
                stats["failed"] += 1
                s.link_failure_count = (s.link_failure_count or 0) + 1
                s.link_status = "broken" if (s.link_failure_count or 0) >= 3 else "timeout"
                if (s.link_failure_count or 0) >= 3:
                    s.data_status = "broken_link"
                    stats["broken"] += 1
            db.add(s)
        db.commit()
        logger.info("link_checker_done %s", stats)
        return stats
    except Exception:
        db.rollback()
        logger.exception("link_checker_failed")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(run_link_check())
