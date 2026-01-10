"""CSRF protection for Foundry Engine."""

import logging
import secrets
from typing import Optional

from fastapi import Cookie, HTTPException, Request, status

logger = logging.getLogger(__name__)


def generate_csrf_token() -> str:
    """Generate a new CSRF token."""
    return secrets.token_urlsafe(32)


async def validate_csrf_token(
    request: Request,
    csrf_cookie: Optional[str] = Cookie(None, alias="csrf_token"),
) -> bool:
    """Validate CSRF token from form against cookie.

    Note: This function manually parses form data to avoid FastAPI's strict
    form validation, which would reject requests with extra form fields.
    The form data is cached on the request state so it can be reused by the endpoint.
    """
    # Check if CSRF is enabled for this site
    if not request.app.state.site_config.security.csrf_enabled:
        return True

    # Parse form data manually to get csrf_token without triggering strict validation
    # Cache it on the request state so the endpoint handler can reuse it
    try:
        if not hasattr(request.state, "form_data"):
            request.state.form_data = await request.form()
        form_data = request.state.form_data
        csrf_token = form_data.get("csrf_token")
    except Exception as e:
        logger.error(f"Failed to parse form data for CSRF validation: {e}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid form data",
        )

    if not csrf_cookie:
        logger.warning("CSRF validation failed: No CSRF cookie found")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF token missing",
        )

    if not csrf_token:
        logger.warning("CSRF validation failed: No CSRF token in form")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF token missing from form",
        )

    if not secrets.compare_digest(csrf_token, csrf_cookie):
        logger.warning("CSRF validation failed: Token mismatch")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid CSRF token",
        )

    return True
