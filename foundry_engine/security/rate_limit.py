"""Rate limiting for Foundry Engine using slowapi."""

import logging

from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from foundry_engine.config import FoundrySettings

logger = logging.getLogger(__name__)


def get_rate_limit_key(request: Request) -> str:
    """Get the key for rate limiting (IP address or user ID)."""
    # Try to get user ID from JWT if authenticated
    if hasattr(request.state, "user_id"):
        return f"user:{request.state.user_id}"

    # Fall back to IP address
    return get_remote_address(request)


# Global limiter instance
limiter = Limiter(key_func=get_rate_limit_key, default_limits=[])


def setup_rate_limiting(app: FastAPI, settings: FoundrySettings) -> None:
    """Setup rate limiting for the application."""
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    logger.info(
        f"Rate limiting enabled: {settings.rate_limit_per_minute}/min, "
        f"{settings.rate_limit_per_hour}/hour"
    )
