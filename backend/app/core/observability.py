import logging
import time
from collections.abc import Awaitable, Callable
from uuid import uuid4

from fastapi import Request, Response
from prometheus_client import Counter, Histogram

request_counter = Counter("astra_http_requests_total", "HTTP requests", ["method", "path", "status"])
request_latency = Histogram("astra_http_request_duration_seconds", "HTTP request latency", ["path"])


def configure_logging(level: str) -> None:
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(name)s %(message)s")


async def request_observability(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    request_id = request.headers.get("x-request-id", str(uuid4()))
    started = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - started
    request_counter.labels(request.method, request.url.path, str(response.status_code)).inc()
    request_latency.labels(request.url.path).observe(duration)
    response.headers["x-request-id"] = request_id
    response.headers["x-content-type-options"] = "nosniff"
    return response
