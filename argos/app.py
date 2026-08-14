"""Command-line entry point for ArgOS."""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from argos.config import APP_NAME, APP_VERSION, load_config
from argos.core.powershell import PowerShellError, PowerShellNotFoundError
from argos.core.privileges import is_administrator
from argos.exceptions import ArgOSError
from argos.logging_config import configure_logging
from argos.modules.sys_information import collect_system_information
from argos.ui import (
    clear_console,
    console,
    print_banner,
    print_error,
    print_info,
    print_muted,
    print_section,
    print_success,
    print_warning,
    read_menu_choice,
    wait_for_user,
)

logger = logging.getLogger("argos.app")


def display_privilege_status() -> None:
    """Display the current process privilege level."""
    if is_administrator():
        print_success("Administrator level : ON")
    else:
        print_warning("Administrator level : OFF \nSome operations may be unavailable.")


def display_main_menu() -> None:
    """Render the interactive main menu."""
    print_section("Main Menu")
    console.print("[menu.number]1.[/menu.number] System information")
    console.print("[menu.number]0.[/menu.number] [menu.exit]Exit[/menu.exit]")


def display_system_information() -> None:
    """Collect and render system information."""
    print_section("System Information")
    print_info("Collecting system information...")

    information = collect_system_information()
    console.print_json(data=information)


def run_menu(
    read_choice: Callable[[], str] = read_menu_choice,
) -> None:
    """Run the interactive application menu."""
    actions: dict[str, Callable[[], Any]] = {
        "1": display_system_information,
    }

    while True:
        clear_console()
        print_banner()
        display_privilege_status()
        display_main_menu()

        choice = read_choice()

        if choice == "0":
            print_muted("Goodbye.")
            return

        action = actions.get(choice)
        if action is None:
            print_warning("Invalid option. Select one of the choices.")
            wait_for_user()
            continue

        try:
            action()
        except PowerShellNotFoundError:
            logger.exception("PowerShell was not found")
            print_error("PowerShell could not be found on this computer.")
        except PowerShellError as error:
            logger.exception("PowerShell execution failed")
            print_error(str(error))
        except ArgOSError as error:
            logger.exception("ArgOS operation failed")
            print_error(str(error))
        except Exception:
            logger.exception("Unexpected application error")
            print_error(
                "An unexpected error occurred. See the ArgOS log for technical details."
            )

        wait_for_user()


def main() -> None:
    """Configure and start ArgOS."""
    config = load_config()
    application_logger = configure_logging(config)

    application_logger.info(
        "%s %s starting; administrator=%s",
        APP_NAME,
        APP_VERSION,
        is_administrator(),
    )

    try:
        run_menu()
    except (KeyboardInterrupt, EOFError):
        application_logger.info("Application interrupted by user")
        console.print()
        print_muted("ArgOS closed.")
