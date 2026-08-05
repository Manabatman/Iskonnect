"""Request logging middleware for audit trail."""
import logging
import time
import traceback
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log request method, path, client IP, response status, and request id."""

    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.request_id = rid
        client_host = request.client.host if request.client else "unknown"
        logger.info("[%s] %s %s from %s", rid, request.method, request.url.path, client_host)
        started = time.perf_counter()
        try:
            response = await call_next(request)
            elapsed_ms = (time.perf_counter() - started) * 1000
            response.headers["X-Request-ID"] = rid
            existing = response.headers.get("Server-Timing")
            total_part = f"wall;dur={elapsed_ms:.2f}"
            response.headers["Server-Timing"] = (
                f"{existing}, {total_part}" if existing else total_part
            )
            logger.info(
                "[%s] %s %s -> %s (%.1fms)",
                rid,
                request.method,
                request.url.path,
                response.status_code,
                elapsed_ms,
            )
            return response
        except Exception:
            logger.error(
                "%s %s from %s UNHANDLED EXCEPTION\n%s",
                request.method,
                request.url.path,
                client_host,
                traceback.format_exc(),
            )
            raise
