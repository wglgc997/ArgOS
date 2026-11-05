from datetime import UTC, datetime
from typing import Any
from unittest.mock import Mock

import pytest

from argos.models import EventRecord, EventSeverity
from argos.modules.event_logs import (
    EventLogQuery,
    EventLogSource,
    collect_event_logs,
    normalize_event_record,
    normalize_event_severity,
    normalize_event_timestamp,
)


def test_query_defaults() -> None:
    query = EventLogQuery()

    assert query.source is EventLogSource.SYSTEM
    assert query.max_events == 100


def test_query_accepts_custom_source_and_limit() -> None:
    query = EventLogQuery(
        source=EventLogSource.APPLICATION,
        max_events=20,
    )

    assert query.source is EventLogSource.APPLICATION
    assert query.max_events == 20


@pytest.mark.parametrize("max_events", [0, -1, True, "100", 1.5])
def test_query_rejects_invalid_limits(max_events: Any) -> None:
    with pytest.raises(ValueError, match="positive integer"):
        EventLogQuery(max_events=max_events)


def test_query_rejects_invalid_source() -> None:
    with pytest.raises(ValueError, match="EventLogSource"):
        EventLogQuery(source="Invalid")  # type: ignore[arg-type]


def make_raw_event(**overrides: Any) -> dict[str, Any]:
    event: dict[str, Any] = {
        "LogName": "System",
        "Id": 6005,
        "RecordId": 12345,
        "TimeCreated": "2026-11-05T13:30:00Z",
        "Level": 4,
        "ProviderName": "EventLog",
        "Message": "The Event Log service was started.",
        "MachineName": "WORKSTATION",
    }
    event.update(overrides)
    return event

@pytest.mark.parametrize(
    ("level", "expected"),
    [
        (1, EventSeverity.CRITICAL),
        (2, EventSeverity.ERROR),
        (3, EventSeverity.WARNING),
        (4, EventSeverity.INFORMATION),
        (5, EventSeverity.SUCCESS),
        (0, EventSeverity.UNKNOWN),
        (99, EventSeverity.UNKNOWN),
        (None, EventSeverity.UNKNOWN),
        ("4", EventSeverity.UNKNOWN),
        (True, EventSeverity.UNKNOWN),
    ],
)
def test_normalize_event_severity(
    level: Any,
    expected: EventSeverity,
) -> None:
    assert normalize_event_severity(level) is expected


def test_normalize_iso_event_timestamp_to_utc() -> None:
    result = normalize_event_timestamp("2026-11-05T10:30:00-03:00")

    assert result == datetime(2026, 11, 5, 13, 30, tzinfo=UTC)


def test_normalize_powershell_event_timestamp() -> None:
    result = normalize_event_timestamp("/Date(1793885400000)/")

    assert result.tzinfo is UTC


@pytest.mark.parametrize("value", [None, "", "invalid"])
def test_rejects_invalid_event_timestamp(value: Any) -> None:
    with pytest.raises(ValueError, match="timestamp"):
        normalize_event_timestamp(value)


def test_normalize_event_record() -> None:
    event = normalize_event_record(make_raw_event())

    assert event == EventRecord(
        log_name="System",
        event_id=6005,
        severity=EventSeverity.INFORMATION,
        source="EventLog",
        time_created=datetime(2026, 11, 5, 13, 30, tzinfo=UTC),
        message="The Event Log service was started.",
        record_id=12345,
    )
def test_normalize_event_record_allows_optional_fields() -> None:
    event = normalize_event_record(
        make_raw_event(
            RecordId=None,
            Message=None,
            Level=None,
        )
    )

    assert event.record_id is None
    assert event.message == ""
    assert event.severity is EventSeverity.UNKNOWN


def test_collect_event_logs_returns_empty_list_for_no_output() -> None:
    runner = Mock()
    runner.run_json.return_value = None

    result = collect_event_logs(EventLogQuery(), runner=runner)

    assert result == []
    runner.run_json.assert_called_once()

def test_collect_event_logs_normalizes_single_event() -> None:
    runner = Mock()
    runner.run_json.return_value = make_raw_event()

    result = collect_event_logs(EventLogQuery(), runner=runner)

    assert len(result) == 1
    assert result[0].event_id == 6005

def test_collect_event_logs_normalizes_event_list() -> None:
    runner = Mock()
    runner.run_json.return_value = [
        make_raw_event(Id=6005),
        make_raw_event(Id=6006, RecordId=12346),
    ]

    result = collect_event_logs(EventLogQuery(), runner=runner)

    assert [event.event_id for event in result] == [6005, 6006]

def test_collect_event_logs_executes_query_command() -> None:
    runner = Mock()
    runner.run_json.return_value = None
    query = EventLogQuery(
        source=EventLogSource.APPLICATION,
        max_events=25,
    )

    collect_event_logs(query, runner=runner)

    command = runner.run_json.call_args.args[0]
    assert "-LogName 'Application'" in command
    assert "-MaxEvents 25" in command

@pytest.mark.parametrize("result", ["invalid", 10, True])
def test_collect_event_logs_rejects_invalid_output(result: Any) -> None:
    runner = Mock()
    runner.run_json.return_value = result

    with pytest.raises(ValueError, match="object"):
        collect_event_logs(EventLogQuery(), runner=runner)


def test_collect_event_logs_rejects_invalid_list_item() -> None:
    runner = Mock()
    runner.run_json.return_value = [make_raw_event(), "invalid"]

    with pytest.raises(ValueError, match="Each Event Log result"):
        collect_event_logs(EventLogQuery(), runner=runner)