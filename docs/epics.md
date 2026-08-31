# ArgOS — Project Epics

> Product roadmap for a Windows administration, diagnostics, and security investigation toolkit.

ArgOS is evolving from the original **Windows-Log-Script** prototype into a modular Python CLI. The intended architecture combines structured PowerShell collection, reusable domain models, a Rich-based interface, internal logging, and focused Windows administration modules.

> [!NOTE]
> **Platform scope:** Windows only. This document describes both implemented work and the planned product direction; it is not a list of currently available features.

## Progress at a glance

| Epic | Area |     Status     | Target outcome |
| :--- | :--- |:--------------:| :--- |
| [EP-01](#ep-01--foundation) | Foundation | 🟢 Implemented | Stable application architecture |
| [EP-02](#ep-02--system-information) | System information | 🟡 In progress | Consolidated Windows inventory |
| [EP-03](#ep-03--windows-event-logs) | Windows Event Logs |  🟠 Prototype  | Searchable, exportable event analysis |
| [EP-04](#ep-04--processes-and-services) | Processes and services |   ⚪ Planned   | Local workload inspection and control |
| [EP-05](#ep-05--network-diagnostics) | Network diagnostics |   ⚪ Planned   | Network troubleshooting workspace |
| [EP-06](#ep-06--security-audit) | Security audit |   ⚪ Planned   | Local security posture findings |
| [EP-07](#ep-07--hardware-and-firmware) | Hardware and firmware |   ⚪ Planned   | Detailed device inventory |
| [EP-08](#ep-08--utilities) | Utilities |   ⚪ Planned   | Hash, integrity, and password tools |
| [EP-09](#ep-09--reports) | Reports |   ⚪ Planned   | Reusable investigation reports |
| [EP-10](#ep-10--quality-packaging-and-release) | Quality and release |   ⚪ Planned   | Tested, installable releases |
| [EP-11](#ep-11--interactive-cli-experience) | CLI experience |   ⚪ Future    | Polished interactive workflows |

### Status legend

| Symbol | Meaning |
| :---: | :--- |
| 🟢 | Implemented |
| 🟡 | In progress |
| 🟠 | Prototype exists; integration is pending |
| ⚪ | Planned or future work |

## Delivery path

```text
Foundation → System Information → Event Logs → Core Admin Modules
                                                 ├─ Processes & Services
                                                 ├─ Network Diagnostics
                                                 ├─ Security Audit
                                                 └─ Hardware & Firmware
                                                            ↓
                                              Utilities → Reports → Release
```

---

## EP-01 — Foundation

**Status:** 🟢 Implemented
**Objective:** Build the shared architecture required by every ArgOS module.

### Available now

- [x] `argos` Python package structure
- [x] Centralized PowerShell process runner
- [x] Automatic PowerShell 7 / Windows PowerShell detection
- [x] JSON and line-based PowerShell result handling
- [x] Centralized reusable PowerShell command definitions
- [x] Shared Rich console and visual theme helpers
- [x] Initial dependency list
- [x] Complete the application entry point and interactive main menu
- [x] Detect and expose Windows administrator privileges
- [x] Add shared `Finding` and `Severity` models
- [x] Configure internal application logging
- [x] Define configuration and error-handling conventions
- [x] Complete packaging metadata in `pyproject.toml`



### Current architecture

```text
argos/
├── core/
│   ├── powershell.py
│   ├── powershell_commands.py
│   └── privileges.py
├── models/
│   ├── __init__.py
│   └── finding.py
├── modules/
│   └── sys_information.py
├── ui/
│   ├── console.py
│   └── theme.py
├── __init__.py
├── __main__.py
├── app.py
├── config.py
├── exceptions.py
└── logging_config.py
```

**Exit criteria:** ArgOS starts through a stable CLI entry point, provides shared logging and models, detects privilege level, and exposes consistent navigation and error handling.

---

## EP-02 — System Information

**Status:** 🟡 In progress — current milestone  
**Objective:** Provide a consolidated, structured view of the local Windows environment.

### Implemented collection

- [x] Computer name and current user
- [x] Windows edition, version, build, architecture, installation date, and boot time
- [x] CPU model, manufacturer, cores, threads, and maximum clock speed
- [x] Total and free physical memory
- [x] Fixed-disk capacity and free space
- [x] GPU, motherboard, and BIOS details
- [x] Timezone and PowerShell version
- [x] Normalization of required hardware fields
- [x] Calculate and present system uptime

### Remaining work


- [ ] Add system language and environment information
- [ ] Render results through Rich panels and tables
- [ ] Add graceful partial-failure handling
- [ ] Add unit tests with mocked PowerShell results
- [ ] Connect the collector to the final CLI navigation

**Technical direction:** Use CIM/PowerShell and Python system APIs through `PowerShellRunner`; avoid scattered or duplicated subprocess calls.

**Exit criteria:** Users can open the system-information module from the CLI and receive a readable, tested overview even when individual data sources are unavailable.

---

## EP-03 — Windows Event Logs

**Status:** 🟠 Prototype exists; architectural refactor pending  
**Objective:** Rebuild and expand the event-log functionality that originated the project.

### Prototype evidence

- [x] Read the Windows System event log
- [x] Export collected events to a text file
- [x] Process collections exceeding 50,000 System events

### Planned sources

- [ ] System, Application, Security, and Setup
- [ ] Microsoft Defender
- [ ] PowerShell
- [ ] Task Scheduler

### Planned analysis and export

- [ ] Limit returned events
- [ ] Filter by event ID, severity, source, and date
- [ ] Search event messages
- [ ] Display results in Rich tables
- [ ] Export TXT, JSON, and CSV
- [ ] Apply consistent severity visualization

| Severity | Visual treatment |
| :--- | :--- |
| Information / success | 🟢 Green |
| Warning | 🟡 Yellow |
| Error / critical / failure | 🔴 Red |

**Exit criteria:** Users can select a log, constrain a query, inspect results safely, and export the same normalized records in supported formats.

---

## EP-04 — Processes and Services

**Status:** ⚪ Planned  
**Objective:** Inspect and administer local Windows processes and services.

| Processes | Services |
| :--- | :--- |
| List and search by name or PID | List and search services |
| PID and parent PID | Running, stopped, and disabled states |
| CPU and memory usage | Startup mode and process ID |
| Owner, executable path, and start time | Start, stop, and restart |
| Terminate with confirmation | Confirm every state-changing action |

> [!CAUTION]
> Administrative or destructive actions must require explicit confirmation and clearly identify their target.

**Exit criteria:** Inspection works without elevation where Windows permits it, while every state-changing operation is deliberate, confirmed, and clearly reported.

---

## EP-05 — Network Diagnostics

**Status:** ⚪ Planned  
**Objective:** Provide a focused workspace for Windows network troubleshooting and investigation.

### Inventory

- Interfaces, IPv4/IPv6 addresses, MAC addresses, and link state
- Default gateway, DNS configuration, proxy configuration, and network profile
- Routing table, ARP table, and firewall status

### Connections

- Active TCP connections and UDP endpoints
- Listening ports
- Owning process correlation

### Diagnostics

- Ping, DNS lookup, TCP port test, and traceroute

**Exit criteria:** Users can move from local configuration to connection ownership and active diagnostics without leaving ArgOS.

---

## EP-06 — Security Audit

**Status:** ⚪ Planned  
**Objective:** Assess the local Windows security posture and produce actionable findings.

ArgOS will report administrative and security observations; it will not present itself as antivirus or EDR software.

### Planned checks

| Protection | Identity and access | Exposure and activity |
| :--- | :--- | :--- |
| Microsoft Defender and signatures | Local users and disabled accounts | Listening ports and network shares |
| Real-time protection | Local Administrators group | Open sessions |
| Windows Firewall profiles | Basic password policy | Authentication events and failed logins |
| BitLocker, Secure Boot, TPM, and UAC | Administrator privilege status | Windows Update status |

### Finding model

Each finding should contain, where applicable:

```text
Severity → Title → Description → Evidence → Source → Recommendation
```

| Level | Meaning |
| :---: | :--- |
| 🟢 Success | Expected protection or configuration is present |
| 🟡 Warning | Review is recommended |
| 🔴 Error | A check failed or an unsafe condition exists |
| 🔴 Critical | Immediate attention is recommended |

**Exit criteria:** Checks return normalized findings with evidence and useful recommendations, without overstating certainty or product scope.

---

## EP-07 — Hardware and Firmware

**Status:** ⚪ Planned  
**Objective:** Build a complete Windows hardware and firmware inventory.

- Computer manufacturer, model, and serial number
- CPU, RAM, and memory slots
- Motherboard and GPU
- Storage devices
- BIOS version, date, and BIOS/UEFI mode
- Secure Boot and TPM
- Battery information

**Technical direction:** Prefer supported PowerShell CIM cmdlets over deprecated WMIC-based implementations. Reuse data already collected by EP-02 instead of issuing duplicate queries.

**Exit criteria:** ArgOS provides a normalized device inventory and handles machines with multiple disks, GPUs, batteries, or missing firmware fields.

---

## EP-08 — Utilities

**Status:** ⚪ Planned  
**Objective:** Add small, dependable tools for administration and investigation.

### Hash and integrity tools

- SHA-256, SHA-512, SHA-3, and BLAKE2
- MD5 and SHA-1 for compatibility only
- Hash text and files
- Compare hashes and verify file integrity

### Password generator

- Cryptographically secure generation with Python's `secrets` module
- Configurable length and character groups
- Optional ambiguous-character exclusion
- Password-strength indication

> [!IMPORTANT]
> Generated passwords and sensitive input must never be written automatically to ArgOS logs or reports.

**Exit criteria:** Utilities behave consistently from the CLI, validate input, and avoid persisting secrets.

---

## EP-09 — Reports

**Status:** ⚪ Planned  
**Objective:** Consolidate ArgOS data and findings into reusable reports.

### Formats

| TXT | JSON | CSV | HTML |
| :---: | :---: | :---: | :---: |
| Human-readable notes | Structured automation | Tabular analysis | Shareable visual report |

### Report content

- System and security overview
- Critical events
- Processes and services
- Network information
- Hardware and BIOS
- Findings and recommendations

Reports will share the CLI's severity semantics and must clearly record collection time, host, module status, and unavailable data.

**Exit criteria:** A single normalized result can be exported consistently without rerunning collection for each format.

---

## EP-10 — Quality, Packaging, and Release

**Status:** ⚪ Planned  
**Objective:** Prepare ArgOS for reliable public distribution.

| Quality | Automation | Documentation | Distribution |
| :--- | :--- | :--- | :--- |
| Unit and integration tests | GitHub Actions | README and architecture guide | CLI entry point |
| Pytest and coverage | Automated linting | Installation and usage | Python package |
| Ruff and MyPy | Automated tests | Screenshots and troubleshooting | PyInstaller evaluation |
| Build validation | Release checks | Changelog | GitHub Releases and versioning |

**Exit criteria:** A clean checkout can be linted, type-checked, tested, packaged, and released through documented, repeatable steps.

---

## EP-11 — Interactive CLI Experience

**Status:** ⚪ Future enhancement  
**Objective:** Turn the functional CLI into a polished and consistent administration interface.

- Improved keyboard and breadcrumb navigation
- Contextual status information and progress indicators
- Rich tables, search, and filtering
- Consistent confirmations and visual language
- User configuration file
- Clear handling of elevation requirements and partial failures

**Exit criteria:** Common workflows are discoverable, consistent, keyboard-friendly, and provide immediate feedback for long-running operations.

---

## Current milestone

### EP-02 — Complete the system-information vertical slice

The next milestone is to take the existing structured collector through the full application path:

```text
PowerShell/CIM → PowerShellRunner → Normalized Python data → Rich UI → Tests
```

Completing this slice will establish the implementation pattern reused by Network, Security, Hardware, and Event Log modules.

### Suggested completion sequence

1. Correct and test system-information normalization.
2. Add a Rich presentation layer for collected data.
3. Connect the module to the application entry point.
4. Add privilege and partial-failure messaging.
5. Establish automated linting and tests before expanding collection modules.

---

## Roadmap principles

- **Read-only first:** collection and inspection are the default.
- **Confirm state changes:** potentially disruptive actions always require explicit confirmation.
- **One PowerShell boundary:** subprocess execution remains centralized.
- **Structured data first:** presentation and export consume the same normalized results.
- **Graceful degradation:** one unavailable source should not invalidate an entire report.
- **Evidence over claims:** security findings include their source and supporting evidence.
