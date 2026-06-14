"""Parameter models."""

from __future__ import annotations

from pydantic import Field

from ._base import XtceBaseModel
from .alarm import (
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
from .datatype import (
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
from .enum import TelemetryDataSource
from .processing import MatchCriteria
from .time import TimeAssociation


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


class PhysicalAddress(XtceBaseModel):
    sub_address: PhysicalAddress | None = Field(default=None)
    source_name: str | None = Field(default=None)
    source_address: str | None = Field(default=None)


class ParameterProperties(XtceBaseModel):
    system_name: str | None = Field(default=None)
    validity_condition: MatchCriteria | None = Field(default=None)
    physical_addresses: list[PhysicalAddress] = Field(default_factory=list)
    time_association: TimeAssociation | None = Field(default=None)
    data_source: TelemetryDataSource = Field(...)
    read_only: bool = Field(default=False)
    persistence: bool = Field(default=True)


class Parameter(NameDescriptionBase):
    properties: ParameterProperties | None = Field(default=None)
    parameter_type_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )
    initial_value: str | None = Field(default=None)

    # TODO verify ref exists
    # TODO verify initial value is correct type
    # TODO verify initial value is within the bounds of the referenced parameter
