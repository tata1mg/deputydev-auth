from abc import ABC, abstractmethod
from fastapi import FastAPI

class BaseListener(ABC):
    """Base class for all service listeners."""

    @abstractmethod
    async def setup(self, app: FastAPI) -> None:
        """Set up the service connection.

        Args:
            app: FastAPI app instance
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close the service connection."""
        pass
