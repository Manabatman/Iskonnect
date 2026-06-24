"""Rate limiter for API endpoints."""
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import settings

_storage = settings.redis_url if settings.redis_url else "memory://"
limiter = Limiter(key_func=get_remote_address, storage_uri=_storage)
