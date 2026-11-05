"""Windows event-log sources and query configuration."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from argos.core.powershell import PowerShellRunner
from argos.core.powershell_commands import build_event_logs_command
from argos.models import EventRecord, EventSeverity


class EventLogSource(StrEnum):
    SYSTEM = "System"
    APPLICATION = "Application"
    SECURITY = "Security"
    SETUP = "Setup"
    DEFENDER = "Microsoft-Windows-Windows Defender/Operational"
    POWERSHELL = "Microsoft-Windows-PowerShell/Operational"
    TASK_SCHEDULER = "Microsoft-Windows-TaskScheduler/Operational"

EVENT_LEVEL_SEVERITIES: dict[int, EventSeverity] = {
    1: EventSeverity.CRITICAL,
    2: EventSeverity.ERROR,
    3: EventSeverity.WARNING,
    4: EventSeverity.INFORMATION,
    5: EventSeverity.SUCCESS,
}

def normalize_event_severity(value: Any) -> EventSeverity:
    """Convert a Windows event level to a normalized severity."""
    if isinstance(value, bool) or not isinstance(value, int):
        return EventSeverity.UNKNOWN

    return EVENT_LEVEL_SEVERITIES.get(value, EventSeverity.UNKNOWN)

POWERSHELL_DATE_PATTERN = re.compile(
    r"^/Date\((?P<milliseconds>-?\d+)(?:[+-]\d{4})?\)/$"
)

@dataclass(frozen=True, slots=True)
class EventLogQuery:
    source: EventLogSource = EventLogSource.SYSTEM
    max_events: int = 100

    def __post_init__(self) -> None:
        if not isinstance(self.source, EventLogSource):
            raise ValueError("source must be an EventLogSource.")

        if (
            isinstance(self.max_events, bool)
            or not isinstance(self.max_events, int)
            or self.max_events <= 0
        ):
            raise ValueError("max_events must be a positive integer.")

def build_event_query_command(query: EventLogQuery) -> str:
    """Translate a validated event query into a PS command."""
    return build_event_logs_command(
        log_name=query.source.value,
        max_events=query.max_events,
    )

def normalize_event_timestamp(value: Any) -> datetime:
    """Convert a PS event timestamp to an aware datetime."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Event timestamp must be a non-empty string.")

    powershell_match = POWERSHELL_DATE_PATTERN.fullmatch(value)

    if powershell_match:
        try:
            milliseconds = int(powershell_match.group("milliseconds"))
            return datetime.fromtimestamp(milliseconds / 1000, tz=UTC)
        except (OSError, OverflowError, ValueError) as error:
            raise ValueError("Event timestamp is invalid.") from error

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("Event timestamp is invalid.") from error

    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)

    return parsed.astimezone(UTC)

def require_integer(value: Any, field_name: str) -> int:
    """Return an integer field or raise a normalization error."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field_name} must be an integer.")

    return value

def normalize_event_record(raw_event: dict[str, Any]) -> EventRecord:
    """Convert one raw PS event into an EventRecord"""
    log_name = raw_event.get("LogName")
    provider = raw_event.get("ProviderName")
    message = raw_event.get("Message")
    record_id = raw_event.get("RecordId")

    if not isinstance(log_name, str):
        raise ValueError("Event LogName must be a string.")

    if not isinstance(provider, str):
        raise ValueError("Event ProviderName must be a string.")

    if message is None:
        normalized_message = ""
    elif isinstance(message, str):
        normalized_message = message
    else:
        raise ValueError("Event Message must be a string or null.")

    normalized_record_id = (
        None
        if record_id is None
        else require_integer(record_id, "Event RecordId")
    )

    return EventRecord(
        log_name=log_name,
        event_id=require_integer(raw_event.get("Id"), "Event Id"),
        severity=normalize_event_severity(raw_event.get("Level")),
        source=provider,
        time_created=normalize_event_timestamp(raw_event.get("TimeCreated")),
        message=normalized_message,
        record_id=normalized_record_id,
    )

def collect_event_logs(
        query: EventLogQuery,
        runner: PowerShellRunner | None = None,
) -> list[EventRecord]:
    """Collect and normalize Windows Event Log records."""
    ps_runner = runner or PowerShellRunner()
    command = build_event_query_command(query)
    result = ps_runner.run_json(command)

    if result is None:
        return []

    if isinstance(result, dict):
        raw_events = [result]
    elif isinstance(result, list):
        raw_events = result
    else:
        raise ValueError(
            "Event Log output must be an object, a list of objects, or null."
        )

    normalized_events: list[EventRecord] = []

    for raw_event in raw_events:
        if not isinstance(raw_event, dict):
            raise ValueError("Each Event Log result must be an object.")

        normalized_events.append(normalize_event_record(raw_event))

    return normalized_events