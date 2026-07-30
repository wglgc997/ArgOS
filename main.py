from pprint import pprint

from ArgOS_cli.core.powershell_commands import GET_OPERATING_SYSTEM
from ArgOS_cli.core.powershell import PowerShellError, PowerShellNotFoundError, PowerShellRunner

# def main() -> None:
#     """Testing here the PS integration"""
#
#     try:
#         runner = PowerShellRunner()
#
#         print(f"PowerShell executable: {runner.executable}")
#         print("Collecting Windows information... \n")
#
#         os = runner.run_json(GET_OPERATING_SYSTEM)
#
#         pprint(os)
#
#     except PowerShellNotFoundError as error:
#         print(f"PowerShell was not found: {error}")
#
#     except PowerShellError as error:
#         print(f"PowerShell execution failed?\n{error}")
#
#     except Exception as error:
#         print(f"Unexpected error: {error}")
#
#
# if __name__ == "__main__":
#     main()


from ui import (
    print_banner,
    print_critical,
    print_error,
    print_info,
    print_muted,
    print_section,
    print_success,
    print_warning,
    wait_for_user,
)


def main() -> None:
    """Test the SentinelCLI Rich console."""

    print_banner()

    print_section("Console test")

    print_success("PowerShell was detected successfully.")
    print_info("Operating system: Windows 11 Enterprise")
    print_warning("The application is not running as administrator.")
    print_error("Unable to access the Security event log.")
    print_critical("Windows Defender real-time protection is disabled.")
    print_muted("ArgOS version 0.1.0")

    wait_for_user()


if __name__ == "__main__":
    main()