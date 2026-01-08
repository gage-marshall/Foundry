"""
Foundry Engine - Main Entry Point

A modular FastAPI-based static site engine optimized for security, reliability, and speed.

This file demonstrates two usage patterns:

1. Environment Variable (Default):
   Set FOUNDRY_SITE_PATH in .env file and call create_app() with no arguments.

2. Programmatic (Recommended when using as dependency):
   Pass site_path directly to create_app() for explicit configuration.
"""

import uvicorn
from pathlib import Path

from foundry_engine import create_app

# Create the FastAPI application
#
# Method 1: Using environment variable (traditional monorepo approach)
# Loads from FOUNDRY_SITE_PATH in .env file
app = create_app()

# Method 2: Using explicit path (recommended when importing as dependency)
# Uncomment to use:
# site_path = Path(__file__).parent / "sites" / "example_site"
# app = create_app(site_path=site_path)

if __name__ == "__main__":
    # Run with uvicorn when executed directly
    # For production, use: gunicorn main:app -c gunicorn.conf.py
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info",
    )
