from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.api.routes import health, market, research, stream
from app.core.config import get_settings
from app.core.observability import configure_logging, request_observability

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(
    title="Astra Wealth API",
    version="0.1.0",
    description="Provider-neutral wealth intelligence APIs with mock-safe defaults.",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.middleware("http")(request_observability)
app.include_router(health.router)
app.include_router(market.router)
app.include_router(research.router)
app.include_router(stream.router)


@app.get("/metrics", include_in_schema=False)
async def metrics() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/", include_in_schema=False)
async def root() -> dict[str, str]:
    return {"service": settings.app_name, "status": "ok", "docs": "/docs"}
