from typing import Any, Optional

import redis.asyncio as redis

from app.utils.config_manager import ConfigManager


class Base:
    _service_prefix: str = "genai"
    _host: str = ConfigManager.configs()["REDIS"]["HOST"]
    _port: int = ConfigManager.configs()["REDIS"]["PORT"]
    _key_prefix: str = ""
    _expire_in_sec: int = 3600  # default 1 hour

    # Defer Redis client initialization
    _redis: redis.Redis | None = None

    @classmethod
    def _make_key(cls, key: str) -> str:
        """Builds a namespaced Redis key."""
        return f"{cls._service_prefix}:{cls._key_prefix}:{key}"

    @classmethod
    async def get_redis_client(cls) -> redis.Redis:
        """Get the Redis client, initializing if necessary."""
        if cls._redis is None:
            cls._redis = redis.Redis(host=cls._host, port=6379, db=0, decode_responses=True)
        return cls._redis

    @classmethod
    async def set(cls, key: str, value: Any, ex: int | None = None) -> None:
        """Set a value in Redis with optional expiration."""
        redis_key = cls._make_key(key)
        redis_client = await cls.get_redis_client()
        await redis_client.set(redis_key, value, ex=ex or cls._expire_in_sec)

    @classmethod
    async def get(cls, key: str) -> Optional[str]:
        """Get a value from Redis."""
        redis_key = cls._make_key(key)
        redis_client = await cls.get_redis_client()
        return await redis_client.get(redis_key)

    @classmethod
    async def delete(cls, key: str) -> None:
        """Delete a key from Redis."""
        redis_key = cls._make_key(key)
        redis_client = await cls.get_redis_client()
        await redis_client.delete(redis_key)
