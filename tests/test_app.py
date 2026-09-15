"""Tests for the ArgOS application navigation."""

from unittest.mock import Mock, patch

from argos.app import display_system_information, run_menu


def test_display_system_information_collects_and_renders() -> None:
    information = {"Computer": "TEST-PC"}

    with (
        patch(
            "argos.app.collect_system_information",
            return_value=information,
        ) as collect,
        patch("argos.app.render_system_information") as render,
        patch("argos.app.print_section"),
        patch("argos.app.print_info"),
    ):
        display_system_information()

    collect.assert_called_once_with()
    render.assert_called_once_with(information)


def test_menu_option_one_opens_system_information() -> None:
    read_choice = Mock(side_effect=["1", "0"])

    with (
        patch("argos.app.display_system_information") as display,
        patch("argos.app.clear_console"),
        patch("argos.app.print_banner"),
        patch("argos.app.display_privilege_status"),
        patch("argos.app.display_main_menu"),
        patch("argos.app.wait_for_user") as wait_for_user,
        patch("argos.app.print_muted"),
    ):
        run_menu(read_choice)

    display.assert_called_once_with()
    wait_for_user.assert_called_once_with()
    assert read_choice.call_count == 2
