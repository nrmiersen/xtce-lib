"""Calibrator models."""

from abc import ABC
from typing import Any, Self

from pydantic import Field, field_validator, model_validator

from xtce_lib.common.xtce_path import XtcePath
from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy, XtceUnsupportedError
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
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_2, cls.__name__)

    @classmethod
    def _from_v1_3(
        cls: type[Self], raw_obj: xtce_1_3.ArgumentMathOperationType
    ) -> Self:
        return cls(
            operation=[
                ValueOperand(value=item.value)
                if isinstance(item, xtce_1_3.ArgumentMathOperationType.ValueOperand)
                else ThisParameterOperand()
                if isinstance(
                    item, xtce_1_3.ArgumentMathOperationType.ThisParameterOperand
                )
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
                for item in raw_obj.choice
            ],
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_2, self.__class__.__name__)

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ArgumentMathOperationType:
        return xtce_1_3.ArgumentMathOperationType(
            choice=[
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
            ],
        )


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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.SplinePointType) -> Self:
        return cls(
            order=raw_obj.order,
            raw=raw_obj.raw,
            calibrated=raw_obj.calibrated,
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.SplinePointType) -> Self:
        return cls(
            order=raw_obj.order,
            raw=raw_obj.raw,
            calibrated=raw_obj.calibrated,
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.SplinePointType) -> Self:
        return cls(
            order=raw_obj.order,
            raw=raw_obj.raw,
            calibrated=raw_obj.calibrated,
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.SplinePointType:
        return xtce_1_1.SplinePointType(
            order=self.order,
            raw=self.raw,
            calibrated=self.calibrated,
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.SplinePointType:
        return xtce_1_2.SplinePointType(
            order=self.order,
            raw=self.raw,
            calibrated=self.calibrated,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.SplinePointType:
        return xtce_1_3.SplinePointType(
            order=self.order,
            raw=self.raw,
            calibrated=self.calibrated,
        )


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

    @classmethod
    def _from_v1_1(
        cls: type[Self], raw_obj: xtce_1_1.CalibratorType.SplineCalibrator
    ) -> Self:
        return cls(
            spline_points=[SplinePoint._from_v1_1(sp) for sp in raw_obj.spline_point],
            order=raw_obj.order,
            extrapolate=raw_obj.extrapolate,
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.SplineCalibratorType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            ancillary_data=[
                AncillaryData._from_v1_2(data)
                for data in raw_obj.ancillary_data_set.ancillary_data
            ]
            if raw_obj.ancillary_data_set is not None
            else [],
            spline_points=[SplinePoint._from_v1_2(sp) for sp in raw_obj.spline_point],
            order=raw_obj.order,
            extrapolate=raw_obj.extrapolate,
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.SplineCalibratorType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            ancillary_data=[
                AncillaryData._from_v1_3(data)
                for data in raw_obj.ancillary_data_set.ancillary_data
            ]
            if raw_obj.ancillary_data_set is not None
            else [],
            spline_points=[SplinePoint._from_v1_3(sp) for sp in raw_obj.spline_point],
            order=raw_obj.order,
            extrapolate=raw_obj.extrapolate,
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.CalibratorType.SplineCalibrator:
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

        return xtce_1_1.CalibratorType.SplineCalibrator(
            spline_point=[sp._to_v1_1(policy) for sp in self.spline_points],
            order=self.order,
            extrapolate=self.extrapolate,
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.SplineCalibratorType:
        return xtce_1_2.SplineCalibratorType(
            name=self.name,
            short_description=self.short_description,
            ancillary_data_set=xtce_1_2.AncillaryDataSetType(
                ancillary_data=[data._to_v1_2(policy) for data in self.ancillary_data]
            ),
            spline_point=[sp._to_v1_2(policy) for sp in self.spline_points],
            order=self.order,
            extrapolate=self.extrapolate,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.SplineCalibratorType:
        return xtce_1_3.SplineCalibratorType(
            name=self.name,
            short_description=self.short_description,
            ancillary_data_set=xtce_1_3.AncillaryDataSetType(
                ancillary_data=[data._to_v1_3(policy) for data in self.ancillary_data]
            ),
            spline_point=[sp._to_v1_3(policy) for sp in self.spline_points],
            order=self.order,
            extrapolate=self.extrapolate,
        )


class Term(XtceBaseModel):
    """Define a term in a polynomial calibrator."""

    coefficient: float
    """The coefficient of the term."""

    exponent: int = Field(..., ge=0)
    """The exponent of the term."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.PolynomialType.Term) -> Self:
        return cls(coefficient=raw_obj.coefficient, exponent=int(raw_obj.exponent))

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.TermType) -> Self:
        return cls(coefficient=raw_obj.coefficient, exponent=raw_obj.exponent)

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.TermType) -> Self:
        return cls(coefficient=raw_obj.coefficient, exponent=raw_obj.exponent)

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.PolynomialType.Term:
        return xtce_1_1.PolynomialType.Term(
            coefficient=self.coefficient, exponent=float(self.exponent)
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.TermType:
        return xtce_1_2.TermType(coefficient=self.coefficient, exponent=self.exponent)

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.TermType:
        return xtce_1_3.TermType(coefficient=self.coefficient, exponent=self.exponent)


class PolynomialCalibrator(BaseCalibrator):
    """Define a polynomial equation for calibration.

    Raw values are converted to calibrated values by finding a position on the line
    corresponding to the raw value.

    """

    terms: list[Term] = Field(default_factory=list)
    """The list of terms that define the polynomial.

    Generally only up to second order powers are reflexive.

    """

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.PolynomialType) -> Self:
        return cls(
            terms=[Term._from_v1_1(t) for t in raw_obj.term],
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.PolynomialCalibratorType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            ancillary_data=[
                AncillaryData._from_v1_2(data)
                for data in raw_obj.ancillary_data_set.ancillary_data
            ]
            if raw_obj.ancillary_data_set is not None
            else [],
            terms=[Term._from_v1_2(t) for t in raw_obj.term],
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.PolynomialCalibratorType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            ancillary_data=[
                AncillaryData._from_v1_3(data)
                for data in raw_obj.ancillary_data_set.ancillary_data
            ]
            if raw_obj.ancillary_data_set is not None
            else [],
            terms=[Term._from_v1_3(t) for t in raw_obj.term],
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.PolynomialType:
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

        return xtce_1_1.PolynomialType(term=[t._to_v1_1(policy) for t in self.terms])

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.PolynomialCalibratorType:
        return xtce_1_2.PolynomialCalibratorType(
            name=self.name,
            short_description=self.short_description,
            ancillary_data_set=xtce_1_2.AncillaryDataSetType(
                ancillary_data=[data._to_v1_2(policy) for data in self.ancillary_data]
            ),
            term=[t._to_v1_2(policy) for t in self.terms],
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.PolynomialCalibratorType:
        return xtce_1_3.PolynomialCalibratorType(
            name=self.name,
            short_description=self.short_description,
            ancillary_data_set=xtce_1_3.AncillaryDataSetType(
                ancillary_data=[data._to_v1_3(policy) for data in self.ancillary_data]
            ),
            term=[t._to_v1_3(policy) for t in self.terms],
        )


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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.CalibratorType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=[Alias._from_v1_1(alias) for alias in raw_obj.alias_set.alias]
            if raw_obj.alias_set
            else [],
            ancillary_data=[
                AncillaryData._from_v1_1(data)
                for data in raw_obj.ancillary_data_set.ancillary_data
            ]
            if raw_obj.ancillary_data_set
            else [],
            calibrator_type=SplineCalibrator._from_v1_1(raw_obj.choice)
            if isinstance(raw_obj.choice, xtce_1_1.CalibratorType.SplineCalibrator)
            else PolynomialCalibrator._from_v1_1(raw_obj.choice)
            if isinstance(raw_obj.choice, xtce_1_1.PolynomialType)
            else MathOperationCalibrator._from_v1_1(unwrap(raw_obj.choice)),
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.CalibratorType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            ancillary_data=[
                AncillaryData._from_v1_2(data)
                for data in raw_obj.ancillary_data_set.ancillary_data
            ]
            if raw_obj.ancillary_data_set
            else [],
            calibrator_type=SplineCalibrator._from_v1_2(raw_obj.choice)
            if isinstance(raw_obj.choice, xtce_1_2.SplineCalibratorType)
            else PolynomialCalibrator._from_v1_2(raw_obj.choice)
            if isinstance(raw_obj.choice, xtce_1_2.PolynomialCalibratorType)
            else MathOperationCalibrator._from_v1_2(unwrap(raw_obj.choice)),
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.CalibratorType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            ancillary_data=[
                AncillaryData._from_v1_3(data)
                for data in raw_obj.ancillary_data_set.ancillary_data
            ]
            if raw_obj.ancillary_data_set
            else [],
            calibrator_type=SplineCalibrator._from_v1_3(raw_obj.choice)
            if isinstance(raw_obj.choice, xtce_1_3.SplineCalibratorType)
            else PolynomialCalibrator._from_v1_3(raw_obj.choice)
            if isinstance(raw_obj.choice, xtce_1_3.PolynomialCalibratorType)
            else MathOperationCalibrator._from_v1_3(unwrap(raw_obj.choice)),
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.CalibratorType:
        return xtce_1_1.CalibratorType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=xtce_1_1.AliasSetType(
                alias=[alias._to_v1_1(policy) for alias in self.aliases]
            ),
            ancillary_data_set=xtce_1_1.DescriptionType.AncillaryDataSet(
                ancillary_data=[data._to_v1_1(policy) for data in self.ancillary_data]
            ),
            choice=self.calibrator_type._to_v1_1(policy),
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.CalibratorType:
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

        return xtce_1_2.CalibratorType(
            name=self.name,
            short_description=self.short_description,
            ancillary_data_set=xtce_1_2.AncillaryDataSetType(
                ancillary_data=[data._to_v1_2(policy) for data in self.ancillary_data]
            ),
            choice=self.calibrator_type._to_v1_2(policy),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.CalibratorType:
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

        return xtce_1_3.CalibratorType(
            name=self.name,
            short_description=self.short_description,
            ancillary_data_set=xtce_1_3.AncillaryDataSetType(
                ancillary_data=[data._to_v1_3(policy) for data in self.ancillary_data]
            ),
            choice=self.calibrator_type._to_v1_3(policy),
        )


class ContextCalibrator(XtceBaseModel):
    """Define a context-specific calibrator.

    The calibration is only applied when the context match is true.

    """

    context_match: ContextMatch
    """The context match that determines when this calibrator is applied."""

    calibrator: Calibrator
    """The calibrator to apply when the context match is true."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.ContextCalibratorType) -> Self:
        return cls(
            context_match=ContextMatch._from_v1_1(raw_obj.context_match),
            calibrator=Calibrator._from_v1_1(raw_obj.calibrator),
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.ContextCalibratorType) -> Self:
        return cls(
            context_match=ContextMatch._from_v1_2(raw_obj.context_match),
            calibrator=Calibrator._from_v1_2(raw_obj.calibrator),
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.ContextCalibratorType) -> Self:
        return cls(
            context_match=ContextMatch._from_v1_3(raw_obj.context_match),
            calibrator=Calibrator._from_v1_3(raw_obj.calibrator),
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.ContextCalibratorType:
        return xtce_1_1.ContextCalibratorType(
            context_match=self.context_match._to_v1_1(policy),
            calibrator=self.calibrator._to_v1_1(policy),
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ContextCalibratorType:
        return xtce_1_2.ContextCalibratorType(
            context_match=self.context_match._to_v1_2(policy),
            calibrator=self.calibrator._to_v1_2(policy),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ContextCalibratorType:
        return xtce_1_3.ContextCalibratorType(
            context_match=self.context_match._to_v1_3(policy),
            calibrator=self.calibrator._to_v1_3(policy),
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


class MathOperation(MathOperationCalibrator, ABC):
    """Base class for math operations."""
