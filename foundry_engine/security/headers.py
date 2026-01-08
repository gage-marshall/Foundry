"""Security headers middleware for Foundry Engine."""

import logging
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from foundry_engine.config import Environment

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to all responses."""

    def __init__(
        self,
        app: ASGIApp,
        allowed_hosts: list[str],
        environment: Environment = Environment.PRODUCTION,
    ) -> None:
        super().__init__(app)
        self.allowed_hosts = allowed_hosts
        self.environment = environment

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and add security headers to response."""
        # Validate host header
        host = request.headers.get("host", "").split(":")[0]
        if self.allowed_hosts and not self._is_allowed_host(host):
            logger.warning(f"Blocked request from unauthorized host: {host}")
            return Response(content="Forbidden", status_code=403)

        # Call next middleware/route
        response = await call_next(request)

        # Add security headers
        self._add_security_headers(response)

        return response

    def _is_allowed_host(self, host: str) -> bool:
        """Check if host is in allowed hosts list (supports wildcards)."""
        for allowed in self.allowed_hosts:
            if allowed == "*":
                return True
            if allowed.startswith("*."):
                # Wildcard subdomain
                domain = allowed[2:]
                if host == domain or host.endswith(f".{domain}"):
                    return True
            elif host == allowed:
                return True
        return False

    def _add_security_headers(self, response: Response) -> None:
        """Add security headers to response."""
        # Content Security Policy
        # Note: Alpine.js requires both 'unsafe-eval' and 'unsafe-inline' for:
        # - 'unsafe-eval': Reactive expressions in x-data, x-bind, x-show, etc.
        # - 'unsafe-inline': Event handlers like @click, @submit, etc.
        # This is a documented Alpine.js limitation: https://alpinejs.dev/advanced/csp
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://unpkg.com https://www.google.com https://www.gstatic.com",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://unpkg.com",
            "font-src 'self' https://fonts.gstatic.com",
            "img-src 'self' data: https:",
            "connect-src 'self' https://cdn.jsdelivr.net https://unpkg.com",
            "object-src 'none'",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'",
        ]
        response.headers["Content-Security-Policy"] = "; ".join(csp_directives)

        # HSTS (only in production)
        if self.environment == Environment.PRODUCTION:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )

        # Other security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        # X-XSS-Protection is deprecated - removed as it's superseded by CSP
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "accelerometer=(), camera=(), geolocation=(), gyroscope=(), "
            "magnetometer=(), microphone=(), payment=(), usb=()"
        )

        # Remove server header if present
        if "server" in response.headers:
            del response.headers["server"]
