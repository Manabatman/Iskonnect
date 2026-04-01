"""
Optional structured (JSON) logging for production observability.
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any


class JsonFormatter(logging.Formatter):
    """Minimal JSON log lines: timestamp, level, logger, message."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def setup_logging(structured: bool) -> None:
    """Configure root handler once (idempotent enough for uvicorn reload)."""
    root = logging.getLogger()
    if root.handlers:
        # Replace first handler formatter if already configured (dev reload)
        for h in root.handlers:
            if isinstance(h, logging.StreamHandler):
                h.setFormatter(
                    JsonFormatter() if structured else logging.Formatter("%(levelname)s %(name)s %(message)s")
                )
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        JsonFormatter() if structured else logging.Formatter("%(levelname)s %(name)s %(message)s")
    )
    root.addHandler(handler)
    root.setLevel(logging.INFO)
