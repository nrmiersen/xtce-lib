"""Alarm models."""

from abc import ABC
from typing import Any, Self

from pydantic import Field, model_validator

from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from .algorithm import InputAlgorithm
from .common import AncillaryData
from .condition import ContextMatch, MatchCriteria
from .enum import ChangeBasis, ChangeSpan, ConcernLevel, RangeForm, TimeUnits
from .range import FloatRange, MultiRange


class BaseAlarm(XtceBaseModel, ABC):
    """Base class for alarms."""

    name: str | None = None
    """An optional name for the alarm.

    Applicable since: XTCE 1.2

    """

    description: str | None = None
    """An optional description for the alarm.

    Applicable since: XTCE 1.2

    """

    ancillary_data: list[AncillaryData] = Field(default_factory=list)
    """Used to contain any ancillary data associated with this alarm.

    Applicable since: XTCE 1.2

    """

    _v1_1_type = None
    _v1_2_type = xtce_1_2.BaseAlarmType
    _v1_3_type = xtce_1_3.BaseAlarmType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.BaseAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["name"] = obj.name
        kwargs["description"] = obj.short_description
        kwargs["ancillary_data"] = (
            [
                AncillaryData._from_v1_2_kwargs(ad)
                for ad in obj.ancillary_data_set.ancillary_data
            ]
            if obj.ancillary_data_set
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.BaseAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["name"] = obj.name
        kwargs["description"] = obj.short_description
        kwargs["ancillary_data"] = (
            [
                AncillaryData._from_v1_3_kwargs(ad)
                for ad in obj.ancillary_data_set.ancillary_data
            ]
            if obj.ancillary_data_set
            else []
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        version = XtceVersion.V1_1

        self._enforce_unsupported_field(
            field_name="name",
            current_value=self.name,
            empty_value=None,
            target_version=version,
            policy=policy,
        )
        self._enforce_unsupported_field(
            field_name="description",
            current_value=self.description,
            empty_value=None,
            target_version=version,
            policy=policy,
        )
        self._enforce_unsupported_field(
            field_name="ancillary_data",
            current_value=self.ancillary_data,
            empty_value=[],
            target_version=version,
            policy=policy,
        )
        return super()._to_v1_1_kwargs(policy)

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["name"] = self.name
        kwargs["short_description"] = self.description
        kwargs["ancillary_data_set"] = (
            xtce_1_2.AncillaryDataSetType(
                ancillary_data=[ad._to_v1_2(policy) for ad in self.ancillary_data]
            )
            if self.ancillary_data
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["name"] = self.name
        kwargs["short_description"] = self.description
        kwargs["ancillary_data_set"] = (
            xtce_1_3.AncillaryDataSetType(
                ancillary_data=[ad._to_v1_3(policy) for ad in self.ancillary_data]
            )
            if self.ancillary_data
            else None
        )
        return kwargs


class AlarmConditions(XtceBaseModel):
    """Define alarms that will be triggered when specific conditions are met."""

    watch_alarm: MatchCriteria | None = None
    """The lowest concern level alarm condition.

    Used to indicate an issue that is worth monitoring.

    """

    warning_alarm: MatchCriteria | None = None
    """The second lowest concern level alarm condition.

    Used to indicate that an issue may be developing.

    """

    distress_alarm: MatchCriteria | None = None
    """A concern level between warning and critical.

    Used to indicate an issue that requires attention.

    """

    critical_alarm: MatchCriteria | None = None
    """The second highest concern level alarm condition.

    Used to indicate an issue that requires prompt attention.

    """

    severe_alarm: MatchCriteria | None = None
    """The highest concern level alarm condition.

    Used to indicate an issue that requires immediate attention.

    """

    _v1_1_type = xtce_1_1.AlarmConditionsType
    _v1_2_type = xtce_1_2.AlarmConditionsType
    _v1_3_type = xtce_1_3.AlarmConditionsType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.AlarmConditionsType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["watch_alarm"] = obj.watch_alarm
        kwargs["warning_alarm"] = obj.warning_alarm
        kwargs["distress_alarm"] = obj.distress_alarm
        kwargs["critical_alarm"] = obj.critical_alarm
        kwargs["severe_alarm"] = obj.severe_alarm
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.AlarmConditionsType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["watch_alarm"] = obj.watch_alarm
        kwargs["warning_alarm"] = obj.warning_alarm
        kwargs["distress_alarm"] = obj.distress_alarm
        kwargs["critical_alarm"] = obj.critical_alarm
        kwargs["severe_alarm"] = obj.severe_alarm
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.AlarmConditionsType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["watch_alarm"] = obj.watch_alarm
        kwargs["warning_alarm"] = obj.warning_alarm
        kwargs["distress_alarm"] = obj.distress_alarm
        kwargs["critical_alarm"] = obj.critical_alarm
        kwargs["severe_alarm"] = obj.severe_alarm
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["watch_alarm"] = self.watch_alarm
        kwargs["warning_alarm"] = self.warning_alarm
        kwargs["distress_alarm"] = self.distress_alarm
        kwargs["critical_alarm"] = self.critical_alarm
        kwargs["severe_alarm"] = self.severe_alarm
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["watch_alarm"] = self.watch_alarm
        kwargs["warning_alarm"] = self.warning_alarm
        kwargs["distress_alarm"] = self.distress_alarm
        kwargs["critical_alarm"] = self.critical_alarm
        kwargs["severe_alarm"] = self.severe_alarm
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["watch_alarm"] = self.watch_alarm
        kwargs["warning_alarm"] = self.warning_alarm
        kwargs["distress_alarm"] = self.distress_alarm
        kwargs["critical_alarm"] = self.critical_alarm
        kwargs["severe_alarm"] = self.severe_alarm
        return kwargs


class CustomAlarm(BaseAlarm):
    """Define a custom alarm based on an input algorithm."""

    input_algorithm: InputAlgorithm
    """The input algorithm used to define the custom alarm.

    Should return a boolean value.

    """

    # TODO semantic validation to ensure return is bool

    _v1_1_type = None
    _v1_2_type = xtce_1_2.CustomAlarmType
    _v1_3_type = xtce_1_3.CustomAlarmType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.CustomAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["input_algorithm"] = InputAlgorithm._from_v1_2_kwargs(
            obj.input_algorithm
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.CustomAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["input_algorithm"] = InputAlgorithm._from_v1_3_kwargs(
            obj.input_algorithm
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["input_algorithm"] = self.input_algorithm._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["input_algorithm"] = self.input_algorithm._to_v1_3(policy)
        return kwargs


class Alarm(BaseAlarm, ABC):
    """Base class for all alarms."""

    alarm: AlarmConditions | CustomAlarm | None = None
    """The alarm conditions or custom alarm associated with this alarm."""

    min_violations: int = Field(default=1, ge=1)
    """The minimum number of consecutive violations required to trigger the alarm."""

    min_conformances: int | None = Field(default=None, ge=1)
    """The minimum number of consecutive instances that do not meet the alarm conditions
    required to leave the alarm state.

    If not set, the default value will match the value of `min_violations`.

    Applicable since: XTCE 1.2

    """

    disabled: bool = False
    """The initial state of the alarm.

    When True, no alarm will be triggered regardless of the alarm conditions.

    Applicable since: XTCE 1.3

    """

    @model_validator(mode="after")
    def check_min_conformances(self) -> Self:
        """If `min_conformances` is not set, assign it the value of `min_violations`."""
        if self.min_conformances is None:
            self.min_conformances = self.min_violations
        return self

    _v1_1_type = xtce_1_1.AlarmType
    _v1_2_type = xtce_1_2.AlarmType
    _v1_3_type = xtce_1_3.AlarmType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.AlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["alarm"] = (
            AlarmConditions._from_v1_1_kwargs(obj.choice)
            if isinstance(obj.choice, xtce_1_1.AlarmConditionsType)
            else CustomAlarm(input_algorithm=InputAlgorithm._from_v1_1(obj.choice))
            if isinstance(obj.choice, xtce_1_1.InputAlgorithmType)
            else None
        )
        kwargs["min_violations"] = obj.min_violations
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.AlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["alarm"] = (
            AlarmConditions._from_v1_2_kwargs(obj.choice)
            if isinstance(obj.choice, xtce_1_2.AlarmConditionsType)
            else CustomAlarm._from_v1_2_kwargs(obj.choice)
            if isinstance(obj.choice, xtce_1_2.CustomAlarmType)
            else None
        )
        kwargs["min_violations"] = obj.min_violations
        kwargs["min_conformances"] = obj.min_conformance
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.AlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["alarm"] = (
            AlarmConditions._from_v1_3_kwargs(obj.choice)
            if isinstance(obj.choice, xtce_1_3.AlarmConditionsType)
            else CustomAlarm._from_v1_3_kwargs(obj.choice)
            if isinstance(obj.choice, xtce_1_3.CustomAlarmType)
            else None
        )
        kwargs["min_violations"] = obj.min_violations
        kwargs["min_conformances"] = obj.min_conformance
        kwargs["disabled"] = obj.disabled
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # xtce_1_1.AlarmType has no parents
        kwargs = {}
        kwargs["choice"] = (
            self.alarm._to_v1_1(policy)
            if isinstance(self.alarm, AlarmConditions)
            else self.alarm.input_algorithm._to_v1_1(policy)
            if isinstance(self.alarm, CustomAlarm)
            else None
        )
        kwargs["min_violations"] = self.min_violations
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="disabled",
            current_value=self.disabled,
            empty_value=False,
            target_version=XtceVersion.V1_2,
            policy=policy,
        )

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = (
            self.alarm._to_v1_2(policy) if self.alarm is not None else None
        )
        kwargs["min_violations"] = self.min_violations
        kwargs["min_conformance"] = self.min_conformances
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = (
            self.alarm._to_v1_3(policy) if self.alarm is not None else None
        )
        kwargs["min_violations"] = self.min_violations
        kwargs["min_conformance"] = self.min_conformances
        kwargs["disabled"] = self.disabled
        return kwargs


class AlarmRanges(BaseAlarm):
    """Define the ranges for different alarm levels.

    All range values are in calibrated engineering units.

    """

    watch_range: FloatRange | None = None
    """The lowest concern level range.

    Used to indicate an issue that is worth monitoring.

    """

    warning_range: FloatRange | None = None
    """The second lowest concern level range.

    Used to indicate that an issue may be developing.

    """

    distress_range: FloatRange | None = None
    """A concern level between warning and critical range.

    Used to indicate an issue that requires attention.

    """

    critical_range: FloatRange | None = None
    """The second highest concern level range.

    Used to indicate an issue that requires prompt attention.

    """

    severe_range: FloatRange | None = None
    """The highest concern level range.

    Used to indicate an issue that requires immediate attention.

    """

    range_form: RangeForm = RangeForm.OUTSIDE
    """The form of the ranges.

    A value of `OUTSIDE` specifies that the most severe range is outside all the other
    ranges:

        -severe -critical -distress -warning -watch
        normal
        +watch +warning +distress +critical +severe

    This means each min, max pair are a range: (-inf, min) or (-inf, min], and
    [max, inf) or (max, inf). However a value of `INSIDE` "inverts" these bands:

        -normal -watch -warning -distress -critical
        severe
        +critical +distress +warning +watch +normal

    This means each min, max pair form a range of (min, max) or [min, max) or (min, max]
    or [min, max]. The most common form used is `OUTSIDE` and it is the default (The set
    notation used defines parenthesis as exclusive and square brackets as inclusive).

    """

    _v1_1_type = xtce_1_1.AlarmRangesType
    _v1_2_type = xtce_1_2.AlarmRangesType
    _v1_3_type = xtce_1_3.AlarmRangesType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.AlarmRangesType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["watch_range"] = (
            FloatRange._from_v1_1_kwargs(obj.watch_range)
            if obj.watch_range is not None
            else None
        )
        kwargs["warning_range"] = (
            FloatRange._from_v1_1_kwargs(obj.warning_range)
            if obj.warning_range is not None
            else None
        )
        kwargs["distress_range"] = (
            FloatRange._from_v1_1_kwargs(obj.distress_range)
            if obj.distress_range is not None
            else None
        )
        kwargs["critical_range"] = (
            FloatRange._from_v1_1_kwargs(obj.critical_range)
            if obj.critical_range is not None
            else None
        )
        kwargs["severe_range"] = (
            FloatRange._from_v1_1_kwargs(obj.severe_range)
            if obj.severe_range is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.AlarmRangesType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["watch_range"] = (
            FloatRange._from_v1_2_kwargs(obj.watch_range)
            if obj.watch_range is not None
            else None
        )
        kwargs["warning_range"] = (
            FloatRange._from_v1_2_kwargs(obj.warning_range)
            if obj.warning_range is not None
            else None
        )
        kwargs["distress_range"] = (
            FloatRange._from_v1_2_kwargs(obj.distress_range)
            if obj.distress_range is not None
            else None
        )
        kwargs["critical_range"] = (
            FloatRange._from_v1_2_kwargs(obj.critical_range)
            if obj.critical_range is not None
            else None
        )
        kwargs["severe_range"] = (
            FloatRange._from_v1_2_kwargs(obj.severe_range)
            if obj.severe_range is not None
            else None
        )
        kwargs["range_form"] = RangeForm(obj.range_form.value)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.AlarmRangesType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["watch_range"] = (
            FloatRange._from_v1_3_kwargs(obj.watch_range)
            if obj.watch_range is not None
            else None
        )
        kwargs["warning_range"] = (
            FloatRange._from_v1_3_kwargs(obj.warning_range)
            if obj.warning_range is not None
            else None
        )
        kwargs["distress_range"] = (
            FloatRange._from_v1_3_kwargs(obj.distress_range)
            if obj.distress_range is not None
            else None
        )
        kwargs["critical_range"] = (
            FloatRange._from_v1_3_kwargs(obj.critical_range)
            if obj.critical_range is not None
            else None
        )
        kwargs["severe_range"] = (
            FloatRange._from_v1_3_kwargs(obj.severe_range)
            if obj.severe_range is not None
            else None
        )
        kwargs["range_form"] = RangeForm(obj.range_form.value)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="range_form",
            current_value=self.range_form,
            empty_value=RangeForm.OUTSIDE,
            target_version=XtceVersion.V1_1,
            policy=policy,
        )

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["watch_range"] = (
            self.watch_range._to_v1_1(policy) if self.watch_range is not None else None
        )
        kwargs["warning_range"] = (
            self.warning_range._to_v1_1(policy)
            if self.warning_range is not None
            else None
        )
        kwargs["distress_range"] = (
            self.distress_range._to_v1_1(policy)
            if self.distress_range is not None
            else None
        )
        kwargs["critical_range"] = (
            self.critical_range._to_v1_1(policy)
            if self.critical_range is not None
            else None
        )
        kwargs["severe_range"] = (
            self.severe_range._to_v1_1(policy)
            if self.severe_range is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["watch_range"] = (
            self.watch_range._to_v1_2(policy) if self.watch_range is not None else None
        )
        kwargs["warning_range"] = (
            self.warning_range._to_v1_2(policy)
            if self.warning_range is not None
            else None
        )
        kwargs["distress_range"] = (
            self.distress_range._to_v1_2(policy)
            if self.distress_range is not None
            else None
        )
        kwargs["critical_range"] = (
            self.critical_range._to_v1_2(policy)
            if self.critical_range is not None
            else None
        )
        kwargs["severe_range"] = (
            self.severe_range._to_v1_2(policy)
            if self.severe_range is not None
            else None
        )
        kwargs["range_form"] = xtce_1_2.RangeFormType(self.range_form.value)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["watch_range"] = (
            self.watch_range._to_v1_3(policy) if self.watch_range is not None else None
        )
        kwargs["warning_range"] = (
            self.warning_range._to_v1_3(policy)
            if self.warning_range is not None
            else None
        )
        kwargs["distress_range"] = (
            self.distress_range._to_v1_3(policy)
            if self.distress_range is not None
            else None
        )
        kwargs["critical_range"] = (
            self.critical_range._to_v1_3(policy)
            if self.critical_range is not None
            else None
        )
        kwargs["severe_range"] = (
            self.severe_range._to_v1_3(policy)
            if self.severe_range is not None
            else None
        )
        kwargs["range_form"] = xtce_1_3.RangeFormType(self.range_form.value)
        return kwargs


class ChangeAlarmRanges(AlarmRanges):
    """Define an alarm that is triggered when the parameter value's rate of change is
    either too fast or too slow.

    The change rate may be with respect to time or with respect to samples (see
    `change_type`). The change may also be either relative (percentage change) or
    absolute (see `change_basis`).

    """

    # TODO this could probably get cleaned up with just a single attribute that's either
    # ChangePerSecondAlarm or ChangePerSampleAlarm

    change_type: ChangeSpan = ChangeSpan.CHANGE_PER_SECOND
    """The type of change rate."""

    change_basis: ChangeBasis = ChangeBasis.ABSOLUTE_CHANGE
    """The basis of the change."""

    span_of_interest_samples: int = Field(default=1, ge=1)
    """The number of samples that the change is measured over."""

    span_of_interest_seconds: float = Field(default=0.0, ge=0.0)
    """The time duration over which the change is measured."""

    _v1_1_type = xtce_1_1.NumericAlarmType.ChangeAlarmRanges
    _v1_2_type = xtce_1_2.ChangeAlarmRangesType
    _v1_3_type = xtce_1_3.ChangeAlarmRangesType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.NumericAlarmType.ChangeAlarmRanges
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["change_type"] = ChangeSpan(obj.change_type.value)
        kwargs["change_basis"] = ChangeBasis(obj.change_basis.value)
        kwargs["span_of_interest_samples"] = obj.span_of_interest_in_samples
        kwargs["span_of_interest_seconds"] = obj.span_of_interest_in_seconds
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ChangeAlarmRangesType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["change_type"] = ChangeSpan(obj.change_type.value)
        kwargs["change_basis"] = ChangeBasis(obj.change_basis.value)
        kwargs["span_of_interest_samples"] = obj.span_of_interest_in_samples
        kwargs["span_of_interest_seconds"] = obj.span_of_interest_in_seconds
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ChangeAlarmRangesType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["change_type"] = ChangeSpan(obj.change_type.value)
        kwargs["change_basis"] = ChangeBasis(obj.change_basis.value)
        kwargs["span_of_interest_samples"] = obj.span_of_interest_in_samples
        kwargs["span_of_interest_seconds"] = obj.span_of_interest_in_seconds
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["change_type"] = xtce_1_1.ChangeAlarmRangesChangeType(
            self.change_type.value
        )
        kwargs["change_basis"] = xtce_1_1.ChangeAlarmRangesChangeBasis(
            self.change_basis.value
        )
        kwargs["span_of_interest_in_samples"] = self.span_of_interest_samples
        kwargs["span_of_interest_in_seconds"] = self.span_of_interest_seconds
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["change_type"] = xtce_1_2.ChangeSpanType(self.change_type.value)
        kwargs["change_basis"] = xtce_1_2.ChangeBasisType(self.change_basis.value)
        kwargs["span_of_interest_in_samples"] = self.span_of_interest_samples
        kwargs["span_of_interest_in_seconds"] = self.span_of_interest_seconds
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["change_type"] = xtce_1_3.ChangeSpanType(self.change_type.value)
        kwargs["change_basis"] = xtce_1_3.ChangeBasisType(self.change_basis.value)
        kwargs["span_of_interest_in_samples"] = self.span_of_interest_samples
        kwargs["span_of_interest_in_seconds"] = self.span_of_interest_seconds
        return kwargs


class TimeAlarmRanges(AlarmRanges):
    """Define alarm ranges for time-based alarms."""

    time_units: TimeUnits = TimeUnits.SECONDS
    """The units of time for the time-based alarm ranges."""

    _v1_1_type = None  # Defined as separate child classes TimeAlarmType
    _v1_2_type = xtce_1_2.TimeAlarmRangesType
    _v1_3_type = xtce_1_3.TimeAlarmRangesType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.TimeAlarmRangesType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["time_units"] = TimeUnits._from_v1_2(obj.time_units)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.TimeAlarmRangesType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["time_units"] = TimeUnits._from_v1_3(obj.time_units)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["time_units"] = self.time_units._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["time_units"] = self.time_units._to_v1_3(policy)
        return kwargs


class AlarmMultiRanges(BaseAlarm):
    """Define any number of alarm ranges."""

    ranges: list[MultiRange] = Field(default_factory=list)
    """List of multiple alarm ranges."""

    _v1_1_type = None
    _v1_2_type = xtce_1_2.AlarmMultiRangesType
    _v1_3_type = xtce_1_3.AlarmMultiRangesType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.AlarmMultiRangesType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["ranges"] = [MultiRange._from_v1_2(r) for r in obj.range]
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.AlarmMultiRangesType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["ranges"] = [MultiRange._from_v1_3(r) for r in obj.range]
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["range"] = [r._to_v1_2(policy) for r in self.ranges]
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["range"] = [r._to_v1_3(policy) for r in self.ranges]
        return kwargs


class StringAlarmLevel(XtceBaseModel):
    """Define a string alarm condition based on a regular expression."""

    level: ConcernLevel
    """The level of concern for this alarm."""

    match_pattern: str
    """The regular expression pattern to match for this alarm."""

    _v1_1_type = xtce_1_1.StringAlarmType.StringAlarmList.StringAlarm
    _v1_2_type = xtce_1_2.StringAlarmLevelType
    _v1_3_type = xtce_1_3.StringAlarmLevelType

    # TODO validate regex in validate_semantics - just throw warning

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.StringAlarmType.StringAlarmList.StringAlarm
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["level"] = ConcernLevel(obj.alarm_level.value)
        kwargs["match_pattern"] = obj.match_pattern
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.StringAlarmLevelType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["level"] = ConcernLevel(obj.alarm_level.value)
        kwargs["match_pattern"] = obj.match_pattern
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.StringAlarmLevelType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["level"] = ConcernLevel(obj.alarm_level.value)
        kwargs["match_pattern"] = obj.match_pattern
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["alarm_level"] = xtce_1_1.AlarmLevels(self.level.value)
        kwargs["match_pattern"] = self.match_pattern
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["alarm_level"] = xtce_1_2.ConcernLevelsType(self.level.value)
        kwargs["match_pattern"] = self.match_pattern
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["alarm_level"] = xtce_1_3.ConcernLevelsType(self.level.value)
        kwargs["match_pattern"] = self.match_pattern
        return kwargs


class EnumerationAlarmLevel(XtceBaseModel):
    """Define an enumeration alarm condition based on a specific enumeration label."""

    level: ConcernLevel
    """The level of concern for this alarm."""

    enumeration_label: str
    """The specific enumeration label that triggers this alarm."""

    _v1_1_type = xtce_1_1.EnumerationAlarmType.EnumerationAlarmList.EnumerationAlarm
    _v1_2_type = xtce_1_2.EnumerationAlarmLevelType
    _v1_3_type = xtce_1_3.EnumerationAlarmLevelType

    # TODO validate that the enumeration_label exists in the enumeration
    # Probably better to do this in a model_validator in the actual enumeration class

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.EnumerationAlarmType.EnumerationAlarmList.EnumerationAlarm
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["level"] = ConcernLevel(obj.alarm_level.value)
        kwargs["enumeration_label"] = obj.enumeration_value
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.EnumerationAlarmLevelType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["level"] = ConcernLevel(obj.alarm_level.value)
        kwargs["enumeration_label"] = obj.enumeration_label
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.EnumerationAlarmLevelType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["level"] = ConcernLevel(obj.alarm_level.value)
        kwargs["enumeration_label"] = obj.enumeration_label
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["alarm_level"] = xtce_1_1.AlarmLevels(self.level.value)
        kwargs["enumeration_value"] = self.enumeration_label
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["alarm_level"] = xtce_1_2.ConcernLevelsType(self.level.value)
        kwargs["enumeration_label"] = self.enumeration_label
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["alarm_level"] = xtce_1_3.ConcernLevelsType(self.level.value)
        kwargs["enumeration_label"] = self.enumeration_label
        return kwargs


class NumericAlarm(Alarm):
    """Define an alarm for numeric data types."""

    static_alarm_ranges: AlarmRanges | None = None
    """Ranges where the alarm is triggered when the parameter value passes some
    threshold value.
    """

    change_alarm_ranges: ChangeAlarmRanges | None = None
    """Ranges where the alarm is triggered when the parameter value changes by a rate or
    quantity from a reference.
    """

    alarm_multi_ranges: AlarmMultiRanges | None = None
    """Similar to `static_alarm_ranges`, but more lenient."""

    _v1_1_type = xtce_1_1.NumericAlarmType
    _v1_2_type = xtce_1_2.NumericAlarmType
    _v1_3_type = xtce_1_3.NumericAlarmType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.NumericAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["static_alarm_ranges"] = (
            AlarmRanges._from_v1_1_kwargs(obj.static_alarm_ranges)
            if obj.static_alarm_ranges is not None
            else None
        )
        kwargs["change_alarm_ranges"] = (
            ChangeAlarmRanges._from_v1_1_kwargs(obj.change_alarm_ranges)
            if obj.change_alarm_ranges is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.NumericAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["static_alarm_ranges"] = (
            AlarmRanges._from_v1_2_kwargs(obj.static_alarm_ranges)
            if obj.static_alarm_ranges is not None
            else None
        )
        kwargs["change_alarm_ranges"] = (
            ChangeAlarmRanges._from_v1_2_kwargs(obj.change_alarm_ranges)
            if obj.change_alarm_ranges is not None
            else None
        )
        kwargs["alarm_multi_ranges"] = (
            AlarmMultiRanges._from_v1_2_kwargs(obj.alarm_multi_ranges)
            if obj.alarm_multi_ranges is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.NumericAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["static_alarm_ranges"] = (
            AlarmRanges._from_v1_3_kwargs(obj.static_alarm_ranges)
            if obj.static_alarm_ranges is not None
            else None
        )
        kwargs["change_alarm_ranges"] = (
            ChangeAlarmRanges._from_v1_3_kwargs(obj.change_alarm_ranges)
            if obj.change_alarm_ranges is not None
            else None
        )
        kwargs["alarm_multi_ranges"] = (
            AlarmMultiRanges._from_v1_3_kwargs(obj.alarm_multi_ranges)
            if obj.alarm_multi_ranges is not None
            else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="alarm_multi_ranges",
            current_value=self.alarm_multi_ranges,
            empty_value=None,
            target_version=XtceVersion.V1_1,
            policy=policy,
        )

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["static_alarm_ranges"] = (
            self.static_alarm_ranges._to_v1_1(policy)
            if self.static_alarm_ranges is not None
            else None
        )
        kwargs["change_alarm_ranges"] = (
            self.change_alarm_ranges._to_v1_1(policy)
            if self.change_alarm_ranges is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["static_alarm_ranges"] = (
            self.static_alarm_ranges._to_v1_2(policy)
            if self.static_alarm_ranges is not None
            else None
        )
        kwargs["change_alarm_ranges"] = (
            self.change_alarm_ranges._to_v1_2(policy)
            if self.change_alarm_ranges is not None
            else None
        )
        kwargs["alarm_multi_ranges"] = (
            self.alarm_multi_ranges._to_v1_2(policy)
            if self.alarm_multi_ranges is not None
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["static_alarm_ranges"] = (
            self.static_alarm_ranges._to_v1_3(policy)
            if self.static_alarm_ranges is not None
            else None
        )
        kwargs["change_alarm_ranges"] = (
            self.change_alarm_ranges._to_v1_3(policy)
            if self.change_alarm_ranges is not None
            else None
        )
        kwargs["alarm_multi_ranges"] = (
            self.alarm_multi_ranges._to_v1_3(policy)
            if self.alarm_multi_ranges is not None
            else None
        )
        return kwargs


class StringAlarm(Alarm):
    """Define an alarm for string data types."""

    alarms: list[StringAlarmLevel] = Field(default_factory=list)
    """List of alarm levels for the alarm.

    Alarms are processed in the order they appear in the list.

    """

    default_level: ConcernLevel = ConcernLevel.NORMAL
    """Default alarm level for the alarm."""

    _v1_1_type = xtce_1_1.StringAlarmType
    _v1_2_type = xtce_1_2.StringAlarmType
    _v1_3_type = xtce_1_3.StringAlarmType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.StringAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["alarms"] = [
            StringAlarmLevel._from_v1_1(a) for a in obj.string_alarm_list.string_alarm
        ]
        kwargs["default_level"] = ConcernLevel(obj.default_alarm_level.value)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.StringAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["alarms"] = (
            [StringAlarmLevel._from_v1_2(a) for a in obj.string_alarm_list.string_alarm]
            if obj.string_alarm_list is not None
            else []
        )
        kwargs["default_level"] = ConcernLevel(obj.default_alarm_level.value)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.StringAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["alarms"] = (
            [StringAlarmLevel._from_v1_3(a) for a in obj.string_alarm_list.string_alarm]
            if obj.string_alarm_list is not None
            else []
        )
        kwargs["default_level"] = ConcernLevel(obj.default_alarm_level.value)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["string_alarm_list"] = xtce_1_1.StringAlarmType.StringAlarmList(
            string_alarm=[a._to_v1_1(policy) for a in self.alarms]
        )
        kwargs["default_alarm_level"] = xtce_1_1.AlarmLevels(self.default_level.value)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["string_alarm_list"] = xtce_1_2.StringAlarmListType(
            string_alarm=[a._to_v1_2(policy) for a in self.alarms]
        )
        kwargs["default_alarm_level"] = xtce_1_2.ConcernLevelsType(
            self.default_level.value
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["string_alarm_list"] = xtce_1_3.StringAlarmListType(
            string_alarm=[a._to_v1_3(policy) for a in self.alarms]
        )
        kwargs["default_alarm_level"] = xtce_1_3.ConcernLevelsType(
            self.default_level.value
        )
        return kwargs


class BinaryAlarm(Alarm):
    """Define an alarm for binary data types."""

    _v1_1_type = xtce_1_1.BinaryAlarmConditionType
    _v1_2_type = xtce_1_2.BinaryAlarmType
    _v1_3_type = xtce_1_3.BinaryAlarmType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.BinaryAlarmConditionType
    ) -> dict[str, Any]:
        return super()._from_v1_1_kwargs(obj)

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.BinaryAlarmType) -> dict[str, Any]:
        return super()._from_v1_2_kwargs(obj)

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.BinaryAlarmType) -> dict[str, Any]:
        return super()._from_v1_3_kwargs(obj)

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        return super()._to_v1_1_kwargs(policy)

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        return super()._to_v1_2_kwargs(policy)

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        return super()._to_v1_3_kwargs(policy)


class BooleanAlarm(Alarm):
    """Define an alarm for boolean data types."""

    _v1_1_type = xtce_1_1.BooleanAlarmType
    _v1_2_type = xtce_1_2.BooleanAlarmType
    _v1_3_type = xtce_1_3.BooleanAlarmType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.BooleanAlarmType) -> dict[str, Any]:
        return super()._from_v1_1_kwargs(obj)

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.BooleanAlarmType) -> dict[str, Any]:
        return super()._from_v1_2_kwargs(obj)

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.BooleanAlarmType) -> dict[str, Any]:
        return super()._from_v1_3_kwargs(obj)

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        return super()._to_v1_1_kwargs(policy)

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        return super()._to_v1_2_kwargs(policy)

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        return super()._to_v1_3_kwargs(policy)


class EnumerationAlarm(Alarm):
    """Define an alarm for enumeration data types."""

    alarms: list[EnumerationAlarmLevel] = Field(default_factory=list)
    """List of alarm levels for the alarm.

    Alarms are processed in the order they appear in the list.

    """

    default_alarm_level: ConcernLevel = ConcernLevel.NORMAL
    """The default alarm level for the alarm."""

    _v1_1_type = xtce_1_1.EnumerationAlarmType
    _v1_2_type = xtce_1_2.EnumerationAlarmType
    _v1_3_type = xtce_1_3.EnumerationAlarmType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.EnumerationAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["alarms"] = [
            EnumerationAlarmLevel._from_v1_1(alarm)
            for alarm in obj.enumeration_alarm_list.enumeration_alarm
        ]
        kwargs["default_alarm_level"] = ConcernLevel(obj.default_alarm_level.value)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.EnumerationAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["alarms"] = (
            [
                EnumerationAlarmLevel._from_v1_2(alarm)
                for alarm in obj.enumeration_alarm_list.enumeration_alarm
            ]
            if obj.enumeration_alarm_list is not None
            else []
        )
        kwargs["default_alarm_level"] = ConcernLevel(obj.default_alarm_level.value)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.EnumerationAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["alarms"] = (
            [
                EnumerationAlarmLevel._from_v1_3(alarm)
                for alarm in obj.enumeration_alarm_list.enumeration_alarm
            ]
            if obj.enumeration_alarm_list is not None
            else []
        )
        kwargs["default_alarm_level"] = ConcernLevel(obj.default_alarm_level.value)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["enumeration_alarm_list"] = (
            xtce_1_1.EnumerationAlarmType.EnumerationAlarmList(
                enumeration_alarm=[alarm._to_v1_1(policy) for alarm in self.alarms]
            )
        )
        kwargs["default_alarm_level"] = xtce_1_1.AlarmLevels(
            self.default_alarm_level.value
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["enumeration_alarm_list"] = xtce_1_2.EnumerationAlarmListType(
            enumeration_alarm=[alarm._to_v1_2(policy) for alarm in self.alarms]
        )
        kwargs["default_alarm_level"] = xtce_1_2.ConcernLevelsType(
            self.default_alarm_level.value
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["enumeration_alarm_list"] = xtce_1_3.EnumerationAlarmListType(
            enumeration_alarm=[alarm._to_v1_3(policy) for alarm in self.alarms]
        )
        kwargs["default_alarm_level"] = xtce_1_3.ConcernLevelsType(
            self.default_alarm_level.value
        )
        return kwargs


class TimeAlarm(Alarm):
    """Define an alarm for time data types."""

    static_alarm_ranges: TimeAlarmRanges | None = None
    """Used to trigger alarms when the parameter value passes some threshold."""

    change_per_second_alarm_ranges: TimeAlarmRanges | None = None
    """Used to trigger alarms when the rate of change of the parameter value passes some
    threshold.
    """

    _v1_1_type = xtce_1_1.TimeAlarmType
    _v1_2_type = xtce_1_2.TimeAlarmType
    _v1_3_type = xtce_1_3.TimeAlarmType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.TimeAlarmType) -> dict[str, Any]:
        # XTCE 1.1 doesn't have a TimeAlarmRangesType. StaticAlarmRanges and
        # ChangePerSecondAlarmRanges are children of TimeAlarmType, but only inherit
        # from AlarmRangesType, so time_units has to be set manually
        static_alarm_ranges = (
            TimeAlarmRanges(
                **TimeAlarmRanges._from_v1_1_kwargs(obj.static_alarm_ranges)
            )
            if obj.static_alarm_ranges is not None
            else None
        )
        if static_alarm_ranges is not None and obj.static_alarm_ranges is not None:
            static_alarm_ranges.time_units = TimeUnits._from_v1_1(
                obj.static_alarm_ranges.time_units
            )
        change_per_second_alarm_ranges = (
            TimeAlarmRanges(
                **TimeAlarmRanges._from_v1_1_kwargs(obj.change_per_second_alarm_ranges)
            )
            if obj.change_per_second_alarm_ranges is not None
            else None
        )
        if (
            change_per_second_alarm_ranges is not None
            and obj.change_per_second_alarm_ranges is not None
        ):
            change_per_second_alarm_ranges.time_units = TimeUnits._from_v1_1(
                obj.change_per_second_alarm_ranges.time_units
            )

        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["static_alarm_ranges"] = static_alarm_ranges
        kwargs["change_per_second_alarm_ranges"] = change_per_second_alarm_ranges
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.TimeAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["static_alarm_ranges"] = (
            TimeAlarmRanges._from_v1_2_kwargs(obj.static_alarm_ranges)
            if obj.static_alarm_ranges is not None
            else None
        )
        kwargs["change_per_second_alarm_ranges"] = (
            TimeAlarmRanges._from_v1_2_kwargs(obj.change_per_second_alarm_ranges)
            if obj.change_per_second_alarm_ranges is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.TimeAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["static_alarm_ranges"] = (
            TimeAlarmRanges._from_v1_3_kwargs(obj.static_alarm_ranges)
            if obj.static_alarm_ranges is not None
            else None
        )
        kwargs["change_per_second_alarm_ranges"] = (
            TimeAlarmRanges._from_v1_3_kwargs(obj.change_per_second_alarm_ranges)
            if obj.change_per_second_alarm_ranges is not None
            else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.1 doesn't have a TimeAlarmRangesType. StaticAlarmRanges and
        # ChangePerSecondAlarmRanges are children of TimeAlarmType, so they need to be
        # instantiated manually
        static_alarm_ranges = (
            xtce_1_1.TimeAlarmType.StaticAlarmRanges(
                **self.static_alarm_ranges._to_v1_1_kwargs(policy),
                time_units=self.static_alarm_ranges.time_units._to_v1_1(policy),
            )
            if self.static_alarm_ranges is not None
            else None
        )
        change_per_second_alarm_ranges = (
            xtce_1_1.TimeAlarmType.ChangePerSecondAlarmRanges(
                **self.change_per_second_alarm_ranges._to_v1_1_kwargs(policy),
                time_units=self.change_per_second_alarm_ranges.time_units._to_v1_1(
                    policy
                ),
            )
            if self.change_per_second_alarm_ranges is not None
            else None
        )
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["static_alarm_ranges"] = static_alarm_ranges
        kwargs["change_per_second_alarm_ranges"] = change_per_second_alarm_ranges
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["static_alarm_ranges"] = (
            self.static_alarm_ranges._to_v1_2(policy)
            if self.static_alarm_ranges is not None
            else None
        )
        kwargs["change_per_second_alarm_ranges"] = (
            self.change_per_second_alarm_ranges._to_v1_2(policy)
            if self.change_per_second_alarm_ranges is not None
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["static_alarm_ranges"] = (
            self.static_alarm_ranges._to_v1_3(policy)
            if self.static_alarm_ranges is not None
            else None
        )
        kwargs["change_per_second_alarm_ranges"] = (
            self.change_per_second_alarm_ranges._to_v1_3(policy)
            if self.change_per_second_alarm_ranges is not None
            else None
        )
        return kwargs


class NumericContextAlarm(NumericAlarm):
    """Define a numeric alarm that is only activated under certain context
    conditions.
    """

    context_match: ContextMatch
    """The match condition that determines when this alarm is active."""

    _v1_1_type = xtce_1_1.NumericContextAlarmType
    _v1_2_type = xtce_1_2.NumericContextAlarmType
    _v1_3_type = xtce_1_3.NumericContextAlarmType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.NumericContextAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["context_match"] = ContextMatch._from_v1_1_kwargs(obj.context_match)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.NumericContextAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["context_match"] = ContextMatch._from_v1_2_kwargs(obj.context_match)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.NumericContextAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["context_match"] = ContextMatch._from_v1_3_kwargs(obj.context_match)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["context_match"] = self.context_match._to_v1_1(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["context_match"] = self.context_match._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["context_match"] = self.context_match._to_v1_3(policy)
        return kwargs


class StringContextAlarm(StringAlarm):
    """Define a string alarm that is only activated under certain context conditions."""

    context_match: ContextMatch
    """The match condition that determines when this alarm is active."""

    _v1_1_type = None
    _v1_2_type = xtce_1_2.StringContextAlarmType
    _v1_3_type = xtce_1_3.StringContextAlarmType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.StringContextAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["context_match"] = ContextMatch._from_v1_2_kwargs(obj.context_match)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.StringContextAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["context_match"] = ContextMatch._from_v1_3_kwargs(obj.context_match)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["context_match"] = self.context_match._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["context_match"] = self.context_match._to_v1_3(policy)
        return kwargs


class BinaryContextAlarm(BinaryAlarm):
    """Define a binary alarm that is only activated under certain context conditions."""

    context_match: ContextMatch
    """The match condition that determines when this alarm is active."""

    _v1_1_type = None
    _v1_2_type = xtce_1_2.BinaryContextAlarmType
    _v1_3_type = xtce_1_3.BinaryContextAlarmType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.BinaryContextAlarmType) -> dict[str, Any]:
        kwargs = super(BinaryAlarm, cls)._from_v1_2_kwargs(obj)
        kwargs["context_match"] = ContextMatch._from_v1_2(obj.context_match)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.BinaryContextAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["context_match"] = ContextMatch._from_v1_3(obj.context_match)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super(BinaryAlarm, self)._to_v1_2_kwargs(policy)
        kwargs["context_match"] = self.context_match._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["context_match"] = self.context_match._to_v1_3(policy)
        return kwargs


class BooleanContextAlarm(BooleanAlarm):
    """Define a boolean alarm that is only activated under certain context
    conditions.
    """

    context_match: ContextMatch
    """The match condition that determines when this alarm is active."""

    _v1_1_type = None
    _v1_2_type = xtce_1_2.BooleanContextAlarmType
    _v1_3_type = xtce_1_3.BooleanContextAlarmType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.BooleanContextAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["context_match"] = ContextMatch._from_v1_2_kwargs(obj.context_match)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.BooleanContextAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["context_match"] = ContextMatch._from_v1_3_kwargs(obj.context_match)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["context_match"] = self.context_match._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["context_match"] = self.context_match._to_v1_3(policy)
        return kwargs


class EnumerationContextAlarm(EnumerationAlarm):
    """Define an enumeration alarm that is only activated under certain context
    conditions.
    """

    context_match: ContextMatch
    """The match condition that determines when this alarm is active."""

    _v1_1_type = None
    _v1_2_type = xtce_1_2.EnumerationContextAlarmType
    _v1_3_type = xtce_1_3.EnumerationContextAlarmType

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.EnumerationContextAlarmType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["context_match"] = ContextMatch._from_v1_2_kwargs(obj.context_match)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.EnumerationContextAlarmType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["context_match"] = ContextMatch._from_v1_3_kwargs(obj.context_match)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["context_match"] = self.context_match._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["context_match"] = self.context_match._to_v1_3(policy)
        return kwargs


class TimeContextAlarm(TimeAlarm):
    """Define a time alarm that is only activated under certain context conditions."""

    context_match: ContextMatch
    """The match condition that determines when this alarm is active."""

    _v1_1_type = None
    _v1_2_type = xtce_1_2.TimeContextAlarmType
    _v1_3_type = xtce_1_3.TimeContextAlarmType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.TimeContextAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["context_match"] = ContextMatch._from_v1_2_kwargs(obj.context_match)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.TimeContextAlarmType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["context_match"] = ContextMatch._from_v1_3_kwargs(obj.context_match)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["context_match"] = self.context_match._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["context_match"] = self.context_match._to_v1_3(policy)
        return kwargs
