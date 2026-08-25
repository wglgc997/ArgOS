"""Tests for the centralized PowerShell runner. """

import json
import subprocess
from unittest.mock import patch

import pytest

from argos.core.powershell import (
    PowerShellError,
    PowerShellNotFoundError,
    PowerShellRunner,
)


def test_detect_executable_prefers_pwsh() -> None:
    with patch("argos.core.powershell.shutil.which") as which:
        which.side_effect = lambda name: (
            "C:\\Program Files\\PowerShell\\7\\pwsh.exe"
            if name == "pwsh"
            else None
        )

        assert PowerShellRunner._detect_executable() == "pwsh"


def test_detect_executable_falls_back_to_windows_powershell() -> None:
    with patch("argos.core.powershell.shutil.which") as which:
        which.side_effect = lambda name: (
            "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
            if name == "powershell"
            else None
        )

        assert PowerShellRunner._detect_executable() == "powershell"


def test_detect_executable_raises_when_powershell_is_missing() -> None:
    with (
        patch("argos.core.powershell.shutil.which", return_value=None),
        pytest.raises(PowerShellNotFoundError),
    ):
        PowerShellRunner._detect_executable()


def test_run_builds_noninteractive_command() -> None:
    completed = subprocess.CompletedProcess(
        args=[],
        returncode=0,
        stdout="value\n",
        stderr="",
    )

    with patch("argos.core.powershell.subprocess.run", return_value=completed) as run:
        result = PowerShellRunner(executable="pwsh").run("Write-Output value")

    assert result.stdout == "value"
    assert result.succeeded is True
    run.assert_called_once_with(
        [
            "pwsh",
            "-NoLogo",
            "-NoProfile",
            "-NonInteractive",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            "Write-Output value",
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_run_raises_for_failed_command() -> None:
    completed = subprocess.CompletedProcess(
        args=[],
        returncode=1,
        stdout="",
        stderr="failure",
    )

    with (
        patch("argos.core.powershell.subprocess.run", return_value=completed),
        pytest.raises(PowerShellError, match="failure"),
    ):
        PowerShellRunner(executable="pwsh").run("Broken-Command")


def test_run_json_parses_structured_output() -> None:
    payload = {"Computer": "TEST-PC"}

    with patch.object(
        PowerShellRunner,
        "run",
        return_value=type(
            "Result",
            (),
            {
                "stdout": json.dumps(payload),
            },
        )(),
    ):
        result = PowerShellRunner(executable="pwsh").run_json("Get-TestData")

    assert result == payload