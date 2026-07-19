"""Verifier models."""

from __future__ import annotations

import datetime
from abc import ABC
from typing import TYPE_CHECKING, Annotated, Any, Self, assert_never

from pydantic import Field

from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy, XtceUnsupportedError
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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.ParameterValueChangeType) -> Self:
        return cls(
            ref=ParameterRef._from_v1_2(raw_obj.parameter_ref),
            change=raw_obj.change.value,
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.ParameterValueChangeType) -> Self:
        return cls(
            ref=ParameterRef._from_v1_3(raw_obj.parameter_ref),
            change=raw_obj.change.value,
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ParameterValueChangeType:
        return xtce_1_2.ParameterValueChangeType(
            parameter_ref=self.ref._to_v1_2(),
            change=xtce_1_2.ChangeValueType(value=self.change),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ParameterValueChangeType:
        return xtce_1_3.ParameterValueChangeType(
            parameter_ref=self.ref._to_v1_3(),
            change=xtce_1_3.ChangeValueType(value=self.change),
        )


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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.CheckWindowType) -> Self:
        return cls(
            start_time=(
                xml_duration_to_timedelta(raw_obj.time_to_start_checking)
                if raw_obj.time_to_start_checking is not None
                else None
            ),
            stop_time=xml_duration_to_timedelta(raw_obj.time_to_stop_checking),
            is_relative_to=TimeWindowIsRelativeTo(
                raw_obj.time_window_is_relative_to.value
            ),
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.CheckWindowType) -> Self:
        return cls(
            start_time=(
                xml_duration_to_timedelta(raw_obj.time_to_start_checking)
                if raw_obj.time_to_start_checking is not None
                else None
            ),
            stop_time=xml_duration_to_timedelta(raw_obj.time_to_stop_checking),
            is_relative_to=TimeWindowIsRelativeTo(
                raw_obj.time_window_is_relative_to.value
            ),
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.CheckWindowType:
        return xtce_1_2.CheckWindowType(
            time_to_start_checking=timedelta_to_xml_duration(self.start_time)
            if self.start_time is not None
            else None,
            time_to_stop_checking=timedelta_to_xml_duration(self.stop_time),
            time_window_is_relative_to=xtce_1_2.TimeWindowIsRelativeToType(
                self.is_relative_to.value
            ),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.CheckWindowType:
        return xtce_1_3.CheckWindowType(
            time_to_start_checking=timedelta_to_xml_duration(self.start_time)
            if self.start_time is not None
            else None,
            time_to_stop_checking=timedelta_to_xml_duration(self.stop_time),
            time_window_is_relative_to=xtce_1_3.TimeWindowIsRelativeToType(
                self.is_relative_to.value
            ),
        )


class CheckWindowAlgorithms(XtceBaseModel):
    """A time window in which the verifier is active, defined by algorithms.

    Used to limit the time allocated to check for verification.

    """

    start_time: InputAlgorithm
    stop_time: InputAlgorithm

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(
        cls: type[Self], raw_obj: xtce_1_2.CheckWindowAlgorithmsType
    ) -> Self:
        return cls(
            start_time=InputAlgorithm._from_v1_2(raw_obj.start_check),
            stop_time=InputAlgorithm._from_v1_2(raw_obj.stop_time),
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], raw_obj: xtce_1_3.CheckWindowAlgorithmsType
    ) -> Self:
        return cls(
            start_time=InputAlgorithm._from_v1_3(raw_obj.start_check),
            stop_time=InputAlgorithm._from_v1_3(raw_obj.stop_time),
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.CheckWindowAlgorithmsType:
        return xtce_1_2.CheckWindowAlgorithmsType(
            start_check=self.start_time._to_v1_2(policy),
            stop_time=self.stop_time._to_v1_2(policy),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.CheckWindowAlgorithmsType:
        return xtce_1_3.CheckWindowAlgorithmsType(
            start_check=self.start_time._to_v1_3(policy),
            stop_time=self.stop_time._to_v1_3(policy),
        )


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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

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
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.CommandVerifierType) -> Self:
        return cls(**cls._from_v1_2_common_kwargs(raw_obj))

    @classmethod
    def _from_v1_2_common_kwargs(
        cls: type[Self],
        raw_obj: xtce_1_2.CommandVerifierType,
    ) -> dict[str, Any]:
        """Build shared v1.2 constructor kwargs for command verifier imports."""
        kwargs: dict[str, Any] = {
            "name": raw_obj.name,
            "short_description": raw_obj.short_description,
            "long_description": raw_obj.long_description,
            "verifier": cls._unpack_verifier_choice_v1_2(raw_obj),
            "check_window": cls._unpack_check_window_choice_v1_2(raw_obj),
        }

        aliases = cls._aliases_from_v1_2(raw_obj.alias_set)
        if aliases:
            kwargs["aliases"] = aliases

        ancillary_data = cls._ancillary_data_from_v1_2(raw_obj.ancillary_data_set)
        if ancillary_data:
            kwargs["ancillary_data"] = ancillary_data

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
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.CommandVerifierType) -> Self:
        return cls(**cls._from_v1_3_common_kwargs(raw_obj))

    @classmethod
    def _from_v1_3_common_kwargs(
        cls: type[Self],
        raw_obj: xtce_1_3.CommandVerifierType,
        *,
        include_argument_restrictions: bool = True,
    ) -> dict[str, Any]:
        """Build shared v1.3 constructor kwargs for command verifier imports."""
        kwargs: dict[str, Any] = {
            "name": raw_obj.name,
            "short_description": raw_obj.short_description,
            "long_description": raw_obj.long_description,
            "verifier": cls._unpack_verifier_choice_v1_3(raw_obj),
            "check_window": cls._unpack_check_window_choice_v1_3(raw_obj),
        }

        aliases = cls._aliases_from_v1_3(raw_obj.alias_set)
        if aliases:
            kwargs["aliases"] = aliases

        ancillary_data = cls._ancillary_data_from_v1_3(raw_obj.ancillary_data_set)
        if ancillary_data:
            kwargs["ancillary_data"] = ancillary_data

        if include_argument_restrictions:
            argument_restrictions = (
                [
                    ArgumentAssignment._from_v1_3(arg)
                    for arg in raw_obj.argument_restriction_list.argument_assignment
                ]
                if raw_obj.argument_restriction_list is not None
                else []
            )
            if argument_restrictions:
                kwargs["argument_restrictions"] = argument_restrictions

        return kwargs

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.CommandVerifierType:
        self._enforce_v1_2_argument_restrictions(policy)

        return xtce_1_2.CommandVerifierType(**self._to_v1_2_common_kwargs(policy))

    def _enforce_v1_2_argument_restrictions(self, policy: DowngradePolicy) -> None:
        """Enforce argument restriction loss rules when exporting to XTCE v1.2."""
        self._enforce_unsupported_field(
            field_name="argument_restrictions",
            current_value=self.argument_restrictions,
            empty_value=[],
            target_version=XtceVersion.V1_2,
            policy=policy,
        )

    def _to_v1_2_common_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        """Build shared v1.2 constructor kwargs for command verifier exports."""
        return {
            "name": self.name,
            "short_description": self.short_description,
            "long_description": self.long_description,
            "alias_set": self._aliases_to_v1_2(policy),
            "ancillary_data_set": self._ancillary_data_to_v1_2(policy),
            "choice": (
                xtce_1_2.ComparisonListType(
                    comparison=[
                        comparison._to_v1_2(policy) for comparison in self.verifier
                    ]
                )
                if isinstance(self.verifier, list)
                else self.verifier._to_v1_2(policy)
            ),
            "choice_1": self.check_window._to_v1_2(policy),
        }

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.CommandVerifierType:
        return xtce_1_3.CommandVerifierType(**self._to_v1_3_common_kwargs(policy))

    def _to_v1_3_common_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        """Build shared v1.3 constructor kwargs for command verifier exports."""
        return {
            "name": self.name,
            "short_description": self.short_description,
            "long_description": self.long_description,
            "alias_set": self._aliases_to_v1_3(policy),
            "ancillary_data_set": self._ancillary_data_to_v1_3(policy),
            "choice": (
                xtce_1_3.ComparisonListType(
                    comparison=[
                        comparison._to_v1_3(policy) for comparison in self.verifier
                    ]
                )
                if isinstance(self.verifier, list)
                else self.verifier._to_v1_3(policy)
            ),
            "choice_1": self.check_window._to_v1_3(policy),
            "argument_restriction_list": (
                xtce_1_3.ArgumentAssignmentListType(
                    argument_assignment=[
                        assignment._to_v1_3(policy)
                        for assignment in self.argument_restrictions
                    ]
                )
                if self.argument_restrictions
                else None
            ),
        }


class TransferredToRangeVerifier(CommandVerifier):
    """Transferred to range means the command has been received by the network that
    connects the ground system to the spacecraft.

    Typically, this verifier would come from something other than the spacecraft, such
    as a modem or front end processor.

    """

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.TransferredToRangeVerifierType:
        self._enforce_v1_2_argument_restrictions(policy)
        return xtce_1_2.TransferredToRangeVerifierType(
            **self._to_v1_2_common_kwargs(policy)
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.TransferredToRangeVerifierType:
        return xtce_1_3.TransferredToRangeVerifierType(
            **self._to_v1_3_common_kwargs(policy)
        )


class SentFromRangeVerifier(CommandVerifier):
    """Sent from range means the command has been transmitted to the spacecraft by the
    network that connects the ground system to the spacecraft.

    Typically, this verifier would come from something other than the spacecraft, such
    as a modem or front end processor.

    """

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.SentFromRangeVerifierType:
        self._enforce_v1_2_argument_restrictions(policy)
        return xtce_1_2.SentFromRangeVerifierType(**self._to_v1_2_common_kwargs(policy))

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.SentFromRangeVerifierType:
        return xtce_1_3.SentFromRangeVerifierType(**self._to_v1_3_common_kwargs(policy))


class ReceivedVerifier(CommandVerifier):
    """A verifier that indicates the destination has received the command."""

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ReceivedVerifierType:
        self._enforce_v1_2_argument_restrictions(policy)
        return xtce_1_2.ReceivedVerifierType(**self._to_v1_2_common_kwargs(policy))

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ReceivedVerifierType:
        return xtce_1_3.ReceivedVerifierType(**self._to_v1_3_common_kwargs(policy))


class AcceptedVerifier(CommandVerifier):
    """A verifier that indicates the destination has accepted the command."""

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.AcceptedVerifierType:
        self._enforce_v1_2_argument_restrictions(policy)
        return xtce_1_2.AcceptedVerifierType(**self._to_v1_2_common_kwargs(policy))

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.AcceptedVerifierType:
        return xtce_1_3.AcceptedVerifierType(**self._to_v1_3_common_kwargs(policy))


class QueuedVerifier(CommandVerifier):
    """A verifier that indicates the command is scheduled for execution by the
    destination.
    """

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.QueuedVerifierType:
        self._enforce_v1_2_argument_restrictions(policy)
        return xtce_1_2.QueuedVerifierType(**self._to_v1_2_common_kwargs(policy))

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.QueuedVerifierType:
        return xtce_1_3.QueuedVerifierType(**self._to_v1_3_common_kwargs(policy))


class ExecutionVerifier(CommandVerifier):
    """A verifier that indicates that the command is being executed."""

    percent_complete: (
        Annotated[float, Field(ge=0.0, le=100.0)] | DynamicValue | None
    ) = None
    """Indicates the percentage of completion of the command execution."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.ExecutionVerifierType) -> Self:
        if raw_obj.percent_complete is None:
            percent_complete = None
        elif isinstance(raw_obj.percent_complete.choice, xtce_1_2.DynamicValueType):
            percent_complete = DynamicValue._from_v1_2(raw_obj.percent_complete.choice)
        else:
            percent_complete = raw_obj.percent_complete.choice

        kwargs = cls._from_v1_2_common_kwargs(raw_obj)
        kwargs["percent_complete"] = percent_complete
        return cls(**kwargs)

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.ExecutionVerifierType) -> Self:
        if raw_obj.percent_complete is None:
            percent_complete = None
        elif isinstance(raw_obj.percent_complete.choice, xtce_1_3.DynamicValueType):
            percent_complete = DynamicValue._from_v1_3(raw_obj.percent_complete.choice)
        else:
            percent_complete = raw_obj.percent_complete.choice

        kwargs = cls._from_v1_3_common_kwargs(raw_obj)
        kwargs["percent_complete"] = percent_complete
        return cls(**kwargs)

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ExecutionVerifierType:
        self._enforce_v1_2_argument_restrictions(policy)
        return xtce_1_2.ExecutionVerifierType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_2(policy),
            ancillary_data_set=self._ancillary_data_to_v1_2(policy),
            choice=xtce_1_2.ComparisonListType(
                comparison=[comparison._to_v1_2(policy) for comparison in self.verifier]
            )
            if isinstance(self.verifier, list)
            else self.verifier._to_v1_2(policy),
            choice_1=self.check_window._to_v1_2(policy),
            percent_complete=xtce_1_2.PercentCompleteType(
                choice=self.percent_complete._to_v1_2(policy)
                if isinstance(self.percent_complete, DynamicValue)
                else self.percent_complete
            )
            if self.percent_complete is not None
            else None,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ExecutionVerifierType:
        return xtce_1_3.ExecutionVerifierType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_3(policy),
            ancillary_data_set=self._ancillary_data_to_v1_3(policy),
            choice=xtce_1_3.ComparisonListType(
                comparison=[comparison._to_v1_3(policy) for comparison in self.verifier]
            )
            if isinstance(self.verifier, list)
            else self.verifier._to_v1_3(policy),
            choice_1=self.check_window._to_v1_3(policy),
            argument_restriction_list=xtce_1_3.ArgumentAssignmentListType(
                argument_assignment=[
                    assignment._to_v1_3(policy)
                    for assignment in self.argument_restrictions
                ]
            )
            if self.argument_restrictions
            else None,
            percent_complete=xtce_1_3.PercentCompleteType(
                choice=self.percent_complete._to_v1_3(policy)
                if isinstance(self.percent_complete, DynamicValue)
                else self.percent_complete
            )
            if self.percent_complete is not None
            else None,
        )


class CompleteVerifier(CommandVerifier):
    """A verifier that indicates that the command has completed execution."""

    return_parm_ref: ParameterRef | None = None
    """The path to the parameter whose value is being checked."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(
        cls: type[Self],
        raw_obj: xtce_1_2.CompleteVerifierType,
    ) -> Self:
        kwargs = cls._from_v1_2_common_kwargs(raw_obj)
        kwargs["return_parm_ref"] = (
            ParameterRef._from_v1_2(raw_obj.return_parm_ref)
            if raw_obj.return_parm_ref is not None
            else None
        )
        return cls(**kwargs)

    @classmethod
    def _from_v1_3(
        cls: type[Self],
        raw_obj: xtce_1_3.CompleteVerifierType,
    ) -> Self:
        kwargs = cls._from_v1_3_common_kwargs(raw_obj)
        kwargs["return_parm_ref"] = (
            ParameterRef._from_v1_3(raw_obj.return_parm_ref)
            if raw_obj.return_parm_ref is not None
            else None
        )
        return cls(**kwargs)

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.CompleteVerifierType:
        self._enforce_v1_2_argument_restrictions(policy)
        return xtce_1_2.CompleteVerifierType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_2(policy),
            ancillary_data_set=self._ancillary_data_to_v1_2(policy),
            choice=xtce_1_2.ComparisonListType(
                comparison=[comparison._to_v1_2(policy) for comparison in self.verifier]
            )
            if isinstance(self.verifier, list)
            else self.verifier._to_v1_2(policy),
            choice_1=self.check_window._to_v1_2(policy),
            return_parm_ref=self.return_parm_ref._to_v1_2(policy)
            if self.return_parm_ref is not None
            else None,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.CompleteVerifierType:
        return xtce_1_3.CompleteVerifierType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_3(policy),
            ancillary_data_set=self._ancillary_data_to_v1_3(policy),
            choice=xtce_1_3.ComparisonListType(
                comparison=[comparison._to_v1_3(policy) for comparison in self.verifier]
            )
            if isinstance(self.verifier, list)
            else self.verifier._to_v1_3(policy),
            choice_1=self.check_window._to_v1_3(policy),
            argument_restriction_list=xtce_1_3.ArgumentAssignmentListType(
                argument_assignment=[
                    assignment._to_v1_3(policy)
                    for assignment in self.argument_restrictions
                ]
            )
            if self.argument_restrictions
            else None,
            return_parm_ref=self.return_parm_ref._to_v1_3(policy)
            if self.return_parm_ref is not None
            else None,
        )


class FailedVerifier(CommandVerifier):
    """A verifier that indicates that the command has failed execution."""

    return_parm_ref: ParameterRef | None = None
    """The path to the parameter whose value is being checked."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(
        cls: type[Self],
        raw_obj: xtce_1_2.FailedVerifierType,
    ) -> Self:
        kwargs = cls._from_v1_2_common_kwargs(raw_obj)
        kwargs["return_parm_ref"] = (
            ParameterRef._from_v1_2(raw_obj.return_parm_ref)
            if raw_obj.return_parm_ref is not None
            else None
        )
        return cls(**kwargs)

    @classmethod
    def _from_v1_3(
        cls: type[Self],
        raw_obj: xtce_1_3.FailedVerifierType,
    ) -> Self:
        kwargs = cls._from_v1_3_common_kwargs(raw_obj)
        kwargs["return_parm_ref"] = (
            ParameterRef._from_v1_3(raw_obj.return_parm_ref)
            if raw_obj.return_parm_ref is not None
            else None
        )
        return cls(**kwargs)

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.FailedVerifierType:
        self._enforce_v1_2_argument_restrictions(policy)
        return xtce_1_2.FailedVerifierType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_2(policy),
            ancillary_data_set=self._ancillary_data_to_v1_2(policy),
            choice=xtce_1_2.ComparisonListType(
                comparison=[comparison._to_v1_2(policy) for comparison in self.verifier]
            )
            if isinstance(self.verifier, list)
            else self.verifier._to_v1_2(policy),
            choice_1=self.check_window._to_v1_2(policy),
            return_parm_ref=self.return_parm_ref._to_v1_2(policy)
            if self.return_parm_ref is not None
            else None,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.FailedVerifierType:
        return xtce_1_3.FailedVerifierType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_3(policy),
            ancillary_data_set=self._ancillary_data_to_v1_3(policy),
            choice=xtce_1_3.ComparisonListType(
                comparison=[comparison._to_v1_3(policy) for comparison in self.verifier]
            )
            if isinstance(self.verifier, list)
            else self.verifier._to_v1_3(policy),
            choice_1=self.check_window._to_v1_3(policy),
            argument_restriction_list=xtce_1_3.ArgumentAssignmentListType(
                argument_assignment=[
                    assignment._to_v1_3(policy)
                    for assignment in self.argument_restrictions
                ]
            )
            if self.argument_restrictions
            else None,
            return_parm_ref=self.return_parm_ref._to_v1_3(policy)
            if self.return_parm_ref is not None
            else None,
        )


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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.VerifierSetType) -> Self:
        return cls(
            transferred_to_range_verifier=(
                TransferredToRangeVerifier._from_v1_2(
                    raw_obj.transferred_to_range_verifier
                )
                if raw_obj.transferred_to_range_verifier is not None
                else None
            ),
            sent_from_range_verifier=(
                SentFromRangeVerifier._from_v1_2(raw_obj.sent_from_range_verifier)
                if raw_obj.sent_from_range_verifier is not None
                else None
            ),
            received_verifier=(
                ReceivedVerifier._from_v1_2(raw_obj.received_verifier)
                if raw_obj.received_verifier is not None
                else None
            ),
            accepted_verifier=(
                AcceptedVerifier._from_v1_2(raw_obj.accepted_verifier)
                if raw_obj.accepted_verifier is not None
                else None
            ),
            queued_verifier=(
                QueuedVerifier._from_v1_2(raw_obj.queued_verifier)
                if raw_obj.queued_verifier is not None
                else None
            ),
            execution_verifiers=[
                ExecutionVerifier._from_v1_2(verifier)
                for verifier in raw_obj.execution_verifier
            ],
            complete_verifiers=[
                CompleteVerifier._from_v1_2(verifier)
                for verifier in raw_obj.complete_verifier
            ],
            failed_verifier=(
                FailedVerifier._from_v1_2(raw_obj.failed_verifier)
                if raw_obj.failed_verifier is not None
                else None
            ),
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.VerifierSetType) -> Self:
        return cls(
            transferred_to_range_verifier=(
                TransferredToRangeVerifier._from_v1_3(
                    raw_obj.transferred_to_range_verifier
                )
                if raw_obj.transferred_to_range_verifier is not None
                else None
            ),
            sent_from_range_verifier=(
                SentFromRangeVerifier._from_v1_3(raw_obj.sent_from_range_verifier)
                if raw_obj.sent_from_range_verifier is not None
                else None
            ),
            received_verifier=(
                ReceivedVerifier._from_v1_3(raw_obj.received_verifier)
                if raw_obj.received_verifier is not None
                else None
            ),
            accepted_verifier=(
                AcceptedVerifier._from_v1_3(raw_obj.accepted_verifier)
                if raw_obj.accepted_verifier is not None
                else None
            ),
            queued_verifier=(
                QueuedVerifier._from_v1_3(raw_obj.queued_verifier)
                if raw_obj.queued_verifier is not None
                else None
            ),
            execution_verifiers=[
                ExecutionVerifier._from_v1_3(verifier)
                for verifier in raw_obj.execution_verifier
            ],
            complete_verifiers=[
                CompleteVerifier._from_v1_3(verifier)
                for verifier in raw_obj.complete_verifier
            ],
            failed_verifier=(
                FailedVerifier._from_v1_3(raw_obj.failed_verifier)
                if raw_obj.failed_verifier is not None
                else None
            ),
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.VerifierSetType:
        return xtce_1_2.VerifierSetType(
            transferred_to_range_verifier=self.transferred_to_range_verifier._to_v1_2(
                policy
            )
            if self.transferred_to_range_verifier is not None
            else None,
            sent_from_range_verifier=self.sent_from_range_verifier._to_v1_2(policy)
            if self.sent_from_range_verifier is not None
            else None,
            received_verifier=self.received_verifier._to_v1_2(policy)
            if self.received_verifier is not None
            else None,
            accepted_verifier=self.accepted_verifier._to_v1_2(policy)
            if self.accepted_verifier is not None
            else None,
            queued_verifier=self.queued_verifier._to_v1_2(policy)
            if self.queued_verifier is not None
            else None,
            execution_verifier=[
                verifier._to_v1_2(policy) for verifier in self.execution_verifiers
            ],
            complete_verifier=[
                verifier._to_v1_2(policy) for verifier in self.complete_verifiers
            ],
            failed_verifier=self.failed_verifier._to_v1_2(policy)
            if self.failed_verifier is not None
            else None,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.VerifierSetType:
        return xtce_1_3.VerifierSetType(
            transferred_to_range_verifier=self.transferred_to_range_verifier._to_v1_3(
                policy
            )
            if self.transferred_to_range_verifier is not None
            else None,
            sent_from_range_verifier=self.sent_from_range_verifier._to_v1_3(policy)
            if self.sent_from_range_verifier is not None
            else None,
            received_verifier=self.received_verifier._to_v1_3(policy)
            if self.received_verifier is not None
            else None,
            accepted_verifier=self.accepted_verifier._to_v1_3(policy)
            if self.accepted_verifier is not None
            else None,
            queued_verifier=self.queued_verifier._to_v1_3(policy)
            if self.queued_verifier is not None
            else None,
            execution_verifier=[
                verifier._to_v1_3(policy) for verifier in self.execution_verifiers
            ],
            complete_verifier=[
                verifier._to_v1_3(policy) for verifier in self.complete_verifiers
            ],
            failed_verifier=self.failed_verifier._to_v1_3(policy)
            if self.failed_verifier is not None
            else None,
        )
