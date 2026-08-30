"""Verifier models."""

from __future__ import annotations

import datetime
from abc import ABC
from typing import TYPE_CHECKING, Annotated, Any, Self, assert_never

from pydantic import Field

from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_2, xtce_1_3
from xtce_lib.xtce._util import timedelta_to_xml_duration, xml_duration_to_timedelta

from ._base import XtceBaseModel
from .algorithm import InputAlgorithm
from .codec import DynamicValue
from .common import OptionalNameDescriptionBase
from .condition import BooleanExpression, Comparison
from .enum import TimeWindowIsRelativeTo
from .reference import ContainerRef, ParameterRef

if TYPE_CHECKING:
    from .command import ArgumentAssignment


class ParameterValueChange(XtceBaseModel):
    """A parameter change in value or specified delta change in value."""

    ref: ParameterRef
    """The path to the parameter whose value is being checked."""

    change: float
    """The change in value for the parameter required to satisfy the verifier."""

    _v1_1_type = None
    _v1_2_type = xtce_1_2.ParameterValueChangeType
    _v1_3_type = xtce_1_3.ParameterValueChangeType

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ParameterValueChangeType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["ref"] = ParameterRef._from_v1_2(obj.parameter_ref)
        kwargs["change"] = obj.change.value
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ParameterValueChangeType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["ref"] = ParameterRef._from_v1_3(obj.parameter_ref)
        kwargs["change"] = obj.change.value
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["parameter_ref"] = self.ref._to_v1_2()
        kwargs["change"] = xtce_1_2.ChangeValueType(value=self.change)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["parameter_ref"] = self.ref._to_v1_3()
        kwargs["change"] = xtce_1_3.ChangeValueType(value=self.change)
        return kwargs


class CheckWindow(XtceBaseModel):
    """A time window in which the verifier is active.

    Used to limit the time allocated to check for verification.

    """

    start_time: datetime.timedelta | None = None
    """The start time of the check window."""

    stop_time: datetime.timedelta
    """The stop time of the check window."""

    is_relative_to: TimeWindowIsRelativeTo = (
        TimeWindowIsRelativeTo.TIME_LAST_VERIFIER_PASSED
    )
    """Specifies what the start and stop times are relative to."""

    _v1_1_type = None
    _v1_2_type = xtce_1_2.CheckWindowType
    _v1_3_type = xtce_1_3.CheckWindowType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.CheckWindowType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["start_time"] = (
            xml_duration_to_timedelta(obj.time_to_start_checking)
            if obj.time_to_start_checking is not None
            else None
        )
        kwargs["stop_time"] = xml_duration_to_timedelta(obj.time_to_stop_checking)
        kwargs["is_relative_to"] = TimeWindowIsRelativeTo(
            obj.time_window_is_relative_to.value
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.CheckWindowType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["start_time"] = (
            xml_duration_to_timedelta(obj.time_to_start_checking)
            if obj.time_to_start_checking is not None
            else None
        )
        kwargs["stop_time"] = xml_duration_to_timedelta(obj.time_to_stop_checking)
        kwargs["is_relative_to"] = TimeWindowIsRelativeTo(
            obj.time_window_is_relative_to.value
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["time_to_start_checking"] = (
            timedelta_to_xml_duration(self.start_time)
            if self.start_time is not None
            else None
        )
        kwargs["time_to_stop_checking"] = timedelta_to_xml_duration(self.stop_time)
        kwargs["time_window_is_relative_to"] = xtce_1_2.TimeWindowIsRelativeToType(
            self.is_relative_to.value
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["time_to_start_checking"] = (
            timedelta_to_xml_duration(self.start_time)
            if self.start_time is not None
            else None
        )
        kwargs["time_to_stop_checking"] = timedelta_to_xml_duration(self.stop_time)
        kwargs["time_window_is_relative_to"] = xtce_1_3.TimeWindowIsRelativeToType(
            self.is_relative_to.value
        )
        return kwargs


class CheckWindowAlgorithms(XtceBaseModel):
    """A time window in which the verifier is active, defined by algorithms.

    Used to limit the time allocated to check for verification.

    """

    start_time: InputAlgorithm
    stop_time: InputAlgorithm

    _v1_1_type = None
    _v1_2_type = xtce_1_2.CheckWindowAlgorithmsType
    _v1_3_type = xtce_1_3.CheckWindowAlgorithmsType

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.CheckWindowAlgorithmsType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["start_time"] = InputAlgorithm._from_v1_2(obj.start_check)
        kwargs["stop_time"] = InputAlgorithm._from_v1_2(obj.stop_time)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.CheckWindowAlgorithmsType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["start_time"] = InputAlgorithm._from_v1_3(obj.start_check)
        kwargs["stop_time"] = InputAlgorithm._from_v1_3(obj.stop_time)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["start_check"] = self.start_time._to_v1_2(policy)
        kwargs["stop_time"] = self.stop_time._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["start_check"] = self.start_time._to_v1_3(policy)
        kwargs["stop_time"] = self.stop_time._to_v1_3(policy)
        return kwargs


class CommandVerifier(OptionalNameDescriptionBase, ABC):
    """Used to check that the command has been successfully executed.

    May be either a custom algorithm, boolean check, the presence of a container, or a
    relative change in the value of a parameter.

    """

    verifier: (
        Comparison
        | list[Comparison]
        | ContainerRef
        | ParameterValueChange
        | InputAlgorithm
        | BooleanExpression
    )
    """The verification method to use."""

    check_window: CheckWindow | CheckWindowAlgorithms
    """The time window in which the verification is active."""

    argument_restrictions: list[ArgumentAssignment] = Field(
        default_factory=list,
        min_length=1,
    )
    """An optional list of argument values that trigger this verifier.

    If not specified, the verifier is always active.

    """

    _v1_1_type = None
    _v1_2_type = xtce_1_2.CommandVerifierType
    _v1_3_type = xtce_1_3.CommandVerifierType

    @classmethod
    def _unpack_verifier_choice_v1_2(
        cls: type[Self], raw_obj: xtce_1_2.CommandVerifierType
    ) -> Any:
        match raw_obj.choice:
            case xtce_1_2.ComparisonType():
                return Comparison._from_v1_2(raw_obj.choice)
            case xtce_1_2.ComparisonListType():
                return [
                    Comparison._from_v1_2(comp) for comp in raw_obj.choice.comparison
                ]
            case xtce_1_2.ContainerRefType():
                return ContainerRef._from_v1_2(raw_obj.choice)
            case xtce_1_2.ParameterValueChangeType():
                return ParameterValueChange._from_v1_2(raw_obj.choice)
            case xtce_1_2.InputAlgorithmType():
                return InputAlgorithm._from_v1_2(raw_obj.choice)
            case xtce_1_2.BooleanExpressionType():
                return BooleanExpression._from_v1_2(raw_obj.choice)
            case None:
                raise ValueError("invalid XTCE XML: verifier choice is None")
            case _:
                assert_never(raw_obj.choice)

    @classmethod
    def _unpack_check_window_choice_v1_2(
        cls: type[Self], raw_obj: xtce_1_2.CommandVerifierType
    ) -> Any:
        match raw_obj.choice_1:
            case xtce_1_2.CheckWindowType():
                return CheckWindow._from_v1_2(raw_obj.choice_1)
            case xtce_1_2.CheckWindowAlgorithmsType():
                return CheckWindowAlgorithms._from_v1_2(raw_obj.choice_1)
            case None:
                raise ValueError("invalid XTCE XML: check_window choice is None")
            case _:
                assert_never(raw_obj.choice_1)

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.CommandVerifierType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["verifier"] = cls._unpack_verifier_choice_v1_2(obj)
        kwargs["check_window"] = cls._unpack_check_window_choice_v1_2(obj)
        return kwargs

    @classmethod
    def _unpack_verifier_choice_v1_3(
        cls: type[Self], raw_obj: xtce_1_3.CommandVerifierType
    ) -> Any:
        match raw_obj.choice:
            case xtce_1_3.ComparisonType():
                return Comparison._from_v1_3(raw_obj.choice)
            case xtce_1_3.ComparisonListType():
                return [
                    Comparison._from_v1_3(comp) for comp in raw_obj.choice.comparison
                ]
            case xtce_1_3.ContainerRefType():
                return ContainerRef._from_v1_3(raw_obj.choice)
            case xtce_1_3.ParameterValueChangeType():
                return ParameterValueChange._from_v1_3(raw_obj.choice)
            case xtce_1_3.InputAlgorithmType():
                return InputAlgorithm._from_v1_3(raw_obj.choice)
            case xtce_1_3.BooleanExpressionType():
                return BooleanExpression._from_v1_3(raw_obj.choice)
            case None:
                raise ValueError("invalid XTCE XML: verifier choice is None")
            case _:
                assert_never(raw_obj.choice)

    @classmethod
    def _unpack_check_window_choice_v1_3(
        cls: type[Self], raw_obj: xtce_1_3.CommandVerifierType
    ) -> Any:
        match raw_obj.choice_1:
            case xtce_1_3.CheckWindowType():
                return CheckWindow._from_v1_3(raw_obj.choice_1)
            case xtce_1_3.CheckWindowAlgorithmsType():
                return CheckWindowAlgorithms._from_v1_3(raw_obj.choice_1)
            case None:
                raise ValueError("invalid XTCE XML: check_window choice is None")
            case _:
                assert_never(raw_obj.choice_1)

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.CommandVerifierType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["verifier"] = cls._unpack_verifier_choice_v1_3(obj)
        kwargs["check_window"] = cls._unpack_check_window_choice_v1_3(obj)
        argument_restrictions = (
            [
                ArgumentAssignment._from_v1_3(arg)
                for arg in obj.argument_restriction_list.argument_assignment
            ]
            if obj.argument_restriction_list is not None
            else []
        )
        if argument_restrictions:
            kwargs["argument_restrictions"] = argument_restrictions
        return kwargs

    def _enforce_v1_2_argument_restrictions(self, policy: DowngradePolicy) -> None:
        """Enforce argument restriction loss rules when exporting to XTCE v1.2."""
        self._enforce_unsupported_field(
            field_name="argument_restrictions",
            current_value=self.argument_restrictions,
            empty_value=[],
            target_version=XtceVersion.V1_2,
            policy=policy,
        )

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_v1_2_argument_restrictions(policy)

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = (
            xtce_1_2.ComparisonListType(
                comparison=[comparison._to_v1_2(policy) for comparison in self.verifier]
            )
            if isinstance(self.verifier, list)
            else self.verifier._to_v1_2(policy)
        )
        kwargs["choice_1"] = self.check_window._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = (
            xtce_1_3.ComparisonListType(
                comparison=[comparison._to_v1_3(policy) for comparison in self.verifier]
            )
            if isinstance(self.verifier, list)
            else self.verifier._to_v1_3(policy)
        )
        kwargs["choice_1"] = self.check_window._to_v1_3(policy)
        kwargs["argument_restriction_list"] = self._build_set(
            items=self.argument_restrictions,
            set_class=xtce_1_3.ArgumentAssignmentListType,
            kwarg_name="argument_assignment",
            converter=lambda assignment: assignment._to_v1_3(policy),
        )
        return kwargs


class TransferredToRangeVerifier(CommandVerifier):
    """Transferred to range means the command has been received by the network that
    connects the ground system to the spacecraft.

    Typically, this verifier would come from something other than the spacecraft, such
    as a modem or front end processor.

    """

    _v1_2_type = xtce_1_2.TransferredToRangeVerifierType
    _v1_3_type = xtce_1_3.TransferredToRangeVerifierType


class SentFromRangeVerifier(CommandVerifier):
    """Sent from range means the command has been transmitted to the spacecraft by the
    network that connects the ground system to the spacecraft.

    Typically, this verifier would come from something other than the spacecraft, such
    as a modem or front end processor.

    """

    _v1_2_type = xtce_1_2.SentFromRangeVerifierType
    _v1_3_type = xtce_1_3.SentFromRangeVerifierType


class ReceivedVerifier(CommandVerifier):
    """A verifier that indicates the destination has received the command."""

    _v1_2_type = xtce_1_2.ReceivedVerifierType
    _v1_3_type = xtce_1_3.ReceivedVerifierType


class AcceptedVerifier(CommandVerifier):
    """A verifier that indicates the destination has accepted the command."""

    _v1_2_type = xtce_1_2.AcceptedVerifierType
    _v1_3_type = xtce_1_3.AcceptedVerifierType


class QueuedVerifier(CommandVerifier):
    """A verifier that indicates the command is scheduled for execution by the
    destination.
    """

    _v1_2_type = xtce_1_2.QueuedVerifierType
    _v1_3_type = xtce_1_3.QueuedVerifierType


class ExecutionVerifier(CommandVerifier):
    """A verifier that indicates that the command is being executed."""

    percent_complete: (
        Annotated[float, Field(ge=0.0, le=100.0)] | DynamicValue | None
    ) = None
    """Indicates the percentage of completion of the command execution."""

    _v1_2_type = xtce_1_2.ExecutionVerifierType
    _v1_3_type = xtce_1_3.ExecutionVerifierType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ExecutionVerifierType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        if obj.percent_complete is None:
            percent_complete = None
        elif isinstance(obj.percent_complete.choice, xtce_1_2.DynamicValueType):
            percent_complete = DynamicValue._from_v1_2(obj.percent_complete.choice)
        else:
            percent_complete = obj.percent_complete.choice
        kwargs["percent_complete"] = percent_complete
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ExecutionVerifierType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        if obj.percent_complete is None:
            percent_complete = None
        elif isinstance(obj.percent_complete.choice, xtce_1_3.DynamicValueType):
            percent_complete = DynamicValue._from_v1_3(obj.percent_complete.choice)
        else:
            percent_complete = obj.percent_complete.choice
        kwargs["percent_complete"] = percent_complete
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["percent_complete"] = (
            xtce_1_2.PercentCompleteType(
                choice=self.percent_complete._to_v1_2(policy)
                if isinstance(self.percent_complete, DynamicValue)
                else self.percent_complete
            )
            if self.percent_complete is not None
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["percent_complete"] = (
            xtce_1_3.PercentCompleteType(
                choice=self.percent_complete._to_v1_3(policy)
                if isinstance(self.percent_complete, DynamicValue)
                else self.percent_complete
            )
            if self.percent_complete is not None
            else None
        )
        return kwargs


class CompleteVerifier(CommandVerifier):
    """A verifier that indicates that the command has completed execution."""

    return_parm_ref: ParameterRef | None = None
    """The path to the parameter whose value is being checked."""

    _v1_2_type = xtce_1_2.CompleteVerifierType
    _v1_3_type = xtce_1_3.CompleteVerifierType

    @classmethod
    def _from_v1_2_kwargs(
        cls,
        obj: xtce_1_2.CompleteVerifierType,
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["return_parm_ref"] = (
            ParameterRef._from_v1_2(obj.return_parm_ref)
            if obj.return_parm_ref is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls,
        obj: xtce_1_3.CompleteVerifierType,
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["return_parm_ref"] = (
            ParameterRef._from_v1_3(obj.return_parm_ref)
            if obj.return_parm_ref is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["return_parm_ref"] = (
            self.return_parm_ref._to_v1_2(policy)
            if self.return_parm_ref is not None
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["return_parm_ref"] = (
            self.return_parm_ref._to_v1_3(policy)
            if self.return_parm_ref is not None
            else None
        )
        return kwargs


class FailedVerifier(CommandVerifier):
    """A verifier that indicates that the command has failed execution."""

    return_parm_ref: ParameterRef | None = None
    """The path to the parameter whose value is being checked."""

    _v1_2_type = xtce_1_2.FailedVerifierType
    _v1_3_type = xtce_1_3.FailedVerifierType

    @classmethod
    def _from_v1_2_kwargs(
        cls,
        obj: xtce_1_2.FailedVerifierType,
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["return_parm_ref"] = (
            ParameterRef._from_v1_2(obj.return_parm_ref)
            if obj.return_parm_ref is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls,
        obj: xtce_1_3.FailedVerifierType,
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["return_parm_ref"] = (
            ParameterRef._from_v1_3(obj.return_parm_ref)
            if obj.return_parm_ref is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["return_parm_ref"] = (
            self.return_parm_ref._to_v1_2(policy)
            if self.return_parm_ref is not None
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["return_parm_ref"] = (
            self.return_parm_ref._to_v1_3(policy)
            if self.return_parm_ref is not None
            else None
        )
        return kwargs


class VerifierSet(XtceBaseModel):
    """A collection of unordered verifiers.

    A command verifier is a conditional check on the telemetry from a space system that
    provides positive indication on the processing state of a command.

    """

    transferred_to_range_verifier: TransferredToRangeVerifier | None = None
    """A verifier that indicates the command has been received by the network that
    connects the ground system to the spacecraft.
    """

    sent_from_range_verifier: SentFromRangeVerifier | None = None
    """A verifier that indicates the command has been transmitted to the spacecraft by
    the network that connects the ground system to the spacecraft.
    """

    received_verifier: ReceivedVerifier | None = None
    """A verifier that indicates the command has been received by the spacecraft."""

    accepted_verifier: AcceptedVerifier | None = None
    """A verifier that indicates the command has been accepted for execution by the
    spacecraft.
    """

    queued_verifier: QueuedVerifier | None = None
    """A verifier that indicates the command has been queued for execution by the
    spacecraft.
    """

    execution_verifiers: list[ExecutionVerifier] = Field(default_factory=list)
    """A set of verifiers that indicate the command is currently being executed by the
    spacecraft.
    """

    complete_verifiers: list[CompleteVerifier] = Field(default_factory=list)
    """A set of verifiers that indicate the command has been successfully executed by
    the spacecraft.
    """

    failed_verifier: FailedVerifier | None = None
    """A verifier that indicates the command has failed to be executed by the
    spacecraft.
    """

    _v1_1_type = None
    _v1_2_type = xtce_1_2.VerifierSetType
    _v1_3_type = xtce_1_3.VerifierSetType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.VerifierSetType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["transferred_to_range_verifier"] = (
            TransferredToRangeVerifier._from_v1_2(obj.transferred_to_range_verifier)
            if obj.transferred_to_range_verifier is not None
            else None
        )
        kwargs["sent_from_range_verifier"] = (
            SentFromRangeVerifier._from_v1_2(obj.sent_from_range_verifier)
            if obj.sent_from_range_verifier is not None
            else None
        )
        kwargs["received_verifier"] = (
            ReceivedVerifier._from_v1_2(obj.received_verifier)
            if obj.received_verifier is not None
            else None
        )
        kwargs["accepted_verifier"] = (
            AcceptedVerifier._from_v1_2(obj.accepted_verifier)
            if obj.accepted_verifier is not None
            else None
        )
        kwargs["queued_verifier"] = (
            QueuedVerifier._from_v1_2(obj.queued_verifier)
            if obj.queued_verifier is not None
            else None
        )
        kwargs["execution_verifiers"] = [
            ExecutionVerifier._from_v1_2(verifier)
            for verifier in obj.execution_verifier
        ]
        kwargs["complete_verifiers"] = [
            CompleteVerifier._from_v1_2(verifier) for verifier in obj.complete_verifier
        ]
        kwargs["failed_verifier"] = (
            FailedVerifier._from_v1_2(obj.failed_verifier)
            if obj.failed_verifier is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.VerifierSetType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["transferred_to_range_verifier"] = (
            TransferredToRangeVerifier._from_v1_3(obj.transferred_to_range_verifier)
            if obj.transferred_to_range_verifier is not None
            else None
        )
        kwargs["sent_from_range_verifier"] = (
            SentFromRangeVerifier._from_v1_3(obj.sent_from_range_verifier)
            if obj.sent_from_range_verifier is not None
            else None
        )
        kwargs["received_verifier"] = (
            ReceivedVerifier._from_v1_3(obj.received_verifier)
            if obj.received_verifier is not None
            else None
        )
        kwargs["accepted_verifier"] = (
            AcceptedVerifier._from_v1_3(obj.accepted_verifier)
            if obj.accepted_verifier is not None
            else None
        )
        kwargs["queued_verifier"] = (
            QueuedVerifier._from_v1_3(obj.queued_verifier)
            if obj.queued_verifier is not None
            else None
        )
        kwargs["execution_verifiers"] = [
            ExecutionVerifier._from_v1_3(verifier)
            for verifier in obj.execution_verifier
        ]
        kwargs["complete_verifiers"] = [
            CompleteVerifier._from_v1_3(verifier) for verifier in obj.complete_verifier
        ]
        kwargs["failed_verifier"] = (
            FailedVerifier._from_v1_3(obj.failed_verifier)
            if obj.failed_verifier is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["transferred_to_range_verifier"] = (
            self.transferred_to_range_verifier._to_v1_2(policy)
            if self.transferred_to_range_verifier is not None
            else None
        )
        kwargs["sent_from_range_verifier"] = (
            self.sent_from_range_verifier._to_v1_2(policy)
            if self.sent_from_range_verifier is not None
            else None
        )
        kwargs["received_verifier"] = (
            self.received_verifier._to_v1_2(policy)
            if self.received_verifier is not None
            else None
        )
        kwargs["accepted_verifier"] = (
            self.accepted_verifier._to_v1_2(policy)
            if self.accepted_verifier is not None
            else None
        )
        kwargs["queued_verifier"] = (
            self.queued_verifier._to_v1_2(policy)
            if self.queued_verifier is not None
            else None
        )
        kwargs["execution_verifier"] = [
            verifier._to_v1_2(policy) for verifier in self.execution_verifiers
        ]
        kwargs["complete_verifier"] = [
            verifier._to_v1_2(policy) for verifier in self.complete_verifiers
        ]
        kwargs["failed_verifier"] = (
            self.failed_verifier._to_v1_2(policy)
            if self.failed_verifier is not None
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["transferred_to_range_verifier"] = (
            self.transferred_to_range_verifier._to_v1_3(policy)
            if self.transferred_to_range_verifier is not None
            else None
        )
        kwargs["sent_from_range_verifier"] = (
            self.sent_from_range_verifier._to_v1_3(policy)
            if self.sent_from_range_verifier is not None
            else None
        )
        kwargs["received_verifier"] = (
            self.received_verifier._to_v1_3(policy)
            if self.received_verifier is not None
            else None
        )
        kwargs["accepted_verifier"] = (
            self.accepted_verifier._to_v1_3(policy)
            if self.accepted_verifier is not None
            else None
        )
        kwargs["queued_verifier"] = (
            self.queued_verifier._to_v1_3(policy)
            if self.queued_verifier is not None
            else None
        )
        kwargs["execution_verifier"] = [
            verifier._to_v1_3(policy) for verifier in self.execution_verifiers
        ]
        kwargs["complete_verifier"] = [
            verifier._to_v1_3(policy) for verifier in self.complete_verifiers
        ]
        kwargs["failed_verifier"] = (
            self.failed_verifier._to_v1_3(policy)
            if self.failed_verifier is not None
            else None
        )
        return kwargs
