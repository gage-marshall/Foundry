"""Hamburger menu navigation for Foundry Engine."""

from typing import Any

from foundry_engine.navigation.base import BaseNavigation


class HamburgerNavigation(BaseNavigation):
    """Hamburger menu navigation."""

    nav_type = "hamburger"
    template_name = "navigation/hamburger.html"

    def get_context(self) -> dict[str, Any]:
        """Get context for hamburger navigation."""
        # Add active state to nav items
        items = []
        for item in self.config.items:
            item_dict = item.model_dump()
            item_dict["is_active"] = self.is_active(item.url)
            items.append(item_dict)

        return {
            "logo": self.config.logo,
            "logo_alt": self.config.logo_alt or "Site Logo",
            "items": items,
            "mobile_breakpoint": self.config.mobile_breakpoint,
        }
