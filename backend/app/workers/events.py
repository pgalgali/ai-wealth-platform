from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class DomainEvent:
    event_type: str
    payload: dict[str, object]
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    schema_version: int = 1


def institutional_change_event(payload: dict[str, object]) -> DomainEvent:
    return DomainEvent(event_type="institutional.change.detected", payload=payload)
