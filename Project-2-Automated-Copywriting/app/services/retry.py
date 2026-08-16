import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


async def retry_async(
    operation: Callable[[], Awaitable[T]],
    retries: int = 3,
    delay: float = 1.0,
) -> T:
    last_error: Exception | None = None

    for attempt in range(retries):
        try:
            return await operation()
        except Exception as exc:
            last_error = exc

            if attempt == retries - 1:
                raise

            await asyncio.sleep(delay * (2 ** attempt))

    raise RuntimeError("Retry operation failed.") from last_error
