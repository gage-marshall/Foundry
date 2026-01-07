"""CSRF protection for Foundry Engine."""

import logging
import secrets
from typing import Optional

from fastapi import Cookie, Form, HTTPException, Request, status

logger = logging.getLogger(__name__)


def generate_csrf_token() -> str:
    """Generate a new CSRF token."""
    return secrets.token_urlsafe(32)


def validate_csrf_token(
    request: Request,
    csrf_token: str = Form(..., alias="csrf_token"),
    csrf_cookie: Optional[str] = Cookie(None, alias="csrf_token"),
) -> bool:
    """Validate CSRF token from form against cookie."""
    # Check if CSRF is enabled for this site
    if not request.app.state.site_config.security.csrf_enabled:
        return True

    if not csrf_cookie:
        logger.warning("CSRF validation failed: No CSRF cookie found")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF token missing",
        )

    if not secrets.compare_digest(csrf_token, csrf_cookie):
        logger.warning("CSRF validation failed: Token mismatch")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid CSRF token",
        )

    return True
