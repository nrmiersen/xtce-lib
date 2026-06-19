"""Argument models."""

from pydantic import Field

from .array import ArgumentDimension
from .datatype import (
    AggregateData,
    ArgumentAbsoluteTimeData,
    ArgumentBinaryData,
    ArgumentBooleanData,
    ArgumentEnumeratedData,
    ArgumentFloatData,
    ArgumentIntegerData,
    ArgumentRelativeTimeData,
    ArgumentStringData,
    ArrayData,
)
from .range import ValidFloatRanges, ValidIntegerRanges


class IntegerArgument(ArgumentIntegerData):
    valid_ranges: ValidIntegerRanges | None = Field(default=None)


class FloatArgument(ArgumentFloatData):
    valid_ranges: ValidFloatRanges | None = Field(default=None)


class StringArgument(ArgumentStringData):
    # Nothing
    pass


class BinaryArgument(ArgumentBinaryData):
    # Nothing
    pass


class BooleanArgument(ArgumentBooleanData):
    # Nothing
    pass


class EnumeratedArgument(ArgumentEnumeratedData):
    # Nothing
    pass


class ArrayArgument(ArrayData):
    dimensions: list[ArgumentDimension] = Field(default_factory=list, min_length=1)


class AggregateArgument(AggregateData):
    # Nothing
    pass


class RelativeTimeArgument(ArgumentRelativeTimeData):
    # Nothing
    pass


class AbsoluteTimeArgument(ArgumentAbsoluteTimeData):
    # Nothing
    pass
