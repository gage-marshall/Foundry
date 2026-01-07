"""Footer section for Foundry Engine."""

from typing import Any

from foundry_engine.sections.base import BaseSection


class FooterSection(BaseSection):
    """Footer section."""

    section_type = "footer"
    template_name = "sections/footer.html"

    def get_context(self) -> dict[str, Any]:
        """Get context for footer section."""
        return {
            "content": self.get_rendered_content(),
            "columns": self.config.get("columns", []),
            "social_links": self.config.get("social_links", []),
            "copyright": self.config.get("copyright"),
            "logo": self.config.get("logo"),
            "background_color": self.config.get("background_color"),
        }
