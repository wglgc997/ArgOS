"""Internal application logging configuration"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from argos.config import AppConfig

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
MAX_LOG_SIZE = 2 * 1024 * 1024
BACKUP_COUNT = 3


def configure_logging(config: AppConfig) -> logging.Logger:
    """Configure and return the root ArgOS logger"""

    config.log_directory.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("argos")
    logger.setLevel(config.log_level)
    logger.propagate = False

    # Avoid duplicate handlers if main() is called more than once.
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

    handler = RotatingFileHandler(
        config.log_file,
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )

    handler.setLevel(config.log_level)
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(handler)

    logger.debug("Logging configured: %$", config.log_file)
    return logger
