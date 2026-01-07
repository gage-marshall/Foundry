"""Navigation registry for Foundry Engine."""

from typing import Type

from foundry_engine.config import NavigationType
from foundry_engine.navigation.base import BaseNavigation
from foundry_engine.navigation.hamburger import HamburgerNavigation
from foundry_engine.navigation.sidebar import SidebarNavigation
from foundry_engine.navigation.top_ribbon import TopRibbonNavigation

# Registry of all available navigation types
NAVIGATION_REGISTRY: dict[NavigationType, Type[BaseNavigation]] = {
    NavigationType.TOP_RIBBON: TopRibbonNavigation,
    NavigationType.HAMBURGER: HamburgerNavigation,
    NavigationType.SIDEBAR: SidebarNavigation,
}


def get_navigation_class(nav_type: NavigationType) -> Type[BaseNavigation] | None:
    """Get navigation class by type."""
    return NAVIGATION_REGISTRY.get(nav_type)


def register_navigation(nav_type: NavigationType, nav_class: Type[BaseNavigation]) -> None:
    """Register a custom navigation type."""
    NAVIGATION_REGISTRY[nav_type] = nav_class


def list_navigation_types() -> list[str]:
    """List all registered navigation types."""
    return [nav_type.value for nav_type in NAVIGATION_REGISTRY.keys()]
