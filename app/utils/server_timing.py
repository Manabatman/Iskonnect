"""Server-Timing header helpers for performance instrumentation (P1-01)."""

from __future__ import annotations

import re
import time
from contextlib import contextmanager
from dataclasses import dataclass, field

_NAME_RE = re.compile(r"[^a-zA-Z0-9_-]")


def _safe_metric_name(name: str) -> str:
    return _NAME_RE.sub("-", name.replace("_", "-"))


@dataclass
class ServerTiming:
    """Collect timing metrics and format a Server-Timing response header."""

    metrics: list[tuple[str, float, str | None]] = field(default_factory=list)

    @contextmanager
    def measure(self, name: str, desc: str | None = None):
        start = time.perf_counter()
        yield
        dur_ms = (time.perf_counter() - start) * 1000
        self.record(name, dur_ms, desc)

    def record(self, name: str, dur_ms: float, desc: str | None = None) -> None:
        self.metrics.append((name, dur_ms, desc))

    def header_value(self) -> str:
        parts: list[str] = []
        for name, dur_ms, desc in self.metrics:
            safe = _safe_metric_name(name)
            part = f"{safe};dur={dur_ms:.2f}"
            if desc:
                escaped = desc.replace("\\", "\\\\").replace('"', '\\"')
                part += f';desc="{escaped}"'
            parts.append(part)
        return ", ".join(parts)

    def attach(self, response) -> None:
        if not self.metrics:
            return
        existing = response.headers.get("Server-Timing")
        value = self.header_value()
        response.headers["Server-Timing"] = f"{existing}, {value}" if existing else value
