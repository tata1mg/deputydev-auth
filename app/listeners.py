import redis.asyncio as redis
from fastapi import FastAPI
from redis.exceptions import RedisError
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DBConnectionError

from app.utils.caches.base import Base
from app.utils.config_manager import ConfigManager

# Global Redis client reference
redis_client: redis.Redis | None = None


async def setup_tortoise(app: FastAPI) -> None:
    try:
        # First register with FastAPI
        register_tortoise(
            app,
            config=ConfigManager.configs()["DB_CONNECTIONS"],
            generate_schemas=True,
            add_exception_handlers=True,
        )

        # Then explicitly initialize Tortoise
        await Tortoise.init(config=ConfigManager.configs()["DB_CONNECTIONS"])
    except Exception as e:
        raise DBConnectionError(e)


async def close_tortoise() -> None:
    try:
        await Tortoise.close_connections()
    except Exception as e:
        raise DBConnectionError(e)


async def setup_cache() -> None:
    """Setup Redis cache connection."""
    global redis_client
    try:
        redis_client = redis.Redis(
            host=ConfigManager.configs()["REDIS_CACHE_HOSTS"]["genai"]["REDIS_HOST"],
            port=ConfigManager.configs()["REDIS_CACHE_HOSTS"]["genai"]["REDIS_PORT"],
            db=0,
            decode_responses=True,
            socket_connect_timeout=5,  # 5 seconds timeout for connection
            retry_on_timeout=True,
            health_check_interval=30,  # Check connection every 30 seconds
        )

        # Test the connection
        if not await redis_client.ping():
            raise RedisError("Failed to ping Redis server")

        # Initialize the redis client for the cache utility
        await Base.get_redis_client()

    except Exception as e:
        redis_client = None
        raise RedisError(f"Failed to initialize Redis: {str(e)}")


async def close_cache() -> None:
    """Close Redis cache connection."""
    global redis_client
    if redis_client:
        try:
            await redis_client.close()
        except Exception as e:
            raise RedisError(e)
