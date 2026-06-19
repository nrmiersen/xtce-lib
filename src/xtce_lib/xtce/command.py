"""Command models."""

import datetime

from pydantic import Field

from ._base import XtceBaseModel
from .algorithm import (
    InputOutputTriggerAlgorithm,
    MathAlgorithm,
)
from .argument import (
    AbsoluteTimeArgument,
    AggregateArgument,
    ArrayArgument,
    BinaryArgument,
    BooleanArgument,
    EnumeratedArgument,
    FloatArgument,
    IntegerArgument,
    RelativeTimeArgument,
    StringArgument,
)
from .calibrator import ArgumentMathOperation
from .common import NameDescriptionBase, NameReferenceWithPath
from .condition import ContextMatch, MatchCriteria
from .container import CommandContainer, SequenceContainer
from .enum import ConsequenceLevel, VerifierType
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
from .reference import ParameterRef
from .stream import CustomStream, FixedFrameStream, VariableFrameStream
from .verifier import VerifierSet


class Argument(NameDescriptionBase):
    # TODO maybe move to argument.py
    argument_type_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )
    initial_value: str | None = Field(default=None)  # TODO figure out typing


class ArgumentAssignment(XtceBaseModel):
    # TODO maybe move to argument.py
    name: str = Field(
        ..., pattern=r"([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)"
    )
    value: str = Field(...)  # TODO figure out typing
    # TODO validate type of value, validate ranges, validate enumerations


class BaseMetaCommand(XtceBaseModel):
    argument_assignments: list[ArgumentAssignment] = Field(
        default_factory=list, min_length=1
    )
    meta_command_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )


class TransmissionConstraint(MatchCriteria):
    argument_restrictions: list[ArgumentAssignment] = Field(
        default_factory=list, min_length=1
    )
    timeout: datetime.timedelta | None = Field(default=None)  # XmlDuration
    suspendable: bool = Field(default=False)


class Significance(XtceBaseModel):
    space_system_at_risk: str | None = Field(
        default=None, pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )
    reason_for_warning: str | None = Field(default=None)
    consequence_level: ConsequenceLevel = Field(default=ConsequenceLevel.NORMAL)


class ContextSignificance(XtceBaseModel):
    context_match: ContextMatch = Field(...)
    significance: Significance = Field(...)


class Interlock(XtceBaseModel):
    scope_to_space_system: str | None = Field(
        default=None, pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )
    verification_to_wait_for: VerifierType = Field(default=VerifierType.COMPLETE)
    verification_progress_percentage: float | None = Field(default=None)
    suspendable: bool = Field(default=False)


class ParameterToSet(XtceBaseModel):
    derivation_or_new_value: str | ArgumentMathOperation | None = Field(default=None)
    set_on_verification: VerifierType = Field(default=VerifierType.COMPLETE)


class ParameterToSuspendAlarmsOn(ParameterRef):
    suspense_time: datetime.timedelta = Field(...)  # XmlDuration
    verifier_to_trigger_on: VerifierType = Field(default=VerifierType.RELEASE)


class MetaCommand(NameDescriptionBase):
    base_meta_command: BaseMetaCommand | None = Field(default=None)
    system_name: str | None = Field(default=None)
    arguments: list[Argument] = Field(default_factory=list, min_length=1)
    command_container: CommandContainer | None = Field(default=None)
    transmission_constraints: list[TransmissionConstraint] = Field(
        default_factory=list, min_length=1
    )
    default_significance: Significance | None = Field(default=None)
    context_significance: list[ContextSignificance] = Field(
        default_factory=list, min_length=1
    )
    interlock: Interlock | None = Field(default=None)
    verifier_set: VerifierSet | None = Field(default=None)
    parameters_to_set: list[ParameterToSet] = Field(default_factory=list, min_length=1)
    parameters_to_suspend_alarms_on: list[ParameterToSuspendAlarmsOn] = Field(
        default_factory=list, min_length=1
    )
    abstract: bool = Field(default=False)


class MetaCommandRef(NameReferenceWithPath):
    """A reference to a MetaCommand.

    Used to include a MetaCommand defined in another sub-system in this sub-system.

    """


class MetaCommandStep(XtceBaseModel):
    argument_assignments: list[ArgumentAssignment] = Field(
        default_factory=list, min_length=1
    )
    meta_command_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )


class BlockMetaCommand(NameDescriptionBase):
    meta_command_steps: list[MetaCommandStep] = Field(
        default_factory=list, min_length=1
    )


class CommandMetadata(XtceBaseModel):
    """Command related metadata.

    Items defined in this area may refer to items defined in TelemetryMetadata.

    """

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
    """Parameters referenced by MetaCommands.

    These parameters are located here so that MetaCommand data can be built
    independently of TelemetryMetadata.

    """

    argument_types: list[
        IntegerArgument
        | FloatArgument
        | StringArgument
        | BinaryArgument
        | BooleanArgument
        | EnumeratedArgument
        | ArrayArgument
        | AggregateArgument
        | RelativeTimeArgument
        | AbsoluteTimeArgument
    ] = Field(default_factory=list)
    """A list of argument types.

    MetaCommand definitions can contain arguments and parameters. Arguments are user
    provided to the specific command definition. Parameters are
    provided/calculated/determined by the software creating the command instance. As a
    result, arguments contain separate type information. In some cases, arguments have
    different descriptive characteristics.

    """

    meta_commands: list[MetaCommand | MetaCommandRef | BlockMetaCommand] = Field(
        default_factory=list,
    )
    """A list of command definitions with their arguments, parameters, and container
    encoding descriptions.
    """

    # TODO validate the reference is a MetaCommand

    containers: list[SequenceContainer] = Field(
        default_factory=list,
        min_length=1,
    )
    """Similar to the telemetry containers, this contains containers that can be
    referenced/shared by MetaCommand definitions.
    """

    streams: list[CustomStream | FixedFrameStream | VariableFrameStream] = Field(
        default_factory=list,
    )
    """Contains an unordered set of streams."""

    algorithms: list[InputOutputTriggerAlgorithm | MathAlgorithm] = Field(
        default_factory=list,
    )
    """Contains an unordered set of algorithms."""

    def validate_semantics(self):
        """Perform semantic validation of this CommandMetadata."""
        # TODO make sure there are no duplicate parameter names
