"""
PowerShell commands used by ArgOS Cli.

This module centralizes reusable PowerShell commands and prevents
PowerShell strings from being scattered throughout the project.
"""

GET_BIOS = (
    "Get-CimInstance Win32-BIOS | "
    "Select-Object Caption, Version, BuildNumber, "
    "SMBIOSBIOSVersion, ReleaseDate"
)

GET_OPERATING_SYSTEM = (
    "Get-CimInstance Win32_OperatingSystem | "
    "Select-Object Manufacturer, Name, SerialNumber, "
    "SMBIOSBIOSVersion, ReleaseDate"
)

GET_COMPUTER_SYSTEM = (
    "Get-CimInstance Win32_ComputerSystem | "
    "Select-Object Manufacturer, Model, Name, "
    "TotalPhysicalMemory, UserName"
)

GET_PROCESSOR = (
    "Get-CimInstance Win32_Processor | "
    "Select-Object Name, Manufacturer, NumberOfCores, "
    "NumberOfLogicalProcessors, MaxClockSpeed"
)

GET_SERVICES = (
    "Get-CimInstance Win32_Service | "
    "Select-Object Name, DisplayName, State, "
    "StartMode, ProcessId"
)

GET_PROCESSES = (
    "Get-Process | "
    "Select-Object Name, Id, CPU, WorkingSet, "
    "StartTime, Path"
)

GET_FIREWALL_PROFILES = (
    "Get-NetFirewallProfile | "
    "Select-Object Name, Enabled, DefaultInboundAction, "
    "DefaultOutboundAction"
)

GET_DEFENDER_STATUS = (
    "Get-MpComputerStatus | "
    "Select-Object AntivirusEnabled, AntispywareEnabled, "
    "RealTimeProtectionEnabled, BehaviorMonitorEnabled, "
    "AntivirusSignatureLastUpdated"
)

GET_LOCAL_USERS = (
    "Get-LocalUser | "
    "Select-Object Name, Enabled, LastLogon, "
    "PasswordRequired, PasswordExpires"
)

GET_NETWORK_ADAPTERS = (
    "Get-NetAdapter | "
    "Select-Object Name, InterfaceDescription, Status, "
    "MacAddress, LinkSpeed"
)

GET_NETWORK_CONFIGURATION = (
    "Get-NetIPConfiguration | "
    "Select-Object InterfaceAlias, InterfaceDescription, "
    "IPv4Address, IPv6Address, IPv4DefaultGateway, DNSServer"
)

GET_TCP_CONNECTIONS = (
    "Get-NetTCPConnection | "
    "Select-Object LocalAddress, LocalPort, RemoteAddress, "
    "RemotePort, State, OwningProcess"
)

GET_TPM = (
    "Get-Tpm | "
    "Select-Object TpmPresent, TpmReady, TpmEnabled, "
    "TpmActivated, ManufacturerIdTxt"
)

GET_BITLOCKER = (
    "Get-BitLockerVolume | "
    "Select-Object MountPoint, VolumeStatus, "
    "ProtectionStatus, EncryptionMethod, EncryptionPercentage"
)