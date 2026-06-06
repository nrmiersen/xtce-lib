"""Processing models."""

from ._base import XtceBaseModel
from .common import NameDescriptionBase


class Checksum(XtceBaseModel):
    pass


class CRC(XtceBaseModel):
    pass


class XOR(XtceBaseModel):
    pass


class Parity(XtceBaseModel):
    pass


class InputOutputTriggerAlgorithm(XtceBaseModel):
    pass


class MathAlgorithm(XtceBaseModel):
    pass


class BaseCalibrator(XtceBaseModel):
    pass


class Calibrator(BaseCalibrator):
    pass


class ContextCalibrator(XtceBaseModel):
    pass


class SimpleAlgorithm(NameDescriptionBase):
    pass


class InputAlgorithm(SimpleAlgorithm):
    pass


class LinearAdjustment(XtceBaseModel):
    pass
