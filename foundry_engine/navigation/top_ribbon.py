"""Top ribbon navigation for Foundry Engine."""

from typing import Any

from foundry_engine.navigation.base import BaseNavigation


class TopRibbonNavigation(BaseNavigation):
    """Top ribbon navigation bar."""

    nav_type = "top_ribbon"
    template_name = "navigation/top_ribbon.html"

    def get_context(self) -> dict[str, Any]:
        """Get context for top ribbon navigation."""
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
            "sticky": self.config.sticky,
            "mobile_breakpoint": self.config.mobile_breakpoint,
        }
