from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Astra Wealth API"
    environment: str = "development"
    data_mode: str = Field(default="mock", validation_alias="DATA_MODE")
    ai_provider: str = Field(default="mock", validation_alias="AI_PROVIDER")
    broker_mode: str = Field(default="disabled", validation_alias="BROKER_MODE")
    database_url: str = Field(default="postgresql+asyncpg://astra:astra@localhost:5432/astra", validation_alias="DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", validation_alias="REDIS_URL")
    elasticsearch_url: str = Field(default="http://localhost:9200", validation_alias="ELASTICSEARCH_URL")
    elasticsearch_api_key: str = Field(default="", validation_alias="ELASTICSEARCH_API_KEY")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    allowed_origins: str = Field(default="http://localhost:3000", validation_alias="ALLOWED_ORIGINS")
    cron_secret: str = Field(default="", validation_alias="CRON_SECRET")
    market_cache_ttl_seconds: int = Field(default=60, validation_alias="MARKET_CACHE_TTL_SECONDS")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    @property
    def origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
