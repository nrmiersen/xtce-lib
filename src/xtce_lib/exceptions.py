"""Xtce-lib exceptions."""

from enum import Enum


class DowngradePolicy(str, Enum):
    """Defines how the library handles data loss when exporting to older XTCE
    versions.
    """

    STRICT = "strict"
    """Raise an exception if any data loss would occur when exporting to an older XTCE
    version.
    """

    WARN = "warn"
    """Log a warning if any data loss would occur when exporting to an older XTCE
    version.
    """

    IGNORE = "ignore"
    """Ignore any data loss when exporting to an older XTCE version."""

class XtceDowngradeError(ValueError):
    """Exception raised when the library is configured to STRICT downgrade policy and an
    export to an older XTCE version would result in data loss.
    """

    pass
