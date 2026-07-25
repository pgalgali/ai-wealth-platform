import asyncio
import json
from collections.abc import AsyncIterator
from datetime import UTC, datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/v1/stream", tags=["streaming"])


async def mock_events() -> AsyncIterator[str]:
    for sequence in range(3):
        payload = {"event": "market.heartbeat", "sequence": sequence, "as_of": datetime.now(UTC).isoformat()}
        yield f"data: {json.dumps(payload)}\n\n"
        await asyncio.sleep(1)


@router.get("/market")
async def market_stream() -> StreamingResponse:
    return StreamingResponse(mock_events(), media_type="text/event-stream")


@router.websocket("/ws")
async def market_websocket(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        for sequence in range(3):
            await websocket.send_json({"event": "market.heartbeat", "sequence": sequence})
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        return
