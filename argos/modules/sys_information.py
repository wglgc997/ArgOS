"""System information collection module

This module collects Windows sys info via PS.
"""

from __future__ import annotations

from typing import Any

from argos.core.powershell import PowerShellRunner
from argos.core.powershell_commands import GET_SYSTEM_INFORMATION


REQUIRED_HARDWARE_FIELDS = (
    "CPU",
    "Memory",
    "Storage",
    "GPU",
    "BaseBoard",
    "BIOS",
)
def collect_system_information (
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

    #Execute the PS command and parse the JSON output
    result = ps_runner.run_json(GET_SYSTEM_INFORMATION)

    if not isinstance(result, dict):
        raise ValueError("System information output must be a dictionary.")

    return normalize_hardware_information(result)

def normalize_hardware_information(
        system_info: dict[str, Any],
) -> dict[str, Any]:
    """
    Ensure hardware fields are always present.

        Args:
            system_info:
                Raw system information collected from PowerShell.

    Returns:
            System information with normalized hardware fields.
        """

    # Add missing hardware fields with an unavailable value
    for field in REQUIRED_HARDWARE_FIELDS:
        system_info.setdefault(field, "Unavailable")

        return system_info