"""Command-line entry point for ArgOS."""

from __future__ import annotations

from pprint import pprint

from argos.modules.sys_information import collect_system_information


def main() -> None:
    """Collect and display Windows system information."""
    pprint(collect_system_information())
