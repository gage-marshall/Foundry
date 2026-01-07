"""Base section class for Foundry Engine."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

from jinja2 import Template
from markdown import Markdown


class BaseSection(ABC):
    """Base class for all section types."""

    section_type: str = "base"
    template_name: str = "base.html"

    def __init__(
        self,
        content: Optional[str] = None,
        config: Optional[dict[str, Any]] = None,
        site_path: Optional[Path] = None,
        markdown_processor: Optional[Markdown] = None,
    ) -> None:
        """
        Initialize section.

        Args:
            content: Path to markdown file (relative to site path)
            config: Section configuration dictionary
            site_path: Path to the site directory
            markdown_processor: Markdown processor instance
        """
        self.content = content
        self.config = config or {}
        self.site_path = site_path
        self.markdown_processor = markdown_processor
        self._rendered_content: Optional[str] = None

    def get_rendered_content(self) -> Optional[str]:
        """Get the rendered HTML content from markdown."""
        if self._rendered_content is None and self.content and self.markdown_processor:
            if self.site_path:
                content_path = self.site_path / "content" / self.content
                if content_path.exists():
                    with open(content_path, "r", encoding="utf-8") as f:
                        md_content = f.read()
                    self._rendered_content = self.markdown_processor.convert(md_content)
                    # Reset markdown processor for next use
                    self.markdown_processor.reset()
        return self._rendered_content

    @abstractmethod
    def get_context(self) -> dict[str, Any]:
        """
        Get the context dictionary for template rendering.

        Returns:
            Dictionary with all data needed for the template
        """
        pass

    def render(self, template: Template) -> str:
        """
        Render the section using the provided template.

        Args:
            template: Jinja2 template to use for rendering

        Returns:
            Rendered HTML string
        """
        context = self.get_context()
        return template.render(**context)

    def validate_config(self) -> None:
        """Validate section configuration. Override in subclasses if needed."""
        pass
