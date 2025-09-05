import redis.asyncio as redis
from fastapi import FastAPI
from redis.exceptions import RedisError

from app.listeners.base import BaseListener
from app.utils.config_manager import ConfigManager


class RedisListener(BaseListener):
    """Listener for Redis cache connections."""

    _host: str = ConfigManager.configs()["REDIS"]["HOST"]
    _port: int = ConfigManager.configs()["REDIS"]["PORT"]

    _client: redis.Redis = None

    async def setup(self, app: FastAPI) -> None:
        """Set up the Redis connection.

        Args:
            app: FastAPI app instance
            **kwargs: Additional configuration parameters
        """
        try:
            self._client = redis.Redis(host=self._host, port=self._port, db=0, decode_responses=True)

            # Test the connection
            if not await self._client.ping():
                raise RedisError("Failed to ping Redis server")

        except Exception as e:
            self._client = None
            raise RedisError(f"Failed to initialize Redis: {str(e)}")

    async def close(self) -> None:
        """Close the Redis connection."""
        if self._client:
            try:
                await self._client.close()
            except Exception as e:
                raise RedisError(f"Error closing Redis connection: {str(e)}")
            finally:
                self._client = None
