"""Shared ArgOS exception types"""


class ArgOSError(Exception):
    """Base class for expected ArgOS app errors"""


class ConfigurationError(ArgOSError):
    """Raised when application configuration is invalid"""


class CollectionError(ArgOSError):
    """Raised when a module cannot collect requested information"""


class PrivilegeRequiredError(ArgOSError):
    """Raised when an application requires information privileges"""
