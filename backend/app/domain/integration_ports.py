from collections.abc import Mapping, Sequence
from typing import Protocol


class BrokerPort(Protocol):
    """User-authorized broker boundary; implementations must never place silent orders."""

    async def connect(self, user_id: str, authorization_code: str) -> str: ...

    async def holdings(self, connection_id: str) -> Sequence[Mapping[str, str]]: ...

    async def create_order_preview(self, connection_id: str, order: Mapping[str, str]) -> Mapping[str, str]: ...


class AccountAggregatorPort(Protocol):
    """Pluggable Account Aggregator boundary; no bank credentials belong in this service."""

    async def create_consent(self, user_id: str, purpose: str) -> str: ...

    async def fetch_statement(self, consent_id: str) -> Mapping[str, object]: ...


class NotificationPort(Protocol):
    async def send(self, channel: str, destination: str, message: str, idempotency_key: str) -> str: ...
