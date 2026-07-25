# Astra Wealth

Astra Wealth is a compliance-first, AI-native wealth intelligence platform for Indian investors. The repository is modular: the Next.js terminal is deployable to Vercel, while the FastAPI service exposes provider-neutral APIs for market data, portfolio intelligence, screeners, alerts, and research workflows.

The repository ships with a complete local mock mode so the product can be run without broker credentials or paid market-data keys. Production connectors are represented by explicit ports and adapters. They must be enabled only after the relevant exchange, data-vendor, broker, and regulatory permissions are in place.

## Included

- Responsive dark terminal UI with Overview, Copilot, Whale Watch, Screener, Portfolio, and Alerts workspaces.
- Typed frontend contracts and mock fixtures for market pulse, smart-money changes, portfolio risk, alerts, and screener rows.
- FastAPI service with health, market overview, whale-watch, screener, and copilot endpoints.
- Provider-neutral adapter interfaces for market data, holdings, notifications, and AI research.
- PostgreSQL/TimescaleDB schema for users, portfolios, positions, time-series prices, signals, citations, and audit logs.
- Docker Compose for local Postgres, Redis, Elasticsearch, API, and web services.
- Kubernetes-ready manifests, NGINX edge configuration, GitHub Actions CI, environment template, OpenAPI document, and production checklist.

## Run the web terminal

```bash
npm install
npm run dev
```

Open `http://localhost:3000`. The default UI uses local fixtures. Set `NEXT_PUBLIC_API_URL` to connect it to the FastAPI service.

## Run the API

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API is available at `http://localhost:8000`, its OpenAPI UI at `/docs`, and health at `/health/ready`.

## Run the full local stack

```bash
docker compose -f infra/docker-compose.yml up --build
```

The local stack defaults to `DATA_MODE=mock`, `AI_PROVIDER=mock`, and `BROKER_MODE=disabled`. No trade can be placed in this mode.

## Architecture

The platform follows a hexagonal boundary:

```text
Next.js / Vercel
        |
        v
FastAPI application services ---- Redis cache / event bus
        |
        +---- Domain ports ---- licensed data adapters
        |                   \\--- broker-authorized adapters
        v
PostgreSQL + TimescaleDB / Elasticsearch
```

See `docs/architecture.md` and `docs/compliance.md` for the boundaries and production gates.

## Compliance boundary

The included fixtures are synthetic. No connector bypasses CAPTCHAs, authentication, paywalls, or terms of service. Optional scraping is not enabled and must only be implemented after a source has explicitly permitted it. Brokerage actions require a user-authorized OAuth/session flow, broker-supported APIs, a confirmation screen, idempotency keys, and an auditable consent record.

This is an engineering foundation, not investment advice or a registered investment-adviser service.
