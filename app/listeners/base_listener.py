from typing import List

from fastapi import FastAPI


class BaseListener:
    """Base listener class that all listeners should inherit from."""

    def __init__(self):
        register_listener(self)

    async def setup(self, app: FastAPI) -> None:
        """Initialize the listener."""
        raise NotImplementedError

    async def close(self) -> None:
        """Cleanup resources used by the listener."""
        raise NotImplementedError


# Module-level list to store all listener instances
_listeners: List[BaseListener] = []


def register_listener(listener: BaseListener) -> None:
    """Register a listener instance."""
    if listener not in _listeners:
        _listeners.append(listener)


async def setup_all_listeners(app: FastAPI) -> None:
    """
    Initialize all registered listeners.

    Args:
        app: FastAPI application instance
    """
    for listener in _listeners:
        try:
            await listener.setup(app)
        except Exception as e:
            # Clean up any listeners that were already initialized
            await close_all_listeners()
            raise RuntimeError(f"Failed to initialize listener {listener.__class__.__name__}: {str(e)}")


async def close_all_listeners() -> None:
    """
    Close all registered listeners in reverse order of initialization.
    """
    for listener in reversed(_listeners):
        try:
            await listener.close()
        except Exception as e:
            # Log the error but continue closing other listeners
            print(f"Error closing listener {listener.__class__.__name__}: {str(e)}")


def get_all_listeners() -> List[BaseListener]:
    """
    Get a list of all registered listeners.

    Returns:
        List of all registered listener instances
    """
    return _listeners.copy()
