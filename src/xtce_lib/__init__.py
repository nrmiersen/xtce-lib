"""xtce-lib."""

import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

from . import generated, xtce
from .common.validation import ValidationReport, XtceSchemaError, XtceSemanticError
from .common.xtce_database import XtceDatabase
from .common.xtce_file import XtceFile
from .common.xtce_path import PathNode, XtcePath
from .common.xtce_registry import ResolvedReference, XtceRegistry
from .common.xtce_version import XtceVersion
from .exceptions import DowngradePolicy, XtceDowngradeError, XtceUnsupportedError

__all__ = [
    "generated",
    "xtce",
    "ValidationReport",
    "XtceSchemaError",
    "XtceSemanticError",
    "XtceDatabase",
    "XtceFile",
    "PathNode",
    "XtcePath",
    "ResolvedReference",
    "XtceRegistry",
    "XtceVersion",
    "DowngradePolicy",
    "XtceDowngradeError",
    "XtceUnsupportedError",
]
