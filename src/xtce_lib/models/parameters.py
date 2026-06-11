"""Parameter models."""

from pydantic import Field

from ._base import XtceBaseModel
from .alarms import (
    BinaryAlarm,
    BinaryContextAlarm,
    BooleanAlarm,
    BooleanContextAlarm,
    EnumerationAlarm,
    EnumerationContextAlarm,
    NumericAlarm,
    NumericContextAlarm,
    StringAlarm,
    StringContextAlarm,
    TimeAlarm,
    TimeContextAlarm,
)
from .array import Dimension
from .common import NameDescriptionBase
from .datatypes import (
    AbsoluteTimeData,
    AggregateData,
    ArrayData,
    BinaryData,
    BooleanData,
    EnumeratedData,
    FloatData,
    IntegerData,
    RelativeTimeData,
    StringData,
)


class IntegerParameter(IntegerData):
    default_alarm: NumericAlarm | None = Field(default=None)
    context_alarms: list[NumericContextAlarm] = Field(
        default_factory=list, min_length=1
    )


class FloatParameter(FloatData):
    default_alarm: NumericAlarm | None = Field(default=None)
    context_alarms: list[NumericContextAlarm] = Field(
        default_factory=list, min_length=1
    )


class StringParameter(StringData):
    default_alarm: StringAlarm | None = Field(default=None)
    context_alarms: list[StringContextAlarm] = Field(default_factory=list, min_length=1)


class BinaryParameter(BinaryData):
    default_alarm: BinaryAlarm | None = Field(default=None)
    context_alarms: list[BinaryContextAlarm] = Field(default_factory=list, min_length=1)


class BooleanParameter(BooleanData):
    default_alarm: BooleanAlarm | None = Field(default=None)
    context_alarms: list[BooleanContextAlarm] = Field(
        default_factory=list, min_length=1
    )


class EnumeratedParameter(EnumeratedData):
    default_alarm: EnumerationAlarm | None = Field(default=None)
    context_alarms: list[EnumerationContextAlarm] = Field(
        default_factory=list, min_length=1
    )


class ArrayParameter(ArrayData):
    dimensions: list[Dimension] = Field(default_factory=list, min_length=1)


class AggregateParameter(AggregateData):
    # Nothing
    pass


class RelativeTimeParameter(RelativeTimeData):
    default_alarm: TimeAlarm | None = Field(default=None)
    context_alarms: list[TimeContextAlarm] = Field(default_factory=list, min_length=1)


class AbsoluteTimeParameter(AbsoluteTimeData):
    # Nothing
    pass


class ParameterProperties(XtceBaseModel):
    pass


class Parameter(NameDescriptionBase):
    properties: ParameterProperties | None = Field(default=None)
