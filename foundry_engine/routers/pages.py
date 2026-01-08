"""Page rendering router for Foundry Engine."""

import logging
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from foundry_engine.config import load_page_config
from foundry_engine.navigation.registry import get_navigation_class
from foundry_engine.navigation.top_ribbon import TopRibbonNavigation
from foundry_engine.sections.registry import get_section_class
from foundry_engine.security.csrf import generate_csrf_token

logger = logging.getLogger(__name__)

router = APIRouter()


def render_navigation(request: Request, current_path: str) -> str:
    """Render navigation based on site configuration."""
    site_config = request.app.state.site_config
    nav_config = site_config.navigation

    nav_class = get_navigation_class(nav_config.type)
    if not nav_class:
        logger.warning(f"Unknown navigation type: {nav_config.type}")
        nav_class = TopRibbonNavigation

    navigation = nav_class(nav_config, current_path)
    template = request.app.state.templates.get_template(navigation.template_name)

    return navigation.render(template)


def render_sections(request: Request, page_config: Any) -> list[str]:
    """Render all sections for a page."""
    site_path = request.app.state.settings.foundry_site_path
    markdown = request.app.state.markdown
    rendered_sections = []

    for section_config in page_config.sections:
        section_class = get_section_class(section_config.type)
        if not section_class:
            logger.warning(f"Unknown section type: {section_config.type}")
            continue

        # Create section instance
        section = section_class(
            content=section_config.content,
            config=section_config.config,
            site_path=site_path,
            markdown_processor=markdown,
        )

        # Generate CSRF token for contact forms
        if section_config.type == "contact":
            csrf_token = generate_csrf_token()
            section.config["csrf_token"] = csrf_token

        # Render section
        template = request.app.state.templates.get_template(section.template_name)

        # Add recaptcha site key if needed
        if section_config.type == "contact" and section.config.get("recaptcha"):
            section.config["recaptcha_site_key"] = request.app.state.settings.recaptcha_site_key

        rendered_sections.append(section.render(template))

    return rendered_sections


@router.get("/", response_class=HTMLResponse)
async def render_homepage(request: Request) -> str:
    """Render the homepage."""
    logger.info(f"Homepage request received from {request.client.host if request.client else 'unknown'}")
    return await render_page(request, "home")


@router.get("/{page_slug}", response_class=HTMLResponse)
@router.get("/{page_slug}/", response_class=HTMLResponse)
async def render_page_route(request: Request, page_slug: str) -> str:
    """Render a page by slug."""
    return await render_page(request, page_slug)


async def render_page(request: Request, page_slug: str) -> str:
    """Common page rendering logic."""
    site_path = request.app.state.settings.foundry_site_path
    site_config = request.app.state.site_config

    logger.info(f"Attempting to render page: {page_slug}")
    logger.info(f"Available pages: {site_config.pages}")

    # Check if page exists in site config
    if page_slug not in site_config.pages:
        logger.warning(f"Page '{page_slug}' not found in site config. Available: {site_config.pages}")
        raise HTTPException(status_code=404, detail=f"Page not found: {page_slug}")

    try:
        # Load page configuration
        page_config = load_page_config(site_path, page_slug)

        # Render navigation
        current_path = "/" if page_slug == "home" else f"/{page_slug}"
        navigation_html = render_navigation(request, current_path)

        # Extract hero image for preloading (first hero section with background_image)
        hero_image = None
        for section_config in page_config.sections:
            if section_config.type == "hero" and section_config.config:
                hero_image = section_config.config.get("background_image")
                if hero_image:
                    break

        # Render sections
        sections_html = render_sections(request, page_config)

        # Render page template
        template = request.app.state.templates.get_template("page.html")

        return template.render(
            request=request,
            site=site_config.site,
            page=page_config.page,
            navigation_html=navigation_html,
            sections=sections_html,
            hero_image=hero_image,
        )

    except FileNotFoundError:
        logger.error(f"Page configuration not found: {page_slug}")
        raise HTTPException(status_code=404, detail="Page not found")
    except Exception as e:
        logger.error(f"Error rendering page {page_slug}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
