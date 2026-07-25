"""Live market data adapter backed by Yahoo Finance's public chart endpoint.

Only `overview()` is genuinely live here. `whale_changes()` and `screen()` still delegate
to the mock adapter, because institutional-change and screener-composite data require a
licensed feed (see docs/compliance.md) that this scaffold does not include. Keeping that
split explicit avoids silently presenting fixture data as if it were live.
"""
import asyncio
import logging
from collections.abc import Sequence
from datetime import UTC, datetime

import httpx

from app.infrastructure.mock_adapters import MockMarketDataAdapter
from app.schemas.market import MarketOverviewResponse, MarketPulse, ScreenerResult, WhaleChange

logger = logging.getLogger(__name__)

_YAHOO_CHART_URL = "https://query2.finance.yahoo.com/v8/finance/chart/{symbol}"

# Yahoo tickers for the indices shown on the Overview panel.
_INDEX_SYMBOLS: list[tuple[str, str]] = [
    ("^NSEI", "NIFTY 50"),
    ("^BSESN", "SENSEX"),
    ("^NSEBANK", "BANK NIFTY"),
    ("^INDIAVIX", "INDIA VIX"),
]


async def _fetch_quote(client: httpx.AsyncClient, symbol: str) -> dict | None:
    try:
        response = await client.get(
            _YAHOO_CHART_URL.format(symbol=symbol),
            params={"interval": "1d", "range": "5d"},
            headers={"User-Agent": "Mozilla/5.0 (AstraWealth/1.0)"},
            timeout=8.0,
        )
        response.raise_for_status()
        payload = response.json()
        result = payload["chart"]["result"][0]
        meta = result["meta"]
        return {
            "price": meta["regularMarketPrice"],
            "previous_close": meta["chartPreviousClose"],
        }
    except Exception:  # noqa: BLE001 - a single failed symbol should not fail the whole overview
        logger.warning("Yahoo Finance fetch failed for symbol=%s", symbol, exc_info=True)
        return None


def _pulse_from_quote(name: str, symbol: str, quote: dict) -> MarketPulse:
    price = quote["price"]
    prev = quote["previous_close"]
    pct_change = ((price - prev) / prev) * 100 if prev else 0.0
    is_vix = symbol == "^INDIAVIX"
    # For VIX, a *drop* reads as calmer markets -> positive tone, mirroring the fixture convention.
    positive = pct_change < 0 if is_vix else pct_change >= 0
    return MarketPulse(
        name=name,
        value=f"{price:,.2f}",
        change=f"{pct_change:+.2f}%",
        tone="positive" if positive else "negative",
    )


class LiveMarketDataAdapter:
    """Real index quotes for overview(); mock fixtures for whale/screener until a licensed feed exists."""

    def __init__(self) -> None:
        self._mock = MockMarketDataAdapter()

    async def overview(self) -> MarketOverviewResponse:
        async with httpx.AsyncClient() as client:
            quotes = await asyncio.gather(*(_fetch_quote(client, symbol) for symbol, _ in _INDEX_SYMBOLS))

        pulse: list[MarketPulse] = []
        failures = 0
        for (symbol, name), quote in zip(_INDEX_SYMBOLS, quotes, strict=True):
            if quote is None:
                failures += 1
                continue
            pulse.append(_pulse_from_quote(name, symbol, quote))

        if not pulse:
            # Total upstream failure: fall back to mock rather than return an empty panel.
            fallback = await self._mock.overview()
            return fallback

        data_quality = round(1.0 - (failures / len(_INDEX_SYMBOLS)), 2)
        return MarketOverviewResponse(
            as_of=datetime.now(UTC).isoformat(),
            source_mode="live",
            pulse=pulse,
            # Market breadth (advances/declines) needs a separate full-market feed, not just
            # index quotes -- left as zeros rather than fabricated until that feed is wired in.
            breadth={"advances": 0, "declines": 0, "ratio": 0.0},
            data_quality=data_quality,
        )

    async def whale_changes(self) -> Sequence[WhaleChange]:
        return await self._mock.whale_changes()

    async def screen(self, filters: Sequence[str], limit: int) -> Sequence[ScreenerResult]:
        return await self._mock.screen(filters, limit)
