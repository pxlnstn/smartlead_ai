"""
Entry Point — Ino Labs Backend

Creates the FastAPI application via the factory pattern
and starts the Uvicorn ASGI server.

Usage:
    python run.py
    # or
    uvicorn run:app --reload
"""

import uvicorn

from app import create_app

# Create the app instance (used by uvicorn CLI: `uvicorn run:app`)
app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "run:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
