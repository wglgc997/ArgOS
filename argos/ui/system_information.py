"""Rich presentation for collected system information."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from argos.ui.console import console


def format_uptime(value: Any) -> str:
    """Format a non-negative integer duration in seconds."""
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return "Unavailable"

    days, remainder = divmod(value, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{days}d {hours:02d}h {minutes:02d}m {seconds:02d}s"

def format_value(value: Any) -> str:
    """Format values without changing the collected data."""
    if value is None or value == "":
        return "Unavailable"

    if isinstance(value, str):
        match = re.fullmatch(r"/Date\((-?\d+)(?:[+-]\d{4})?\)/", value)
        if match:
            try:
                timestamp = int(match.group(1)) / 1000
                date = datetime.fromtimestamp(timestamp, tz=UTC)
                return date.strftime("%Y-%m-%d %H:%M:%S UTC")
            except (OverflowError, OSError, ValueError):
                return "Unavailable"

    if isinstance(value, list):
        return ", ".join(format_value(item) for item in value) or "Unavailable"

    return str(value)

def render_section(title: str, value: Any, output: Console) -> None:
    """Render a section, supporting one or multiple devices."""
    if isinstance(value, list) and value:
        for index, item in enumerate(value, start=1):
            render_section(f"{title} {index}", item, output)
        return

    table = Table(
        show_header=False,
        expand=True,
        border_style="cyan",
    )
    table.add_column("Field", style="green", ratio=1)
    table.add_column("Value", ratio=3)

    if isinstance(value, dict) and value:
        for field, item in value.items():
            label = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", str(field))
            table.add_row(Text(label), Text(format_value(item)))
    else:
        status = format_value(value) if value else "Unavailable"
        table.add_row(Text("Status"), Text(status))

    output.print(Panel(table, title=Text(title), border_style="cyan"))

def render_system_information(
        information: dict[str, Any],
        output: Console = console,
) -> None:
    """Render an inventory using the shared console or a test console."""
    overview = {
        "Computer": information.get("Computer"),
        "Current user": information.get("LocalUser"),
        "Architecture": information.get("Architecture"),
        "PowerShell": information.get("PowerShell"),
        "Uptime": format_uptime(information.get("UptimeSeconds"))
    }
    render_section("Overview", overview, output)

    sections = (
        ("WindowsVersion", "Windows"),
        ("Timezone", "Timezone"),
        ("CPU", "CPU"),
        ("Memory", "Memory"),
        ("Storage", "Storage"),
        ("GPU", "GPU"),
        ("BaseBoard", "Motherboard"),
        ("BIOS", "BIOS"),
    )

    for key, title in sections:
        render_section(title, information.get(key), output)