"""
Foundry Engine - Main Entry Point

A modular FastAPI-based static site engine optimized for security, reliability, and speed.
"""

import uvicorn

from foundry_engine.app import create_app

# Create the FastAPI application
app = create_app()

if __name__ == "__main__":
    # Run with uvicorn when executed directly
    # For production, use: uvicorn main:app --host 0.0.0.0 --port 8000
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info",
    )
