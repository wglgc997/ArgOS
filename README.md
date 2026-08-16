# ArgOS

> A Python toolkit for Windows administration, diagnostics, and security investigation.

## Technologies & Tools

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![PowerShell](https://img.shields.io/badge/PowerShell-7%2B-5391FE?logo=powershell&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-10%20%7C%2011-0078D4?logo=windows&logoColor=white)
![Rich](https://img.shields.io/badge/CLI-Rich-E85D04)
![Pytest](https://img.shields.io/badge/Tests-pytest-0A9EDC?logo=pytest&logoColor=white)
![Ruff](https://img.shields.io/badge/Lint-Ruff-D7FF64?logo=ruff&logoColor=black)
![mypy](https://img.shields.io/badge/Types-mypy-2A6DB2)

- **Core:** Python 3.11+, PowerShell
- **Interface:** Rich, Questionary
- **System integration:** psutil, pywin32
- **Templates:** Jinja2
- **Quality:** pytest, Ruff, mypy

ArgOS collects structured information from a Windows computer through a centralized PowerShell integration. The project is being built as a modular command-line application that brings system inventory, troubleshooting, and local security checks into one consistent interface.

> [!IMPORTANT]
> ArgOS is under active development. The system-information collector and core PowerShell layer are available now; most other modules described below are planned.

## Why ArgOS?

Windows investigation often means jumping between commands, management consoles, and scripts. ArgOS aims to provide a single, reusable toolkit with:

- structured results instead of unprocessed command output;
- centralized and testable PowerShell execution;
- a consistent terminal experience powered by Rich;
- reusable modules for administration and investigation;
- exportable findings and reports.

## Current capabilities

The current implementation can collect and normalize:

- computer name and current user;
- Windows edition, version, build, architecture, and boot time;
- CPU and physical memory details;
- fixed-disk capacity and free space;
- GPU, motherboard, and BIOS information;
- timezone and PowerShell version.

ArgOS automatically prefers PowerShell 7 (`pwsh`) and falls back to Windows PowerShell when necessary. PowerShell results are converted to JSON and returned to Python as structured data.

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer
- PowerShell 7 or Windows PowerShell 5.1

Some future checks, including Security event logs, Defender, firewall, BitLocker, and service administration, may require an elevated terminal.

## Quick start

Clone the repository and enter the project directory:

```powershell
git clone https://github.com/wglgc997/Windows-Log-Script.git ArgOS
cd ArgOS
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies and run ArgOS:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

The current entry point prints the collected system information as a Python dictionary. A complete interactive CLI and formatted Rich views are part of the ongoing work.

## Example output

Values vary by computer, but the collected data follows this shape:

```python
{
    "Computer": "WORKSTATION-01",
    "WindowsVersion": {
        "Name": "Microsoft Windows 11 Enterprise",
        "Version": "10.0.26100",
        "Build": "26100",
    },
    "Architecture": "64-bit",
    "CPU": {
        "Name": "Processor model",
        "Cores": 8,
        "LogicalProcessors": 16,
    },
    "Memory": {"TotalGB": 32.0, "FreeGB": 18.4},
    "Storage": [...],
    "GPU": [...],
    "BaseBoard": {...},
    "BIOS": {...},
    "PowerShell": "7.5.0",
}
```

## Project structure

```text
ArgOS/
|-- argos/
|   |-- core/                 # PowerShell runner and reusable commands
|   |-- modules/              # Administration and investigation modules
|   |-- ui/                   # Rich console helpers and visual theme
|   `-- app.py                # Application layer (in development)
|-- docs/
|   `-- epics.md              # Detailed roadmap and project progress
|-- main.py                   # Current development entry point
`-- requirements.txt          # Runtime and development dependencies
```

## Roadmap

| Area | Status |
| --- | --- |
| Core PowerShell integration | Implemented |
| System information | In progress |
| Windows Event Logs | Prototype / refactor planned |
| Processes and services | Planned |
| Network diagnostics | Planned |
| Local security audit | Planned |
| Hardware and firmware | Planned |
| Hash and password utilities | Planned |
| JSON, CSV, TXT, and HTML reports | Planned |
| Packaging, tests, and CI/CD | Planned |

See [Project Epics](docs/epics.md) for the detailed scope and milestones.

## Safety and scope

ArgOS is an administration and investigation aid. It is not an antivirus, EDR platform, or replacement for professional incident-response tooling.

Read-only collection is preferred by design. Features that change system state, such as terminating processes or controlling services, are planned to require explicit confirmation. Review commands before using the project on production systems.

## Contributing

Contributions, bug reports, and suggestions are welcome. To contribute:

1. Fork the repository and create a focused branch.
2. Keep PowerShell execution inside `argos/core/powershell.py` and reusable commands inside `argos/core/powershell_commands.py`.
3. Add or update tests for behavioral changes.
4. Run the quality checks before opening a pull request:

```powershell
pytest
ruff check .
mypy argos
```

If you are proposing a larger feature, open an issue first so its scope can be aligned with the roadmap.

## Project status

ArgOS is currently a pre-release project. Interfaces, output structures, and installation steps may change while the CLI foundation and first modules are completed.
