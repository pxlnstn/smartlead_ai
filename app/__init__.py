"""
Application Factory — ino Backend

Assembles all components: CORS middleware, database initialization,
and route registration into a single FastAPI instance.

Usage:
    from app import create_app
    app = create_app()
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.routes import api_router, health_router
from config import APP_VERSION, CORS_ORIGINS, DEBUG

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup / shutdown lifecycle manager.

    - On startup: initialize the database (create tables if needed).
    - On shutdown: clean up resources.
    """
    logger.info("🚀 ino API starting up...")
    await init_db()
    logger.info("✅ Database initialized.")
    yield
    logger.info("👋 ino API shutting down.")


def create_app() -> FastAPI:
    """Application factory — creates and configures the FastAPI instance.

    Wiring order:
        1. Create FastAPI app with lifespan
        2. Add CORS middleware
        3. Include API and health routers
    """
    app = FastAPI(
        title="ino AI API",
        description="ino website assistant and demo lead collection service.",
        version=APP_VERSION,
        lifespan=lifespan,
        docs_url="/docs" if DEBUG else None,
        redoc_url="/redoc" if DEBUG else None,
    )

    # --- CORS Middleware ---
    # Allows Wix Studio (or any configured origin) to call this API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=CORS_ORIGINS != ["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Register Routers ---
    static_dir = Path(__file__).resolve().parent / "static"
    app.mount("/media", StaticFiles(directory=static_dir), name="media")
    app.include_router(health_router)
    app.include_router(api_router)

    logger.info(
        "App created — CORS origins: %s | Debug: %s | Version: %s",
        CORS_ORIGINS,
        DEBUG,
        APP_VERSION,
    )

    return app
