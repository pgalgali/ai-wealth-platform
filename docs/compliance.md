# Compliance and data-use boundary

The platform is designed to support licensed and publicly available sources. Source adapters must be approved before activation and must document:

- source owner, license or terms URL, permitted use, rate limits, and retention policy;
- whether data is delayed, real-time, derived, or user-provided;
- the fields that may be displayed, cached, exported, or used for model training;
- a contact and kill switch for takedown or source-policy changes.

The system must not bypass CAPTCHAs, login walls, paywalls, robots restrictions, or anti-bot controls. If a source does not provide an authorized API or permitted feed, the adapter remains an interface plus mock implementation.

Broker connections are user-authorized only. A production order workflow requires OAuth/session authorization, broker-side order permissions, a pre-trade confirmation, idempotency key, limit/risk checks, audit event, and a clear failure state. No autonomous agent may submit an order.

AI output must show citations, data timestamps, confidence, material risk flags, and a non-advisory disclaimer. Fin-Debunk scores are a research signal and must not be presented as a legal finding or factual determination without human review.
