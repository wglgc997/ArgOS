from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class EventLogRecord:
    """Represents a single event log record."""

    log_name: str
    event_id: int
    record_id: int
    timestamp: datetime
    level: int | None
    provider: str
    message: str
    computer: str