import time

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from tortoise import Tortoise

from app.services.pong import Pong

service_health_checker_route = APIRouter()


@service_health_checker_route.get(
    "/ping", summary="Ping endpoint", description="Returns pong to confirm service is running"
)
async def ping() -> JSONResponse:
    pong = Pong()
    return JSONResponse(pong.get_message())


@service_health_checker_route.get(
    "/health/db", summary="Database Health Check", description="Checks if the database connection is alive"
)
async def db_health_check() -> JSONResponse:
    try:
        conn = Tortoise.get_connection("default")
        await conn.execute_query("SELECT 1")
        return JSONResponse({"status": "ok"})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {e}",
        )


@service_health_checker_route.get(
    "/health/redis", summary="Redis Health Check", description="Checks if the Redis connection is alive"
)
async def redis_health_check() -> JSONResponse:
    from app.listeners import redis_client

    if not redis_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Redis client is not initialized. Check if Redis service is running and properly configured.",
        )

    try:
        # Test basic operations
        test_key = f"health_check_{int(time.time())}"
        test_value = "test_value"

        # Set a value with expiration
        await redis_client.set(test_key, test_value, ex=5)

        # Get the value back
        value = await redis_client.get(test_key)

        if value != test_value:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Redis test value mismatch")

        return JSONResponse(
            {
                "status": "ok",
            }
        )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Redis operation failed: {str(e)}")
