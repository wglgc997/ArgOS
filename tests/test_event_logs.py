import pytest

from argos.modules.event_logs import EventLogQuery, EventLogSource


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
def test_query_rejects_invalid_limits(max_events) -> None:
    with pytest.raises(ValueError, match="positive integer"):
        EventLogQuery(max_events=max_events)


def test_query_rejects_invalid_source() -> None:
    with pytest.raises(ValueError, match="EventLogSource"):
        EventLogQuery(source="Invalid")