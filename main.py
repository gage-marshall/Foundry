"""
Foundry Engine - Example Entry Point

This is a minimal example showing how to use Foundry Engine as a package.
In your own site repository, you would create a similar main.py file.

Usage in your site repository:
    1. Install: pip install git+ssh://git@github.com/yourorg/foundry-engine.git@main
    2. Create main.py that imports foundry_engine
    3. Pass your site directory path to create_app()
"""

import uvicorn
from pathlib import Path
from foundry_engine import create_app

# For actual usage: your site directory should contain:
# - config.yaml (site configuration)
# - content/ (pages and sections)
# - theme/ (custom CSS)
# - assets/ (images, etc.)
site_path = Path(__file__).parent

# Create the FastAPI application with your site path
app = create_app(site_path=site_path)

if __name__ == "__main__":
    # Development server
    # For production, use: gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
