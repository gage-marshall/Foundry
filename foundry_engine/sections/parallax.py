"""Parallax section for Foundry Engine."""

from typing import Any

from foundry_engine.sections.base import BaseSection


class ParallaxSection(BaseSection):
    """Parallax scrolling section."""

    section_type = "parallax"
    template_name = "sections/parallax.html"

    def get_context(self) -> dict[str, Any]:
        """Get context for parallax section."""
        return {
            "content": self.get_rendered_content(),
            "background_image": self.config.get("background_image"),
            "height": self.config.get("height", "60vh"),
            "speed": self.config.get("speed", 0.5),  # Parallax speed factor
            "overlay_opacity": self.config.get("overlay_opacity", 0.3),
        }
