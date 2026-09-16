"""Normalized Windows Event Log domain model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any


class EventSeverity(StrEnum):
    """Normalized severity assigned to a Windows event."""

    SUCCESS = "success"
    INFORMATION = "information"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    FAILURE = "failure"
    UNKNOWN  = "unknown"


@dataclass(frozen=True, slots=True)
class EventRecord:
    """Represent one normalized Windows Event Log record"""

    log_name: str
    event_id: int
    severity: EventSeverity
    source: str
    time_created: datetime
    message: str
    record_id: int | None = None

    def __post_init__(self) -> None:
        """Validate the normalized event fields."""

        if not self.log_name.strip():
            raise ValueError("Event log name cannot be empty.")

        if self.event_id <0:
            raise ValueError("Event ID cannot be negative.")

        if not self.source.strip():
            raise ValueError("Event source cannot be empty.")

        if self.time_created.tzinfo is None:
            raise ValueError("Event timestamp must include timezone information.")

        if self.record_id is not None and self.record_id <0:
            raise ValueError("Event record ID cannot be negative.")

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable event representation."""

        return {
            "log_name": self.log_name,
            "event_id": self.event_id,
            "severity": self.severity.value,
            "source": self.source,
            "time_created": self.time_created.isoformat(),
            "message": self.message,
            "record_id": self.record_id,
        }
