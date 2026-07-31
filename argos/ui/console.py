"""
Console utilities used by ArgOS.

This module provides a single Rich Console instance and helper functions
for displaying messages consistently throughout the application.
"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from argos.ui.theme import SENTINEL_THEME

console = Console(
    theme=SENTINEL_THEME,
    highlight=False,
)

def print_banner() -> None:
    """Display the ArgOS app banner"""

    title = Text()
    title.append("ARGOS CLI\n", style="title")
    title.append(
        "Windows Administration & Security Investigation",
        style="subtitle",
    )

    console.print(
        Panel(
            title,
            border_style="cyan",
            padding=(1,4),
            expand=False,
        )
    )

def print_success(message: str) -> None:
    """Display a successful operation message"""

    console.print(f"[success]✓ {message}[/success]")

def print_warning(message: str) -> None:
    """Display a warning message."""

    console.print(f"[warning]⚠ {message}[/warning]")


def print_error(message: str) -> None:
    """Display an error message."""

    console.print(f"[error]✗ {message}[/error]")


def print_critical(message: str) -> None:
    """Display a critical error message."""

    console.print(f"[critical] CRITICAL [/critical] [error]{message}[/error]")


def print_info(message: str) -> None:
    """Display an informational message."""

    console.print(f"[info]ℹ {message}[/info]")


def print_muted(message: str) -> None:
    """Display secondary or less important information."""

    console.print(f"[muted]{message}[/muted]")


def print_section(title: str) -> None:
    """Display a section separator."""

    console.rule(
        f"[title]{title}[/title]",
        style="cyan",
    )

def clear_console() -> None:
    """Clear the terminal screen"""

    console.clear()

def wait_for_user(message: str = "Press Enter to continue ...") -> None:
    """Pause the execution until the user press Enter"""

    console.input(f"[muted]{message}[/muted]")

