"""Thin, fail-open Redis cache used to avoid re-fetching live market data on every request.

Design intent: a cache outage should degrade to "fetch live" or "serve mock", never to a
hard 500. Vercel functions are stateless and short-lived, so this cache (backed by a managed
Redis such as Upstash) is what makes a scheduled refresh (Vercel Cron) actually useful --
requests read the cached snapshot instead of re-hitting the upstream data source per request.
"""
import json
import logging
from typing import Any

from app.core.config import get_settings

logger = logging.getLogger(__name__)

_redis_client: Any = None
_redis_unavailable = False


async def _get_client() -> Any:
    global _redis_client, _redis_unavailable
    if _redis_unavailable:
        return None
    if _redis_client is not None:
        return _redis_client
    try:
        import redis.asyncio as redis  # imported lazily so the API still boots without redis installed

        settings = get_settings()
        _redis_client = redis.from_url(settings.redis_url, decode_responses=True, socket_connect_timeout=2)
        return _redis_client
    except Exception:  # noqa: BLE001 - cache must never break the request path
        logger.warning("Redis cache unavailable; continuing without cache", exc_info=True)
        _redis_unavailable = True
        return None


async def cache_get(key: str) -> dict | None:
    client = await _get_client()
    if client is None:
        return None
    try:
        raw = await client.get(key)
        return json.loads(raw) if raw else None
    except Exception:  # noqa: BLE001
        logger.warning("Redis GET failed for key=%s", key, exc_info=True)
        return None


async def cache_set(key: str, value: dict, ttl_seconds: int) -> None:
    client = await _get_client()
    if client is None:
        return
    try:
        await client.set(key, json.dumps(value), ex=ttl_seconds)
    except Exception:  # noqa: BLE001
        logger.warning("Redis SET failed for key=%s", key, exc_info=True)
