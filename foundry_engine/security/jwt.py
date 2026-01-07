"""JWT authentication utilities for Foundry Engine."""

import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from foundry_engine.config import FoundrySettings

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)


def create_access_token(
    data: dict[str, str], settings: FoundrySettings, expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token."""
    if not settings.jwt_secret_key:
        raise ValueError("JWT_SECRET_KEY not configured")

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expiration_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def decode_access_token(token: str, settings: FoundrySettings) -> dict[str, str]:
    """Decode and verify a JWT access token."""
    if not settings.jwt_secret_key:
        raise ValueError("JWT_SECRET_KEY not configured")

    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError as e:
        logger.warning(f"JWT decode error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    request: Request, credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[dict[str, str]]:
    """Get current user from JWT token."""
    # Check if JWT is enabled for this site
    if not request.app.state.site_config.security.jwt_enabled:
        return None

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = decode_access_token(token, request.app.state.settings)

    # Store user ID in request state for rate limiting
    if "sub" in payload:
        request.state.user_id = payload["sub"]

    return payload


def require_auth(user: Optional[dict[str, str]] = Depends(get_current_user)) -> dict[str, str]:
    """Dependency to require authentication."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
