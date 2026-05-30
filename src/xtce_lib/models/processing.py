"""Processing models."""

from ._base import XtceBaseModel
from .common import NameDescriptionBase


class InputOutputTriggerAlgorithm(XtceBaseModel):
    pass


class MathAlgorithm(XtceBaseModel):
    pass


class ErrorDetectCorrect(XtceBaseModel):
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
