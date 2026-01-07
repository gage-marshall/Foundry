"""Text/markdown section for Foundry Engine."""

from typing import Any

from foundry_engine.sections.base import BaseSection


class TextSection(BaseSection):
    """Simple text/markdown content section."""

    section_type = "text"
    template_name = "sections/text.html"

    def get_context(self) -> dict[str, Any]:
        """Get context for text section."""
        return {
            "content": self.get_rendered_content(),
            "max_width": self.config.get("max_width", "800px"),
            "text_align": self.config.get("text_align", "left"),
            "background_color": self.config.get("background_color"),
            "padding": self.config.get("padding", "4rem 2rem"),
        }
