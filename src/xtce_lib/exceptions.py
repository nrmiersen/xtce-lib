"""Xtce-lib exceptions."""

from enum import Enum

from xtce_lib.common.xtce_version import XtceVersion


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


class XtceUnsupportedError(ValueError):
    """Exception raised when the library encounters an XTCE element that is not supported
    in the current version.
    """

    def __init__(self, version: XtceVersion, element_name: str) -> None:
        """Initialize the exception with the unsupported element and version."""
        super().__init__(
            f"XTCE {version.value} does not support the '{element_name}' element."
        )
