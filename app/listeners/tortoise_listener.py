from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DBConnectionError

from app.listeners.base import BaseListener
from app.utils.config_manager import ConfigManager


class TortoiseListener(BaseListener):
    """Listener for Tortoise ORM database connections."""

    async def setup(self, app: FastAPI) -> None:
        """Set up the Tortoise ORM connection.

        Args:
            app: FastAPI app instance
        """
        try:
            # Register with FastAPI
            register_tortoise(
                app,
                config=ConfigManager.configs()["DB_CONNECTIONS"],
                generate_schemas=True,
                add_exception_handlers=True,
            )

            # Explicitly initialize Tortoise
            await Tortoise.init(config=ConfigManager.configs()["DB_CONNECTIONS"])
        except Exception as e:
            raise DBConnectionError(f"Failed to initialize Tortoise ORM: {str(e)}")

    async def close(self) -> None:
        """Close all database connections."""
        try:
            await Tortoise.close_connections()
        except Exception as e:
            raise DBConnectionError(f"Error closing database connections: {str(e)}")
