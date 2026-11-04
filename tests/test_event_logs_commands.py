import pytest

from argos.core.powershell_commands import build_event_logs_command
from argos.modules.event_logs import (
    EventLogQuery,
    EventLogSource,
    build_event_query_command,
)


@pytest.mark.parametrize("source", list(EventLogSource))
def test_query_preserves_selected_source(source: EventLogSource) -> None:
    command = build_event_query_command(
        EventLogQuery(source=source, max_events=25)
    )

    assert f"-LogName '{source.value}'" in command
    assert "-MaxEvents 25" in command
    assert "-ErrorAction Stop" in command
    assert "ConvertTo-Json" not in command


def test_command_escapes_apostrophes() -> None:
    command = build_event_logs_command("Example'Log", 10)

    assert "-LogName 'Example''Log'" in command


@pytest.mark.parametrize("log_name", ["", "   "])
def test_command_rejects_blank_log_name(log_name: str) -> None:
    with pytest.raises(ValueError, match="must not be blank"):
        build_event_logs_command(log_name, 10)


@pytest.mark.parametrize("max_events", [0, -1, True])
def test_command_rejects_invalid_limit(max_events: int) -> None:
    with pytest.raises(ValueError, match="positive integer"):
        build_event_logs_command("System", max_events)