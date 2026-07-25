from app.domain.ports import MarketDataPort, ResearchPort
from app.schemas.market import CopilotResponse, ScreenerRequest, ScreenerResponse


class MarketService:
    def __init__(self, provider: MarketDataPort) -> None:
        self.provider = provider

    async def overview(self):
        return await self.provider.overview()

    async def whale_changes(self):
        return await self.provider.whale_changes()

    async def screen(self, request: ScreenerRequest) -> ScreenerResponse:
        results = await self.provider.screen(request.filters, request.limit)
        return ScreenerResponse(query=request, source_mode="mock", results=list(results))


class CopilotService:
    def __init__(self, provider: ResearchPort) -> None:
        self.provider = provider

    async def answer(self, question: str) -> CopilotResponse:
        answer, confidence, risk_flags, citations = await self.provider.answer(question)
        return CopilotResponse(
            answer=answer,
            confidence=confidence,
            risk_flags=risk_flags,
            citations=citations,
            disclaimer="Research support only. Not investment, tax, or legal advice.",
        )
