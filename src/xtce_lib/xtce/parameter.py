"""Parameter models."""

from __future__ import annotations

import datetime
from typing import Annotated, Any

from pydantic import AfterValidator, Field

from xtce_lib.common.xtce_path import XtcePath, require_regex
from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3
from xtce_lib.xtce._util import coerce, uncoerce

from ._base import XtceBaseModel
from ._pattern import NAME_REF_W_PATH
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
from .condition import MatchCriteria
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
from .time import TimeAssociation


class IntegerParameter(IntegerData):
    """Define an integer parameter."""

    default_alarm: NumericAlarm | None = None
    """The default alarm for this integer parameter."""

    context_alarms: list[NumericContextAlarm] = Field(default_factory=list)
    """The context alarms for this integer parameter."""

    _v1_1_type = xtce_1_1.ParameterTypeSetType.IntegerParameterType
    _v1_2_type = xtce_1_2.IntegerParameterType
    _v1_3_type = xtce_1_3.IntegerParameterType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.ParameterTypeSetType.IntegerParameterType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["default_alarm"] = (
            NumericAlarm._from_v1_1(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [
                NumericContextAlarm._from_v1_1(alarm)
                for alarm in obj.context_alarm_list.context_alarm
            ]
            if obj.context_alarm_list is not None
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.IntegerParameterType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["default_alarm"] = (
            NumericAlarm._from_v1_2(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [
                NumericContextAlarm._from_v1_2(alarm)
                for alarm in obj.context_alarm_list.context_alarm
            ]
            if obj.context_alarm_list is not None
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.IntegerParameterType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["default_alarm"] = (
            NumericAlarm._from_v1_3(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [
                NumericContextAlarm._from_v1_3(alarm)
                for alarm in obj.context_alarm_list.context_alarm
            ]
            if obj.context_alarm_list is not None
            else []
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_1(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["context_alarm_list"] = (
            xtce_1_1.ParameterTypeSetType.IntegerParameterType.ContextAlarmList(
                context_alarm=[alarm._to_v1_1(policy) for alarm in self.context_alarms]
            )
            if self.context_alarms
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_2(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["context_alarm_list"] = (
            xtce_1_2.NumericContextAlarmListType(
                context_alarm=[alarm._to_v1_2(policy) for alarm in self.context_alarms]
            )
            if self.context_alarms
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_3(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["context_alarm_list"] = (
            xtce_1_3.NumericContextAlarmListType(
                context_alarm=[alarm._to_v1_3(policy) for alarm in self.context_alarms]
            )
            if self.context_alarms
            else None
        )
        return kwargs


class FloatParameter(FloatData):
    """Define a float parameter."""

    default_alarm: NumericAlarm | None = None
    """The default alarm for this float parameter."""

    context_alarms: list[NumericContextAlarm] = Field(default_factory=list)
    """The context alarms for this float parameter."""

    _v1_1_type = xtce_1_1.ParameterTypeSetType.FloatParameterType
    _v1_2_type = xtce_1_2.FloatParameterType
    _v1_3_type = xtce_1_3.FloatParameterType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.ParameterTypeSetType.FloatParameterType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["default_alarm"] = (
            NumericAlarm._from_v1_1(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [
                NumericContextAlarm._from_v1_1(alarm)
                for alarm in obj.context_alarm_list.context_alarm
            ]
            if obj.context_alarm_list is not None
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.FloatParameterType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["default_alarm"] = (
            NumericAlarm._from_v1_2(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [
                NumericContextAlarm._from_v1_2(alarm)
                for alarm in obj.context_alarm_list.context_alarm
            ]
            if obj.context_alarm_list is not None
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.FloatParameterType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["default_alarm"] = (
            NumericAlarm._from_v1_3(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [
                NumericContextAlarm._from_v1_3(alarm)
                for alarm in obj.context_alarm_list.context_alarm
            ]
            if obj.context_alarm_list is not None
            else []
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_1(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["context_alarm_list"] = (
            xtce_1_1.ParameterTypeSetType.FloatParameterType.ContextAlarmList(
                context_alarm=[alarm._to_v1_1(policy) for alarm in self.context_alarms]
            )
            if self.context_alarms
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_2(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["context_alarm_list"] = (
            xtce_1_2.NumericContextAlarmListType(
                context_alarm=[alarm._to_v1_2(policy) for alarm in self.context_alarms]
            )
            if self.context_alarms
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_3(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["context_alarm_list"] = (
            xtce_1_3.NumericContextAlarmListType(
                context_alarm=[alarm._to_v1_3(policy) for alarm in self.context_alarms]
            )
            if self.context_alarms
            else None
        )
        return kwargs


class StringParameter(StringData):
    """Define a string parameter."""

    default_alarm: StringAlarm | None = None
    """The default alarm for this string parameter."""

    context_alarms: list[StringContextAlarm] = Field(default_factory=list)
    """The context alarms for this string parameter."""

    _v1_1_type = xtce_1_1.ParameterTypeSetType.StringParameterType
    _v1_2_type = xtce_1_2.StringParameterType
    _v1_3_type = xtce_1_3.StringParameterType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.ParameterTypeSetType.StringParameterType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["default_alarm"] = (
            StringAlarm._from_v1_1(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [
                StringContextAlarm._from_v1_1(alarm)
                for alarm in obj.context_alarm_list.context_alarm
            ]
            if obj.context_alarm_list is not None
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.StringParameterType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["default_alarm"] = (
            StringAlarm._from_v1_2(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [
                StringContextAlarm._from_v1_2(alarm)
                for alarm in obj.context_alarm_list.context_alarm
            ]
            if obj.context_alarm_list is not None
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.StringParameterType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["default_alarm"] = (
            StringAlarm._from_v1_3(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [
                StringContextAlarm._from_v1_3(alarm)
                for alarm in obj.context_alarm_list.context_alarm
            ]
            if obj.context_alarm_list is not None
            else []
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_1(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["context_alarm_list"] = (
            xtce_1_1.ParameterTypeSetType.StringParameterType.ContextAlarmList(
                context_alarm=[alarm._to_v1_1(policy) for alarm in self.context_alarms]
            )
            if self.context_alarms
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_2(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["context_alarm_list"] = (
            xtce_1_2.StringContextAlarmListType(
                context_alarm=[alarm._to_v1_2(policy) for alarm in self.context_alarms]
            )
            if self.context_alarms
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_3(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["context_alarm_list"] = (
            xtce_1_3.StringContextAlarmListType(
                context_alarm=[alarm._to_v1_3(policy) for alarm in self.context_alarms]
            )
            if self.context_alarms
            else None
        )
        return kwargs


class BinaryParameter(BinaryData):
    """Define a binary parameter."""

    default_alarm: BinaryAlarm | None = None
    """The default alarm for this binary parameter."""

    context_alarms: list[BinaryContextAlarm] = Field(default_factory=list)
    """The context alarms for this binary parameter."""

    _v1_1_type = xtce_1_1.ParameterTypeSetType.BinaryParameterType
    _v1_2_type = xtce_1_2.BinaryParameterType
    _v1_3_type = xtce_1_3.BinaryParameterType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.ParameterTypeSetType.BinaryParameterType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["default_alarm"] = (
            BinaryAlarm._from_v1_1(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [
                BinaryContextAlarm._from_v1_1(alarm)
                for alarm in obj.context_alarm_list.context_alarm
            ]
            if obj.context_alarm_list is not None
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.BinaryParameterType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["default_alarm"] = (
            BinaryAlarm._from_v1_2(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [
                BinaryContextAlarm._from_v1_2(alarm)
                for alarm in obj.binary_context_alarm_list.context_alarm
            ]
            if obj.binary_context_alarm_list is not None
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.BinaryParameterType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["default_alarm"] = (
            BinaryAlarm._from_v1_3(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [
                BinaryContextAlarm._from_v1_3(alarm)
                for alarm in obj.context_alarm_list.context_alarm
            ]
            if obj.context_alarm_list is not None
            else []
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_1(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["context_alarm_list"] = (
            xtce_1_1.ParameterTypeSetType.BinaryParameterType.ContextAlarmList(
                context_alarm=[alarm._to_v1_1(policy) for alarm in self.context_alarms]
            )
            if self.context_alarms
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_2(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["binary_context_alarm_list"] = (
            xtce_1_2.BinaryContextAlarmListType(
                context_alarm=[alarm._to_v1_2(policy) for alarm in self.context_alarms]
            )
            if self.context_alarms
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_3(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["context_alarm_list"] = (
            xtce_1_3.BinaryContextAlarmListType(
                context_alarm=[alarm._to_v1_3(policy) for alarm in self.context_alarms]
            )
            if self.context_alarms
            else None
        )
        return kwargs


class BooleanParameter(BooleanData):
    """Define a boolean parameter."""

    default_alarm: BooleanAlarm | None = None
    """The default alarm for this boolean parameter."""

    context_alarms: list[BooleanContextAlarm] = Field(default_factory=list)
    """The context alarms for this boolean parameter."""

    _v1_1_type = xtce_1_1.ParameterTypeSetType.BooleanParameterType
    _v1_2_type = xtce_1_2.BooleanParameterType
    _v1_3_type = xtce_1_3.BooleanParameterType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.ParameterTypeSetType.BooleanParameterType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["default_alarm"] = (
            BooleanAlarm._from_v1_1(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [
                BooleanContextAlarm._from_v1_1(alarm)
                for alarm in obj.context_alarm_list.context_alarm
            ]
            if obj.context_alarm_list is not None
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.BooleanParameterType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["default_alarm"] = (
            BooleanAlarm._from_v1_2(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [
                BooleanContextAlarm._from_v1_2(alarm)
                for alarm in obj.context_alarm_list.context_alarm
            ]
            if obj.context_alarm_list is not None
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.BooleanParameterType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["default_alarm"] = (
            BooleanAlarm._from_v1_3(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [
                BooleanContextAlarm._from_v1_3(alarm)
                for alarm in obj.context_alarm_list.context_alarm
            ]
            if obj.context_alarm_list is not None
            else []
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_1(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["context_alarm_list"] = (
            xtce_1_1.ParameterTypeSetType.BooleanParameterType.ContextAlarmList(
                context_alarm=[alarm._to_v1_1(policy) for alarm in self.context_alarms]
            )
            if self.context_alarms
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_2(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["context_alarm_list"] = (
            xtce_1_2.BooleanContextAlarmListType(
                context_alarm=[alarm._to_v1_2(policy) for alarm in self.context_alarms]
            )
            if self.context_alarms
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_3(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["context_alarm_list"] = (
            xtce_1_3.BooleanContextAlarmListType(
                context_alarm=[alarm._to_v1_3(policy) for alarm in self.context_alarms]
            )
            if self.context_alarms
            else None
        )
        return kwargs


class EnumeratedParameter(EnumeratedData):
    """Define an enumerated parameter."""

    default_alarm: EnumerationAlarm | None = None
    """The default alarm for this enumerated parameter."""

    context_alarms: list[EnumerationContextAlarm] = Field(default_factory=list)
    """The context alarms for this enumerated parameter."""

    _v1_1_type = xtce_1_1.ParameterTypeSetType.EnumeratedParameterType
    _v1_2_type = xtce_1_2.EnumeratedParameterType
    _v1_3_type = xtce_1_3.EnumeratedParameterType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.ParameterTypeSetType.EnumeratedParameterType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["default_alarm"] = (
            EnumerationAlarm._from_v1_1(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [EnumerationContextAlarm._from_v1_1(obj.context_alarm_list.context_alarm)]
            if obj.context_alarm_list is not None
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.EnumeratedParameterType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["default_alarm"] = (
            EnumerationAlarm._from_v1_2(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [
                EnumerationContextAlarm._from_v1_2(alarm)
                for alarm in obj.context_alarm_list.context_alarm
            ]
            if obj.context_alarm_list is not None
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.EnumeratedParameterType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["default_alarm"] = (
            EnumerationAlarm._from_v1_3(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [
                EnumerationContextAlarm._from_v1_3(alarm)
                for alarm in obj.context_alarm_list.context_alarm
            ]
            if obj.context_alarm_list is not None
            else []
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_list_length(
            field_name="context_alarms",
            current_value=self.context_alarms,
            min_length=0,
            max_length=1,
            target_version=XtceVersion.V1_1,
            policy=policy,
            fallback=self.context_alarms[:1],
        )

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_1(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["context_alarm_list"] = (
            xtce_1_1.ParameterTypeSetType.EnumeratedParameterType.ContextAlarmList(
                context_alarm=self.context_alarms[0]._to_v1_1(policy)
            )
            if self.context_alarms
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_2(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["context_alarm_list"] = (
            xtce_1_2.EnumerationContextAlarmListType(
                context_alarm=[alarm._to_v1_2(policy) for alarm in self.context_alarms]
            )
            if self.context_alarms
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_3(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["context_alarm_list"] = (
            xtce_1_3.EnumerationContextAlarmListType(
                context_alarm=[alarm._to_v1_3(policy) for alarm in self.context_alarms]
            )
            if self.context_alarms
            else None
        )
        return kwargs


class ArrayParameter(ArrayData):
    """Define an array parameter."""

    dimensions: list[Dimension] = Field(default_factory=list)
    """The dimensions of this array parameter."""

    _v1_1_type = xtce_1_1.ArrayDataTypeType
    _v1_2_type = xtce_1_2.ArrayParameterType
    _v1_3_type = xtce_1_3.ArrayParameterType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.ArrayDataTypeType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        # TODO maybe find a better way to handle this
        kwargs["dimensions"] = [
            Dimension(start_index=0, end_index=1)
            for _ in range(obj.number_of_dimensions)
        ]
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ArrayParameterType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["dimensions"] = [
            Dimension._from_v1_2(dim) for dim in obj.dimension_list.dimension
        ]
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ArrayParameterType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["dimensions"] = [
            Dimension._from_v1_3(dim) for dim in obj.dimension_list.dimension
        ]
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(
            policy, number_of_dimensions=len(self.dimensions)
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["dimension_list"] = xtce_1_2.DimensionListType(
            dimension=[dim._to_v1_2(policy) for dim in self.dimensions]
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["dimension_list"] = xtce_1_3.DimensionListType(
            dimension=[dim._to_v1_3(policy) for dim in self.dimensions]
        )
        return kwargs


class AggregateParameter(AggregateData):
    """Define an aggregate parameter."""

    _v1_1_type = xtce_1_1.AggregateDataType
    _v1_2_type = xtce_1_2.AggregateParameterType
    _v1_3_type = xtce_1_3.AggregateParameterType

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        return kwargs


class RelativeTimeParameter(RelativeTimeData):
    """Define a relative time parameter."""

    default_alarm: TimeAlarm | None = None
    """The default alarm for this relative time parameter."""

    context_alarms: list[TimeContextAlarm] = Field(default_factory=list)
    """The context alarms for this relative time parameter."""

    _v1_1_type = xtce_1_1.ParameterTypeSetType.RelativeTimeParameterType
    _v1_2_type = xtce_1_2.RelativeTimeParameterType
    _v1_3_type = xtce_1_3.RelativeTimeParameterType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.ParameterTypeSetType.RelativeTimeParameterType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["default_alarm"] = (
            TimeAlarm._from_v1_1(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [
                TimeContextAlarm._from_v1_1(alarm)
                for alarm in obj.context_alarm_list.context_alarm
            ]
            if obj.context_alarm_list is not None
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.RelativeTimeParameterType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["default_alarm"] = (
            TimeAlarm._from_v1_2(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [
                TimeContextAlarm._from_v1_2(alarm)
                for alarm in obj.context_alarm_list.context_alarm
            ]
            if obj.context_alarm_list is not None
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.RelativeTimeParameterType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["default_alarm"] = (
            TimeAlarm._from_v1_3(obj.default_alarm)
            if obj.default_alarm is not None
            else None
        )
        kwargs["context_alarms"] = (
            [
                TimeContextAlarm._from_v1_3(alarm)
                for alarm in obj.context_alarm_list.context_alarm
            ]
            if obj.context_alarm_list is not None
            else []
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_1(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["context_alarm_list"] = (
            xtce_1_1.ParameterTypeSetType.RelativeTimeParameterType.ContextAlarmList(
                context_alarm=[alarm._to_v1_1(policy) for alarm in self.context_alarms]
            )
            if self.context_alarms
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_2(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["context_alarm_list"] = (
            xtce_1_2.TimeContextAlarmListType(
                context_alarm=[alarm._to_v1_2(policy) for alarm in self.context_alarms]
            )
            if self.context_alarms
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["default_alarm"] = (
            self.default_alarm._to_v1_3(policy)
            if self.default_alarm is not None
            else None
        )
        kwargs["context_alarm_list"] = (
            xtce_1_3.TimeContextAlarmListType(
                context_alarm=[alarm._to_v1_3(policy) for alarm in self.context_alarms]
            )
            if self.context_alarms
            else None
        )
        return kwargs


class AbsoluteTimeParameter(AbsoluteTimeData):
    """Define an absolute time parameter."""

    _v1_1_type = xtce_1_1.AbsoluteTimeDataType
    _v1_2_type = xtce_1_2.AbsoluteTimeParameterType
    _v1_3_type = xtce_1_3.AbsoluteTimeParameterType

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        return kwargs


class PhysicalAddress(XtceBaseModel):
    """Define the physical address that this parameter is collected from.

    i.e. a memory location, a location on a data collection bus.

    """

    sub_address: PhysicalAddress | None = None
    """A sub-address within the physical address.

    Used to further specify the location if it fractionally occupies the address.

    """

    source_name: str | None = None
    """The name of the source from which this physical address is collected."""

    source_address: str | None = None
    """The address of the source from which this physical address is collected."""

    _v1_1_type = xtce_1_1.PhysicalAddressType
    _v1_2_type = xtce_1_2.PhysicalAddressType
    _v1_3_type = xtce_1_3.PhysicalAddressType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.PhysicalAddressType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["sub_address"] = (
            PhysicalAddress._from_v1_1(obj.sub_address)
            if obj.sub_address is not None
            else None
        )
        kwargs["source_name"] = obj.source_name
        kwargs["source_address"] = obj.source_address
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.PhysicalAddressType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["sub_address"] = (
            PhysicalAddress._from_v1_2(obj.sub_address)
            if obj.sub_address is not None
            else None
        )
        kwargs["source_name"] = obj.source_name
        kwargs["source_address"] = obj.source_address
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.PhysicalAddressType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["sub_address"] = (
            PhysicalAddress._from_v1_3(obj.sub_address)
            if obj.sub_address is not None
            else None
        )
        kwargs["source_name"] = obj.source_name
        kwargs["source_address"] = obj.source_address
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["sub_address"] = (
            self.sub_address._to_v1_1(policy) if self.sub_address is not None else None
        )
        kwargs["source_name"] = self.source_name
        kwargs["source_address"] = self.source_address
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["sub_address"] = (
            self.sub_address._to_v1_2(policy) if self.sub_address is not None else None
        )
        kwargs["source_name"] = self.source_name
        kwargs["source_address"] = self.source_address
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["sub_address"] = (
            self.sub_address._to_v1_3(policy) if self.sub_address is not None else None
        )
        kwargs["source_name"] = self.source_name
        kwargs["source_address"] = self.source_address
        return kwargs


class ParameterProperties(XtceBaseModel):
    """Define extended properties or attributes of a parameter."""

    system_name: str | None = None
    """The system name of the parameter."""

    validity_condition: MatchCriteria | None = None
    """The validity condition of the parameter."""

    physical_addresses: list[PhysicalAddress] = Field(default_factory=list)
    """The physical addresses associated with the parameter."""

    time_association: TimeAssociation | None = None
    """The time association of the parameter."""

    data_source: TelemetryDataSource | None = None
    """The data source of the parameter."""

    read_only: bool = False
    """Indicates if the parameter is read-only."""

    persistence: bool = True
    """Indicates if the parameter is persistent."""

    _v1_1_type = xtce_1_1.ParameterPropertiesType
    _v1_2_type = xtce_1_2.ParameterPropertiesType
    _v1_3_type = xtce_1_3.ParameterPropertiesType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.ParameterPropertiesType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["system_name"] = obj.system_name
        kwargs["validity_condition"] = (
            MatchCriteria._from_v1_1(obj.validity_condition)
            if obj.validity_condition is not None
            else None
        )
        kwargs["physical_addresses"] = (
            [
                PhysicalAddress._from_v1_1(pa)
                for pa in obj.physical_address_set.physical_address
            ]
            if obj.physical_address_set is not None
            else []
        )
        kwargs["time_association"] = (
            TimeAssociation._from_v1_1(obj.time_association)
            if obj.time_association is not None
            else None
        )
        kwargs["data_source"] = (
            TelemetryDataSource(obj.data_source.value)
            if obj.data_source is not None
            else None
        )
        kwargs["read_only"] = obj.read_only
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ParameterPropertiesType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["system_name"] = obj.system_name
        kwargs["validity_condition"] = (
            MatchCriteria._from_v1_2(obj.validity_condition)
            if obj.validity_condition is not None
            else None
        )
        kwargs["physical_addresses"] = (
            [
                PhysicalAddress._from_v1_2(pa)
                for pa in obj.physical_address_set.physical_address
            ]
            if obj.physical_address_set is not None
            else []
        )
        kwargs["time_association"] = (
            TimeAssociation._from_v1_2(obj.time_association)
            if obj.time_association is not None
            else None
        )
        kwargs["data_source"] = (
            TelemetryDataSource(obj.data_source.value)
            if obj.data_source is not None
            else None
        )
        kwargs["read_only"] = obj.read_only
        kwargs["persistence"] = obj.persistence
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ParameterPropertiesType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["system_name"] = obj.system_name
        kwargs["validity_condition"] = (
            MatchCriteria._from_v1_3(obj.validity_condition)
            if obj.validity_condition is not None
            else None
        )
        kwargs["physical_addresses"] = (
            [
                PhysicalAddress._from_v1_3(pa)
                for pa in obj.physical_address_set.physical_address
            ]
            if obj.physical_address_set is not None
            else []
        )
        kwargs["time_association"] = (
            TimeAssociation._from_v1_3(obj.time_association)
            if obj.time_association is not None
            else None
        )
        kwargs["data_source"] = (
            TelemetryDataSource(obj.data_source.value)
            if obj.data_source is not None
            else None
        )
        kwargs["read_only"] = obj.read_only
        kwargs["persistence"] = obj.persistence
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="persistence",
            current_value=self.persistence,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=True,
        )

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["system_name"] = self.system_name
        kwargs["validity_condition"] = (
            self.validity_condition._to_v1_1(policy)
            if self.validity_condition is not None
            else None
        )
        kwargs["physical_address_set"] = (
            xtce_1_1.ParameterPropertiesType.PhysicalAddressSet(
                physical_address=[pa._to_v1_1(policy) for pa in self.physical_addresses]
            )
            if self.physical_addresses
            else None
        )
        kwargs["time_association"] = (
            self.time_association._to_v1_1(policy)
            if self.time_association is not None
            else None
        )
        if self.data_source == TelemetryDataSource.GROUND:
            # TODO handle in enums.py later, too lazy right now
            self._enforce_unsupported_field(
                field_name="data_source",
                current_value=self.data_source,
                target_version=XtceVersion.V1_1,
                policy=policy,
                empty_value=None,
            )
            kwargs["data_source"] = None
        elif self.data_source is not None:
            kwargs["data_source"] = xtce_1_1.ParameterPropertiesTypeDataSource(
                self.data_source.value
            )
        else:
            kwargs["data_source"] = None
        kwargs["read_only"] = self.read_only
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["system_name"] = self.system_name
        kwargs["validity_condition"] = (
            self.validity_condition._to_v1_2(policy)
            if self.validity_condition is not None
            else None
        )
        kwargs["physical_address_set"] = (
            xtce_1_2.PhysicalAddressSetType(
                physical_address=[pa._to_v1_2(policy) for pa in self.physical_addresses]
            )
            if self.physical_addresses
            else None
        )
        kwargs["time_association"] = (
            self.time_association._to_v1_2(policy)
            if self.time_association is not None
            else None
        )
        kwargs["data_source"] = (
            xtce_1_2.TelemetryDataSourceType(self.data_source.value)
            if self.data_source is not None
            else None
        )
        kwargs["read_only"] = self.read_only
        kwargs["persistence"] = self.persistence
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["system_name"] = self.system_name
        kwargs["validity_condition"] = (
            self.validity_condition._to_v1_3(policy)
            if self.validity_condition is not None
            else None
        )
        kwargs["physical_address_set"] = (
            xtce_1_3.PhysicalAddressSetType(
                physical_address=[pa._to_v1_3(policy) for pa in self.physical_addresses]
            )
            if self.physical_addresses
            else None
        )
        kwargs["time_association"] = (
            self.time_association._to_v1_3(policy)
            if self.time_association is not None
            else None
        )
        kwargs["data_source"] = (
            xtce_1_3.TelemetryDataSourceType(self.data_source.value)
            if self.data_source is not None
            else None
        )
        kwargs["read_only"] = self.read_only
        kwargs["persistence"] = self.persistence
        return kwargs


class Parameter(NameDescriptionBase):
    """Define the properties and characteristics of a parameter."""

    parameter_type_ref: Annotated[
        XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))
    ] = Field(
        ...,
        examples=["TODO"],
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to a parameter type."""

    initial_value: (
        int
        | float
        | str
        | bool
        | bytes
        | datetime.timedelta
        | datetime.datetime
        | list[
            int | float | str | bool | bytes | datetime.timedelta | datetime.datetime
        ]
        | dict[
            str,
            int | float | str | bool | bytes | datetime.timedelta | datetime.datetime,
        ]
        | None
    ) = None
    """The initial value of the parameter."""

    properties: ParameterProperties | None = None
    """Optional additional properties for the parameter."""

    # TODO verify ref exists
    # TODO verify initial value is correct type
    # TODO verify initial value is within the bounds of the referenced parameter
    # TODO need handling for lists/dicts

    _v1_1_type = xtce_1_1.ParameterSetType.Parameter
    _v1_2_type = xtce_1_2.ParameterType
    _v1_3_type = xtce_1_3.ParameterType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.ParameterSetType.Parameter
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["parameter_type_ref"] = XtcePath(obj.parameter_type_ref)
        kwargs["initial_value"] = (
            coerce(obj.initial_value) if obj.initial_value is not None else None
        )
        kwargs["properties"] = (
            ParameterProperties._from_v1_1(obj.parameter_properties)
            if obj.parameter_properties is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ParameterType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["parameter_type_ref"] = XtcePath(obj.parameter_type_ref)
        kwargs["initial_value"] = (
            coerce(obj.initial_value) if obj.initial_value is not None else None
        )
        kwargs["properties"] = (
            ParameterProperties._from_v1_2(obj.parameter_properties)
            if obj.parameter_properties is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ParameterType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["parameter_type_ref"] = XtcePath(obj.parameter_type_ref)
        kwargs["initial_value"] = (
            coerce(obj.initial_value) if obj.initial_value is not None else None
        )
        kwargs["properties"] = (
            ParameterProperties._from_v1_3(obj.parameter_properties)
            if obj.parameter_properties is not None
            else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["parameter_type_ref"] = str(self.parameter_type_ref)
        if self.initial_value is None:
            initial_value = None
        elif isinstance(self.initial_value, (list, dict)):
            initial_value = str(self.initial_value)
        else:
            initial_value = uncoerce(self.initial_value)
        kwargs["initial_value"] = initial_value
        kwargs["parameter_properties"] = (
            self.properties._to_v1_1(policy) if self.properties is not None else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["parameter_type_ref"] = str(self.parameter_type_ref)
        if self.initial_value is None:
            initial_value = None
        elif isinstance(self.initial_value, (list, dict)):
            initial_value = str(self.initial_value)
        else:
            initial_value = uncoerce(self.initial_value)
        kwargs["initial_value"] = initial_value
        kwargs["parameter_properties"] = (
            self.properties._to_v1_2(policy) if self.properties is not None else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["parameter_type_ref"] = str(self.parameter_type_ref)
        if self.initial_value is None:
            initial_value = None
        elif isinstance(self.initial_value, (list, dict)):
            initial_value = str(self.initial_value)
        else:
            initial_value = uncoerce(self.initial_value)
        kwargs["initial_value"] = initial_value
        kwargs["parameter_properties"] = (
            self.properties._to_v1_3(policy) if self.properties is not None else None
        )
        return kwargs
