from datetime import UTC, datetime
from collections.abc import Sequence
from uuid import uuid4

from app.schemas.market import Citation, MarketOverviewResponse, MarketPulse, ScreenerResult, WhaleChange


class MockMarketDataAdapter:
    """Synthetic fixture adapter used for local development and contract tests."""

    async def overview(self) -> MarketOverviewResponse:
        return MarketOverviewResponse(
            as_of=datetime.now(UTC).isoformat(),
            source_mode="mock",
            pulse=[
                MarketPulse(name="NIFTY 50", value="24,840.75", change="+0.82%", tone="positive"),
                MarketPulse(name="SENSEX", value="81,332.12", change="+0.76%", tone="positive"),
                MarketPulse(name="BANK NIFTY", value="56,112.40", change="+1.28%", tone="positive"),
                MarketPulse(name="INDIA VIX", value="13.42", change="-3.06%", tone="positive"),
            ],
            breadth={"advances": 1240, "declines": 702, "ratio": 1.76},
            data_quality=0.98,
        )

    async def whale_changes(self) -> Sequence[WhaleChange]:
        return [
            WhaleChange(name="Mukul Agrawal", category="Investor", action="Added", holding="Radico Khaitan", change="+1.2%", signal="positive", date="Today"),
            WhaleChange(name="Dolly Khanna", category="Investor", action="Trimmed", holding="Mahanagar Gas", change="-0.8%", signal="warning", date="Today"),
            WhaleChange(name="Parag Parikh Flexi Cap", category="Mutual fund", action="New buy", holding="HDFC AMC", change="0.6%", signal="positive", date="Yesterday"),
            WhaleChange(name="SBI Mutual Fund", category="Mutual fund", action="Exited", holding="Zydus Lifesciences", change="0.0%", signal="negative", date="Yesterday"),
            WhaleChange(name="Ashish Kacholia", category="Investor", action="Added", holding="SJS Enterprises", change="+0.5%", signal="positive", date="18 Jun"),
        ]

    async def screen(self, filters: Sequence[str], limit: int) -> Sequence[ScreenerResult]:
        del filters
        rows = [
            ScreenerResult(ticker="HDFCAMC", company="HDFC Asset Management", sector="Financials", composite=92, quality=90, momentum=95, valuation="Fair"),
            ScreenerResult(ticker="POLYCAB", company="Polycab India", sector="Industrials", composite=88, quality=92, momentum=86, valuation="Fair"),
            ScreenerResult(ticker="RADICO", company="Radico Khaitan", sector="Consumer", composite=86, quality=84, momentum=89, valuation="Rich"),
            ScreenerResult(ticker="CERA", company="Cera Sanitaryware", sector="Consumer", composite=82, quality=87, momentum=77, valuation="Fair"),
            ScreenerResult(ticker="KPITTECH", company="KPIT Technologies", sector="Technology", composite=78, quality=91, momentum=64, valuation="Rich"),
        ]
        return rows[:limit]


class MockResearchAdapter:
    async def answer(self, question: str) -> tuple[str, float, list[str], list[Citation]]:
        return (
            f"For '{question}', the mock research workflow finds a constructive smart-money signal but recommends confirmation before acting. Review valuation, liquidity, and your target allocation before making any decision.",
            0.78,
            ["Valuation may be ahead of the long-term trend", "This fixture is not live investment research"],
            [
                Citation(title="Licensed exchange filing adapter placeholder", source="NSE adapter contract"),
                Citation(title="Mutual fund disclosure adapter placeholder", source="AMFI adapter contract"),
            ],
        )


class MockNotificationAdapter:
    async def publish(self, event_type: str, payload: dict[str, str]) -> str:
        del event_type, payload
        return f"mock-event-{uuid4()}"
