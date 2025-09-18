import signal
import sys
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, NoReturn

from app.utils.config_manager import ConfigManager

ConfigManager.initialize()

import uvicorn  # noqa: E402
from elasticapm.contrib.starlette import ElasticAPM  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.logger import logger  # noqa: E402
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware  # noqa: E402

from app.apm.apm import get_apm_client  # noqa: E402
from app.listeners.base_listener import close_all_listeners, setup_all_listeners  # noqa: E402
from app.routes import __all_routes__  # noqa: E402
from app.sentry.sentry import init_sentry  # noqa: E402


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
        except Exception as e:  # noqa: BLE001
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

    # Only enable APM if it's configured and enabled
    apm_config = ConfigManager.configs()["APM"]
    if apm_config.get("ENABLED", False) and apm_config.get("SERVER_URL"):
        apm = get_apm_client(apm_config=apm_config, service_config=ConfigManager.configs()["APP"])
        app.add_middleware(ElasticAPM, client=apm)
        logger.info("APM monitoring enabled")

    # Register routes
    for route in __all_routes__:
        app.include_router(route)

    return app


def signal_handler(signum: int, frame: Any) -> NoReturn:
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
    except Exception as e:  # noqa: BLE001
        logger.error(f"Failed to start service: {e}", exc_info=True)
        sys.exit(1)


app = create_app()

if __name__ == "__main__":
    main()
