from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from argos.models.event_log import EventLogRecord


def test_record_preserves_event_data() -> None:
    timestamp = datetime(2026, 10, 15, 12, 0, tzinfo=UTC)

    record = EventLogRecord(
        log_name="System",
        event_id=7036,
        record_id=42,
        timestamp=timestamp,
        level=4,
        provider="Service Control Manager",
        message="The service entered the running state.",
        computer="WORKSTATION",
    )

    assert record.timestamp == timestamp
    assert record.event_id == 7036
    assert record.record_id == 42
    assert record.level == 4
    assert record.provider == "Service Control Manager"


def test_record_cannot_be_modified() -> None:
    record = EventLogRecord(
        log_name="System",
        event_id=7036,
        record_id=42,
        timestamp=datetime(2026, 10, 15, tzinfo=UTC),
        level=None,
        provider="Service Control Manager",
        message="",
        computer="WORKSTATION",
    )

    with pytest.raises(FrozenInstanceError):
        record.message = "Changed"