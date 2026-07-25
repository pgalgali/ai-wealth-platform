from typing import Literal

from pydantic import BaseModel, Field

Tone = Literal["positive", "negative", "neutral", "warning"]


class MarketPulse(BaseModel):
    name: str
    value: str
    change: str
    tone: Tone


class WhaleChange(BaseModel):
    name: str
    category: str
    action: str
    holding: str
    change: str
    signal: Tone
    date: str


class MarketOverviewResponse(BaseModel):
    as_of: str
    source_mode: str
    pulse: list[MarketPulse]
    breadth: dict[str, float]
    data_quality: float = Field(ge=0, le=1)


class ScreenerRequest(BaseModel):
    universe: str = Field(default="nifty_500", min_length=1, max_length=64)
    filters: list[str] = Field(default_factory=lambda: ["quality", "momentum"])
    limit: int = Field(default=25, ge=1, le=100)


class ScreenerResult(BaseModel):
    ticker: str
    company: str
    sector: str
    composite: int = Field(ge=0, le=100)
    quality: int = Field(ge=0, le=100)
    momentum: int = Field(ge=0, le=100)
    valuation: str


class ScreenerResponse(BaseModel):
    query: ScreenerRequest
    source_mode: str
    results: list[ScreenerResult]


class CopilotRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    portfolio_context: bool = True


class Citation(BaseModel):
    title: str
    source: str
    published_at: str | None = None
    url: str | None = None


class CopilotResponse(BaseModel):
    answer: str
    confidence: float = Field(ge=0, le=1)
    risk_flags: list[str]
    citations: list[Citation]
    disclaimer: str
