"""Windows privilege detection."""

from __future__ import annotations

import ctypes
import os


def is_administrator() -> bool:
    """Return whether ArgOS is running with administrator privileges."""

    if os.name != "nt":
        return False

    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except (AttributeError, OSError):
        return False
