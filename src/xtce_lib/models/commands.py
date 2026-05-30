"""Command models."""

from pydantic import Field

from ._base import XtceBaseModel
from .arguments import (
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
from .common import NameDescriptionBase, NameReferenceWithPath
from .containers import SequenceContainer
from .parameters import (
    AbsoluteTimeParameter,
    AggregateParameter,
    ArrayParameter,
    BinaryParameter,
    BooleanParameter,
    EnumeratedParameter,
    FloatParameter,
    IntegerParameter,
    Parameter,
    ParameterRef,
    RelativeTimeParameter,
    StringParameter,
)
from .processing import InputOutputTriggerAlgorithm, MathAlgorithm
from .stream import CustomStream, FixedFrameStream, VariableFrameStream


class MetaCommand(NameDescriptionBase):
    pass


class MetaCommandRef(NameReferenceWithPath):
    """A reference to a MetaCommand.

    Used to include a MetaCommand defined in another sub-system in this sub-system.
    """


class BlockMetaCommand(NameDescriptionBase):
    pass


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

    def validate(self):
        """Perform semantic validation of this CommandMetadata."""
        # TODO make sure there are no duplicate parameter names
