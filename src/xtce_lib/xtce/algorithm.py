"""Algorithm models."""

from pydantic import Field

from ._base import XtceBaseModel
from .calibrator import MathOperation
from .common import NameDescriptionBase
from .enum import BitOrder, ChecksumTypeName, ParityForm, ReferencePoint
from .misc import Constant
from .reference import (
    ArgumentInstanceRef,
    InputParameterInstanceRef,
    OutputParameterRef,
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


class TriggeredMathOperation(MathOperation):
    trigger_set: TriggerSet = Field(...)
    output_parameter_ref: str = Field(
        ...,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
    )


class MathAlgorithm(NameDescriptionBase):
    math_operation: TriggeredMathOperation = Field(...)


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
