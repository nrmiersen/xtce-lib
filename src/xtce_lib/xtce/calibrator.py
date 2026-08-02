"""Calibrator models."""

from abc import ABC
from typing import Any, Self

from pydantic import Field, field_validator, model_validator

from xtce_lib.common.xtce_path import XtcePath
from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from ._util import unwrap
from .common import Alias, AncillaryData
from .condition import ContextMatch
from .enum import MathOperator
from .reference import ArgumentInstanceRef, ParameterInstanceRef


class ValueOperand(XtceBaseModel):
    """Use a constant in the calculation."""

    value: float | str
    """The constant value used in the calculation."""

    @field_validator("value")
    @classmethod
    def validate_numeric_string(cls, value: float | str) -> float | str:
        """Validate that the value is either a float or a numeric string."""
        if isinstance(value, str):
            try:
                float(value)
            except ValueError as exc:
                raise ValueError(
                    "value must be a float or a string convertible to float"
                ) from exc
        return value


class ThisParameterOperand(XtceBaseModel):
    """Use the value of this parameter in the calculation."""


class BaseCalibrator(XtceBaseModel, ABC):
    """Base class for all calibrators.

    Note - the name is non-reference-able.

    """

    name: str | None = None
    """An optional name for this calibrator.

    Applicable since: XTCE 1.2

    """

    short_description: str | None = None
    """A short description of this calibrator.

    Applicable since: XTCE 1.2

    """

    ancillary_data: list[AncillaryData] = Field(default_factory=list)
    """Any ancillary data associated with the element.

    Applicable since: XTCE 1.2

    """

    _v1_1_type = None
    _v1_2_type = xtce_1_2.BaseCalibratorType
    _v1_3_type = xtce_1_3.BaseCalibratorType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.BaseCalibratorType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["name"] = obj.name
        kwargs["short_description"] = obj.short_description
        kwargs["ancillary_data"] = (
            [
                AncillaryData._from_v1_2(data)
                for data in obj.ancillary_data_set.ancillary_data
            ]
            if obj.ancillary_data_set is not None
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.BaseCalibratorType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["name"] = obj.name
        kwargs["short_description"] = obj.short_description
        kwargs["ancillary_data"] = (
            [
                AncillaryData._from_v1_3(data)
                for data in obj.ancillary_data_set.ancillary_data
            ]
            if obj.ancillary_data_set is not None
            else []
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        version = XtceVersion.V1_1

        self._enforce_unsupported_field(
            field_name="name",
            current_value=self.name,
            empty_value=None,
            target_version=version,
            policy=policy,
        )
        self._enforce_unsupported_field(
            field_name="short_description",
            current_value=self.short_description,
            empty_value=None,
            target_version=version,
            policy=policy,
        )
        self._enforce_unsupported_field(
            field_name="ancillary_data",
            current_value=self.ancillary_data,
            empty_value=[],
            target_version=version,
            policy=policy,
        )

        return super()._to_v1_1_kwargs(policy)

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["name"] = self.name
        kwargs["short_description"] = self.short_description
        kwargs["ancillary_data_set"] = xtce_1_2.AncillaryDataSetType(
            ancillary_data=[data._to_v1_2(policy) for data in self.ancillary_data]
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["name"] = self.name
        kwargs["short_description"] = self.short_description
        kwargs["ancillary_data_set"] = xtce_1_3.AncillaryDataSetType(
            ancillary_data=[data._to_v1_3(policy) for data in self.ancillary_data]
        )
        return kwargs


class MathOperationCalibrator(BaseCalibrator):
    """Define a math operation calibrator."""

    operation: list[
        ValueOperand | ThisParameterOperand | MathOperator | ParameterInstanceRef
    ] = Field(default_factory=list)
    """The sequence of operands and operators for the math operation."""

    _v1_1_type = xtce_1_1.MathOperationType
    _v1_2_type = xtce_1_2.MathOperationCalibratorType
    _v1_3_type = xtce_1_3.MathOperationCalibratorType

    @model_validator(mode="after")
    def validate_rpn_sequence(self) -> Self:
        """Validate that the math operation sequence is a valid RPN expression."""
        if not self.operation:
            return self

        stack_depth = 0

        for index, item in enumerate(self.operation):
            if isinstance(item, MathOperator):
                popped = item.required_operands
                pushed = item.pushed_operands

                if stack_depth < popped:
                    raise ValueError(
                        f"RPN stack underflow at index {index}: "
                        f"operator '{item.value}' requires {popped} operands, "
                        f"but stack depth is {stack_depth}"
                    )

                # Calculate the new depth
                stack_depth = stack_depth - popped + pushed

            else:
                stack_depth += 1

        if stack_depth != 1:
            raise ValueError(
                f"invalid RPN sequence: expected final stack depth of 1, "
                f"but got {stack_depth}. ensure all operators have matching operands"
            )

        return self

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.MathOperationType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["operation"] = [
            ValueOperand(value=float(item))
            if isinstance(item, float)
            else MathOperator(value=item.value)
            if isinstance(item, xtce_1_1.MathOperatorsType)
            else ParameterInstanceRef(ref=XtcePath(item.parameter_ref))
            if isinstance(item, xtce_1_1.ParameterInstanceRefType)
            else ThisParameterOperand()
            for item in obj.choice
        ]
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.MathOperationCalibratorType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["operation"] = [
            ValueOperand(value=item.value)
            if isinstance(item, xtce_1_2.MathOperationCalibratorType.ValueOperand)
            else ThisParameterOperand()
            if isinstance(
                item, xtce_1_2.MathOperationCalibratorType.ThisParameterOperand
            )
            else ParameterInstanceRef(
                ref=XtcePath(item.parameter_ref),
                instance=item.instance,
                use_calibrated_value=item.use_calibrated_value,
            )
            if isinstance(item, xtce_1_2.ParameterInstanceRefType)
            else MathOperator(value=item.value)
            for item in obj.choice
        ]
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.MathOperationCalibratorType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["operation"] = [
            ValueOperand(value=item.value)
            if isinstance(item, xtce_1_3.MathOperationCalibratorType.ValueOperand)
            else ThisParameterOperand()
            if isinstance(
                item, xtce_1_3.MathOperationCalibratorType.ThisParameterOperand
            )
            else ParameterInstanceRef(
                ref=XtcePath(item.parameter_ref),
                instance=item.instance,
                use_calibrated_value=item.use_calibrated_value,
            )
            if isinstance(item, xtce_1_3.ParameterInstanceRefType)
            else MathOperator(value=item.value)
            for item in obj.choice
        ]
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["choice"] = [
            float(item.value)
            if isinstance(item, ValueOperand)
            else object()
            if isinstance(item, ThisParameterOperand)
            else xtce_1_1.MathOperatorsType(value=item.value)
            if isinstance(item, MathOperator)
            else xtce_1_1.ParameterInstanceRefType(
                parameter_ref=str(item.ref),
                instance=item.instance,
                use_calibrated_value=item.use_calibrated_value,
            )
            for item in self.operation
        ]
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = [
            xtce_1_2.MathOperationCalibratorType.ValueOperand(value=str(item.value))
            if isinstance(item, ValueOperand)
            else xtce_1_2.MathOperationCalibratorType.ThisParameterOperand()
            if isinstance(item, ThisParameterOperand)
            else xtce_1_2.MathOperatorsType(value=item.value)
            if isinstance(item, MathOperator)
            else xtce_1_2.ParameterInstanceRefType(
                parameter_ref=str(item.ref),
                instance=item.instance,
                use_calibrated_value=item.use_calibrated_value,
            )
            for item in self.operation
        ]
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = [
            xtce_1_3.MathOperationCalibratorType.ValueOperand(value=str(item.value))
            if isinstance(item, ValueOperand)
            else xtce_1_3.MathOperationCalibratorType.ThisParameterOperand()
            if isinstance(item, ThisParameterOperand)
            else xtce_1_3.MathOperatorsType(value=item.value)
            if isinstance(item, MathOperator)
            else xtce_1_3.ParameterInstanceRefType(
                parameter_ref=str(item.ref),
                instance=item.instance,
                use_calibrated_value=item.use_calibrated_value,
            )
            for item in self.operation
        ]
        return kwargs


class ArgumentMathOperation(XtceBaseModel):
    """Define an argument math operation."""

    operation: list[
        ValueOperand
        | ThisParameterOperand
        | MathOperator
        | ParameterInstanceRef
        | ArgumentInstanceRef
    ] = Field(default_factory=list)

    _v1_1_type = None
    _v1_2_type = None
    _v1_3_type = xtce_1_3.ArgumentMathOperationType

    @model_validator(mode="after")
    def validate_rpn_sequence(self) -> Self:
        """Validate that the math operation sequence is a valid RPN expression."""
        if not self.operation:
            return self

        stack_depth = 0

        for index, item in enumerate(self.operation):
            if isinstance(item, MathOperator):
                popped = item.required_operands
                pushed = item.pushed_operands

                if stack_depth < popped:
                    raise ValueError(
                        f"RPN stack underflow at index {index}: "
                        f"operator '{item.value}' requires {popped} operands, "
                        f"but stack depth is {stack_depth}"
                    )

                # Calculate the new depth
                stack_depth = stack_depth - popped + pushed

            else:
                stack_depth += 1

        if stack_depth != 1:
            raise ValueError(
                f"invalid RPN sequence: expected final stack depth of 1, "
                f"but got {stack_depth}. ensure all operators have matching operands"
            )

        return self

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentMathOperationType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["operation"] = [
            ValueOperand(value=item.value)
            if isinstance(item, xtce_1_3.ArgumentMathOperationType.ValueOperand)
            else ThisParameterOperand()
            if isinstance(item, xtce_1_3.ArgumentMathOperationType.ThisParameterOperand)
            else ParameterInstanceRef(
                ref=XtcePath(item.parameter_ref),
                instance=item.instance,
                use_calibrated_value=item.use_calibrated_value,
            )
            if isinstance(item, xtce_1_3.ParameterInstanceRefType)
            else ArgumentInstanceRef(
                ref=item.argument_ref,
                use_calibrated_value=item.use_calibrated_value,
            )
            if isinstance(item, xtce_1_3.ArgumentInstanceRefType)
            else MathOperator(value=item.value)
            for item in obj.choice
        ]
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = [
            xtce_1_3.ArgumentMathOperationType.ValueOperand(value=str(item.value))
            if isinstance(item, ValueOperand)
            else xtce_1_3.ArgumentMathOperationType.ThisParameterOperand()
            if isinstance(item, ThisParameterOperand)
            else xtce_1_3.MathOperatorsType(value=item.value)
            if isinstance(item, MathOperator)
            else xtce_1_3.ParameterInstanceRefType(
                parameter_ref=str(item.ref),
                instance=item.instance,
                use_calibrated_value=item.use_calibrated_value,
            )
            if isinstance(item, ParameterInstanceRef)
            else xtce_1_3.ArgumentInstanceRefType(
                argument_ref=str(item.ref),
                use_calibrated_value=item.use_calibrated_value,
            )
            for item in self.operation
        ]
        return kwargs


class SplinePoint(XtceBaseModel):
    """Define a point on a spline or piecewise function."""

    order: int = Field(default=1, ge=0)
    """The order of the interpolation function:

    - `0`: flat line from this point to the next point
    - `1`: linear interpolation (default)
    - `2`: quadratic interpolation
    - `3`: cubic interpolation
    - `n`: nth-order interpolation

    """

    raw: float
    """The raw encoded value."""

    calibrated: float
    """The calibrated value corresponding to the raw encoded value."""

    _v1_1_type = xtce_1_1.SplinePointType
    _v1_2_type = xtce_1_2.SplinePointType
    _v1_3_type = xtce_1_3.SplinePointType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.SplinePointType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["order"] = obj.order
        kwargs["raw"] = obj.raw
        kwargs["calibrated"] = obj.calibrated
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.SplinePointType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["order"] = obj.order
        kwargs["raw"] = obj.raw
        kwargs["calibrated"] = obj.calibrated
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.SplinePointType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["order"] = obj.order
        kwargs["raw"] = obj.raw
        kwargs["calibrated"] = obj.calibrated
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["order"] = self.order
        kwargs["raw"] = self.raw
        kwargs["calibrated"] = self.calibrated
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["order"] = self.order
        kwargs["raw"] = self.raw
        kwargs["calibrated"] = self.calibrated
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["order"] = self.order
        kwargs["raw"] = self.raw
        kwargs["calibrated"] = self.calibrated
        return kwargs


class SplineCalibrator(BaseCalibrator):
    """Define a spline function for calibration.

    Requires a set of at least two spline points. Raw values are converted to calibrated
    values by finding a position on the line corresponding to the raw value.

    """

    spline_points: list[SplinePoint] = Field(default_factory=list, min_length=2)
    """The set of spline points defining the calibration curve."""

    order: int = Field(default=1, ge=0)
    """The global order of the interpolation function:

    - `0`: flat line from this point to the next point
    - `1`: linear interpolation (default)
    - `2`: quadratic interpolation
    - `3`: cubic interpolation
    - `n`: nth-order interpolation

    (can be overridden by individual spline points)
    """

    extrapolate: bool = False
    """Whether to allow extrapolation beyond the defined spline points."""

    _v1_1_type = xtce_1_1.CalibratorType.SplineCalibrator
    _v1_2_type = xtce_1_2.SplineCalibratorType
    _v1_3_type = xtce_1_3.SplineCalibratorType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.CalibratorType.SplineCalibrator
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["spline_points"] = [
            SplinePoint._from_v1_1(sp) for sp in obj.spline_point
        ]
        kwargs["order"] = obj.order
        kwargs["extrapolate"] = obj.extrapolate
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.SplineCalibratorType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["spline_points"] = [
            SplinePoint._from_v1_2(sp) for sp in obj.spline_point
        ]
        kwargs["order"] = obj.order
        kwargs["extrapolate"] = obj.extrapolate
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.SplineCalibratorType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["spline_points"] = [
            SplinePoint._from_v1_3(sp) for sp in obj.spline_point
        ]
        kwargs["order"] = obj.order
        kwargs["extrapolate"] = obj.extrapolate
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["spline_point"] = [sp._to_v1_1(policy) for sp in self.spline_points]
        kwargs["order"] = self.order
        kwargs["extrapolate"] = self.extrapolate
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["spline_point"] = [sp._to_v1_2(policy) for sp in self.spline_points]
        kwargs["order"] = self.order
        kwargs["extrapolate"] = self.extrapolate
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["spline_point"] = [sp._to_v1_3(policy) for sp in self.spline_points]
        kwargs["order"] = self.order
        kwargs["extrapolate"] = self.extrapolate
        return kwargs


class Term(XtceBaseModel):
    """Define a term in a polynomial calibrator."""

    coefficient: float
    """The coefficient of the term."""

    exponent: int = Field(..., ge=0)
    """The exponent of the term."""

    _v1_1_type = xtce_1_1.PolynomialType.Term
    _v1_2_type = xtce_1_2.TermType
    _v1_3_type = xtce_1_3.TermType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.PolynomialType.Term) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["coefficient"] = obj.coefficient
        kwargs["exponent"] = int(obj.exponent)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.TermType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["coefficient"] = obj.coefficient
        kwargs["exponent"] = obj.exponent
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.TermType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["coefficient"] = obj.coefficient
        kwargs["exponent"] = obj.exponent
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["coefficient"] = self.coefficient
        kwargs["exponent"] = self.exponent
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["coefficient"] = self.coefficient
        kwargs["exponent"] = self.exponent
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["coefficient"] = self.coefficient
        kwargs["exponent"] = self.exponent
        return kwargs


class PolynomialCalibrator(BaseCalibrator):
    """Define a polynomial equation for calibration.

    Raw values are converted to calibrated values by finding a position on the line
    corresponding to the raw value.

    """

    terms: list[Term] = Field(default_factory=list)
    """The list of terms that define the polynomial.

    Generally only up to second order powers are reflexive.

    """

    _v1_1_type = xtce_1_1.PolynomialType
    _v1_2_type = xtce_1_2.PolynomialCalibratorType
    _v1_3_type = xtce_1_3.PolynomialCalibratorType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.PolynomialType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["terms"] = [Term._from_v1_1(t) for t in obj.term]
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.PolynomialCalibratorType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["terms"] = [Term._from_v1_2(t) for t in obj.term]
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.PolynomialCalibratorType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["terms"] = [Term._from_v1_3(t) for t in obj.term]
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["term"] = [t._to_v1_1(policy) for t in self.terms]
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["term"] = [t._to_v1_2(policy) for t in self.terms]
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["term"] = [t._to_v1_3(policy) for t in self.terms]
        return kwargs


class Calibrator(BaseCalibrator):
    """Define a generic calibrator to transform raw values to calibrated values."""

    long_description: str | None = None
    """Optional long form description to be used for explanatory descriptions of this
    element and may include HTML markup using CDATA.

    Long descriptions are of unbounded length.

    Only supported by XTCE 1.1

    """

    aliases: list[Alias] = Field(default_factory=list)
    """Used to contain alternate names or IDs for the element.

    Only supported by XTCE 1.1

    """

    calibrator_type: SplineCalibrator | PolynomialCalibrator | MathOperationCalibrator
    """The specific calibrator instance used for this generic calibrator."""

    _v1_1_type = xtce_1_1.CalibratorType
    _v1_2_type = xtce_1_2.CalibratorType
    _v1_3_type = xtce_1_3.CalibratorType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.CalibratorType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["long_description"] = obj.long_description
        kwargs["aliases"] = (
            [Alias._from_v1_1(a) for a in obj.alias_set.alias]
            if obj.alias_set is not None
            else []
        )
        kwargs["calibrator_type"] = (
            SplineCalibrator._from_v1_1(obj.choice)
            if isinstance(obj.choice, xtce_1_1.CalibratorType.SplineCalibrator)
            else PolynomialCalibrator._from_v1_1(obj.choice)
            if isinstance(obj.choice, xtce_1_1.PolynomialType)
            else MathOperationCalibrator._from_v1_1(unwrap(obj.choice))
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.CalibratorType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["calibrator_type"] = (
            SplineCalibrator._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.SplineCalibratorType)
            else PolynomialCalibrator._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.PolynomialCalibratorType)
            else MathOperationCalibrator._from_v1_2(unwrap(obj.choice))
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.CalibratorType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["calibrator_type"] = (
            SplineCalibrator._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.SplineCalibratorType)
            else PolynomialCalibrator._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.PolynomialCalibratorType)
            else MathOperationCalibrator._from_v1_3(unwrap(obj.choice))
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["long_description"] = self.long_description
        kwargs["alias_set"] = (
            xtce_1_1.AliasSetType(
                alias=[alias._to_v1_1(policy) for alias in self.aliases]
            )
            if self.aliases
            else None
        )
        kwargs["choice"] = self.calibrator_type._to_v1_1(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        version = XtceVersion.V1_2

        self._enforce_unsupported_field(
            field_name="long_description",
            current_value=self.long_description,
            empty_value=None,
            target_version=version,
            policy=policy,
        )
        self._enforce_unsupported_field(
            field_name="aliases",
            current_value=self.aliases,
            empty_value=[],
            target_version=version,
            policy=policy,
        )

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = self.calibrator_type._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        version = XtceVersion.V1_3

        self._enforce_unsupported_field(
            field_name="long_description",
            current_value=self.long_description,
            empty_value=None,
            target_version=version,
            policy=policy,
        )
        self._enforce_unsupported_field(
            field_name="aliases",
            current_value=self.aliases,
            empty_value=[],
            target_version=version,
            policy=policy,
        )

        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = self.calibrator_type._to_v1_3(policy)
        return kwargs


class ContextCalibrator(XtceBaseModel):
    """Define a context-specific calibrator.

    The calibration is only applied when the context match is true.

    """

    context_match: ContextMatch
    """The context match that determines when this calibrator is applied."""

    calibrator: Calibrator
    """The calibrator to apply when the context match is true."""

    _v1_1_type = xtce_1_1.ContextCalibratorType
    _v1_2_type = xtce_1_2.ContextCalibratorType
    _v1_3_type = xtce_1_3.ContextCalibratorType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.ContextCalibratorType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["context_match"] = ContextMatch._from_v1_1(obj.context_match)
        kwargs["calibrator"] = Calibrator._from_v1_1(obj.calibrator)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ContextCalibratorType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["context_match"] = ContextMatch._from_v1_2(obj.context_match)
        kwargs["calibrator"] = Calibrator._from_v1_2(obj.calibrator)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ContextCalibratorType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["context_match"] = ContextMatch._from_v1_3(obj.context_match)
        kwargs["calibrator"] = Calibrator._from_v1_3(obj.calibrator)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["context_match"] = self.context_match._to_v1_1(policy)
        kwargs["calibrator"] = self.calibrator._to_v1_1(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["context_match"] = self.context_match._to_v1_2(policy)
        kwargs["calibrator"] = self.calibrator._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["context_match"] = self.context_match._to_v1_3(policy)
        kwargs["calibrator"] = self.calibrator._to_v1_3(policy)
        return kwargs

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.ContextCalibratorType) -> Self:
        return cls(
            context_match=ContextMatch._from_v1_1(raw_obj.context_match),
            calibrator=Calibrator._from_v1_1(raw_obj.calibrator),
        )


class LinearAdjustment(XtceBaseModel):
    """A linear adjustment to apply to a parameter value.

    The default values of slope=1.0 and intercept=0.0 result in no adjustment being
    applied.

    """

    slope: float = 1.0
    """The slope of the linear adjustment."""

    intercept: float = 0.0
    """The intercept of the linear adjustment."""

    _v1_1_type = xtce_1_1.DecimalValueType.DynamicValue.LinearAdjustment
    _v1_2_type = xtce_1_2.LinearAdjustmentType
    _v1_3_type = xtce_1_3.LinearAdjustmentType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.DecimalValueType.DynamicValue.LinearAdjustment
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["slope"] = obj.slope
        kwargs["intercept"] = obj.intercept
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.LinearAdjustmentType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["slope"] = obj.slope or 1.0
        kwargs["intercept"] = obj.intercept
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.LinearAdjustmentType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["slope"] = obj.slope
        kwargs["intercept"] = obj.intercept
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["slope"] = self.slope
        kwargs["intercept"] = self.intercept
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["slope"] = self.slope
        kwargs["intercept"] = self.intercept
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["slope"] = self.slope
        kwargs["intercept"] = self.intercept
        return kwargs


class MathOperation(MathOperationCalibrator, ABC):
    """Base class for math operations."""
