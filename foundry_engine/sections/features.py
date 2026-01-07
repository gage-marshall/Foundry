"""Features grid section for Foundry Engine."""

from typing import Any

from foundry_engine.sections.base import BaseSection


class FeaturesSection(BaseSection):
    """Features grid section."""

    section_type = "features"
    template_name = "sections/features.html"

    def get_context(self) -> dict[str, Any]:
        """Get context for features section."""
        return {
            "content": self.get_rendered_content(),
            "features": self.config.get("features", []),
            "columns": self.config.get("columns", 3),
            "icon_style": self.config.get("icon_style", "outlined"),  # outlined, filled, none
            "card_style": self.config.get("card_style", "elevated"),  # flat, elevated, outlined
        }
