"""FastAPI application factory for Foundry Engine."""

import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from foundry_engine.config import FoundrySettings, load_site_config
from foundry_engine.routers import contact, pages
from foundry_engine.security import SecurityHeadersMiddleware, setup_rate_limiting
from foundry_engine.utils.markdown import setup_markdown_processor

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    # Load settings
    settings = FoundrySettings()

    # Set log level from settings
    logging.getLogger().setLevel(settings.log_level)
    logger.info(f"Starting Foundry Engine in {settings.foundry_env.value} mode")

    # Verify site path exists
    site_path_abs = settings.foundry_site_path.absolute()
    logger.info(f"Looking for site at: {site_path_abs}")

    if not settings.foundry_site_path.exists():
        logger.error(f"Site path does not exist: {site_path_abs}")
        logger.error(f"Current working directory: {Path.cwd()}")
        logger.error(f"Directory contents: {list(Path.cwd().iterdir())}")
        raise FileNotFoundError(
            f"Site path does not exist: {site_path_abs}"
        )

    # Load site configuration
    try:
        site_config = load_site_config(settings.foundry_site_path)
        logger.info(f"Loaded site configuration for: {site_config.site.name}")
        logger.info(f"Available pages: {site_config.pages}")
    except Exception as e:
        logger.error(f"Failed to load site configuration: {e}", exc_info=True)
        raise

    # Create FastAPI app
    app = FastAPI(
        title=site_config.site.name,
        description=site_config.site.description or "Powered by Foundry Engine",
        version="0.1.0",
        docs_url="/docs" if settings.foundry_env == "development" else None,
        redoc_url="/redoc" if settings.foundry_env == "development" else None,
    )

    # Add security headers middleware
    app.add_middleware(
        SecurityHeadersMiddleware,
        allowed_hosts=site_config.security.allowed_hosts,
        environment=settings.foundry_env,
    )

    # Setup rate limiting
    if settings.rate_limit_enabled:
        setup_rate_limiting(app, settings)

    # Setup Jinja2 templates
    engine_templates_path = Path(__file__).parent / "templates"
    templates = Jinja2Templates(directory=str(engine_templates_path))

    # Setup markdown processor
    markdown_processor = setup_markdown_processor()

    # Mount static files with custom StaticFiles class for caching
    from foundry_engine.utils.static import CachedStaticFiles
    
    engine_static_path = Path(__file__).parent / "static"
    if engine_static_path.exists():
        app.mount("/static/engine", CachedStaticFiles(directory=str(engine_static_path)), name="engine")

    # Mount site-specific assets
    site_assets_path = settings.foundry_site_path / "assets"
    if site_assets_path.exists():
        app.mount("/assets", CachedStaticFiles(directory=str(site_assets_path)), name="assets")

    # Mount site theme CSS
    site_theme_path = settings.foundry_site_path / "theme"
    if site_theme_path.exists():
        app.mount("/theme", CachedStaticFiles(directory=str(site_theme_path)), name="theme")

    # Store configuration in app state
    app.state.settings = settings
    app.state.site_config = site_config
    app.state.templates = templates
    app.state.markdown = markdown_processor

    # Health check endpoints (MUST be before routers with catch-all routes)
    @app.get("/health")
    @app.get("/healthz")
    async def health_check() -> dict[str, str]:
        """Health check endpoint for monitoring."""
        return {"status": "healthy", "service": "foundry-engine"}

    # Favicon redirect (handle default browser request for /favicon.ico)
    @app.get("/favicon.ico")
    async def favicon_redirect() -> Response:
        """Redirect default favicon.ico request to configured favicon."""
        from fastapi.responses import RedirectResponse
        favicon_url = site_config.site.favicon or "/assets/favicon.svg"
        return RedirectResponse(url=favicon_url, status_code=301)

    # Robots.txt
    @app.get("/robots.txt")
    async def robots_txt() -> Response:
        """Serve robots.txt for search engine crawlers."""
        from fastapi.responses import PlainTextResponse

        # Generate robots.txt content
        robots_content = f"""User-agent: *
Allow: /

Sitemap: {site_config.site.domain if site_config.site.domain else ''}/sitemap.xml
"""
        return PlainTextResponse(content=robots_content.strip())

    # Include routers (pages router has catch-all /{page_slug})
    app.include_router(pages.router)
    app.include_router(contact.router)

    # Startup event
    @app.on_event("startup")
    async def startup_event() -> None:
        """Called when application starts."""
        logger.info(f"Foundry Engine starting - Environment: {settings.foundry_env.value}")
        logger.info(f"Serving site: {site_config.site.name}")

    # Shutdown event
    @app.on_event("shutdown")
    async def shutdown_event() -> None:
        """Called when application shuts down - cleanup resources."""
        logger.info("Foundry Engine shutting down gracefully...")
        # Add any cleanup tasks here (close connections, etc.)
        logger.info("Shutdown complete")

    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle uncaught exceptions."""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        if settings.foundry_env == "development":
            return JSONResponse(
                status_code=500,
                content={"detail": str(exc), "type": type(exc).__name__},
            )
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    logger.info("Foundry Engine initialization complete")
    return app
