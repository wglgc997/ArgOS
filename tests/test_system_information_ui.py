"""Tests for the system-information presentation."""

from copy import deepcopy
from io import StringIO
from typing import Any

import pytest
from rich.console import Console

from argos.ui.system_information import (
    format_value,
    render_system_information,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, "Unavailable"),
        ("", "Unavailable"),
        (0, "0"),
        ("/Date(0)/", "1970-01-01 00:00:00 UTC"),
        ("/Date(0-0300)/", "1970-01-01 00:00:00 UTC"),
        ("/Date(invalid)/", "/Date(invalid)/"),
    ],
)
def test_format_value(value: Any, expected: str) -> None:
    assert format_value(value) == expected


def test_render_single_disk_and_multiple_gpus() -> None:
    information: dict[str, Any] = {
        "Computer": "[TEST-PC]",
        "Storage": {"Drive": "C:", "FreeGB": 0},
        "GPU": [{"Name": "Intel Graphics"}, {"Name": "NVIDIA Graphics"}],
        "WindowsVersion": {"InstallDate": "/Date(0)/"},
    }
    original = deepcopy(information)
    stream = StringIO()
    output = Console(file=stream, width=100, color_system=None)

    render_system_information(information, output)

    rendered = stream.getvalue()
    assert "[TEST-PC]" in rendered
    assert "C:" in rendered
    assert "Free GB" in rendered
    assert "GPU 1" in rendered
    assert "GPU 2" in rendered
    assert "Intel Graphics" in rendered
    assert "NVIDIA Graphics" in rendered
    assert "1970-01-01 00:00:00 UTC" in rendered
    assert information == original


def test_render_multiple_disks() -> None:
    stream = StringIO()
    output = Console(file=stream, width=100, color_system=None)

    render_system_information(
        {"Storage": [{"Drive": "C:"}, {"Drive": "D:"}]},
        output,
    )

    rendered = stream.getvalue()
    assert "Storage 1" in rendered
    assert "Storage 2" in rendered
    assert "C:" in rendered
    assert "D:" in rendered


@pytest.mark.parametrize("value", [None, [], {}, "Unavailable"])
def test_render_unavailable_hardware(value: Any) -> None:
    stream = StringIO()
    output = Console(file=stream, width=100, color_system=None)

    render_system_information({"GPU": value}, output)

    rendered = stream.getvalue()
    assert "GPU" in rendered
    assert "Unavailable" in rendered