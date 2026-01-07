"""Call-to-action section for Foundry Engine."""

from typing import Any

from foundry_engine.sections.base import BaseSection


class CTASection(BaseSection):
    """Call-to-action section."""

    section_type = "cta"
    template_name = "sections/cta.html"

    def get_context(self) -> dict[str, Any]:
        """Get context for CTA section."""
        return {
            "content": self.get_rendered_content(),
            "heading": self.config.get("heading", "Ready to get started?"),
            "subheading": self.config.get("subheading"),
            "buttons": self.config.get("buttons", []),
            "background_color": self.config.get("background_color"),
            "background_image": self.config.get("background_image"),
            "overlay_opacity": self.config.get("overlay_opacity", 0.7),
            "text_align": self.config.get("text_align", "center"),
        }
