# Production checklist

## Before enabling live data

- [ ] Sign and record each exchange, mutual-fund, broker, messaging, and market-data license.
- [ ] Replace `DATA_MODE=mock` only after adapter contract tests pass against a sandbox or approved feed.
- [ ] Configure Redis, Postgres/TimescaleDB, Elasticsearch, backups, retention, and encryption at rest.
- [ ] Store secrets in Vault or a managed secret store; never commit `.env` files or API keys.
- [ ] Configure rate limits, source-specific quotas, retries with jitter, circuit breakers, and cache TTLs.
- [ ] Add Sentry, Prometheus, Grafana, alert routing, on-call ownership, and incident runbooks.

## Before enabling broker actions

- [ ] Validate broker API terms and the permitted automation scope.
- [ ] Implement user authorization, token encryption, consent records, order idempotency, and two-step confirmation.
- [ ] Run paper trading and failure-injection tests; keep `BROKER_MODE=disabled` in all preview environments.
- [ ] Add RBAC, transaction limits, kill switch, reconciliation, and immutable audit events.

## Before public launch

- [ ] Complete threat modeling, OWASP review, dependency scanning, DAST, and secret scanning.
- [ ] Complete accessibility, responsive, localization, and performance checks.
- [ ] Reach the coverage target with unit, integration, browser, load, and recovery tests.
- [ ] Obtain legal review for disclosures, investment-advice perimeter, privacy, consent, and data retention.
