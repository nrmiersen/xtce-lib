"""Calibrator models."""

from pydantic import Field

from ._base import XtceBaseModel
from .common import AncillaryData
from .condition import ContextMatch
from .enum import MathOperators
from .reference import ArgumentInstanceRef, ParameterInstanceRef


class ValueOperand(XtceBaseModel):
    value: str = Field(default="")


class ThisParameterOperand(XtceBaseModel):
    value: str = Field(default="")


class BaseCalibrator(XtceBaseModel):
    ancillary_data: list[AncillaryData] = Field(default_factory=list, min_length=1)
    name: str | None = Field(default=None)
    short_description: str | None = Field(default=None)


class MathOperationCalibrator(XtceBaseModel):
    operation: list[
        ValueOperand | ThisParameterOperand | MathOperators | ParameterInstanceRef
    ] = Field(default_factory=list)


class SplinePoint(XtceBaseModel):
    order: int = Field(default=1, ge=0)
    raw: float = Field(...)
    calibrated: float = Field(...)


class SplineCalibrator(BaseCalibrator):
    spline_points: list[SplinePoint] = Field(default_factory=list, min_length=2)
    order: int = Field(default=1, ge=0)
    extrapolate: bool = Field(default=False)


class Term(XtceBaseModel):
    coefficient: float = Field(...)
    exponent: int = Field(..., ge=0)


class PolynomialCalibrator(BaseCalibrator):
    terms: list[Term] = Field(default_factory=list, min_length=1)


class Calibrator(BaseCalibrator):
    calibrator_type: (
        SplineCalibrator | PolynomialCalibrator | MathOperationCalibrator | None
    ) = Field(default=None)


class ContextCalibrator(XtceBaseModel):
    context_match: ContextMatch = Field(...)


class LinearAdjustment(XtceBaseModel):
    slope: float = Field(default=1.0)
    intercept: float = Field(default=0.0)


class MathOperation(MathOperationCalibrator):
    # Nothing
    pass


class ArgumentMathOperation(XtceBaseModel):
    operation: list[
        ValueOperand
        | ThisParameterOperand
        | MathOperators
        | ParameterInstanceRef
        | ArgumentInstanceRef
    ] = Field(default_factory=list)
