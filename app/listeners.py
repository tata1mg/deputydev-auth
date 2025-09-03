from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
import logging

from app.config import get_settings

def setup_tortoise(app: FastAPI = None) -> None:
    settings = get_settings()
    try:
        register_tortoise(
            app,
            config=settings.tortoise_config,
            generate_schemas=True,
            add_exception_handlers=True,
        )
        logging.info("Database initialized with FastAPI integration")
    except Exception as e:
        logging.error(f"Failed to initialize database: {e}")
        raise

async def close_tortoise() -> None:
    from tortoise import Tortoise
    try:
        await Tortoise.close_connections()
        logging.info("Database connections closed successfully")
    except Exception as e:
        logging.error(f"Error closing database connections: {e}")
        raise
