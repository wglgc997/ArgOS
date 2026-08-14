"""Application configuration and filesystem conventions."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

APP_NAME = "ArgOS"
APP_VERSION = "0.1.0"


def default_data_directory() -> Path:
    """Return the platform-appropriate ArgOS data directory"""

    local_app_data = os.environ.get("LOCALAPPDATA")

    if local_app_data:
        return Path(local_app_data) / APP_NAME

    return Path.home() / f".{APP_NAME.lower()}"


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Runtime configuration shared across the application"""

    data_directory: Path
    log_level: str = "INFO"

    @property
    def log_directory(self) -> Path:
        """Return the directory used for application logs."""

        return self.data_directory / "logs"

    @property
    def log_file(self) -> Path:
        """Return the main application log file."""

        return self.log_directory / "argos.log"


def load_config() -> AppConfig:
    """Load application configuration from the environment"""

    configured_directory = os.environ.get("ARGOS_DATA_DIR")
    configured_level = os.environ.get("ARGOS_LOG_LEVEL", "INFO").upper()

    data_directory = (
        Path(configured_directory).expanduser()
        if configured_directory
        else default_data_directory()
    )

    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if configured_level not in valid_levels:
        configured_level = "INFO"

    return AppConfig(data_directory=data_directory, log_level=configured_level)
