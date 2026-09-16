"""Tests for the normalized Windows Event Log model."""

from datetime import UTC, datetime

import pytest

from argos.models import EventRecord, EventSeverity


def make_event(
    *,
    log_name: str = "System",
    event_id: int = 6005,
    severity: EventSeverity = EventSeverity.INFORMATION,
    source: str = "EventLog",
    time_created: datetime | None = None,
    message: str = "The Event Log service was started.",
    record_id: int | None = 12345,
) -> EventRecord:
    return EventRecord(
        log_name=log_name,
        event_id=event_id,
        severity=severity,
        source=source,
        time_created=time_created
        or datetime(2026, 9, 16, 10, 30, tzinfo=UTC),
        message=message,
        record_id=record_id,
    )


def test_event_record_to_dict() -> None:
    event = make_event()

    assert event.to_dict() == {
        "log_name": "System",
        "event_id": 6005,
        "severity": "information",
        "source": "EventLog",
        "time_created": "2026-09-16T10:30:00+00:00",
        "message": "The Event Log service was started.",
        "record_id": 12345,
    }


@pytest.mark.parametrize("log_name", ["", "   "])
def test_rejects_empty_log_name(log_name: str) -> None:
    with pytest.raises(ValueError, match="log name cannot be empty"):
        make_event(log_name=log_name)


def test_rejects_negative_event_id() -> None:
    with pytest.raises(ValueError, match="Event ID cannot be negative"):
        make_event(event_id=-1)


@pytest.mark.parametrize("source", ["", "   "])
def test_rejects_empty_source(source: str) -> None:
    with pytest.raises(ValueError, match="source cannot be empty"):
        make_event(source=source)


def test_rejects_timestamp_without_timezone() -> None:
    with pytest.raises(ValueError, match="must include timezone"):
        make_event(time_created=datetime(2026, 9, 16, 10, 30))


def test_rejects_negative_record_id() -> None:
    with pytest.raises(ValueError, match="record ID cannot be negative"):
        make_event(record_id=-1)


def test_allows_missing_record_id_and_empty_message() -> None:
    event = make_event(record_id=None, message="")

    assert event.record_id is None
    assert event.message == ""