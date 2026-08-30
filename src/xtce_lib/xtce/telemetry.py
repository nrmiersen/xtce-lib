"""Telemetry models."""

from typing import Any

from pydantic import Field

from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from .algorithm import InputOutputTriggerAlgorithm, MathAlgorithm
from .common import NameDescriptionBase, OptionalNameDescriptionBase
from .condition import MatchCriteria
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
from .reference import ContainerRef, ParameterRef
from .stream import CustomStream, FixedFrameStream, VariableFrameStream


class Message(NameDescriptionBase):
    """Define a telemetry message used to identify a container within a service."""

    match_criteria: MatchCriteria
    """Criteria to match the message within the service."""

    container_ref: ContainerRef
    """Reference to the container associated with the message."""

    _v1_1_type = xtce_1_1.TelemetryMetaDataType.MessageSet.Message
    _v1_2_type = xtce_1_2.MessageType
    _v1_3_type = xtce_1_3.MessageType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.TelemetryMetaDataType.MessageSet.Message
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["match_criteria"] = MatchCriteria._from_v1_1(obj.match_criteria)
        kwargs["container_ref"] = ContainerRef._from_v1_1(obj.contain_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.MessageType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["match_criteria"] = MatchCriteria._from_v1_2(obj.match_criteria)
        kwargs["container_ref"] = ContainerRef._from_v1_2(obj.container_ref)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.MessageType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["match_criteria"] = MatchCriteria._from_v1_3(obj.match_criteria)
        kwargs["container_ref"] = ContainerRef._from_v1_3(obj.container_ref)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["match_criteria"] = self.match_criteria._to_v1_1(policy)
        kwargs["contain_ref"] = self.container_ref._to_v1_1(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["match_criteria"] = self.match_criteria._to_v1_2(policy)
        kwargs["container_ref"] = self.container_ref._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["match_criteria"] = self.match_criteria._to_v1_3(policy)
        kwargs["container_ref"] = self.container_ref._to_v1_3(policy)
        return kwargs


class MessageSet(OptionalNameDescriptionBase):
    """Define a set of telemetry messages."""

    messages: list[Message] = Field(default_factory=list)
    """A list of telemetry messages."""

    _v1_1_type = xtce_1_1.TelemetryMetaDataType.MessageSet
    _v1_2_type = xtce_1_2.MessageSetType
    _v1_3_type = xtce_1_3.MessageSetType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.TelemetryMetaDataType.MessageSet
    ) -> dict[str, Any]:
        # MessageSet in XTCE 1.1 does not inherit from a base class
        kwargs: dict[str, Any] = {}
        kwargs["name"] = obj.name
        kwargs["messages"] = [Message._from_v1_1(m) for m in obj.message]
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.MessageSetType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["messages"] = [Message._from_v1_2(m) for m in obj.message]
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.MessageSetType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["messages"] = [Message._from_v1_3(m) for m in obj.message]
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="short_description",
            current_value=self.short_description,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=None,
        )
        self._enforce_unsupported_field(
            field_name="long_description",
            current_value=self.long_description,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=None,
        )
        self._enforce_unsupported_field(
            field_name="aliases",
            current_value=self.aliases,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=[],
        )
        self._enforce_unsupported_field(
            field_name="ancillary_data",
            current_value=self.ancillary_data,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=[],
        )

        kwargs: dict[str, Any] = {}
        kwargs["name"] = self.name
        kwargs["message"] = [m._to_v1_1(policy) for m in self.messages]
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["message"] = [m._to_v1_2(policy) for m in self.messages]
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["message"] = [m._to_v1_3(policy) for m in self.messages]
        return kwargs


class TelemetryMetadata(XtceBaseModel):
    """Telemetry related metadata."""

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
    """A list of parameters."""

    containers: list[SequenceContainer] = Field(default_factory=list)
    """A list of sequence containers."""

    message_set: MessageSet | None = None
    """The message set."""

    streams: list[CustomStream | FixedFrameStream | VariableFrameStream] = Field(
        default_factory=list,
    )
    """A list of streams."""

    algorithms: list[InputOutputTriggerAlgorithm | MathAlgorithm] = Field(
        default_factory=list,
    )
    """A list of algorithms."""

    _v1_1_type = xtce_1_1.TelemetryMetaDataType
    _v1_2_type = xtce_1_2.TelemetryMetaDataType
    _v1_3_type = xtce_1_3.TelemetryMetaDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.TelemetryMetaDataType) -> dict[str, Any]:
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
        kwargs["containers"] = (
            [
                SequenceContainer._from_v1_1(sc)
                for sc in obj.container_set.sequence_container
            ]
            if obj.container_set is not None
            else []
        )
        kwargs["message_set"] = (
            MessageSet._from_v1_1(obj.message_set)
            if obj.message_set is not None
            else None
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
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.TelemetryMetaDataType) -> dict[str, Any]:
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
        kwargs["containers"] = (
            [
                SequenceContainer._from_v1_2(sc)
                for sc in obj.container_set.sequence_container
            ]
            if obj.container_set is not None
            else []
        )
        kwargs["message_set"] = (
            MessageSet._from_v1_2(obj.message_set)
            if obj.message_set is not None
            else None
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
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.TelemetryMetaDataType) -> dict[str, Any]:
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
        kwargs["containers"] = (
            [
                SequenceContainer._from_v1_3(sc)
                for sc in obj.container_set.sequence_container
            ]
            if obj.container_set is not None
            else []
        )
        kwargs["message_set"] = (
            MessageSet._from_v1_3(obj.message_set)
            if obj.message_set is not None
            else None
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
        kwargs["parameter_type_set"] = self._build_set(
            items=self.parameter_types,
            set_class=xtce_1_1.ParameterTypeSetType,
            kwarg_name="choice",
            converter=lambda p: p._to_v1_1(policy),
        )
        kwargs["parameter_set"] = self._build_set(
            items=self.parameters,
            set_class=xtce_1_1.ParameterSetType,
            kwarg_name="choice",
            converter=lambda p: p._to_v1_1(policy),
        )
        kwargs["container_set"] = self._build_set(
            items=self.containers,
            set_class=xtce_1_1.ContainerSetType,
            kwarg_name="sequence_container",
            converter=lambda c: c._to_v1_1(policy),
        )
        kwargs["message_set"] = (
            self.message_set._to_v1_1(policy) if self.message_set else None
        )
        kwargs["stream_set"] = self._build_set(
            items=self.streams,
            set_class=xtce_1_1.StreamSetType,
            kwarg_name="stream",
            converter=lambda s: s._to_v1_1(policy),
        )
        kwargs["algorithm_set"] = self._build_set(
            items=self.algorithms,
            set_class=xtce_1_1.AlgorithmSetType,
            kwarg_name="algorithm",
            converter=lambda a: a._to_v1_1(policy),
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["parameter_type_set"] = self._build_set(
            items=self.parameter_types,
            set_class=xtce_1_2.ParameterTypeSetType,
            kwarg_name="choice",
            converter=lambda p: p._to_v1_2(policy),
        )
        kwargs["parameter_set"] = self._build_set(
            items=self.parameters,
            set_class=xtce_1_2.ParameterSetType,
            kwarg_name="choice",
            converter=lambda p: p._to_v1_2(policy),
        )
        kwargs["container_set"] = self._build_set(
            items=self.containers,
            set_class=xtce_1_2.ContainerSetType,
            kwarg_name="sequence_container",
            converter=lambda c: c._to_v1_2(policy),
        )
        kwargs["message_set"] = (
            self.message_set._to_v1_2(policy) if self.message_set else None
        )
        kwargs["stream_set"] = self._build_set(
            items=self.streams,
            set_class=xtce_1_2.StreamSetType,
            kwarg_name="stream",
            converter=lambda s: s._to_v1_2(policy),
        )
        kwargs["algorithm_set"] = self._build_set(
            items=self.algorithms,
            set_class=xtce_1_2.AlgorithmSetType,
            kwarg_name="algorithm",
            converter=lambda a: a._to_v1_2(policy),
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["parameter_type_set"] = self._build_set(
            items=self.parameter_types,
            set_class=xtce_1_3.ParameterTypeSetType,
            kwarg_name="choice",
            converter=lambda p: p._to_v1_3(policy),
        )
        kwargs["parameter_set"] = self._build_set(
            items=self.parameters,
            set_class=xtce_1_3.ParameterSetType,
            kwarg_name="choice",
            converter=lambda p: p._to_v1_3(policy),
        )
        kwargs["container_set"] = self._build_set(
            items=self.containers,
            set_class=xtce_1_3.ContainerSetType,
            kwarg_name="sequence_container",
            converter=lambda c: c._to_v1_3(policy),
        )
        kwargs["message_set"] = (
            self.message_set._to_v1_3(policy) if self.message_set else None
        )
        kwargs["stream_set"] = self._build_set(
            items=self.streams,
            set_class=xtce_1_3.StreamSetType,
            kwarg_name="stream",
            converter=lambda s: s._to_v1_3(policy),
        )
        kwargs["algorithm_set"] = self._build_set(
            items=self.algorithms,
            set_class=xtce_1_3.AlgorithmSetType,
            kwarg_name="algorithm",
            converter=lambda a: a._to_v1_3(policy),
        )
        return kwargs
