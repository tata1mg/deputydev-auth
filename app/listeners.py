import logging

from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise


def setup_tortoise(app: FastAPI = None) -> None:
    try:
        register_tortoise(
            app,
            config={},
            generate_schemas=True,
            add_exception_handlers=True,
        )
        logging.info("Database initialized with FastAPI integration")
    except Exception as e:
        logging.error(f"Failed to initialize database: {e}")
        raise


async def close_tortoise() -> None:
    try:
        await Tortoise.close_connections()
        logging.info("Database connections closed successfully")
    except Exception as e:
        logging.error(f"Error closing database connections: {e}")
        raise
