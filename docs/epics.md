ArgOS --- Project Epics & Current Progress

Windows Administration, Diagnostics & Security Toolkit
Current scope: Windows only.

Project Vision

ArgOS is a Python-based interactive CLI focused on Windows system
administration, diagnostics, investigation, and security auditing.

The project is being refactored from the original Windows-Log-Script
into a modular application with a Rich-based interface, centralized
PowerShell integration, reusable models, internal logging, and dedicated
Windows administration modules.

EP-01 --- Foundation

Objective: Build the architectural foundation required by all ArgOS
modules.

Scope

Refactor the original project structure

Rename the project to ArgOS

Create the argos/ Python package

Configure project dependencies

Create centralized Rich console

Create Rich visual theme

Create interactive main menu

Add semantic colors for success, warning, and error states

Detect Windows administrator privileges

Create centralized PowerShell executor

Create centralized PowerShell command definitions

Create common models (Finding, Severity)

Configure internal application logging

Implemented architecture

argos/
├── core/
│   ├── __init__.py
│   ├── logger.py
│   ├── models.py
│   ├── permissions.py
│   ├── powershell.py
│   └── powershell_commands.py
│
├── ui/
│   ├── __init__.py
│   ├── console.py
│   ├── menus.py
│   └── theme.py
│
├── __init__.py
├── __main__.py
└── app.py

Current CLI foundation

The application can display the ArgOS banner, render the main menu with
Rich, show semantic status colors, detect whether the current process
has administrator privileges, and execute PowerShell commands through a
centralized runner.

Status: ✅ Foundation implemented.

EP-02 --- System Information

Objective: Provide a consolidated view of the local Windows
environment.

Planned features

Windows edition and version

Windows build number

Computer name

Current user

Architecture

System uptime

CPU information

Physical memory

Storage information

GPU information

Motherboard information

BIOS information

PowerShell version

Timezone

System language

Environment information

Technical direction

Use CIM/PowerShell and Python system APIs through the existing
PowerShellRunner, avoiding duplicated subprocess calls.

Status: ⏳ Planned.

EP-03 --- Windows Event Logs

Objective: Refactor and expand the functionality that originated the
project.

Existing functionality

Read Windows System Event Log

Export collected events to a text file

Successfully process large event collections

The original prototype was able to collect more than 50,000 System
events and write them to system_log.txt.

Planned refactor

Integrate event collection into the ArgOS architecture

System logs

Application logs

Security logs

Setup logs

Windows Defender logs

PowerShell logs

Task Scheduler logs

Limit number of returned events

Filter by Event ID

Filter by severity

Filter by source

Filter by date

Search event messages

Rich table visualization

TXT export

JSON export

CSV export

Severity visualization

🟢 Information / Success

🟡 Warning

🔴 Error / Critical / Failure

Status: 🟡 Prototype exists; architectural refactor pending.

EP-04 --- Processes & Services

Objective: Inspect and administer Windows processes and services.

Processes

List running processes

PID and parent PID

CPU utilization

Memory utilization

Process owner

Executable path

Process start time

Search by name or PID

Terminate a process with confirmation

Services

List Windows services

Running services

Stopped services

Disabled services

Startup mode

Search services

Start service

Stop service

Restart service

Administrative or destructive actions must require explicit
confirmation.

Status: ⏳ Planned.

EP-05 --- Network Diagnostics

Objective: Provide Windows network troubleshooting and investigation
tools.

Planned features

Network interfaces

IPv4 addresses

IPv6 addresses

MAC addresses

Default gateway

DNS configuration

Active TCP connections

UDP endpoints

Listening ports

Process associated with connections

Routing table

ARP table

Ping

DNS lookup

TCP port test

Traceroute

Proxy configuration

Windows network profile

Firewall status

Status: ⏳ Planned.

EP-06 --- Security Audit

Objective: Perform a local Windows security posture assessment.

ArgOS will provide administrative/security findings rather than
presenting itself as an antivirus or EDR product.

Planned checks

Administrator privilege status

Microsoft Defender status

Defender real-time protection

Defender signature information

Windows Firewall profiles

BitLocker

Secure Boot

TPM

UAC

Windows Update status

Local users

Local Administrators group

Open sessions

Network shares

Listening ports

Authentication events

Failed logins

Disabled accounts

Basic password policy

Finding model

Security results will use the common Finding/Severity architecture:

🟢 SUCCESS
🟡 WARNING
🔴 ERROR
🔴 CRITICAL

Where appropriate, findings can contain a description, evidence, source,
severity, and recommendation.

Status: ⏳ Planned.

EP-07 --- Hardware & Firmware

Objective: Inspect Windows hardware and firmware information.

Planned features

Computer manufacturer

Computer model

Serial number

CPU

RAM

Memory slots

Motherboard

GPU

Storage devices

BIOS version

BIOS date

BIOS/UEFI mode

Secure Boot

TPM

Battery information

PowerShell CIM cmdlets will be preferred over deprecated WMIC-based
implementations.

Status: ⏳ Planned.

EP-08 --- Utilities

Objective: Add useful administration and investigation utilities.

Hash tools

SHA-256

SHA-512

SHA-3

BLAKE2

MD5 for compatibility

SHA-1 for compatibility

Hash text

Hash files

Compare hashes

File integrity verification

Password generator

Cryptographically secure generation using secrets

Custom password length

Uppercase characters

Lowercase characters

Numbers

Symbols

Optional ambiguous-character exclusion

Password strength indication

Generated passwords must not be automatically written to ArgOS logs.

Status: ⏳ Planned.

EP-09 --- Reports

Objective: Consolidate ArgOS findings into reusable reports.

Planned formats

TXT

JSON

CSV

HTML

HTML report sections

System overview

Security overview

Critical events

Processes

Services

Network information

Hardware and BIOS

Findings and recommendations

Reports will use the same green/yellow/red severity model as the CLI.

Status: ⏳ Planned.

EP-10 --- Quality, Packaging & Release

Objective: Prepare ArgOS for reliable public distribution.

Quality

Unit tests

Integration tests

Pytest

Coverage reporting

Ruff

MyPy

CI/CD

GitHub Actions

Automated linting

Automated tests

Build validation

Documentation

Complete README

Architecture documentation

Installation guide

Usage examples

Screenshots

Troubleshooting guide

Changelog

Packaging

Define CLI entry point

Package Python application

Evaluate PyInstaller executable

GitHub Releases

Versioning strategy

Status: ⏳ Planned.

EP-11 --- Interactive CLI Experience

Objective: Evolve the CLI from a functional menu into a polished
administration interface.

Planned improvements

Improved keyboard navigation

Breadcrumb navigation

Status information

Progress indicators

Rich tables

Search and filtering

Consistent confirmation prompts

Configuration file

Consistent visual language across modules

Status: ⏳ Future enhancement.

Current Project Status

EP-01  Foundation                    ✅ Implemented
EP-02  System Information            ⏳ Next
EP-03  Windows Event Logs            🟡 Prototype exists
EP-04  Processes & Services          ⏳ Planned
EP-05  Network Diagnostics           ⏳ Planned
EP-06  Security Audit                ⏳ Planned
EP-07  Hardware & Firmware           ⏳ Planned
EP-08  Utilities                     ⏳ Planned
EP-09  Reports                       ⏳ Planned
EP-10  Quality & Release             ⏳ Planned
EP-11  Interactive CLI Experience    ⏳ Future

Current Technical Foundation

ArgOS currently has the architectural foundation required to begin
implementing Windows modules:

Python modular package structure

Rich-based CLI

Centralized visual theme

Main application menu

Windows administrator privilege detection

Centralized PowerShell execution

Reusable PowerShell commands

Common finding/severity models

Internal logging

Existing Windows Event Log prototype

Next Milestone

EP-02 --- System Information

The next milestone is to connect the existing PowerShell foundation to
real Windows system data and present the results through the Rich
interface.

This will establish the implementation pattern that later modules such
as Network, Security, Hardware, and Event Logs can reuse.