import asyncio
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import TypeVar

Result = TypeVar("Result")


@dataclass(frozen=True)
class RetryPolicy:
    attempts: int = 3
    base_delay_seconds: float = 0.25
    max_delay_seconds: float = 3.0

    async def run(self, operation: Callable[[], Awaitable[Result]]) -> Result:
        last_error: Exception | None = None
        for attempt in range(self.attempts):
            try:
                return await operation()
            except Exception as error:  # provider adapters map expected failures before this boundary
                last_error = error
                if attempt == self.attempts - 1:
                    break
                delay = min(self.max_delay_seconds, self.base_delay_seconds * (2**attempt))
                await asyncio.sleep(delay)
        assert last_error is not None
        raise last_error


class TtlCache:
    def __init__(self) -> None:
        self._items: dict[str, tuple[float, object]] = {}

    def get(self, key: str) -> object | None:
        item = self._items.get(key)
        if item is None or item[0] <= time.monotonic():
            self._items.pop(key, None)
            return None
        return item[1]

    def set(self, key: str, value: object, ttl_seconds: float) -> None:
        self._items[key] = (time.monotonic() + ttl_seconds, value)
