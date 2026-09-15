"""Tests for the system-information presentation."""

from copy import deepcopy
from io import StringIO
from typing import Any

import pytest
from rich.console import Console

from argos.ui.system_information import (
    format_uptime,
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


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0, "0d 00h 00m 00s"),
        (59, "0d 00h 00m 59s"),
        (60, "0d 00h 01m 00s"),
        (3600, "0d 01h 00m 00s"),
        (86400, "1d 00h 00m 00s"),
        (90061, "1d 01h 01m 01s"),
        (None, "Unavailable"),
        (-1, "Unavailable"),
        ("90061", "Unavailable"),
        (True, "Unavailable"),
        (1.5, "Unavailable"),
    ],
)
def test_format_uptime(value: Any, expected: str) -> None:
    assert format_uptime(value) == expected


def test_render_uptime_in_overview() -> None:
    stream = StringIO()
    output = Console(file=stream, width=100, color_system=None)

    render_system_information({"UptimeSeconds": 90061}, output)

    rendered = stream.getvalue()
    assert "Uptime" in rendered
    assert "1d 01h 01m 01s" in rendered


def test_render_language_and_environment_information() -> None:
    stream = StringIO()
    output = Console(file=stream, width=100, color_system=None)

    render_system_information(
        {
            "Language": {
                "SystemLocale": "pt-BR",
                "UserCulture": "pt-BR",
                "UserInterfaceCulture": "en-US",
            },
            "Environment": {
                "DomainOrWorkgroup": "TEST-WORKGROUP",
                "PartOfDomain": False,
                "SystemType": "x64-based PC",
            },
        },
        output,
    )

    rendered = stream.getvalue()
    assert "Language" in rendered
    assert "System Locale" in rendered
    assert "pt-BR" in rendered
    assert "User Interface Culture" in rendered
    assert "en-US" in rendered
    assert "Environment" in rendered
    assert "Domain Or Workgroup" in rendered
    assert "TEST-WORKGROUP" in rendered
    assert "Part Of Domain" in rendered
    assert "False" in rendered
    assert "System Type" in rendered
    assert "x64-based PC" in rendered


def test_render_partial_collection_warning() -> None:
    stream = StringIO()
    output = Console(file=stream, width=100, color_system=None)

    render_system_information(
        {
            "Computer": "TEST-PC",
            "CPU": {"Name": "Test CPU"},
            "GPU": "Unavailable",
            "UnavailableSources": ["GPU", "BIOS"],
        },
        output,
    )

    rendered = stream.getvalue()
    assert "TEST-PC" in rendered
    assert "Test CPU" in rendered
    assert "Collection warnings" in rendered
    assert "Unavailable Sources" in rendered
    assert "GPU, BIOS" in rendered
    assert rendered.count("Overview") == 1


def test_render_omits_warning_when_all_sources_are_available() -> None:
    stream = StringIO()
    output = Console(file=stream, width=100, color_system=None)

    render_system_information(
        {"UnavailableSources": []},
        output,
    )

    assert "Collection warnings" not in stream.getvalue()
