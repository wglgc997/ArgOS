"""
Utility responsible for executing PowerShell commands.

This module centralizes all interactions with PowerShell so the rest of
the application never calls subprocess directly.
"""

from __future__ import  annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from typing import Any



class PowerShellError(RuntimeError):
    """Raised when a PowerShell command fails."""


class PowerShellNotFoundError(FileNotFoundError):
    """Raised when PowerShell is not installed or cannot be found."""

@dataclass(slots=True)
class PowerShellResult:
    """Represent the execution result of a PowerShell command."""

    command: str
    stdout: str
    stderr: str
    return_code: int

    @property
    def succeeded(self) -> bool:
        """Return True when the command executed successfully"""
        return self.return_code == 0


class PowerShellRunner:
    """
    Execute PowerShell commands.

    This class should be the only place in the project
    responsible for launching PS processes.
    """

    def __init__(
            self,
            executable: str | None = None,
            timeout: int = 60,
    ) -> None:
        """
        Initialize the PowerShell runner.

            Args:
                executable:
                    PowerShell executable.
                    Defaults to pwsh if installed,
                    otherwise falls back to powershell.exe.

            timeout:
                    Maximum execution time in seconds.
        """

        self.timeout = timeout

        if executable:
            self.executable = executable
        else:
            self.executable = self.detect_executable()

    @staticmethod
    def _detect_executable() -> str:
        """
        Detect the available PowerShell executable.

            Preference:
                1. pwsh (PowerShell 7)
                2. powershell.exe (Windows PowerShell)
        """

        if shutil.which("pwsh"):
            return "pwsh"
        if shutil.which("powershell"):
            return "powershell"
        raise PowerShellNotFoundError(
            "PowerShell executable was not found."
        )

    def run(
            self,
            command: str,
            *,
            check: bool = True,
    ) -> PowerShellResult:
        """
        Execute a PowerShell command.

            Args:
            command:
                PowerShell command.

            check:
                Raise an exception if the command fails.

            Returns:
                Execution result.
        """

        completed = subprocess.run(
            [
                self.executable,
                "-NoLogo",
                "_NoProfile",
                "-NonInteractive",
                "_ExecutionPolicy",
                "Bypass",
                "_Command",
                command,
            ],
            capture_output=True,
            text=True,
            timeout=self.timeout,
        )

        result = PowerShellResult(
            command=command,
            stdout=completed.stdout.strip(),
            stderr=completed.stderr.strip(),
            return_code=completed.returncode,
        )

        if check and not result.succeeded:
            raise PowerShellError(
                f"PowerShell command failed.\n"
                f"Command: {command}\n"
                f"Exit code: {result.return_code}\n"
                f"Error: {result.stderr}"
            )
        return result

    def run_json(
            self,
            command: str,
    ) -> dict[str, Any] | list[Any]:
        """
        Execute a command and parse JSON output.

        The caller should NOT append ConvertTo-Json.
        This method does it automatically.

        Args:
            command:
                PowerShell command.

            Returns:
                Parsed JSON object.
        """

        json_command = (
            f"{command} | ConvertTo-Json -Depth 10 -Compress"
        )

        result = self.run(json_command)

        if not result.stdout:
            return {}

        return json.loads(result.stdout)

    def run_line(
            self,
            command: str,
    ) -> list[str]:
        """
        Execute a command and return output lines.
        """

        result = self.run(command)

        return[
            line
            for line in result.stdout.splitlines()
            if line.strip()
        ]

    def exists(
            self,
            command: str,
    ) -> bool:
        """
        Check whether a command executes successfully.
        """
        try:
            self.run(command)
            return True
        except PowerShellError:
            return False
