import signal
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator, NoReturn

from app.utils.config_manager import ConfigManager

ConfigManager.initialize()

import uvicorn
from elasticapm.contrib.starlette import ElasticAPM
from fastapi import FastAPI
from fastapi.logger import logger
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.apm.apm import get_apm_client
from app.listeners.base_listener import close_all_listeners, setup_all_listeners
from app.routes import __all_routes__
from app.sentry.sentry import init_sentry


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting DeputyDev Auth Service...")

    try:
        # Initialize listeners
        await setup_all_listeners(app)
        init_sentry(ConfigManager.configs()["SENTRY"])

        logger.info(
            f"Service started successfully on {ConfigManager.configs()['APP']['HOST']}:{ConfigManager.configs()['APP']['PORT']}"
        )
        yield
    finally:
        logger.info("Shutting down DeputyDev Auth Service...")
        try:
            # Close listeners in reverse order
            await close_all_listeners()
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
        logger.info("Service shutdown complete")


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application instance.
    """
    app = FastAPI(
        title=ConfigManager.configs()["APP"]["NAME"],
        description=ConfigManager.configs()["APP"]["DESCRIPTION"],
        version=ConfigManager.configs()["APP"]["VERSION"],
        debug=ConfigManager.configs()["APP"]["DEBUG"],
        lifespan=lifespan,
        servers=ConfigManager.configs()["APP"]["SERVERS"],
    )

    app.add_middleware(SentryAsgiMiddleware)

    apm = get_apm_client(apm_config=ConfigManager.configs()["APM"], service_config=ConfigManager.configs()["APP"])
    app.add_middleware(ElasticAPM, client=apm)

    # Register routes
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

        uvicorn.run(
            "app.service:app",
            host=ConfigManager.configs()["APP"]["HOST"],
            port=ConfigManager.configs()["APP"]["PORT"],
            reload=ConfigManager.configs()["APP"]["DEBUG"],
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
