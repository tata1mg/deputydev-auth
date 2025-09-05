from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DBConnectionError

from app.listeners.base_listener import BaseListener
from app.utils.config_manager import ConfigManager

class TortoiseListener(BaseListener):
    """Listener for Tortoise ORM database connections."""
    _host: str = ConfigManager.configs()["DB_CREDENTIALS"]["HOST"]
    _port: int = ConfigManager.configs()["DB_CREDENTIALS"]["PORT"]
    _user: str = ConfigManager.configs()["DB_CREDENTIALS"]["USER"]
    _password: str = ConfigManager.configs()["DB_CREDENTIALS"]["PASSWORD"]
    _database: str = ConfigManager.configs()["DB_CREDENTIALS"]["DATABASE"]

    _config = {
        "connections": {
            "default": {
                "engine": "tortoise.backends.asyncpg",
                "credentials": {
                    "host": _host,
                    "port": _port,
                    "user": _user,
                    "password": _password,
                    "database": _database,
                }
            }
        },
        "apps": {
            "dao": {
                "models": [
                    "app.models.dao.postgres"
                ],
                "default_connection": "default"
            }
        }
    }

    async def setup(self, app: FastAPI) -> None:
        """Set up the Tortoise ORM connection.

        Args:
            app: FastAPI app instance
        """
        try:
            # Register with FastAPI
            register_tortoise(
                app,
                config=self._config,
                generate_schemas=True,
                add_exception_handlers=True,
            )

            # Explicitly initialize Tortoise
            await Tortoise.init(config=self._config)
        except Exception as e:
            raise DBConnectionError(f"Failed to initialize Tortoise ORM: {str(e)}")

    async def close(self) -> None:
        """Close all database connections."""
        try:
            await Tortoise.close_connections()
        except Exception as e:
            raise DBConnectionError(f"Error closing database connections: {str(e)}")
