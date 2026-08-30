"""Command models."""

from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Annotated, Any

from pydantic import AfterValidator, Field

from xtce_lib.common.xtce_path import XtcePath, require_regex
from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from ._pattern import EXPD_NAME_REF_NO_PATH, EXPD_NAME_REF_W_PATH, NAME_REF_W_PATH
from ._util import (
    coerce,
    timedelta_to_xml_duration,
    uncoerce,
    xml_duration_to_timedelta,
)
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
from .calibrator import ArgumentMathOperation
from .common import NameDescriptionBase
from .condition import ContextMatch, MatchCriteria
from .container import CommandContainer, SequenceContainer
from .enum import ConsequenceLevel, VerifierType
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
from .reference import ParameterRef
from .stream import CustomStream, FixedFrameStream, VariableFrameStream
from .verifier import VerifierSet


class Argument(NameDescriptionBase):
    """Define an argument for a command."""

    # TODO maybe move to argument.py

    argument_type_ref: Annotated[
        XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))
    ] = Field(
        ...,
        examples=["TODO"],
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to an argument type."""

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
    """The initial value of the argument."""

    _v1_1_type = xtce_1_1.MetaCommandType.ArgumentList.Argument
    _v1_2_type = xtce_1_2.ArgumentType
    _v1_3_type = xtce_1_3.ArgumentType

    # TODO need handling for lists/dicts

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.MetaCommandType.ArgumentList.Argument
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["argument_type_ref"] = XtcePath(obj.argument_type_ref)
        kwargs["initial_value"] = (
            coerce(obj.initial_value) if obj.initial_value is not None else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ArgumentType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["argument_type_ref"] = XtcePath(obj.argument_type_ref)
        kwargs["initial_value"] = (
            coerce(obj.initial_value) if obj.initial_value is not None else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ArgumentType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["argument_type_ref"] = XtcePath(obj.argument_type_ref)
        kwargs["initial_value"] = (
            coerce(obj.initial_value) if obj.initial_value is not None else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["argument_type_ref"] = str(self.argument_type_ref)
        if self.initial_value is None:
            initial_value = None
        elif isinstance(self.initial_value, (list, dict)):
            initial_value = str(self.initial_value)
        else:
            initial_value = uncoerce(self.initial_value)
        kwargs["initial_value"] = initial_value
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["argument_type_ref"] = str(self.argument_type_ref)
        if self.initial_value is None:
            initial_value = None
        elif isinstance(self.initial_value, (list, dict)):
            initial_value = str(self.initial_value)
        else:
            initial_value = uncoerce(self.initial_value)
        kwargs["initial_value"] = initial_value
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["argument_type_ref"] = str(self.argument_type_ref)
        if self.initial_value is None:
            initial_value = None
        elif isinstance(self.initial_value, (list, dict)):
            initial_value = str(self.initial_value)
        else:
            initial_value = uncoerce(self.initial_value)
        kwargs["initial_value"] = initial_value
        return kwargs


class ArgumentAssignment(XtceBaseModel):
    """Define an assignment of a value to a command argument."""

    # TODO maybe move to argument.py
    name: Annotated[XtcePath, AfterValidator(require_regex(EXPD_NAME_REF_NO_PATH))] = (
        Field(
            ...,
            examples=["TODO"],
            json_schema_extra={"pattern": EXPD_NAME_REF_NO_PATH},
        )
    )
    """The name of the argument to assign."""

    value: int | float | str | bool | bytes | datetime.timedelta | datetime.datetime

    # TODO validate type of value, validate ranges, validate enumerations

    _v1_1_type = xtce_1_1.MetaCommandType.BaseMetaCommand.ArgumentAssignmentList.ArgumentAssignment
    _v1_2_type = xtce_1_2.ArgumentAssignmentType
    _v1_3_type = xtce_1_3.ArgumentAssignmentType

    @classmethod
    def _from_v1_1_kwargs(
        cls,
        obj: xtce_1_1.MetaCommandType.BaseMetaCommand.ArgumentAssignmentList.ArgumentAssignment,
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["name"] = XtcePath(obj.argument_name)
        kwargs["value"] = coerce(obj.argument_value)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ArgumentAssignmentType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["name"] = XtcePath(obj.argument_name)
        kwargs["value"] = coerce(obj.argument_value)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ArgumentAssignmentType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["name"] = XtcePath(obj.argument_name)
        kwargs["value"] = coerce(obj.argument_value)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["argument_name"] = str(self.name)
        kwargs["argument_value"] = uncoerce(self.value)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["argument_name"] = str(self.name)
        kwargs["argument_value"] = uncoerce(self.value)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["argument_name"] = str(self.name)
        kwargs["argument_value"] = uncoerce(self.value)
        return kwargs


class BaseMetaCommand(XtceBaseModel):
    """Define a base meta command."""

    argument_assignments: list[ArgumentAssignment] = Field(default_factory=list)
    """List of argument assignments for the base meta command."""

    meta_command_ref: Annotated[
        XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))
    ] = Field(
        ...,
        examples=["TODO"],
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to a meta command."""

    _v1_1_type = xtce_1_1.MetaCommandType.BaseMetaCommand
    _v1_2_type = xtce_1_2.BaseMetaCommandType
    _v1_3_type = xtce_1_3.BaseMetaCommandType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.MetaCommandType.BaseMetaCommand
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["argument_assignments"] = (
            [
                ArgumentAssignment._from_v1_1_kwargs(a)
                for a in obj.argument_assignment_list.argument_assignment
            ]
            if obj.argument_assignment_list is not None
            else []
        )
        kwargs["meta_command_ref"] = XtcePath(obj.meta_command_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.BaseMetaCommandType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["argument_assignments"] = (
            [
                ArgumentAssignment._from_v1_2_kwargs(a)
                for a in obj.argument_assignment_list.argument_assignment
            ]
            if obj.argument_assignment_list is not None
            else []
        )
        kwargs["meta_command_ref"] = XtcePath(obj.meta_command_ref)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.BaseMetaCommandType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["argument_assignments"] = (
            [
                ArgumentAssignment._from_v1_3_kwargs(a)
                for a in obj.argument_assignment_list.argument_assignment
            ]
            if obj.argument_assignment_list is not None
            else []
        )
        kwargs["meta_command_ref"] = XtcePath(obj.meta_command_ref)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["argument_assignment_list"] = (
            xtce_1_1.MetaCommandType.BaseMetaCommand.ArgumentAssignmentList(
                argument_assignment=[
                    a._to_v1_1(policy) for a in self.argument_assignments
                ]
            )
            if self.argument_assignments
            else None
        )
        kwargs["meta_command_ref"] = str(self.meta_command_ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["argument_assignment_list"] = (
            xtce_1_2.ArgumentAssignmentListType(
                argument_assignment=[a._to_v1_2(policy) for a in self.argument_assignments]
            )
            if self.argument_assignments
            else None
        )
        kwargs["meta_command_ref"] = str(self.meta_command_ref)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["argument_assignment_list"] = (
            xtce_1_3.ArgumentAssignmentListType(
                argument_assignment=[a._to_v1_3(policy) for a in self.argument_assignments]
            )
            if self.argument_assignments
            else None
        )
        kwargs["meta_command_ref"] = str(self.meta_command_ref)
        return kwargs


class TransmissionConstraint(MatchCriteria):
    """Define a transmission constraint for a meta command."""

    argument_restrictions: list[ArgumentAssignment] = Field(default_factory=list)
    """A list of argument values that restrict the transmission of the meta command."""

    timeout: datetime.timedelta | None = None
    """The maximum time allowed for the transmission of the meta command."""

    suspendable: bool = False
    """Indicates whether the transmission of the meta command can be suspended."""

    _v1_1_type = (
        xtce_1_1.MetaCommandType.TransmissionConstraintList.TransmissionConstraint
    )
    _v1_2_type = xtce_1_2.TransmissionConstraintType
    _v1_3_type = xtce_1_3.TransmissionConstraintType

    @classmethod
    def _from_v1_1_kwargs(
        cls,
        obj: xtce_1_1.MetaCommandType.TransmissionConstraintList.TransmissionConstraint,
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["argument_restrictions"] = []
        kwargs["timeout"] = (
            xml_duration_to_timedelta(obj.time_out)
            if obj.time_out is not None
            else None
        )
        kwargs["suspendable"] = obj.suspendable
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.TransmissionConstraintType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["argument_restrictions"] = []
        kwargs["timeout"] = (
            xml_duration_to_timedelta(obj.time_out)
            if obj.time_out is not None
            else None
        )
        kwargs["suspendable"] = obj.suspendable
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.TransmissionConstraintType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["argument_restrictions"] = (
            [
                ArgumentAssignment._from_v1_3(a)
                for a in obj.argument_restriction_list.argument_assignment
            ]
            if obj.argument_restriction_list is not None
            else []
        )
        kwargs["timeout"] = (
            xml_duration_to_timedelta(obj.time_out)
            if obj.time_out is not None
            else None
        )
        kwargs["suspendable"] = obj.suspendable
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="argument_restrictions",
            current_value=self.argument_restrictions,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=[],
        )
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["time_out"] = (
            timedelta_to_xml_duration(self.timeout)
            if self.timeout is not None
            else None
        )
        kwargs["suspendable"] = self.suspendable
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="argument_restrictions",
            current_value=self.argument_restrictions,
            target_version=XtceVersion.V1_2,
            policy=policy,
            empty_value=[],
        )
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["time_out"] = (
            timedelta_to_xml_duration(self.timeout)
            if self.timeout is not None
            else None
        )
        kwargs["suspendable"] = self.suspendable
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["argument_restriction_list"] = (
            xtce_1_3.ArgumentAssignmentListType(
                argument_assignment=[
                    a._to_v1_3(policy) for a in self.argument_restrictions
                ]
            )
            if self.argument_restrictions
            else None
        )
        kwargs["time_out"] = (
            timedelta_to_xml_duration(self.timeout)
            if self.timeout is not None
            else None
        )
        kwargs["suspendable"] = self.suspendable
        return kwargs


class Significance(XtceBaseModel):
    """Define the significance of a meta command."""

    space_system_at_risk: Annotated[
        XtcePath | None, AfterValidator(require_regex(NAME_REF_W_PATH))
    ] = Field(
        default=None,
        examples=["TODO"],
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to the space system that is at risk."""

    reason_for_warning: str | None = None
    """Describe the reason for the warning."""

    consequence_level: ConsequenceLevel = ConsequenceLevel.NORMAL
    """Indicate the level of consequence associated with the warning."""

    _v1_1_type = xtce_1_1.SignificanceType
    _v1_2_type = xtce_1_2.SignificanceType
    _v1_3_type = xtce_1_3.SignificanceType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.SignificanceType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["space_system_at_risk"] = (
            XtcePath(obj.space_system_at_risk)
            if obj.space_system_at_risk is not None
            else None
        )
        kwargs["reason_for_warning"] = obj.reason_for_warning
        if obj.consequence_level is not None:
            try:
                consequence_level = ConsequenceLevel(obj.consequence_level.value)
            except ValueError:
                consequence_level = ConsequenceLevel.NORMAL
        else:
            consequence_level = ConsequenceLevel.NORMAL
        kwargs["consequence_level"] = consequence_level
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.SignificanceType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["space_system_at_risk"] = (
            XtcePath(obj.space_system_at_risk)
            if obj.space_system_at_risk is not None
            else None
        )
        kwargs["reason_for_warning"] = obj.reason_for_warning
        kwargs["consequence_level"] = ConsequenceLevel(obj.consequence_level.value)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.SignificanceType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["space_system_at_risk"] = (
            XtcePath(obj.space_system_at_risk)
            if obj.space_system_at_risk is not None
            else None
        )
        kwargs["reason_for_warning"] = obj.reason_for_warning
        kwargs["consequence_level"] = ConsequenceLevel(obj.consequence_level.value)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["space_system_at_risk"] = (
            str(self.space_system_at_risk)
            if self.space_system_at_risk is not None
            else None
        )
        kwargs["reason_for_warning"] = self.reason_for_warning

        self._enforce_restricted_value(
            field_name="consequence_level",
            current_value=self.consequence_level,
            allowed_values={
            ConsequenceLevel.NORMAL,
            ConsequenceLevel.CRITICAL,
        },
            target_version=XtceVersion.V1_1,
            policy=policy,
        )
        try:
            consequence_level = xtce_1_1.SignificanceTypeConsequenceLevel(
                self.consequence_level.value
            )
        except ValueError:
            consequence_level = xtce_1_1.SignificanceTypeConsequenceLevel.NONE
        kwargs["consequence_level"] = consequence_level
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["space_system_at_risk"] = (
            str(self.space_system_at_risk)
            if self.space_system_at_risk is not None
            else None
        )
        kwargs["reason_for_warning"] = self.reason_for_warning
        kwargs["consequence_level"] = xtce_1_2.ConsequenceLevelType(
            self.consequence_level.value
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["space_system_at_risk"] = (
            str(self.space_system_at_risk)
            if self.space_system_at_risk is not None
            else None
        )
        kwargs["reason_for_warning"] = self.reason_for_warning
        kwargs["consequence_level"] = xtce_1_3.ConsequenceLevelType(
            self.consequence_level.value
        )
        return kwargs


class ContextSignificance(XtceBaseModel):
    """Define a context significance within a command."""

    context_match: ContextMatch
    """The context match criteria that must be met to enable to significance."""

    significance: Significance
    """The significance of this meta command."""

    _v1_1_type = xtce_1_1.MetaCommandType.ContextSignificanceList.ContextSignificance
    _v1_2_type = xtce_1_2.ContextSignificanceType
    _v1_3_type = xtce_1_3.ContextSignificanceType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.MetaCommandType.ContextSignificanceList.ContextSignificance
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["context_match"] = ContextMatch._from_v1_1(obj.context_match)
        kwargs["significance"] = Significance._from_v1_1(obj.significance)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ContextSignificanceType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["context_match"] = ContextMatch._from_v1_2(obj.context_match)
        kwargs["significance"] = Significance._from_v1_2(obj.significance)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ContextSignificanceType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["context_match"] = ContextMatch._from_v1_3(obj.context_match)
        kwargs["significance"] = Significance._from_v1_3(obj.significance)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["context_match"] = self.context_match._to_v1_1(policy)
        kwargs["significance"] = self.significance._to_v1_1(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["context_match"] = self.context_match._to_v1_2(policy)
        kwargs["significance"] = self.significance._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["context_match"] = self.context_match._to_v1_3(policy)
        kwargs["significance"] = self.significance._to_v1_3(policy)
        return kwargs


class Interlock(XtceBaseModel):
    """Define a constraint on the next command.

    Interlocks only apply to the next command. They will block successive commands until
    this command has reached a certain stage of verification.

    """

    scope_to_space_system: Annotated[
        XtcePath | None, AfterValidator(require_regex(NAME_REF_W_PATH))
    ] = Field(
        default=None,
        examples=["TODO"],
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to the space system this interlock applies to."""

    verification_to_wait_for: VerifierType = VerifierType.COMPLETE
    """The type of verification to wait for before the interlock is considered
    satisfied.
    """

    verification_progress_percentage: float | None = None
    """The progress percentage of the verification to wait for before the interlock is
    considered satisfied.
    """

    suspendable: bool = False
    """Indicates whether the interlock can be suspended."""

    _v1_1_type = xtce_1_1.MetaCommandType.Interlock
    _v1_2_type = xtce_1_2.InterlockType
    _v1_3_type = xtce_1_3.InterlockType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.MetaCommandType.Interlock
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["scope_to_space_system"] = (
            XtcePath(obj.scope_to_space_system)
            if obj.scope_to_space_system is not None
            else None
        )
        kwargs["verification_to_wait_for"] = VerifierType(
            obj.verification_to_wait_for.value
        )
        kwargs["verification_progress_percentage"] = (
            float(obj.verification_progress_percentage)
            if obj.verification_progress_percentage is not None
            else None
        )
        kwargs["suspendable"] = obj.suspendable
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.InterlockType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["scope_to_space_system"] = (
            XtcePath(obj.scope_to_space_system)
            if obj.scope_to_space_system is not None
            else None
        )
        kwargs["verification_to_wait_for"] = VerifierType(
            obj.verification_to_wait_for.value
        )
        kwargs["verification_progress_percentage"] = (
            float(obj.verification_progress_percentage)
            if obj.verification_progress_percentage is not None
            else None
        )
        kwargs["suspendable"] = obj.suspendable
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.InterlockType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["scope_to_space_system"] = (
            XtcePath(obj.scope_to_space_system)
            if obj.scope_to_space_system is not None
            else None
        )
        kwargs["verification_to_wait_for"] = VerifierType(
            obj.verification_to_wait_for.value
        )
        kwargs["verification_progress_percentage"] = (
            float(obj.verification_progress_percentage)
            if obj.verification_progress_percentage is not None
            else None
        )
        kwargs["suspendable"] = obj.suspendable
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["scope_to_space_system"] = (
            str(self.scope_to_space_system)
            if self.scope_to_space_system is not None
            else None
        )
        kwargs["verification_to_wait_for"] = xtce_1_1.VerifierEnumerationType(
            self.verification_to_wait_for.value
        )
        kwargs["verification_progress_percentage"] = (
            Decimal(str(self.verification_progress_percentage))
            if self.verification_progress_percentage is not None
            else None
        )
        kwargs["suspendable"] = self.suspendable
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["scope_to_space_system"] = (
            str(self.scope_to_space_system)
            if self.scope_to_space_system is not None
            else None
        )
        kwargs["verification_to_wait_for"] = xtce_1_2.VerifierEnumerationType(
            self.verification_to_wait_for.value
        )
        kwargs["verification_progress_percentage"] = (
            Decimal(str(self.verification_progress_percentage))
            if self.verification_progress_percentage is not None
            else None
        )
        kwargs["suspendable"] = self.suspendable
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["scope_to_space_system"] = (
            str(self.scope_to_space_system)
            if self.scope_to_space_system is not None
            else None
        )
        kwargs["verification_to_wait_for"] = xtce_1_3.VerifierEnumerationType(
            self.verification_to_wait_for.value
        )
        kwargs["verification_progress_percentage"] = (
            Decimal(str(self.verification_progress_percentage))
            if self.verification_progress_percentage is not None
            else None
        )
        kwargs["suspendable"] = self.suspendable
        return kwargs


class ParameterToSet(ParameterRef):
    """Define a parameter to set after a command has been verified."""

    derivation_or_new_value: str | ArgumentMathOperation | None = None
    """The derivation or new value to set for the parameter."""

    set_on_verification: VerifierType = VerifierType.COMPLETE
    """The verification stage at which the parameter should be set."""

    _v1_1_type = xtce_1_1.MetaCommandType.ParameterToSetList.ParameterToSet
    _v1_2_type = xtce_1_2.ParameterToSetType
    _v1_3_type = xtce_1_3.ParameterToSetType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.MetaCommandType.ParameterToSetList.ParameterToSet
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["derivation_or_new_value"] = (
            ArgumentMathOperation._from_v1_1(obj.choice)
            if isinstance(obj.choice, xtce_1_1.MathOperationType)
            else obj.choice
        )
        kwargs["set_on_verification"] = VerifierType(obj.set_on_verification.value)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ParameterToSetType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["derivation_or_new_value"] = (
            ArgumentMathOperation._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.MathOperationCalibratorType)
            else obj.choice
        )
        kwargs["set_on_verification"] = VerifierType(obj.set_on_verification.value)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ParameterToSetType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["derivation_or_new_value"] = (
            ArgumentMathOperation._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.ArgumentMathOperationType)
            else obj.choice
        )
        kwargs["set_on_verification"] = VerifierType(obj.set_on_verification.value)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["choice"] = (
            self.derivation_or_new_value._to_v1_1(policy)
            if isinstance(self.derivation_or_new_value, ArgumentMathOperation)
            else self.derivation_or_new_value
        )
        kwargs["set_on_verification"] = xtce_1_1.VerifierEnumerationType(
            self.set_on_verification.value
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = (
            self.derivation_or_new_value._to_v1_2(policy)
            if isinstance(self.derivation_or_new_value, ArgumentMathOperation)
            else self.derivation_or_new_value
        )
        kwargs["set_on_verification"] = xtce_1_2.VerifierEnumerationType(
            self.set_on_verification.value
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = (
            self.derivation_or_new_value._to_v1_3(policy)
            if isinstance(self.derivation_or_new_value, ArgumentMathOperation)
            else self.derivation_or_new_value
        )
        kwargs["set_on_verification"] = xtce_1_3.VerifierEnumerationType(
            self.set_on_verification.value
        )
        return kwargs


class ParameterToSuspendAlarmsOn(ParameterRef):
    """Define a parameter to suspend alarms on when a verifier finishes."""

    suspense_time: datetime.timedelta
    """The duration for which alarms should be suspended on this parameter."""

    verifier_to_trigger_on: VerifierType = VerifierType.RELEASE
    """The verifier that triggers the suspension of alarms on this parameter."""

    _v1_1_type = xtce_1_1.MetaCommandType.ParametersToSuspendAlarmsOnSet.ParameterToSuspendAlarmsOn
    _v1_2_type = xtce_1_2.ParameterToSuspendAlarmsOnType
    _v1_3_type = xtce_1_3.ParameterToSuspendAlarmsOnType

    @classmethod
    def _from_v1_1_kwargs(
        cls,
        obj: xtce_1_1.MetaCommandType.ParametersToSuspendAlarmsOnSet.ParameterToSuspendAlarmsOn,
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["suspense_time"] = xml_duration_to_timedelta(obj.suspense_time)
        kwargs["verifier_to_trigger_on"] = VerifierType(
            obj.verifier_to_trigger_on.value
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ParameterToSuspendAlarmsOnType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["suspense_time"] = xml_duration_to_timedelta(obj.suspense_time)
        kwargs["verifier_to_trigger_on"] = VerifierType(
            obj.verifier_to_trigger_on.value
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ParameterToSuspendAlarmsOnType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["suspense_time"] = xml_duration_to_timedelta(obj.suspense_time)
        kwargs["verifier_to_trigger_on"] = VerifierType(
            obj.verifier_to_trigger_on.value
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["suspense_time"] = timedelta_to_xml_duration(self.suspense_time)
        kwargs["verifier_to_trigger_on"] = xtce_1_1.VerifierEnumerationType(
            self.verifier_to_trigger_on.value
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["suspense_time"] = timedelta_to_xml_duration(self.suspense_time)
        kwargs["verifier_to_trigger_on"] = xtce_1_2.VerifierEnumerationType(
            self.verifier_to_trigger_on.value
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["suspense_time"] = timedelta_to_xml_duration(self.suspense_time)
        kwargs["verifier_to_trigger_on"] = xtce_1_3.VerifierEnumerationType(
            self.verifier_to_trigger_on.value
        )
        return kwargs


class MetaCommand(NameDescriptionBase):
    """Define a command."""

    base_meta_command: BaseMetaCommand | None = None
    """The base meta-command from which this command inherits."""

    system_name: str | None = None
    """The name of the system to which this command belongs."""

    arguments: list[Argument] = Field(default_factory=list)
    """The list of arguments for this command."""

    command_container: CommandContainer | None = None
    """The command container associated with this command."""

    transmission_constraints: list[TransmissionConstraint] = Field(default_factory=list)
    """The list of transmission constraints for this command."""

    default_significance: Significance | None = None
    """The default significance for this command."""

    context_significance: list[ContextSignificance] = Field(default_factory=list)
    """The list of context-specific significances for this command."""

    interlock: Interlock | None = None
    """The interlock associated with this command."""

    verifier_set: VerifierSet | None = None
    """The verifier set associated with this command."""

    parameters_to_set: list[ParameterToSet] = Field(default_factory=list)
    """The list of parameters to set when this command is executed."""

    parameters_to_suspend_alarms_on: list[ParameterToSuspendAlarmsOn] = Field(
        default_factory=list
    )
    """The list of parameters for which alarms should be suspended when this command is
    executed.
    """

    abstract: bool = False
    """Indicates whether this command is abstract."""

    _v1_1_type = xtce_1_1.MetaCommandType
    _v1_2_type = xtce_1_2.MetaCommandType
    _v1_3_type = xtce_1_3.MetaCommandType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.MetaCommandType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["base_meta_command"] = (
            BaseMetaCommand._from_v1_1(obj.base_meta_command)
            if obj.base_meta_command is not None
            else None
        )
        kwargs["system_name"] = obj.system_name if obj.system_name is not None else None
        kwargs["arguments"] = (
            [Argument._from_v1_1(arg) for arg in obj.argument_list.argument]
            if obj.argument_list is not None
            else []
        )
        kwargs["command_container"] = (
            CommandContainer._from_v1_1(obj.command_container)
            if obj.command_container is not None
            else None
        )
        kwargs["transmission_constraints"] = (
            [
                TransmissionConstraint._from_v1_1(tc)
                for tc in obj.transmission_constraint_list.transmission_constraint
            ]
            if obj.transmission_constraint_list is not None
            else []
        )
        kwargs["default_significance"] = (
            Significance._from_v1_1(obj.default_significance)
            if obj.default_significance is not None
            else None
        )
        kwargs["context_significance"] = (
            [
                ContextSignificance._from_v1_1(cs)
                for cs in obj.context_significance_list.context_significance
            ]
            if obj.context_significance_list is not None
            else []
        )
        kwargs["interlock"] = (
            Interlock._from_v1_1(obj.interlock)
            if obj.interlock is not None
            else None
        )
        kwargs["verifier_set"] = (
            VerifierSet._from_v1_1(obj.verifier_set)
            if obj.verifier_set is not None
            else None
        )
        kwargs["parameters_to_set"] = (
            [
                ParameterToSet._from_v1_1(pts)
                for pts in obj.parameter_to_set_list.parameter_to_set
            ]
            if obj.parameter_to_set_list is not None
            else []
        )
        kwargs["parameters_to_suspend_alarms_on"] = (
            [
                ParameterToSuspendAlarmsOn._from_v1_1(ptsa)
                for ptsa in obj.parameters_to_suspend_alarms_on_set.parameter_to_suspend_alarms_on
            ]
            if obj.parameters_to_suspend_alarms_on_set is not None
            else []
        )
        kwargs["abstract"] = obj.abstract
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.MetaCommandType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["base_meta_command"] = (
            BaseMetaCommand._from_v1_2(obj.base_meta_command)
            if obj.base_meta_command is not None
            else None
        )
        kwargs["system_name"] = obj.system_name if obj.system_name is not None else None
        kwargs["arguments"] = (
            [Argument._from_v1_2(arg) for arg in obj.argument_list.argument]
            if obj.argument_list is not None
            else []
        )
        kwargs["command_container"] = (
            CommandContainer._from_v1_2(obj.command_container)
            if obj.command_container is not None
            else None
        )
        kwargs["transmission_constraints"] = (
            [
                TransmissionConstraint._from_v1_2(tc)
                for tc in obj.transmission_constraint_list.transmission_constraint
            ]
            if obj.transmission_constraint_list is not None
            else []
        )
        kwargs["default_significance"] = (
            Significance._from_v1_2(obj.default_significance)
            if obj.default_significance is not None
            else None
        )
        kwargs["context_significance"] = (
            [
                ContextSignificance._from_v1_2(cs)
                for cs in obj.context_significance_list.context_significance
            ]
            if obj.context_significance_list is not None
            else []
        )
        kwargs["interlock"] = (
            Interlock._from_v1_2(obj.interlock)
            if obj.interlock is not None
            else None
        )
        kwargs["verifier_set"] = (
            VerifierSet._from_v1_2(obj.verifier_set)
            if obj.verifier_set is not None
            else None
        )
        kwargs["parameters_to_set"] = (
            [
                ParameterToSet._from_v1_2(pts)
                for pts in obj.parameter_to_set_list.parameter_to_set
            ]
            if obj.parameter_to_set_list is not None
            else []
        )
        kwargs["parameters_to_suspend_alarms_on"] = (
            [
                ParameterToSuspendAlarmsOn._from_v1_2(ptsa)
                for ptsa in obj.parameters_to_suspend_alarms_on_set.parameter_to_suspend_alarms_on
            ]
            if obj.parameters_to_suspend_alarms_on_set is not None
            else []
        )
        kwargs["abstract"] = obj.abstract
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.MetaCommandType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["base_meta_command"] = (
            BaseMetaCommand._from_v1_3(obj.base_meta_command)
            if obj.base_meta_command is not None
            else None
        )
        kwargs["system_name"] = obj.system_name if obj.system_name is not None else None
        kwargs["arguments"] = (
            [Argument._from_v1_3(arg) for arg in obj.argument_list.argument]
            if obj.argument_list is not None
            else []
        )
        kwargs["command_container"] = (
            CommandContainer._from_v1_3(obj.command_container)
            if obj.command_container is not None
            else None
        )
        kwargs["transmission_constraints"] = (
            [
                TransmissionConstraint._from_v1_3(tc)
                for tc in obj.transmission_constraint_list.transmission_constraint
            ]
            if obj.transmission_constraint_list is not None
            else []
        )
        kwargs["default_significance"] = (
            Significance._from_v1_3(obj.default_significance)
            if obj.default_significance is not None
            else None
        )
        kwargs["context_significance"] = (
            [
                ContextSignificance._from_v1_3(cs)
                for cs in obj.context_significance_list.context_significance
            ]
            if obj.context_significance_list is not None
            else []
        )
        kwargs["interlock"] = (
            Interlock._from_v1_3(obj.interlock)
            if obj.interlock is not None
            else None
        )
        kwargs["verifier_set"] = (
            VerifierSet._from_v1_3(obj.verifier_set)
            if obj.verifier_set is not None
            else None
        )
        kwargs["parameters_to_set"] = (
            [
                ParameterToSet._from_v1_3(pts)
                for pts in obj.parameter_to_set_list.parameter_to_set
            ]
            if obj.parameter_to_set_list is not None
            else []
        )
        kwargs["parameters_to_suspend_alarms_on"] = (
            [
                ParameterToSuspendAlarmsOn._from_v1_3(ptsa)
                for ptsa in obj.parameters_to_suspend_alarms_on_set.parameter_to_suspend_alarms_on
            ]
            if obj.parameters_to_suspend_alarms_on_set is not None
            else []
        )
        kwargs["abstract"] = obj.abstract
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["base_meta_command"] = (
            self.base_meta_command._to_v1_1(policy)
            if self.base_meta_command is not None
            else None
        )
        kwargs["system_name"] = self.system_name
        kwargs["command_container"] = (
            self.command_container._to_v1_1(policy)
            if self.command_container is not None
            else None
        )
        kwargs["argument_list"] = (
            xtce_1_1.MetaCommandType.ArgumentList(
                argument=[arg._to_v1_1(policy) for arg in self.arguments]
            )
            if self.arguments
            else None
        )
        kwargs["transmission_constraint_list"] = (
            xtce_1_1.MetaCommandType.TransmissionConstraintList(
                transmission_constraint=[
                    tc._to_v1_1(policy) for tc in self.transmission_constraints
                ]
            )
            if self.transmission_constraints
            else None
        )
        kwargs["default_significance"] = (
            self.default_significance._to_v1_1(policy)
            if self.default_significance is not None
            else None
        )
        kwargs["context_significance_list"] = (
            xtce_1_1.MetaCommandType.ContextSignificanceList(
                context_significance=[
                    cs._to_v1_1(policy) for cs in self.context_significance
                ]
            )
            if self.context_significance
            else None
        )
        kwargs["interlock"] = (
            self.interlock._to_v1_1(policy)
            if self.interlock is not None
            else None
        )
        kwargs["verifier_set"] = (
            self.verifier_set._to_v1_1(policy)
            if self.verifier_set is not None
            else None
        )
        kwargs["parameter_to_set_list"] = (
            xtce_1_1.MetaCommandType.ParameterToSetList(
                parameter_to_set=[pts._to_v1_1(policy) for pts in self.parameters_to_set]
            )
            if self.parameters_to_set
            else None
        )
        kwargs["parameters_to_suspend_alarms_on_set"] = (
            xtce_1_1.MetaCommandType.ParametersToSuspendAlarmsOnSet(
                parameter_to_suspend_alarms_on=[
                    ptsa._to_v1_1(policy)
                    for ptsa in self.parameters_to_suspend_alarms_on
                ]
            )
            if self.parameters_to_suspend_alarms_on
            else None
        )
        kwargs["abstract"] = self.abstract
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["base_meta_command"] = (
            self.base_meta_command._to_v1_2(policy)
            if self.base_meta_command is not None
            else None
        )
        kwargs["system_name"] = self.system_name
        kwargs["command_container"] = (
            self.command_container._to_v1_2(policy)
            if self.command_container is not None
            else None
        )
        kwargs["argument_list"] = (
            xtce_1_2.ArgumentListType(
                argument=[arg._to_v1_2(policy) for arg in self.arguments]
            )
            if self.arguments
            else None
        )
        kwargs["transmission_constraint_list"] = (
            xtce_1_2.TransmissionConstraintListType(
                transmission_constraint=[
                    tc._to_v1_2(policy) for tc in self.transmission_constraints
                ]
            )
            if self.transmission_constraints
            else None
        )
        kwargs["default_significance"] = (
            self.default_significance._to_v1_2(policy)
            if self.default_significance is not None
            else None
        )
        kwargs["context_significance_list"] = (
            xtce_1_2.ContextSignificanceListType(
                context_significance=[
                    cs._to_v1_2(policy) for cs in self.context_significance
                ]
            )
            if self.context_significance
            else None
        )
        kwargs["interlock"] = (
            self.interlock._to_v1_2(policy)
            if self.interlock is not None
            else None
        )
        kwargs["verifier_set"] = (
            self.verifier_set._to_v1_2(policy)
            if self.verifier_set is not None
            else None
        )
        kwargs["parameter_to_set_list"] = (
            xtce_1_2.ParameterToSetListType(
                parameter_to_set=[pts._to_v1_2(policy) for pts in self.parameters_to_set]
            )
            if self.parameters_to_set
            else None
        )
        kwargs["parameters_to_suspend_alarms_on_set"] = (
            xtce_1_2.ParametersToSuspendAlarmsOnSetType(
                parameter_to_suspend_alarms_on=[
                    ptsa._to_v1_2(policy)
                    for ptsa in self.parameters_to_suspend_alarms_on
                ]
            )
            if self.parameters_to_suspend_alarms_on
            else None
        )
        kwargs["abstract"] = self.abstract
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["base_meta_command"] = (
            self.base_meta_command._to_v1_3(policy)
            if self.base_meta_command is not None
            else None
        )
        kwargs["system_name"] = self.system_name
        kwargs["command_container"] = (
            self.command_container._to_v1_3(policy)
            if self.command_container is not None
            else None
        )
        kwargs["argument_list"] = (
            xtce_1_3.ArgumentListType(
                argument=[arg._to_v1_3(policy) for arg in self.arguments]
            )
            if self.arguments
            else None
        )
        kwargs["transmission_constraint_list"] = (
            xtce_1_3.TransmissionConstraintListType(
                transmission_constraint=[
                    tc._to_v1_3(policy) for tc in self.transmission_constraints
                ]
            )
            if self.transmission_constraints
            else None
        )
        kwargs["default_significance"] = (
            self.default_significance._to_v1_3(policy)
            if self.default_significance is not None
            else None
        )
        kwargs["context_significance_list"] = (
            xtce_1_3.ContextSignificanceListType(
                context_significance=[
                    cs._to_v1_3(policy) for cs in self.context_significance
                ]
            )
            if self.context_significance
            else None
        )
        kwargs["interlock"] = (
            self.interlock._to_v1_3(policy)
            if self.interlock is not None
            else None
        )
        kwargs["verifier_set"] = (
            self.verifier_set._to_v1_3(policy)
            if self.verifier_set is not None
            else None
        )
        kwargs["parameter_to_set_list"] = (
            xtce_1_3.ParameterToSetListType(
                parameter_to_set=[pts._to_v1_3(policy) for pts in self.parameters_to_set]
            )
            if self.parameters_to_set
            else None
        )
        kwargs["parameters_to_suspend_alarms_on_set"] = (
            xtce_1_3.ParametersToSuspendAlarmsOnSetType(
                parameter_to_suspend_alarms_on=[
                    ptsa._to_v1_3(policy)
                    for ptsa in self.parameters_to_suspend_alarms_on
                ]
            )
            if self.parameters_to_suspend_alarms_on
            else None
        )
        kwargs["abstract"] = self.abstract
        return kwargs


class MetaCommandRef(XtceBaseModel):
    """A reference to a MetaCommand.

    Used to include a MetaCommand defined in another sub-system in this sub-system.

    """

    name: Annotated[XtcePath, AfterValidator(require_regex(EXPD_NAME_REF_W_PATH))] = (
        Field(
            ...,
            examples=[
                "TODO",
            ],
            json_schema_extra={"pattern": EXPD_NAME_REF_W_PATH},
        )
    )
    """A Unix-like path to a meta command."""

    def __str__(self) -> str:
        """Return the reference as a string."""
        return str(self.name)


class MetaCommandStep(XtceBaseModel):
    """Define a single meta command step within a meta command block."""

    argument_assignments: list[ArgumentAssignment] = Field(default_factory=list)
    """List of argument assignments for this meta command step."""

    meta_command_ref: Annotated[
        XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))
    ] = Field(
        ...,
        examples=["TODO"],
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to a meta command."""

    _v1_1_type = xtce_1_1.CommandMetaDataType.MetaCommandSet.BlockMetaCommand.MetaCommandStepList.MetaCommandStep
    _v1_2_type = xtce_1_2.MetaCommandStepType
    _v1_3_type = xtce_1_3.MetaCommandStepType

    @classmethod
    def _from_v1_1_kwargs(
        cls,
        obj: xtce_1_1.CommandMetaDataType.MetaCommandSet.BlockMetaCommand.MetaCommandStepList.MetaCommandStep,
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["argument_assignments"] = (
            [
                # XTCE 1.1 has a separate Argument type just for this
                ArgumentAssignment(
                    name=XtcePath(a.name),
                    value=coerce(a.value),
                )
                for a in obj.argument_list.argument
            ]
            if obj.argument_list is not None
            else []
        )
        kwargs["meta_command_ref"] = XtcePath(obj.meta_command_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.MetaCommandStepType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["argument_assignments"] = (
            [
                ArgumentAssignment._from_v1_2(a)
                for a in obj.argument_assigment_list.argument_assignment
            ]
            if obj.argument_assigment_list is not None
            else []
        )
        kwargs["meta_command_ref"] = XtcePath(obj.meta_command_ref)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.MetaCommandStepType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["argument_assignments"] = (
            [
                ArgumentAssignment._from_v1_3(a)
                for a in obj.argument_assignment_list.argument_assignment
            ]
            if obj.argument_assignment_list is not None
            else []
        )
        kwargs["meta_command_ref"] = XtcePath(obj.meta_command_ref)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["argument_list"] = (
            xtce_1_1.CommandMetaDataType.MetaCommandSet.BlockMetaCommand.MetaCommandStepList.MetaCommandStep.ArgumentList(
                argument=[
                    xtce_1_1.CommandMetaDataType.MetaCommandSet.BlockMetaCommand.MetaCommandStepList.MetaCommandStep.ArgumentList.Argument(
                        name=str(a.name),
                        value=uncoerce(a.value),
                    )
                    for a in self.argument_assignments
                ]
            )
            if self.argument_assignments
            else None
        )
        kwargs["meta_command_ref"] = str(self.meta_command_ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["argument_assigment_list"] = (
            xtce_1_2.ArgumentAssignmentListType(
                argument_assignment=[a._to_v1_2(policy) for a in self.argument_assignments]
            )
            if self.argument_assignments
            else None
        )
        kwargs["meta_command_ref"] = str(self.meta_command_ref)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["argument_assignment_list"] = (
            xtce_1_3.ArgumentAssignmentListType(
                argument_assignment=[a._to_v1_3(policy) for a in self.argument_assignments]
            )
            if self.argument_assignments
            else None
        )
        kwargs["meta_command_ref"] = str(self.meta_command_ref)
        return kwargs


class BlockMetaCommand(NameDescriptionBase):
    """Define an ordered grouping of meta commands."""

    meta_command_steps: list[MetaCommandStep] = Field(..., min_length=1)
    """A list of meta command steps.

    Duplicates are allowed. Command arguments must be fully specified.

    """

    # TODO verify arguments are fully specified

    _v1_1_type = xtce_1_1.CommandMetaDataType.MetaCommandSet.BlockMetaCommand
    _v1_2_type = xtce_1_2.BlockMetaCommandType
    _v1_3_type = xtce_1_3.BlockMetaCommandType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.CommandMetaDataType.MetaCommandSet.BlockMetaCommand
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["meta_command_steps"] = [
            MetaCommandStep._from_v1_1(s)
            for s in obj.meta_command_step_list.meta_command_step
        ]
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.BlockMetaCommandType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["meta_command_steps"] = [
            MetaCommandStep._from_v1_2(s)
            for s in obj.meta_command_step_list.meta_command_step
        ]
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.BlockMetaCommandType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["meta_command_steps"] = [
            MetaCommandStep._from_v1_3(s)
            for s in obj.meta_command_step_list.meta_command_step
        ]
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["meta_command_step_list"] = (
            xtce_1_1.CommandMetaDataType.MetaCommandSet.BlockMetaCommand.MetaCommandStepList(
                meta_command_step=[s._to_v1_1(policy) for s in self.meta_command_steps]
            )
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["meta_command_step_list"] = xtce_1_2.MetaCommandStepListType(
            meta_command_step=[s._to_v1_2(policy) for s in self.meta_command_steps]
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["meta_command_step_list"] = xtce_1_3.MetaCommandStepListType(
            meta_command_step=[s._to_v1_3(policy) for s in self.meta_command_steps]
        )
        return kwargs


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

    containers: list[SequenceContainer] = Field(default_factory=list)
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

    def validate_semantics(self):
        """Perform semantic validation of this CommandMetadata."""
        # TODO make sure there are no duplicate parameter names

    _v1_1_type = xtce_1_1.CommandMetaDataType
    _v1_2_type = xtce_1_2.CommandMetaDataType
    _v1_3_type = xtce_1_3.CommandMetaDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.CommandMetaDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["parameter_types"] = (
            [
                IntegerParameter._from_v1_1(p)
                if isinstance(p, xtce_1_1.ParameterTypeSetType.IntegerParameterType)
                else FloatParameter._from_v1_1(p)
                if isinstance(p, xtce_1_1.ParameterTypeSetType.FloatParameterType)
                else StringParameter._from_v1_1(p)
                if isinstance(p, xtce_1_1.ParameterTypeSetType.StringParameterType)
                else BinaryParameter._from_v1_1(p)
                if isinstance(p, xtce_1_1.ParameterTypeSetType.BinaryParameterType)
                else BooleanParameter._from_v1_1(p)
                if isinstance(p, xtce_1_1.ParameterTypeSetType.BooleanParameterType)
                else EnumeratedParameter._from_v1_1(p)
                if isinstance(p, xtce_1_1.ParameterTypeSetType.EnumeratedParameterType)
                else ArrayParameter._from_v1_1(p)
                if isinstance(p, xtce_1_1.ArrayDataTypeType)
                else AggregateParameter._from_v1_1(p)
                if isinstance(p, xtce_1_1.AggregateDataType)
                else RelativeTimeParameter._from_v1_1(p)
                if isinstance(
                    p, xtce_1_1.ParameterTypeSetType.RelativeTimeParameterType
                )
                else AbsoluteTimeParameter._from_v1_1(p)
                for p in obj.parameter_type_set.choice
            ]
            if obj.parameter_type_set is not None
            else []
        )
        kwargs["parameters"] = (
            [
                Parameter._from_v1_1(p)
                if isinstance(p, xtce_1_1.ParameterSetType.Parameter)
                else ParameterRef._from_v1_1(p)
                for p in obj.parameter_set.choice
            ]
            if obj.parameter_set is not None
            else []
        )
        kwargs["argument_types"] = (
            [
                IntegerArgument._from_v1_1(p)
                if isinstance(p, xtce_1_1.ArgumentTypeSetType.IntegerArgumentType)
                else FloatArgument._from_v1_1(p)
                if isinstance(p, xtce_1_1.ArgumentTypeSetType.FloatArgumentType)
                else StringArgument._from_v1_1(p)
                if isinstance(p, xtce_1_1.StringDataType)
                else BinaryArgument._from_v1_1(p)
                if isinstance(p, xtce_1_1.BinaryDataType)
                else BooleanArgument._from_v1_1(p)
                if isinstance(p, xtce_1_1.BooleanDataType)
                else EnumeratedArgument._from_v1_1(p)
                if isinstance(p, xtce_1_1.EnumeratedDataType)
                else ArrayArgument._from_v1_1(p)
                if isinstance(p, xtce_1_1.ArrayDataTypeType)
                else AggregateArgument._from_v1_1(p)
                if isinstance(p, xtce_1_1.AggregateDataType)
                else RelativeTimeArgument._from_v1_1(p)
                if isinstance(p, xtce_1_1.RelativeTimeDataType)
                else AbsoluteTimeArgument._from_v1_1(p)
                for p in obj.argument_type_set.choice
            ]
            if obj.argument_type_set is not None
            else []
        )
        kwargs["meta_commands"] = (
            [
                MetaCommand._from_v1_1(mc)
                if isinstance(mc, xtce_1_1.MetaCommandType)
                else BlockMetaCommand._from_v1_1(mc)
                if isinstance(
                    mc, xtce_1_1.CommandMetaDataType.MetaCommandSet.BlockMetaCommand
                )
                else MetaCommandRef(name=XtcePath(mc))
                for mc in obj.meta_command_set.choice
            ]
            if getattr(obj, "meta_command_set", None) is not None
            else []
        )
        kwargs["containers"] = (
            [
                SequenceContainer._from_v1_1(sc)
                for sc in obj.command_container_set.command_container
            ]
            if obj.command_container_set is not None
            else []
        )
        kwargs["streams"] = (
            [
                CustomStream._from_v1_1(s)
                if isinstance(s, xtce_1_1.CustomStreamType)
                else FixedFrameStream._from_v1_1(s)
                if isinstance(s, xtce_1_1.FixedFrameStreamType)
                else VariableFrameStream._from_v1_1(s)
                for s in obj.stream_set.choice
            ]
            if obj.stream_set is not None
            else []
        )
        kwargs["algorithms"] = (
            [
                InputOutputTriggerAlgorithm._from_v1_1(a)
                if isinstance(a, xtce_1_1.InputOutputTriggerAlgorithmType)
                else MathAlgorithm._from_v1_1(a)
                for a in obj.algorithm_set.choice
            ]
            if obj.algorithm_set is not None
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.CommandMetaDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["parameter_types"] = (
            [
                IntegerParameter._from_v1_2(p)
                if isinstance(p, xtce_1_2.IntegerParameterType)
                else FloatParameter._from_v1_2(p)
                if isinstance(p, xtce_1_2.FloatParameterType)
                else StringParameter._from_v1_2(p)
                if isinstance(p, xtce_1_2.StringParameterType)
                else BinaryParameter._from_v1_2(p)
                if isinstance(p, xtce_1_2.BinaryParameterType)
                else BooleanParameter._from_v1_2(p)
                if isinstance(p, xtce_1_2.BooleanParameterType)
                else EnumeratedParameter._from_v1_2(p)
                if isinstance(p, xtce_1_2.EnumeratedParameterType)
                else ArrayParameter._from_v1_2(p)
                if isinstance(p, xtce_1_2.ArrayDataTypeType)
                else AggregateParameter._from_v1_2(p)
                if isinstance(p, xtce_1_2.AggregateDataType)
                else RelativeTimeParameter._from_v1_2(p)
                if isinstance(p, xtce_1_2.RelativeTimeParameterType)
                else AbsoluteTimeParameter._from_v1_2(p)
                for p in obj.parameter_type_set.choice
            ]
            if obj.parameter_type_set is not None
            else []
        )
        kwargs["parameters"] = (
            [
                Parameter._from_v1_2(p)
                if isinstance(p, xtce_1_2.ParameterType)
                else ParameterRef._from_v1_2(p)
                for p in obj.parameter_set.choice
            ]
            if obj.parameter_set is not None
            else []
        )
        kwargs["argument_types"] = (
            [
                IntegerArgument._from_v1_2(p)
                if isinstance(p, xtce_1_2.IntegerArgumentType)
                else FloatArgument._from_v1_2(p)
                if isinstance(p, xtce_1_2.FloatArgumentType)
                else StringArgument._from_v1_2(p)
                if isinstance(p, xtce_1_2.StringArgumentType)
                else BinaryArgument._from_v1_2(p)
                if isinstance(p, xtce_1_2.BinaryArgumentType)
                else BooleanArgument._from_v1_2(p)
                if isinstance(p, xtce_1_2.BooleanArgumentType)
                else EnumeratedArgument._from_v1_2(p)
                if isinstance(p, xtce_1_2.EnumeratedArgumentType)
                else ArrayArgument._from_v1_2(p)
                if isinstance(p, xtce_1_2.ArrayArgumentType)
                else AggregateArgument._from_v1_2(p)
                if isinstance(p, xtce_1_2.AggregateArgumentType)
                else RelativeTimeArgument._from_v1_2(p)
                if isinstance(p, xtce_1_2.RelativeTimeArgumentType)
                else AbsoluteTimeArgument._from_v1_2(p)
                for p in obj.argument_type_set.choice
            ]
            if obj.argument_type_set is not None
            else []
        )
        kwargs["meta_commands"] = (
            [
                MetaCommand._from_v1_2(mc)
                if isinstance(mc, xtce_1_2.MetaCommandType)
                else BlockMetaCommand._from_v1_2(mc)
                if isinstance(mc, xtce_1_2.BlockMetaCommandType)
                else MetaCommandRef(name=XtcePath(mc))
                for mc in obj.meta_command_set.choice
            ]
            if obj.meta_command_set is not None
            else []
        )
        kwargs["containers"] = (
            [
                SequenceContainer._from_v1_2(sc)
                for sc in obj.command_container_set.command_container
            ]
            if obj.command_container_set is not None
            else []
        )
        kwargs["streams"] = (
            [
                CustomStream._from_v1_2(s)
                if isinstance(s, xtce_1_2.CustomStreamType)
                else FixedFrameStream._from_v1_2(s)
                if isinstance(s, xtce_1_2.FixedFrameStreamType)
                else VariableFrameStream._from_v1_2(s)
                for s in obj.stream_set.choice
            ]
            if obj.stream_set is not None
            else []
        )
        kwargs["algorithms"] = (
            [
                InputOutputTriggerAlgorithm._from_v1_2(a)
                if isinstance(a, xtce_1_2.InputOutputTriggerAlgorithmType)
                else MathAlgorithm._from_v1_2(a)
                for a in obj.algorithm_set.choice
            ]
            if obj.algorithm_set is not None
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.CommandMetaDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["parameter_types"] = (
            [
                IntegerParameter._from_v1_3(p)
                if isinstance(p, xtce_1_3.IntegerParameterType)
                else FloatParameter._from_v1_3(p)
                if isinstance(p, xtce_1_3.FloatParameterType)
                else StringParameter._from_v1_3(p)
                if isinstance(p, xtce_1_3.StringParameterType)
                else BinaryParameter._from_v1_3(p)
                if isinstance(p, xtce_1_3.BinaryParameterType)
                else BooleanParameter._from_v1_3(p)
                if isinstance(p, xtce_1_3.BooleanParameterType)
                else EnumeratedParameter._from_v1_3(p)
                if isinstance(p, xtce_1_3.EnumeratedParameterType)
                else ArrayParameter._from_v1_3(p)
                if isinstance(p, xtce_1_3.ArrayDataTypeType)
                else AggregateParameter._from_v1_3(p)
                if isinstance(p, xtce_1_3.AggregateDataType)
                else RelativeTimeParameter._from_v1_3(p)
                if isinstance(p, xtce_1_3.RelativeTimeParameterType)
                else AbsoluteTimeParameter._from_v1_3(p)
                for p in obj.parameter_type_set.choice
            ]
            if obj.parameter_type_set is not None
            else []
        )
        kwargs["parameters"] = (
            [
                Parameter._from_v1_3(p)
                if isinstance(p, xtce_1_3.ParameterType)
                else ParameterRef._from_v1_3(p)
                for p in obj.parameter_set.choice
            ]
            if obj.parameter_set is not None
            else []
        )
        kwargs["argument_types"] = (
            [
                IntegerArgument._from_v1_3(p)
                if isinstance(p, xtce_1_3.IntegerArgumentType)
                else FloatArgument._from_v1_3(p)
                if isinstance(p, xtce_1_3.FloatArgumentType)
                else StringArgument._from_v1_3(p)
                if isinstance(p, xtce_1_3.StringArgumentType)
                else BinaryArgument._from_v1_3(p)
                if isinstance(p, xtce_1_3.BinaryArgumentType)
                else BooleanArgument._from_v1_3(p)
                if isinstance(p, xtce_1_3.BooleanArgumentType)
                else EnumeratedArgument._from_v1_3(p)
                if isinstance(p, xtce_1_3.EnumeratedArgumentType)
                else ArrayArgument._from_v1_3(p)
                if isinstance(p, xtce_1_3.ArrayArgumentType)
                else AggregateArgument._from_v1_3(p)
                if isinstance(p, xtce_1_3.AggregateArgumentType)
                else RelativeTimeArgument._from_v1_3(p)
                if isinstance(p, xtce_1_3.RelativeTimeArgumentType)
                else AbsoluteTimeArgument._from_v1_3(p)
                for p in obj.argument_type_set.choice
            ]
            if obj.argument_type_set is not None
            else []
        )
        kwargs["meta_commands"] = (
            [
                MetaCommand._from_v1_3(mc)
                if isinstance(mc, xtce_1_3.MetaCommandType)
                else BlockMetaCommand._from_v1_3(mc)
                if isinstance(mc, xtce_1_3.BlockMetaCommandType)
                else MetaCommandRef(name=XtcePath(mc))
                for mc in obj.meta_command_set.choice
            ]
            if obj.meta_command_set is not None
            else []
        )
        kwargs["containers"] = (
            [
                SequenceContainer._from_v1_3(sc)
                for sc in obj.command_container_set.command_container
            ]
            if obj.command_container_set is not None
            else []
        )
        kwargs["streams"] = (
            [
                CustomStream._from_v1_3(s)
                if isinstance(s, xtce_1_3.CustomStreamType)
                else FixedFrameStream._from_v1_3(s)
                if isinstance(s, xtce_1_3.FixedFrameStreamType)
                else VariableFrameStream._from_v1_3(s)
                for s in obj.stream_set.choice
            ]
            if obj.stream_set is not None
            else []
        )
        kwargs["algorithms"] = (
            [
                InputOutputTriggerAlgorithm._from_v1_3(a)
                if isinstance(a, xtce_1_3.InputOutputTriggerAlgorithmType)
                else MathAlgorithm._from_v1_3(a)
                for a in obj.algorithm_set.choice
            ]
            if obj.algorithm_set is not None
            else []
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["parameter_type_set"] = (
            xtce_1_1.ParameterTypeSetType(
                choice=[p._to_v1_1(policy) for p in self.parameter_types]
            )
            if self.parameter_types
            else None
        )
        kwargs["parameter_set"] = (
            xtce_1_1.ParameterSetType(
                choice=[p._to_v1_1(policy) for p in self.parameters]
            )
            if self.parameters
            else None
        )
        kwargs["argument_type_set"] = (
            xtce_1_1.ArgumentTypeSetType(
                choice=[a._to_v1_1(policy) for a in self.argument_types]
            )
            if self.argument_types
            else None
        )
        kwargs["meta_command_set"] = (
            xtce_1_1.CommandMetaDataType.MetaCommandSet(
                choice=[
                    str(mc.name) if isinstance(mc, MetaCommandRef) else mc._to_v1_1(policy)
                    for mc in self.meta_commands
                ]
            )
        )
        kwargs["command_container_set"] = (
            xtce_1_1.CommandContainerSetType(
                command_container=[c._to_v1_1(policy) for c in self.containers]
            )
            if self.containers
            else None
        )
        kwargs["stream_set"] = (
            xtce_1_1.StreamSetType(
                choice=[s._to_v1_1(policy) for s in self.streams]
            )
            if self.streams
            else None
        )
        kwargs["algorithm_set"] = (
            xtce_1_1.AlgorithmSetType(
                choice=[a._to_v1_1(policy) for a in self.algorithms]
            )
            if self.algorithms
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["parameter_type_set"] = (
            xtce_1_2.ParameterTypeSetType(
                choice=[p._to_v1_2(policy) for p in self.parameter_types]
            )
            if self.parameter_types
            else None
        )
        kwargs["parameter_set"] = (
            xtce_1_2.ParameterSetType(
                choice=[p._to_v1_2(policy) for p in self.parameters]
            )
            if self.parameters
            else None
        )
        kwargs["argument_type_set"] = (
            xtce_1_2.ArgumentTypeSetType(
                choice=[a._to_v1_2(policy) for a in self.argument_types]
            )
            if self.argument_types
            else None
        )
        kwargs["meta_command_set"] = (
            xtce_1_2.MetaCommandSetType(
                choice=[
                    str(mc.name) if isinstance(mc, MetaCommandRef) else mc._to_v1_2(policy)
                    for mc in self.meta_commands
                ]
            )
            if self.meta_commands
            else None
        )
        kwargs["command_container_set"] = (
            xtce_1_2.CommandContainerSetType(
                command_container=[c._to_v1_2(policy) for c in self.containers]
            )
            if self.containers
            else None
        )
        kwargs["stream_set"] = (
            xtce_1_2.StreamSetType(
                choice=[s._to_v1_2(policy) for s in self.streams]
            )
            if self.streams
            else None
        )
        kwargs["algorithm_set"] = (
            xtce_1_2.AlgorithmSetType(
                choice=[a._to_v1_2(policy) for a in self.algorithms]
            )
            if self.algorithms
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["parameter_type_set"] = (
            xtce_1_3.ParameterTypeSetType(
                choice=[p._to_v1_3(policy) for p in self.parameter_types]
            )
            if self.parameter_types
            else None
        )
        kwargs["parameter_set"] = (
            xtce_1_3.ParameterSetType(
                choice=[p._to_v1_3(policy) for p in self.parameters]
            )
            if self.parameters
            else None
        )
        kwargs["argument_type_set"] = (
            xtce_1_3.ArgumentTypeSetType(
                choice=[a._to_v1_3(policy) for a in self.argument_types]
            )
            if self.argument_types
            else None
        )
        kwargs["meta_command_set"] = (
            xtce_1_3.MetaCommandSetType(
                choice=[
                    str(mc.name) if isinstance(mc, MetaCommandRef) else mc._to_v1_3(policy)
                    for mc in self.meta_commands
                ]
            )
            if self.meta_commands
            else None
        )
        kwargs["command_container_set"] = (
            xtce_1_3.CommandContainerSetType(
                command_container=[c._to_v1_3(policy) for c in self.containers]
            )
            if self.containers
            else None
        )
        kwargs["stream_set"] = (
            xtce_1_3.StreamSetType(
                choice=[s._to_v1_3(policy) for s in self.streams]
            )
            if self.streams
            else None
        )
        kwargs["algorithm_set"] = (
            xtce_1_3.AlgorithmSetType(
                choice=[a._to_v1_3(policy) for a in self.algorithms]
            )
            if self.algorithms
            else None
        )
        return kwargs
