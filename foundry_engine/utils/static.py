"""Custom static files handler with aggressive caching and compression."""

import gzip
import io
from typing import Any

from fastapi.staticfiles import StaticFiles
from starlette.datastructures import Headers
from starlette.responses import Response


class CachedStaticFiles(StaticFiles):
    """StaticFiles with 30-day cache headers and gzip compression for optimal performance."""

    # File extensions that should be compressed
    COMPRESSIBLE_TYPES = {
        ".css", ".js", ".html", ".json", ".xml", ".svg",
        ".txt", ".csv", ".md", ".yaml", ".yml"
    }
    
    # Minimum file size for compression (in bytes)
    MIN_COMPRESS_SIZE = 1024  # 1KB

    async def get_response(self, path: str, scope: Any) -> Response:
        """Override to add cache control headers and compression."""
        response = await super().get_response(path, scope)
        
        # Add aggressive cache headers (30 days = 2592000 seconds)
        # Use immutable directive for modern browsers
        response.headers["Cache-Control"] = "public, max-age=2592000, immutable"
        
        # Add compression for compatible clients
        request_headers = Headers(scope=scope)
        accept_encoding = request_headers.get("accept-encoding", "")
        
        # Check if client accepts gzip and file should be compressed
        if "gzip" in accept_encoding and self._should_compress(path, response):
            compressed_body = self._compress_body(response.body)
            
            # Only use compressed version if it's actually smaller
            if compressed_body and len(compressed_body) < len(response.body):
                response.body = compressed_body
                response.headers["Content-Encoding"] = "gzip"
                response.headers["Content-Length"] = str(len(compressed_body))
                response.headers["Vary"] = "Accept-Encoding"
        
        return response
    
    def _should_compress(self, path: str, response: Response) -> bool:
        """Determine if response should be compressed."""
        # Check if file extension is compressible
        if not any(path.endswith(ext) for ext in self.COMPRESSIBLE_TYPES):
            return False
        
        # Check minimum size
        body_size = len(response.body) if hasattr(response, "body") else 0
        if body_size < self.MIN_COMPRESS_SIZE:
            return False
        
        # Don't compress if already compressed
        if response.headers.get("Content-Encoding"):
            return False
        
        return True
    
    def _compress_body(self, body: bytes) -> bytes | None:
        """Compress body with gzip."""
        try:
            buf = io.BytesIO()
            with gzip.GzipFile(fileobj=buf, mode="wb", compresslevel=6) as f:
                f.write(body)
            return buf.getvalue()
        except Exception:
            # Return None if compression fails
            return None
