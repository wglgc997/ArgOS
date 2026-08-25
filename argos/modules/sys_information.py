"""System information collection module

This module collects Windows sys info via PS.
"""

from __future__ import annotations

import re
from copy import deepcopy
from datetime import UTC, datetime
from typing import Any

from argos.core.powershell import PowerShellRunner
from argos.core.powershell_commands import GET_SYSTEM_INFORMATION

UNAVAILABLE = "Unavailable"

POWERSHELL_DATE_PATTERN = re.compile(
    r"^/Date\((?P<milliseconds>-?\d+)(?:[+-]\d{4})?\)/$"
)

SCALAR_FIELDS = ("Computer", "WindowsBuild", "Architecture", "LocalUser", "PowerShell")

STRUCTURED_FIELDS = {
    "WindowsVersion": (
        "Name",
        "Version",
        "Build",
        "InstallDate",
        "LastBootUpTime",
    ),
    "CPU": (
        "Name",
        "Manufacturer",
        "Cores",
        "LogicalProcessors",
        "MaxClockSpeedMHz",
    ),
    "Timezone": (
        "Id",
        "DisplayName",
        "StandardName",
    ),
    "Memory": (
        "TotalGB",
        "FreeGB",
    ),
    "BaseBoard": (
        "Manufacturer",
        "Product",
        "SerialNumber",
    ),
    "BIOS": ("Manufacturer", "Version", "SerialNumber", "ReleaseDate"),
}

COLLECTION_FIELDS = {
    "Storage": (
        "Drive",
        "FileSystem",
        "VolumeName",
        "TotalGB",
        "FreeGB",
    ),
    "GPU": (
        "Name",
        "DriverVersion",
        "VideoProcessor",
        "AdapterRAMGB",
    ),
}


def collect_system_information(
    runner: PowerShellRunner | None = None,
) -> dict[str, Any]:
    """
    Collect Windows system information.

    Args:
        runner:
            Optional PowerShell runner used to execute commands.

    Returns:
        Dictionary containing system information.
    """

    # Reuse an existing runner or create a new one
    ps_runner = runner or PowerShellRunner()

    # Execute the PowerShell command and parse the JSON output
    result = ps_runner.run_json(GET_SYSTEM_INFORMATION)

    if not isinstance(result, dict):
        raise ValueError("System information output must be a dictionary.")

    return normalize_hardware_information(result)


def normalize_timestamp(value: Any) -> str:
    """Convert a PowerShell or ISO-8601 timestamp to UTC ISO 8601."""

    if not isinstance(value, str) or value == UNAVAILABLE:
        return UNAVAILABLE

    powershell_match = POWERSHELL_DATE_PATTERN.fullmatch(value)

    if powershell_match:
        try:
            milliseconds = int(powershell_match.group("milliseconds"))
            parsed = datetime.fromtimestamp(
                milliseconds / 1000,
                tz=UTC,
            )
        except (OSError, OverflowError, ValueError):
            return UNAVAILABLE
    else:
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return UNAVAILABLE

        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        else:
            parsed = parsed.astimezone(UTC)

    return parsed.isoformat().replace("+00:00", "Z")


def value_or_unavailable(value: Any) -> Any:
    """Replace missing and blank values with the unavailable marker."""
    if value is None or value == "":
        return UNAVAILABLE

    return value


def normalize_mapping(
    value: Any,
    expected_fields: tuple[str, ...],
) -> dict[str, Any]:
    """Normalize one structured system-info section."""
    source = value if isinstance(value, dict) else {}

    return {field: value_or_unavailable(source.get(field)) for field in expected_fields}


def normalize_collection(
    value: Any,
    expected_fields: tuple[str, ...],
) -> list[dict[str, Any]]:
    """Normalize a PowerShell singleton or array into a list."""
    if value is None or value == UNAVAILABLE:
        return []

    items = value if isinstance(value, list) else [value]

    return [normalize_mapping(item, expected_fields) for item in items]


def normalize_hardware_information(
    system_info: dict[str, Any],
) -> dict[str, Any]:
    """
    Return system information using a stable data structure.

    Args:
        system_info:
            Raw system information collected from PowerShell.

    Returns:
        A normalized copy of the collected system information.
    """

    normalized = deepcopy(system_info)

    for field in SCALAR_FIELDS:
        normalized[field] = value_or_unavailable(normalized.get(field))

    for field, expected_fields in STRUCTURED_FIELDS.items():
        normalized[field] = normalize_mapping(
            normalized.get(field),
            expected_fields,
        )

    for field, expected_fields in COLLECTION_FIELDS.items():
        normalized[field] = normalize_collection(
            normalized.get(field),
            expected_fields,
        )

    windows_version = normalized["WindowsVersion"]
    windows_version["InstallDate"] = normalize_timestamp(windows_version["InstallDate"])
    windows_version["LastBootUpTime"] = normalize_timestamp(
        windows_version["LastBootUpTime"]
    )
    bios = normalized["BIOS"]
    bios["ReleaseDate"] = normalize_timestamp(bios["ReleaseDate"])
    return normalized
