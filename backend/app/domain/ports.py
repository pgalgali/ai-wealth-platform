from collections.abc import Sequence
from typing import Protocol

from app.schemas.market import Citation, MarketOverviewResponse, ScreenerResult, WhaleChange


class MarketDataPort(Protocol):
    async def overview(self) -> MarketOverviewResponse: ...

    async def whale_changes(self) -> Sequence[WhaleChange]: ...

    async def screen(self, filters: Sequence[str], limit: int) -> Sequence[ScreenerResult]: ...


class ResearchPort(Protocol):
    async def answer(self, question: str) -> tuple[str, float, list[str], list[Citation]]: ...


class NotificationPort(Protocol):
    async def publish(self, event_type: str, payload: dict[str, str]) -> str: ...
