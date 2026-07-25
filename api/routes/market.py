from fastapi import APIRouter, Depends, Header, HTTPException

from app.core.config import get_settings
from app.domain.ports import MarketDataPort
from app.domain.services import MarketService
from app.infrastructure.cache import cache_get, cache_set
from app.infrastructure.live_adapters import LiveMarketDataAdapter
from app.infrastructure.mock_adapters import MockMarketDataAdapter
from app.schemas.market import MarketOverviewResponse, ScreenerRequest, ScreenerResponse, WhaleChange

router = APIRouter(prefix="/v1", tags=["market intelligence"])

_OVERVIEW_CACHE_KEY = "market:overview"


def get_market_data_adapter() -> MarketDataPort:
    settings = get_settings()
    if settings.data_mode == "live":
        return LiveMarketDataAdapter()
    return MockMarketDataAdapter()


def get_market_service() -> MarketService:
    return MarketService(get_market_data_adapter())


@router.get("/market/overview", response_model=MarketOverviewResponse)
async def overview(service: MarketService = Depends(get_market_service)) -> MarketOverviewResponse:
    settings = get_settings()
    cached = await cache_get(_OVERVIEW_CACHE_KEY)
    if cached is not None:
        return MarketOverviewResponse(**cached)

    result = await service.overview()
    await cache_set(_OVERVIEW_CACHE_KEY, result.model_dump(), settings.market_cache_ttl_seconds)
    return result


@router.get("/whales/changes", response_model=list[WhaleChange])
async def whale_changes(service: MarketService = Depends(get_market_service)) -> list[WhaleChange]:
    return list(await service.whale_changes())


@router.post("/screener/scan", response_model=ScreenerResponse)
async def scan(request: ScreenerRequest, service: MarketService = Depends(get_market_service)) -> ScreenerResponse:
    return await service.screen(request)


@router.get("/market/refresh", include_in_schema=False)
async def refresh(
    service: MarketService = Depends(get_market_service),
    authorization: str | None = Header(default=None),
) -> dict[str, str]:
    """Called by Vercel Cron on a schedule to pre-warm the overview cache.

    Vercel Cron only issues GET requests. When a `CRON_SECRET` env var is set on the
    project, Vercel automatically attaches it as `Authorization: Bearer <CRON_SECRET>`
    on cron-triggered invocations -- so we validate against that same convention rather
    than a custom header, and this route stays protected without any extra wiring.
    """
    settings = get_settings()
    expected = f"Bearer {settings.cron_secret}"
    if not settings.cron_secret or authorization != expected:
        raise HTTPException(status_code=401, detail="Missing or invalid cron secret")

    result = await service.overview()
    await cache_set(_OVERVIEW_CACHE_KEY, result.model_dump(), settings.market_cache_ttl_seconds)
    return {"status": "refreshed", "as_of": result.as_of}
