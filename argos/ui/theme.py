"""
ArgOS visual theme.

Centralize the colors and styles used by the CMD interface.
"""

from rich.theme import Theme

SENTINEL_THEME = Theme(
    {
        # General statuses
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "critical": "bold white on red",
        "info": "bold cyan",
        "muted": "dim white",
        # Application elements
        "title": "bold cyan",
        "subtitle": "cyan",
        "menu.number": "bold cyan",
        "menu.option": "white",
        "menu.exit": "bold red",
        # System statuses
        "status.enabled": "bold green",
        "status.disabled": "bold red",
        "status.unknown": "bold yellow",
        # Event log levels
        "event.information": "green",
        "event.success": "green",
        "event.warning": "yellow",
        "event.error": "red",
        "event.critical": "bold white on red",
        "event.failure": "bold red",
        # Tables
        "table.header": "bold cyan",
        "table.border": "cyan",
    }
)
