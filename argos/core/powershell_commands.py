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
    "Select-Object Caption, Version, BuildNumber, "
    "OSArchitecture, InstallDate, LastBootUpTime"
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

GET_PROCESSES = "Get-Process | Select-Object Name, Id, CPU, WorkingSet, StartTime, Path"

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

GET_SYSTEM_INFORMATION = """
$os = Get-CimInstance Win32_OperatingSystem
$computer = Get-CimInstance Win32_ComputerSystem
$cpu = Get-CimInstance Win32_Processor
$bios = Get-CimInstance Win32_BIOS
$disks = Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3"
$gpu = Get-CimInstance Win32_VideoController
$baseboard = Get-CimInstance Win32_BaseBoard
$timezone = Get-TimeZone

# Build a structured object with required sys info

# Custom object with named fields
[PSCustomObject]@{
    Computer = $computer.Name
    WindowsVersion = [PSCustomObject]@{
        # Windows product name, such as Windows 11 Enterprise
        Name = $os.Caption

        # Windows internal version number
        Version = $os.Version

        # Windows build number
        Build = $os.BuildNumber

        # Original Windows installation date
        InstallDate = $os.InstallDate

        # Last operating system boot timestamp
        LastBootUpTime = $os.LastBootUpTime
    }
    WindowsBuild = $os.BuildNumber
    Architecture = $os.OSArchitecture
    CPU = [PSCustomObject]@{
        # CPU model name
        Name = $cpu.Name

        # CPU manufacturer
        Manufacturer = $cpu.Manufacturer

        # Number of physical CPU cores
        Cores = $cpu.NumberOfCores

        # Number of logical processors / threads
        LogicalProcessors = $cpu.NumberOfLogicalProcessors

        # Maximum clock speed in MHz
        MaxClockSpeedMHz = $cpu.MaxClockSpeed
    }

    # Get the current logged-in user from the Windows environment
    LocalUser = [Environment]::UserName

    # Get the configured Windows timezone
    Timezone = [PSCustomObject]@{
        Id = $timezone.Id
        DisplayName = $timezone.DisplayName
        StandardName = $timezone.StandardName
    }
    
    Memory = [PSCustomObject]@{
        TotalGB = [math]::Round($computer.TotalPhysicalMemory / 1GB, 2)
        FreeGB = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
    }
    
    Storage = $disks | ForEach-Object {
        # Return one storage object per local fixed disk
        [PSCustomObject]@{
            Drive = $_.DeviceID
            FileSystem = $_.FileSystem
            VolumeName = $_.VolumeName
            TotalGB = [math]::Round($_.Size / 1GB, 2)
            FreeGB = [math]::Round($_.FreeSpace / 1GB, 2)
        }
    }

    GPU = $gpu | ForEach-Object {
        # Return one video controller object per detected GPU
        [PSCustomObject]@{
            Name = $_.Name
            DriverVersion = $_.DriverVersion
            VideoProcessor = $_.VideoProcessor
            AdapterRAMGB = [math]::Round($_.AdapterRAM / 1GB, 2)
        }
    }

    BaseBoard = [PSCustomObject]@{
        # Motherboard manufacturer
        Manufacturer = $baseboard.Manufacturer

        # Motherboard product/model
        Product = $baseboard.Product

        # Motherboard serial number
        SerialNumber = $baseboard.SerialNumber
    }

    BIOS = [PSCustomObject]@{
        # BIOS manufacturer
        Manufacturer = $bios.Manufacturer

        # BIOS SMBIOS version
        Version = $bios.SMBIOSBIOSVersion

        # BIOS serial number
        SerialNumber = $bios.SerialNumber

        # BIOS release date
        ReleaseDate = $bios.ReleaseDate
    }


    PowerShell = $PSVersionTable.PSVersion.ToString()
}
"""
