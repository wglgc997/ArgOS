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
    """Display the ArgOS application banner."""
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
            padding=(1, 4),
            expand=False,
        )
    )


def print_success(message: str) -> None:
    """Display a successful operation."""
    console.print(f"[success][OK] {message}[/success]")


def print_warning(message: str) -> None:
    """Display a warning."""
    console.print(f"[warning][WARNING] {message}[/warning]")


def print_error(message: str) -> None:
    """Display an error."""
    console.print(f"[error][ERROR] {message}[/error]")


def print_critical(message: str) -> None:
    """Display a critical error."""
    console.print(f"[critical] CRITICAL [/critical] [error]{message}[/error]")


def print_info(message: str) -> None:
    """Display informational output."""
    console.print(f"[info][INFO] {message}[/info]")


def print_muted(message: str) -> None:
    """Display secondary information."""
    console.print(f"[muted]{message}[/muted]")


def print_section(title: str) -> None:
    """Display a section separator."""
    console.rule(f"[title]{title}[/title]", style="cyan")


def clear_console() -> None:
    """Clear the terminal."""
    console.clear()


def wait_for_user(message: str = "Press Enter to continue...") -> None:
    """Pause until the user presses Enter."""
    console.input(f"[muted]{message}[/muted]")


def read_menu_choice(prompt: str = "Select an option") -> str:
    """Read and normalize a menu selection."""
    return console.input(f"[menu.number]{prompt}: [/menu.number]").strip()
