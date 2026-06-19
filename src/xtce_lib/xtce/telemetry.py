"""Telemetry models."""

from pydantic import Field

from ._base import XtceBaseModel
from .common import NameDescriptionBase, OptionalNameDescriptionBase
from .container import SequenceContainer
from .parameter import (
    AbsoluteTimeParameter,
    AggregateParameter,
    ArrayParameter,
    BinaryParameter,
    BooleanParameter,
    EnumeratedParameter,
    FloatParameter,
    IntegerParameter,
    Parameter,
    RelativeTimeParameter,
    StringParameter,
)
from .processing import InputOutputTriggerAlgorithm, MatchCriteria, MathAlgorithm
from .reference import ParameterRef
from .stream import CustomStream, FixedFrameStream, VariableFrameStream


class Message(NameDescriptionBase):
    match_criteria: MatchCriteria = Field(...)
    container_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )


class MessageSet(OptionalNameDescriptionBase):
    messages: list[Message] = Field(default_factory=list)


class TelemetryMetadata(XtceBaseModel):
    """Telemetry related metadata."""

    parameter_types: list[
        IntegerParameter
        | FloatParameter
        | StringParameter
        | BinaryParameter
        | BooleanParameter
        | EnumeratedParameter
        | ArrayParameter
        | AggregateParameter
        | RelativeTimeParameter
        | AbsoluteTimeParameter
    ] = Field(default_factory=list)
    """A list of parameter types."""
    parameters: list[Parameter | ParameterRef] = Field(default_factory=list)
    containers: list[SequenceContainer] = Field(default_factory=list, min_length=1)
    message_set: MessageSet | None = Field(default=None)
    streams: list[CustomStream | FixedFrameStream | VariableFrameStream] = Field(
        default_factory=list,
    )
    algorithms: list[InputOutputTriggerAlgorithm | MathAlgorithm] = Field(
        default_factory=list,
    )
