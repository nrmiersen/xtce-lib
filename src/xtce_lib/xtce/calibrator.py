"""Calibrator models."""

from typing import Any, Self

from pydantic import Field

from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy, XtceUnsupportedError
from xtce_lib.generated import xtce_1_2, xtce_1_3

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
    raw: float
    calibrated: float


class SplineCalibrator(BaseCalibrator):
    spline_points: list[SplinePoint] = Field(default_factory=list, min_length=2)
    order: int = Field(default=1, ge=0)
    extrapolate: bool = Field(default=False)


class Term(XtceBaseModel):
    coefficient: float
    exponent: int = Field(..., ge=0)


class PolynomialCalibrator(BaseCalibrator):
    terms: list[Term] = Field(default_factory=list, min_length=1)


class Calibrator(BaseCalibrator):
    calibrator_type: (
        SplineCalibrator | PolynomialCalibrator | MathOperationCalibrator | None
    ) = Field(default=None)


class ContextCalibrator(XtceBaseModel):
    context_match: ContextMatch


class LinearAdjustment(XtceBaseModel):
    """A linear adjustment to apply to a parameter value.

    The default values of slope=1.0 and intercept=0.0 result in no adjustment being
    applied.

    """

    slope: float = 1.0
    """The slope of the linear adjustment."""

    intercept: float = 0.0
    """The intercept of the linear adjustment."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.LinearAdjustmentType) -> Self:
        return cls(slope=(raw_obj.slope or 1.0), intercept=raw_obj.intercept)

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.LinearAdjustmentType) -> Self:
        return cls(slope=raw_obj.slope, intercept=raw_obj.intercept)

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.LinearAdjustmentType:
        return xtce_1_2.LinearAdjustmentType(slope=self.slope, intercept=self.intercept)

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.LinearAdjustmentType:
        return xtce_1_3.LinearAdjustmentType(slope=self.slope, intercept=self.intercept)


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
