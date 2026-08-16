import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


async def run_concurrently(
    operations: list[Callable[[], Awaitable[T]]],
    max_concurrent: int = 3,
) -> list[T]:
    semaphore = asyncio.Semaphore(max_concurrent)

    async def execute(
        operation: Callable[[], Awaitable[T]],
    ) -> T:
        async with semaphore:
            return await operation()

    return await asyncio.gather(
        *(execute(operation) for operation in operations)
    )
