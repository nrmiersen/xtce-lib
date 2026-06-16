"""Processing models."""

from __future__ import annotations

from pydantic import Field

from ._base import XtceBaseModel
from .common import AncillaryData, NameDescriptionBase
from .enum import (
    BitOrder,
    ChecksumTypeName,
    ComparisonOperator,
    MathOperators,
    ParityForm,
    ReferencePoint,
)
from .misc import Constant
from .reference import (
    ArgumentInstanceRef,
    InputParameterInstanceRef,
    OutputParameterRef,
    ParameterInstanceRef,
)
from .trigger import TriggerSet


class AlgorithmText(XtceBaseModel):
    value: str = Field(default="")  # TODO figure out what this is
    language: str = Field(default="pseudo")


class ExternalAlgorithm(XtceBaseModel):
    implementation_name: str = Field(...)
    algorithm_location: str = Field(...)


class SimpleAlgorithm(NameDescriptionBase):
    algorithm_text: AlgorithmText | None = Field(default=None)
    external_algorithms: list[ExternalAlgorithm] = Field(
        default_factory=list, min_length=1
    )


class InputAlgorithm(SimpleAlgorithm):
    inputs: list[InputParameterInstanceRef | Constant] = Field(default_factory=list)


class ArgumentInputAlgorithm(SimpleAlgorithm):
    inputs: list[InputParameterInstanceRef | ArgumentInstanceRef | Constant] = Field(
        default_factory=list
    )


class Comparison(ParameterInstanceRef):
    comparison_operator: ComparisonOperator = Field(
        default=ComparisonOperator.EQUALS_SIGN_EQUALS_SIGN
    )
    value: str = Field(...)  # TODO enforce type?


class ArgumentComparison(XtceBaseModel):
    instance: ParameterInstanceRef | ArgumentInstanceRef | None = Field(default=None)
    comparison_operator: ComparisonOperator = Field(
        default=ComparisonOperator.EQUALS_SIGN_EQUALS_SIGN
    )
    value: str = Field(...)


class BaseComparison(XtceBaseModel):
    # Nothing
    pass


class ComparisonCheck(BaseComparison):
    todo_name: list[ParameterInstanceRef | ComparisonOperator] = Field(
        default_factory=list,
        min_length=2,
        max_length=3,
    )
    value: str | None = Field(default=None)  # TODO enforce type?


class ArgumentComparisonCheck(BaseComparison):
    refs: list[ParameterInstanceRef | ArgumentInstanceRef] = Field(
        default_factory=list, max_length=2
    )
    comparison_operator: ComparisonOperator = Field(...)
    value: str | None = Field(default=None)


class BaseConditions(XtceBaseModel):
    # Nothing
    pass


class AndedConditions(BaseConditions):
    conditions: list[ComparisonCheck | OredConditions] = Field(
        default_factory=list, min_length=2
    )


class ArgumentAndedConditions(BaseConditions):
    conditions: list[ArgumentComparisonCheck | ArgumentOredConditions] = Field(
        default_factory=list, min_length=2
    )


class OredConditions(BaseConditions):
    conditions: list[ComparisonCheck | AndedConditions] = Field(
        default_factory=list, min_length=2
    )


class ArgumentOredConditions(BaseConditions):
    conditions: list[ArgumentComparisonCheck | ArgumentAndedConditions] = Field(
        default_factory=list, min_length=2
    )


class BooleanExpression(XtceBaseModel):
    comparison: ComparisonCheck | AndedConditions | OredConditions | None = Field(
        default=None
    )


class ArgumentBooleanExpression(XtceBaseModel):
    comparison: (
        ArgumentComparisonCheck
        | ArgumentAndedConditions
        | ArgumentOredConditions
        | None
    ) = Field(default=None)


class MatchCriteria(XtceBaseModel):
    criteria: (
        Comparison | list[Comparison] | BooleanExpression | InputAlgorithm | None
    ) = Field(
        default=None, min_length=1
    )  # TODO maybe still use separate ComparisonList object


class ArgumentMatchCriteria(XtceBaseModel):
    criteria: (
        ArgumentComparison
        | list[ArgumentComparison]
        | ArgumentBooleanExpression
        | ArgumentInputAlgorithm
        | None
    ) = Field(default=None, min_length=1)


class DiscreteLookup(MatchCriteria):
    value: int = Field(...)


class ArgumentDiscreteLookup(ArgumentMatchCriteria):
    value: int = Field(...)


class ContextMatch(MatchCriteria):
    # Nothing
    pass


class DiscreteLookupList(XtceBaseModel):
    """Describe an ordered table of integer values and associated conditions, forming a
    lookup table.

    The list may have duplicates. The table is evaluated from first to last, the first
    condition to be true returns the value associated with it.

    """

    lookups: list[DiscreteLookup] = Field(default_factory=list, min_length=1)
    """Describe a lookup condition set using discrete values from parameters."""

    default_value: int = Field(...)
    """In the event that no lookup condition evaluates to true, then this value will be
    used.
    """


class ArgumentDiscreteLookupList(XtceBaseModel):
    lookups: list[ArgumentDiscreteLookup] = Field(default_factory=list, min_length=1)
    default_value: int = Field(...)


class ValueOperand(XtceBaseModel):
    value: str = Field(default="")


class ThisParameterOperand(XtceBaseModel):
    value: str = Field(default="")


class MathOperationCalibrator(XtceBaseModel):
    operation: list[
        ValueOperand | ThisParameterOperand | MathOperators | ParameterInstanceRef
    ] = Field(default_factory=list)


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


class TriggeredMathOperation(MathOperation):
    trigger_set: TriggerSet = Field(...)
    output_parameter_ref: str = Field(
        ...,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
    )


class MathAlgorithm(NameDescriptionBase):
    math_operation: TriggeredMathOperation = Field(...)


class BaseCalibrator(XtceBaseModel):
    ancillary_data: list[AncillaryData] = Field(default_factory=list, min_length=1)
    name: str | None = Field(default=None)
    short_description: str | None = Field(default=None)


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


class InputOutputAlgorithm(InputAlgorithm):
    outputs: list[OutputParameterRef] = Field(default_factory=list, min_length=1)
    thread: bool = Field(default=False)


class InputOutputTriggerAlgorithm(InputOutputAlgorithm):
    triggers: TriggerSet | None = Field(default=None)
    trigger_container: str | None = Field(
        default=None,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
    )
    priority: int | None = Field(default=None)


class Checksum(XtceBaseModel):
    input_algorithm: InputAlgorithm | None = Field(default=None)
    bits_from_reference: int = Field(default=0, ge=0)
    reference: ReferencePoint = Field(default=ReferencePoint.START)
    name: ChecksumTypeName = Field(...)
    hash_size_in_bits: int | None = Field(default=None, ge=1)
    parameter_ref: str | None = Field(
        default=None,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
    )


class CRC(XtceBaseModel):
    polynomial: bytes = Field(...)
    init_remainder: bytes | None = Field(default=None)
    final_xor: bytes | None = Field(default=None)
    width: int = Field(..., ge=1)
    reflect_data: bool = Field(default=False)
    reflect_remainder: bool = Field(default=False)
    direction: BitOrder = Field(default=BitOrder.MOST_SIGNIFICANT_BIT_FIRST)
    bits_from_reference: int = Field(default=0, ge=0)
    reference: ReferencePoint = Field(default=ReferencePoint.START)
    parameter_ref: str | None = Field(
        default=None,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
    )


class XOR(XtceBaseModel):
    bits_from_reference: int = Field(default=0, ge=0)
    reference: ReferencePoint = Field(default=ReferencePoint.START)
    parameter_ref: str | None = Field(
        default=None,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
    )


class Parity(XtceBaseModel):
    parity_form: ParityForm = Field(...)
    bits_from_reference: int = Field(default=0, ge=0)
    reference: ReferencePoint = Field(default=ReferencePoint.START)
    parameter_ref: str | None = Field(
        default=None,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
    )


# TODO probably write base class for Checksum, CRC, XOR, Parity
