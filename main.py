from pprint import pprint

from ArgOS_cli.core.powershell_commands import GET_OPERATING_SYSTEM
from ArgOS_cli.core.powershell import PowerShellError, PowerShellNotFoundError, PowerShellRunner

def main() -> None:
    """Testing here the PS integration"""

    try:
        runner = PowerShellRunner()

        print(f"PowerShell executable: {runner.executable}")
        print("Collecting Windows information... \n")

        os = runner.run_json(GET_OPERATING_SYSTEM)

        pprint(os)

    except PowerShellNotFoundError as error:
        print(f"PowerShell was not found: {error}")

    except PowerShellError as error:
        print(f"PowerShell execution failed?\n{error}")

    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()

