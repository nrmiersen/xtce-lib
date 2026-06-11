"""Alarm models."""

from pydantic import Field

from ._base import XtceBaseModel
from .common import AncillaryData
from .enums import ChangeBasis, ChangeSpan, ConcernLevel, RangeForm, TimeUnits
from .match import ContextMatch, MatchCriteria
from .processing import InputAlgorithm
from .range import FloatRange, MultiRangeType


class BaseAlarm(XtceBaseModel):
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    ancillary_data: list[AncillaryData] = Field(
        default_factory=list,
        min_length=1,
    )


class AlarmConditions(XtceBaseModel):
    watch_alarm: MatchCriteria | None = Field(default=None)
    warning_alarm: MatchCriteria | None = Field(default=None)
    distress_alarm: MatchCriteria | None = Field(default=None)
    critical_alarm: MatchCriteria | None = Field(default=None)
    severe_alarm: MatchCriteria | None = Field(default=None)


class CustomAlarm(BaseAlarm):
    input_algorithm: InputAlgorithm = Field(...)


class Alarm(BaseAlarm):
    alarm_type: AlarmConditions | CustomAlarm | None = Field(default=None)
    min_violations: int = Field(default=1, ge=1)
    min_conformances: int = Field(default=1, ge=1)
    disabled: bool = Field(default=False)


class AlarmRanges(BaseAlarm):
    watch_range: FloatRange | None = Field(default=None)
    warning_range: FloatRange | None = Field(default=None)
    distress_range: FloatRange | None = Field(default=None)
    critical_range: FloatRange | None = Field(default=None)
    severe_range: FloatRange | None = Field(default=None)
    range_form: RangeForm = Field(default=RangeForm.OUTSIDE)


class ChangeAlarmRanges(AlarmRanges):
    change_type: ChangeSpan = Field(default=ChangeSpan.CHANGE_PER_SECOND)
    change_basis: ChangeBasis = Field(default=ChangeBasis.ABSOLUTE_CHANGE)
    span_of_interest_samples: int = Field(default=1, ge=1)
    span_of_interest_seconds: float = Field(default=0.0, ge=0.0)


class AlarmMultiRanges(BaseAlarm):
    range: list[MultiRangeType] = Field(default_factory=list, min_length=1)


class NumericAlarm(Alarm):
    static_alarm_ranges: AlarmRanges | None = Field(default=None)
    change_alarm_ranges: ChangeAlarmRanges | None = Field(default=None)
    alarm_multi_ranges: AlarmMultiRanges | None = Field(default=None)


class NumericContextAlarm(NumericAlarm):
    context_match: ContextMatch = Field(...)


class StringAlarmLevel(XtceBaseModel):
    level: ConcernLevel = Field(...)
    match_pattern: str = Field(...)  # TODO check xsd


class StringAlarm(Alarm):
    alarms: list[StringAlarmLevel] = Field(default_factory=list, min_length=1)
    default_alarm_level: ConcernLevel = Field(default=ConcernLevel.NORMAL)


class StringContextAlarm(StringAlarm):
    context_match: ContextMatch = Field(...)


class BinaryAlarm(Alarm):
    pass


class BinaryContextAlarm(BinaryAlarm):
    context_match: ContextMatch = Field(...)


class BooleanAlarm(Alarm):
    pass


class BooleanContextAlarm(BooleanAlarm):
    context_match: ContextMatch = Field(...)


class EnumerationAlarmLevel(XtceBaseModel):
    level: ConcernLevel = Field(...)
    enumeration_label: str = Field(...)  # validate label exists


class EnumerationAlarm(Alarm):
    alarms: list[EnumerationAlarmLevel] = Field(default_factory=list, min_length=1)
    default_alarm_level: ConcernLevel = Field(default=ConcernLevel.NORMAL)


class EnumerationContextAlarm(EnumerationAlarm):
    context_match: ContextMatch = Field(...)


class TimeAlarmRanges(AlarmRanges):
    time_units: TimeUnits = Field(default=TimeUnits.SECONDS)


class TimeAlarm(Alarm):
    static_alarm_ranges: TimeAlarmRanges | None = Field(default=None)
    changes_per_second_alarm_ranges: TimeAlarmRanges | None = Field(default=None)


class TimeContextAlarm(TimeAlarm):
    context_match: ContextMatch = Field(...)
