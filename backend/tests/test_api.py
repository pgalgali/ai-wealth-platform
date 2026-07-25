from httpx import ASGITransport, AsyncClient

from app.main import app


async def test_ready_health() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


async def test_market_overview_contract() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/v1/market/overview")

    body = response.json()
    assert response.status_code == 200
    assert body["source_mode"] == "mock"
    assert body["pulse"][0]["name"] == "NIFTY 50"


async def test_copilot_has_disclaimer() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/v1/copilot/ask", json={"question": "Analyze HDFC AMC"})

    assert response.status_code == 200
    assert "Not investment" in response.json()["disclaimer"]
