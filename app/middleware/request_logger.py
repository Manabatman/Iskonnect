"""Request logging middleware for audit trail."""
import logging
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
        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = rid
            logger.info("[%s] %s %s -> %s", rid, request.method, request.url.path, response.status_code)
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
