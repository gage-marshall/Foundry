"""Testimonials section for Foundry Engine."""

from typing import Any

from foundry_engine.sections.base import BaseSection


class TestimonialsSection(BaseSection):
    """Testimonials section."""

    section_type = "testimonials"
    template_name = "sections/testimonials.html"

    def get_context(self) -> dict[str, Any]:
        """Get context for testimonials section."""
        return {
            "content": self.get_rendered_content(),
            "testimonials": self.config.get("testimonials", []),
            "layout": self.config.get("layout", "grid"),  # grid, carousel, single
            "columns": self.config.get("columns", 2),
            "show_ratings": self.config.get("show_ratings", True),
        }
