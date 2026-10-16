"""Windows privilege detection."""

from __future__ import annotations

import ctypes
import sys


def is_administrator() -> bool:
    """Return whether ArgOS is running with administrator privileges."""

    if sys.platform != "win32":
        return False

    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except (AttributeError, OSError):
        return False
