"""Model type aliases."""

from .algorithm import InputOutputTriggerAlgorithm, MathAlgorithm
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
from .command import BlockMetaCommand, MetaCommand
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
from .space_system import SpaceSystem
from .stream import CustomStream, FixedFrameStream, VariableFrameStream
from .telemetry import Message

ReferenceableXtceObject = (
    SpaceSystem
    | IntegerParameter
    | FloatParameter
    | StringParameter
    | BinaryParameter
    | BooleanParameter
    | EnumeratedParameter
    | ArrayParameter
    | AggregateParameter
    | RelativeTimeParameter
    | AbsoluteTimeParameter
    | Parameter
    | IntegerArgument
    | FloatArgument
    | StringArgument
    | BinaryArgument
    | BooleanArgument
    | EnumeratedArgument
    | ArrayArgument
    | AggregateArgument
    | RelativeTimeArgument
    | AbsoluteTimeArgument
    | MetaCommand
    | BlockMetaCommand
    | SequenceContainer
    | CustomStream
    | FixedFrameStream
    | VariableFrameStream
    | InputOutputTriggerAlgorithm
    | MathAlgorithm
    | Message
)
