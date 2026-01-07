"""Sidebar navigation for Foundry Engine."""

from typing import Any

from foundry_engine.navigation.base import BaseNavigation


class SidebarNavigation(BaseNavigation):
    """Sidebar navigation."""

    nav_type = "sidebar"
    template_name = "navigation/sidebar.html"

    def get_context(self) -> dict[str, Any]:
        """Get context for sidebar navigation."""
        # Add active state to nav items
        items = []
        for item in self.config.items:
            item_dict = item.model_dump()
            item_dict["is_active"] = self.is_active(item.url)

            # Handle nested items
            if item.children:
                children = []
                for child in item.children:
                    child_dict = child.model_dump()
                    child_dict["is_active"] = self.is_active(child.url)
                    children.append(child_dict)
                item_dict["children"] = children

            items.append(item_dict)

        return {
            "logo": self.config.logo,
            "logo_alt": self.config.logo_alt or "Site Logo",
            "items": items,
            "collapsible": self.config.config.get("collapsible", True) if hasattr(self.config, "config") else True,
        }
