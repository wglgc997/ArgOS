"""Windows event-log sources and query configuration."""

from dataclasses import dataclass
from enum import StrEnum


class EventLogSource(StrEnum):
    SYSTEM = "System"
    APPLICATION = "Application"
    SECURITY = "Security"
    SETUP = "Setup"
    DEFENDER = "Microsoft-Windows-Windows Defender/Operational"
    POWERSHELL = "Microsoft-Windows-PowerShell/Operational"
    TASK_SCHEDULER = "Microsoft-Windows-TaskScheduler/Operational"


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