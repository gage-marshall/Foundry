"""Section registry for Foundry Engine."""

from typing import Type

from foundry_engine.sections.base import BaseSection
from foundry_engine.sections.contact import ContactSection
from foundry_engine.sections.cta import CTASection
from foundry_engine.sections.features import FeaturesSection
from foundry_engine.sections.footer import FooterSection
from foundry_engine.sections.gallery import GallerySection
from foundry_engine.sections.hero import HeroSection
from foundry_engine.sections.parallax import ParallaxSection
from foundry_engine.sections.text import TextSection
from foundry_engine.sections.testimonials import TestimonialsSection

# Registry of all available section types
SECTION_REGISTRY: dict[str, Type[BaseSection]] = {
    "hero": HeroSection,
    "parallax": ParallaxSection,
    "gallery": GallerySection,
    "text": TextSection,
    "contact": ContactSection,
    "cta": CTASection,
    "features": FeaturesSection,
    "testimonials": TestimonialsSection,
    "footer": FooterSection,
}


def get_section_class(section_type: str) -> Type[BaseSection] | None:
    """Get section class by type name."""
    return SECTION_REGISTRY.get(section_type)


def register_section(section_type: str, section_class: Type[BaseSection]) -> None:
    """Register a custom section type."""
    SECTION_REGISTRY[section_type] = section_class


def list_section_types() -> list[str]:
    """List all registered section types."""
    return list(SECTION_REGISTRY.keys())
