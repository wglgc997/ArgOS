"""System information collection module

This module collects Windows sys info via PS.
"""

from __future__ import annotations

from typing import Any

from argos.core.powershell import PowerShellRunner
from argos.core.powershell_commands import GET_SYSTEM_INFORMATION



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

    return result