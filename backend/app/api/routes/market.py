from fastapi import APIRouter, Depends

from app.domain.services import MarketService
from app.infrastructure.mock_adapters import MockMarketDataAdapter
from app.schemas.market import MarketOverviewResponse, ScreenerRequest, ScreenerResponse, WhaleChange

router = APIRouter(prefix="/v1", tags=["market intelligence"])
market_service = MarketService(MockMarketDataAdapter())


def get_market_service() -> MarketService:
    return market_service


@router.get("/market/overview", response_model=MarketOverviewResponse)
async def overview(service: MarketService = Depends(get_market_service)) -> MarketOverviewResponse:
    return await service.overview()


@router.get("/whales/changes", response_model=list[WhaleChange])
async def whale_changes(service: MarketService = Depends(get_market_service)) -> list[WhaleChange]:
    return list(await service.whale_changes())


@router.post("/screener/scan", response_model=ScreenerResponse)
async def scan(request: ScreenerRequest, service: MarketService = Depends(get_market_service)) -> ScreenerResponse:
    return await service.screen(request)
