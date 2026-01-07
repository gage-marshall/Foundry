"""Gallery section for Foundry Engine."""

from typing import Any

from foundry_engine.sections.base import BaseSection


class GallerySection(BaseSection):
    """Photo gallery section."""

    section_type = "gallery"
    template_name = "sections/gallery.html"

    def get_context(self) -> dict[str, Any]:
        """Get context for gallery section."""
        return {
            "content": self.get_rendered_content(),
            "images": self.config.get("images", []),
            "layout": self.config.get("layout", "grid"),  # grid, masonry, carousel
            "columns": self.config.get("columns", 3),
            "gap": self.config.get("gap", "1rem"),
            "lightbox": self.config.get("lightbox", True),
            "captions": self.config.get("captions", {}),  # {image_path: caption}
        }
