"""Hero section for Foundry Engine."""

from typing import Any, Optional

from foundry_engine.sections.base import BaseSection


class HeroSection(BaseSection):
    """Hero section with background image and CTA."""

    section_type = "hero"
    template_name = "sections/hero.html"

    def get_context(self) -> dict[str, Any]:
        """Get context for hero section."""
        return {
            "content": self.get_rendered_content(),
            "background_image": self.config.get("background_image"),
            "background_video": self.config.get("background_video"),
            "height": self.config.get("height", "100vh"),
            "overlay_opacity": self.config.get("overlay_opacity", 0.5),
            "text_align": self.config.get("text_align", "center"),
            "cta_button": self.config.get("cta_button"),
            "parallax": self.config.get("parallax", False),
        }
