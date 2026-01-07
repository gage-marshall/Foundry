"""Base navigation class for Foundry Engine."""

from abc import ABC, abstractmethod
from typing import Any

from jinja2 import Template

from foundry_engine.config import NavigationConfig


class BaseNavigation(ABC):
    """Base class for all navigation types."""

    nav_type: str = "base"
    template_name: str = "base.html"

    def __init__(self, config: NavigationConfig, current_path: str = "/") -> None:
        """
        Initialize navigation.

        Args:
            config: Navigation configuration from site config
            current_path: Current page path for active state
        """
        self.config = config
        self.current_path = current_path

    def is_active(self, url: str) -> bool:
        """Check if a navigation item is active based on current path."""
        if url == "/" and self.current_path == "/":
            return True
        if url != "/" and self.current_path.startswith(url):
            return True
        return False

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
        Render the navigation using the provided template.

        Args:
            template: Jinja2 template to use for rendering

        Returns:
            Rendered HTML string
        """
        context = self.get_context()
        return template.render(**context)
