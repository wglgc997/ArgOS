"""Tests for system-information collection and normalization."""

from typing import Any
from unittest.mock import Mock

import pytest

from argos.core.powershell import PowerShellRunner
from argos.core.powershell_commands import GET_SYSTEM_INFORMATION
from argos.modules.sys_information import (
    REQUIRED_HARDWARE_FIELDS,
    collect_system_information,
    normalize_hardware_information,
)


def test_collect_system_information_uses_injected_runner() -> None:
    expected: dict[str, Any] = {
        "Computer": "TEST-PC",
        "CPU": {"Name": "Test CPU"},
        "Memory": {"TotalGB": 16},
        "Storage": [],
        "GPU": [],
        "BaseBoard": {},
        "BIOS": {},
    }
    runner = Mock(spec=PowerShellRunner)
    runner.run_json.return_value = expected.copy()

    result = collect_system_information(runner)

    runner.run_json.assert_called_once_with(GET_SYSTEM_INFORMATION)
    assert result["Computer"] == "TEST-PC"
    assert result["CPU"] == {"Name": "Test CPU"}


def test_normalize_adds_missing_hardware_fields() -> None:
    result = normalize_hardware_information({"Computer": "TEST-PC"})

    for field in REQUIRED_HARDWARE_FIELDS:
        assert result[field] == "Unavailable"


def test_normalize_preserves_existing_hardware_values() -> None:
    source: dict[str, Any] = {
        field: {"available": True} for field in REQUIRED_HARDWARE_FIELDS
    }

    result = normalize_hardware_information(source.copy())

    assert result == source


def test_collect_rejects_non_dictionary_output() -> None:
    runner = Mock(spec=PowerShellRunner)
    runner.run_json.return_value = ["unexpected"]

    with pytest.raises(
        ValueError,
        match="System information output must be a dictionary",
    ):
        collect_system_information(runner)

@pytest.mark.parametrize("field", REQUIRED_HARDWARE_FIELDS)
def test_normalize_replaces_null_hardware_fields(field: str) -> None:
    result = normalize_hardware_information({field: None})

    assert result[field] == "Unavailable"


def test_normalize_does_not_modify_input() -> None:
    source: dict[str, Any] = {"Computer": "TEST-PC", "CPU": None}

    result = normalize_hardware_information(source)

    assert source == {"Computer": "TEST-PC", "CPU": None}
    assert result is not source
    assert result["CPU"] == "Unavailable"


def test_normalize_preserves_empty_collections_and_zero() -> None:
    source: dict[str, Any] = {
        "Storage": [],
        "GPU": [],
        "Memory": {"FreeGB": 0},
    }

    result = normalize_hardware_information(source)

    assert result["Storage"] == []
    assert result["GPU"] == []
    assert result["Memory"] == {"FreeGB": 0}


def test_collect_normalizes_null_hardware_from_powershell() -> None:
    runner = Mock(spec=PowerShellRunner)
    runner.run_json.return_value = {"Computer": "TEST-PC", "BIOS": None}

    result = collect_system_information(runner)

    assert result["Computer"] == "TEST-PC"
    assert result["BIOS"] == "Unavailable"