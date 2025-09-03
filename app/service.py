import logging
import signal
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator, NoReturn

from app.utils.config_manager import ConfigManager

ConfigManager.initialize()

import uvicorn
from fastapi import FastAPI

from app.listeners import close_tortoise, setup_tortoise
from app.routes import __all_routes__

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager handling startup and shutdown.
    """
    logger.info("Starting DeputyDev Auth Service...")
    setup_tortoise(app)
    logger.info(f"Service started successfully on {settings.app.host}:{settings.app.port}")
    yield
    logger.info("Shutting down DeputyDev Auth Service...")
    await close_tortoise()
    logger.info("Service shutdown complete")


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application instance.
    """
    app = FastAPI(
        title="DeputyDev Auth Service",
        description="Authentication service for DeputyDev",
        version="1.0.0",
        debug=True,
        lifespan=lifespan,
    )

    # Routes
    for route in __all_routes__:
        app.include_router(route)

    return app


def signal_handler(signum: int, frame) -> NoReturn:
    """
    Graceful shutdown signal handler.
    """
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    sys.exit(0)


def main() -> None:
    """
    Main entry point to start the DeputyDev Auth Service.
    """
    try:
        logger.info("Starting DeputyDev Auth Service...")

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Run Uvicorn server with or without reload (debug mode)
        uvicorn.run(
            "app.service:app",
            host=settings.app.host,
            port=settings.app.port,
            reload=settings.app.debug,
            log_level=settings.logging.level.lower(),
            access_log=True,
            server_header=False,
            date_header=False,
        )

    except KeyboardInterrupt:
        logger.info("Service interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Failed to start service: {e}", exc_info=True)
        sys.exit(1)


app = create_app()

if __name__ == "__main__":
    main()
