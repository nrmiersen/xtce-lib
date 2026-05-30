"""xtce-lib."""

import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

from . import generated
from .common import XtceFile
from .xtce_path import XtcePath

__all__ = ["XtcePath", "XtceFile", "generated"]
