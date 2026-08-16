import pytest

from app.services.retry import retry_async


@pytest.mark.asyncio
async def test_retry_succeeds_after_failures():
    attempts = 0

    async def operation():
        nonlocal attempts
        attempts += 1

        if attempts < 3:
            raise RuntimeError("Temporary failure")

        return "SUCCESS"

    result = await retry_async(
        operation,
        retries=3,
        delay=0,
    )

    assert result == "SUCCESS"
    assert attempts == 3


@pytest.mark.asyncio
async def test_retry_raises_after_all_attempts():
    attempts = 0

    async def operation():
        nonlocal attempts
        attempts += 1
        raise RuntimeError("Permanent failure")

    with pytest.raises(RuntimeError, match="Permanent failure"):
        await retry_async(
            operation,
            retries=3,
            delay=0,
        )

    assert attempts == 3
