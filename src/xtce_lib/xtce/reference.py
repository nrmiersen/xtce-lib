"""Reference models."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Any

from pydantic import AfterValidator, Field

from xtce_lib.common.validation import ValidationReport, XtceSemanticError
from xtce_lib.common.xtce_path import XtcePath, require_regex
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from ._pattern import EXPD_NAME_REF_NO_PATH, EXPD_NAME_REF_W_PATH, NAME_REF_W_PATH

if TYPE_CHECKING:
    from xtce_lib.common.xtce_registry import XtceRegistry


class ParameterRef(XtceBaseModel):
    """A reference to a parameter."""

    ref: Annotated[XtcePath, AfterValidator(require_regex(EXPD_NAME_REF_W_PATH))] = (
        Field(
            ...,
            examples=[
                "/ConkSat/Bus/BatteryVoltage",
                "../Bus/BatteryVoltage",
                "../Payload/Camera/ExposureTime",
            ],
            json_schema_extra={"pattern": EXPD_NAME_REF_W_PATH},
        )
    )
    """A Unix-like path to a parameter.

    Standalone ParameterRefs can only reference parameters, and are not allowed to
    reference array elements or aggregate members.

    """

    def validate_semantics(
        self,
        report: ValidationReport[XtceSemanticError],
        registry: XtceRegistry,
        scope: XtcePath,
    ) -> None:
        """Validate this object's semantics.

        Rules:
            - The reference must not contain an array index or aggregate member.
            - The reference must exist.
            - The reference must be an instance of Parameter.

        """
        if self.ref.contains_array or self.ref.contains_aggregate:
            report.add_error(
                XtceSemanticError(
                    scope=scope,
                    message=f"reference '{self.ref}' contains an array index or "
                    "aggregate member, but a standalone ParameterRef must reference a "
                    "parameter only",
                )
            )

        from .parameter import Parameter

        try:
            result = registry.resolve(self.ref, scope)
            if not isinstance(result.target, Parameter):
                report.add_error(
                    XtceSemanticError(
                        scope=scope,
                        message=f"reference '{self.ref}' resolved to a "
                        f"'{type(result.target).__name__}' type, "
                        f"but a 'Parameter' type was expected",
                    )
                )

        except KeyError:
            report.add_error(
                XtceSemanticError(
                    scope=scope,
                    message=f"reference '{self.ref}' does not resolve to a valid object "
                    f"from scope '{scope}'",
                )
            )

    _v1_1_type = xtce_1_1.ParameterRefType
    _v1_2_type = xtce_1_2.ParameterRefType
    _v1_3_type = xtce_1_3.ParameterRefType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.ParameterRefType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.parameter_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ParameterRefType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.parameter_ref)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ParameterRefType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.parameter_ref)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["parameter_ref"] = str(self.ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["parameter_ref"] = str(self.ref)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["parameter_ref"] = str(self.ref)
        return kwargs


class OutputParameterRef(ParameterRef):
    """A reference to a parameter that is the output of an algorithm."""

    output_name: str | None = Field(default=None)
    """An optional 'friendly' name for the output parameter."""

    def validate_semantics(
        self,
        report: ValidationReport[XtceSemanticError],
        registry: XtceRegistry,
        scope: XtcePath,
    ) -> None:
        """Validate this object's semantics.

        Rules:
            - The reference must not contain an array index or aggregate member.
            - The reference must exist.
            - The reference must be an instance of Parameter.

        """
        # TODO make sure this isn't supposed to be an array or aggregate
        if self.ref.contains_array or self.ref.contains_aggregate:
            report.add_error(
                XtceSemanticError(
                    scope=scope,
                    message=f"reference '{self.ref}' contains an array index or "
                    "aggregate member, but an OutputParameterRef must reference a "
                    "parameter only",
                )
            )

        from .parameter import Parameter

        try:
            result = registry.resolve(self.ref, scope)
            if not isinstance(result.target, Parameter):
                report.add_error(
                    XtceSemanticError(
                        scope=scope,
                        message=f"reference '{self.ref}' resolved to a "
                        f"'{type(result.target).__name__}' type, "
                        f"but a 'Parameter' type was expected",
                    )
                )

        except KeyError:
            report.add_error(
                XtceSemanticError(
                    scope=scope,
                    message=f"reference '{self.ref}' does not resolve to a valid object "
                    f"from scope '{scope}'",
                )
            )

    _v1_1_type = xtce_1_1.InputOutputAlgorithmType.OutputSet.OutputParameterRef
    _v1_2_type = xtce_1_2.OutputParameterRefType
    _v1_3_type = xtce_1_3.OutputParameterRefType

    @classmethod
    def _from_v1_1_kwargs(
        cls,
        obj: xtce_1_1.InputOutputAlgorithmType.OutputSet.OutputParameterRef,
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["output_name"] = obj.output_name
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.OutputParameterRefType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["output_name"] = obj.output_name
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.OutputParameterRefType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["output_name"] = obj.output_name
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["output_name"] = self.output_name
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["output_name"] = self.output_name
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["output_name"] = self.output_name
        return kwargs


class ParameterInstanceRef(ParameterRef):
    """A reference to an instance of a parameter.

    Used when the value of a parameter is required for a calculation or as an index
    value.

    """

    instance: int = Field(default=0, examples=[-1, 0, 1])
    """The instance of the parameter to reference.

    A positive value is forward in time, a negative value is backward in time, and zero
    is the current instance.

    """

    use_calibrated_value: bool = Field(default=True)
    """Whether to use the calibrated value of the parameter instance.

    If False, the raw/uncalibrated value of the parameter instance will be used.

    """

    def validate_semantics(
        self,
        report: ValidationReport[XtceSemanticError],
        registry: XtceRegistry,
        scope: XtcePath,
    ) -> None:
        """Validate this object's semantics.

        Rules:
            - The reference must exist.
            - The reference must be an instance of Parameter.

        """
        # TODO need parameter type classes to be defined before semantic validation can be implemented

    _v1_1_type = xtce_1_1.ParameterInstanceRefType
    _v1_2_type = xtce_1_2.ParameterInstanceRefType
    _v1_3_type = xtce_1_3.ParameterInstanceRefType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.ParameterInstanceRefType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["instance"] = obj.instance
        kwargs["use_calibrated_value"] = obj.use_calibrated_value
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ParameterInstanceRefType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["instance"] = obj.instance
        kwargs["use_calibrated_value"] = obj.use_calibrated_value
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ParameterInstanceRefType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["instance"] = obj.instance
        kwargs["use_calibrated_value"] = obj.use_calibrated_value
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["instance"] = self.instance
        kwargs["use_calibrated_value"] = self.use_calibrated_value
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["instance"] = self.instance
        kwargs["use_calibrated_value"] = self.use_calibrated_value
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["instance"] = self.instance
        kwargs["use_calibrated_value"] = self.use_calibrated_value
        return kwargs


class ArgumentInstanceRef(XtceBaseModel):
    """A reference to an instance of an argument.

    Always resolves locally to the metacommand.

    """

    ref: str = Field(..., pattern=EXPD_NAME_REF_NO_PATH)
    """The name of the argument to reference."""

    use_calibrated_value: bool = Field(default=True)
    """Whether to use the calibrated value of the argument instance.

    If False, the raw/uncalibrated value of the argument instance will be used.

    """

    def validate_semantics(self, registry: XtceRegistry, scope: XtcePath) -> None:
        """Validate this object's semantics.

        Rules:
            - The reference must exist in the metacommand's argument list.

        """
        # TODO maybe need to pass in metacommand or argument list
        # TODO need argument type classes to be defined before semantic validation can be implemented

    _v1_1_type = None
    _v1_2_type = xtce_1_2.ArgumentInstanceRefType
    _v1_3_type = xtce_1_3.ArgumentInstanceRefType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ArgumentInstanceRefType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["ref"] = obj.argument_ref
        kwargs["use_calibrated_value"] = obj.use_calibrated_value
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ArgumentInstanceRefType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["ref"] = obj.argument_ref
        kwargs["use_calibrated_value"] = obj.use_calibrated_value
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["argument_ref"] = str(self.ref)
        kwargs["use_calibrated_value"] = self.use_calibrated_value
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["argument_ref"] = str(self.ref)
        kwargs["use_calibrated_value"] = self.use_calibrated_value
        return kwargs


class InputParameterInstanceRef(ParameterInstanceRef):
    """A reference to an instance of a parameter.

    Used when the value of a parameter is required for a calculation or as an index
    value, where an optional input name is provided.

    """

    input_name: str | None = Field(default=None)
    """An optional 'friendly' name for the input parameter."""

    def validate_semantics(self, registry: XtceRegistry, scope: XtcePath) -> None:
        """Validate this object's semantics.

        Rules:
            - The reference must not contain an array index or aggregate member.
            - The reference must exist.
            - The reference must be an instance of Parameter.

        """
        # TODO need parameter type classes to be defined before semantic validation can be implemented

    _v1_1_type = xtce_1_1.InputAlgorithmType.InputSet.ParameterInstanceRef
    _v1_2_type = xtce_1_2.InputParameterInstanceRefType
    _v1_3_type = xtce_1_3.InputParameterInstanceRefType

    @classmethod
    def _from_v1_1_kwargs(
        cls,
        obj: xtce_1_1.InputAlgorithmType.InputSet.ParameterInstanceRef,
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["input_name"] = obj.input_name
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.InputParameterInstanceRefType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["input_name"] = obj.input_name
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.InputParameterInstanceRefType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["input_name"] = obj.input_name
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["input_name"] = self.input_name
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["input_name"] = self.input_name
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["input_name"] = self.input_name
        return kwargs


class ContainerRef(XtceBaseModel):
    """A reference to a container."""

    ref: Annotated[XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))] = Field(
        ...,
        examples=[
            "/Telemetry/Power/PowerStatus",
            "../Thermal/ThermalStatus",
            "Command/ExecutionReport",
        ],
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to a sequence container."""

    def validate_semantics(
        self,
        report: ValidationReport[XtceSemanticError],
        registry: XtceRegistry,
        scope: XtcePath,
    ) -> None:
        """Validate this object's semantics.

        Rules:
            - The reference must not contain an array index or aggregate member.
            - The reference must exist.
            - The reference must be an instance of SequenceContainer.

        """
        if self.ref.contains_array or self.ref.contains_aggregate:
            report.add_error(
                XtceSemanticError(
                    scope=scope,
                    message=f"reference '{self.ref}' contains an array index or "
                    "aggregate member, but a ContainerRef must reference a sequence "
                    "container only",
                )
            )

        from .container import SequenceContainer

        try:
            result = registry.resolve(self.ref, scope)
            if not isinstance(result.target, SequenceContainer):
                report.add_error(
                    XtceSemanticError(
                        scope=scope,
                        message=f"reference '{self.ref}' resolved to a "
                        f"'{type(result.target).__name__}' type, "
                        f"but a 'SequenceContainer' type was expected",
                    )
                )

        except KeyError:
            report.add_error(
                XtceSemanticError(
                    scope=scope,
                    message=f"reference '{self.ref}' does not resolve to a valid "
                    f"object from scope '{scope}'",
                )
            )

    _v1_1_type = xtce_1_1.ContainerRefType
    _v1_2_type = xtce_1_2.ContainerRefType
    _v1_3_type = xtce_1_3.ContainerRefType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.ContainerRefType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.container_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ContainerRefType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.container_ref)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ContainerRefType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.container_ref)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["container_ref"] = str(self.ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["container_ref"] = str(self.ref)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["container_ref"] = str(self.ref)
        return kwargs


class ServiceRef(XtceBaseModel):
    """A reference to a service."""

    ref: Annotated[XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))] = Field(
        ...,
        examples=[
            "/ConkSat/PowerService",
            "../ThermalService",
            "CommandService",
        ],
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to a service."""

    def validate_semantics(
        self,
        report: ValidationReport[XtceSemanticError],
        registry: XtceRegistry,
        scope: XtcePath,
    ) -> None:
        """Validate this object's semantics.

        Rules:
            - The reference must not contain an array index or aggregate member.
            - The reference must exist.
            - The reference must be an instance of Service.

        """
        if self.ref.contains_array or self.ref.contains_aggregate:
            raise ValueError(
                f"reference '{self.ref}' contains an array index or aggregate member, "
                f"but a ServiceRef must reference a service only"
            )

        from .space_system import Service

        try:
            result = registry.resolve(self.ref, scope)
            if not isinstance(result.target, Service):
                report.add_error(
                    XtceSemanticError(
                        scope=scope,
                        message=f"reference '{self.ref}' resolved to a "
                        f"'{type(result.target).__name__}' type, "
                        f"but a 'Service' type was expected",
                    )
                )

        except KeyError:
            report.add_error(
                XtceSemanticError(
                    scope=scope,
                    message=f"reference '{self.ref}' does not resolve to a valid "
                    f"object from scope '{scope}'",
                )
            )

    _v1_1_type = xtce_1_1.ServiceRefType
    _v1_2_type = xtce_1_2.ServiceRefType
    _v1_3_type = xtce_1_3.ServiceRefType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.ServiceRefType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.service_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ServiceRefType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.service_ref)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ServiceRefType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.service_ref)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["service_ref"] = str(self.ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["service_ref"] = str(self.ref)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["service_ref"] = str(self.ref)
        return kwargs


class StreamRef(XtceBaseModel):
    """A reference to a stream."""

    ref: Annotated[XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))] = Field(
        ...,
        examples=[
            "/ConkSat/PowerStream",
            "../ThermalStream",
            "CommandStream",
        ],
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to a stream."""

    def validate_semantics(
        self,
        report: ValidationReport[XtceSemanticError],
        registry: XtceRegistry,
        scope: XtcePath,
    ) -> None:
        """Validate this object's semantics.

        Rules:
            - The reference must not contain an array index or aggregate member.
            - The reference must exist.
            - The reference must be an instance of CustomStream, FixedFrameStream or
                VariableFrameStream.

        """
        if self.ref.contains_array or self.ref.contains_aggregate:
            raise ValueError(
                f"reference '{self.ref}' contains an array index or aggregate member, "
                f"but a StreamRef must reference a stream only"
            )

        from .stream import CustomStream, FixedFrameStream, VariableFrameStream

        try:
            result = registry.resolve(self.ref, scope)
            if not isinstance(
                result.target, (CustomStream, FixedFrameStream, VariableFrameStream)
            ):
                report.add_error(
                    XtceSemanticError(
                        scope=scope,
                        message=f"reference '{self.ref}' resolved to a "
                        f"'{type(result.target).__name__}' type, "
                        f"but a 'CustomStream', 'FixedFrameStream' or "
                        f"'VariableFrameStream' type was expected",
                    )
                )

        except KeyError:
            report.add_error(
                XtceSemanticError(
                    scope=scope,
                    message=f"reference '{self.ref}' does not resolve to a valid "
                    f"object from scope '{scope}'",
                )
            )

    _v1_1_type = xtce_1_1.StreamRefType
    _v1_2_type = xtce_1_2.StreamRefType
    _v1_3_type = xtce_1_3.StreamRefType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.StreamRefType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.stream_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.StreamRefType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.stream_ref)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.StreamRefType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.stream_ref)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["stream_ref"] = str(self.ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["stream_ref"] = str(self.ref)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["stream_ref"] = str(self.ref)
        return kwargs
