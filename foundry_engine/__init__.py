"""
Foundry Engine - A modular FastAPI-based static site engine.

Designed for security, reliability, and speed.

Example usage as a dependency:
    from pathlib import Path
    from foundry_engine import create_app

    # Create app with explicit site path
    site_path = Path(__file__).parent / "my_site"
    app = create_app(site_path=site_path)
"""

from foundry_engine.app import create_app
from foundry_engine.config import FoundrySettings

__version__ = "0.1.0"
__all__ = ["create_app", "FoundrySettings", "__version__"]
