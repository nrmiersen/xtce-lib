"""Reference models."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Any, Self, assert_never

from pydantic import AfterValidator, Field

from xtce_lib.common.xtce_path import XtcePath, require_regex
from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy, XtceUnsupportedError
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
                "/SimpleSat/Bus/BatteryVoltage",
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

    def validate_semantics(self, registry: XtceRegistry, scope: XtcePath) -> None:
        """Validate this object's semantics.

        Rules:
            - The reference must not contain an array index or aggregate member.
            - The reference must exist.
            - The reference must be an instance of Parameter.

        """
        if self.ref.contains_array or self.ref.contains_aggregate:
            raise ValueError(
                f"reference '{self.ref}' contains an array index or aggregate member, "
                f"but a standalone ParameterRef must reference a parameter only."
            )

        from .parameter import Parameter

        try:
            result = registry.resolve(self.ref, scope)
            if not isinstance(result.target, Parameter):
                raise ValueError(
                    f"reference '{self.ref}' resolved to a "
                    f"'{type(result.target).__name__}' type, "
                    f"but a 'Parameter' type was expected."
                )

        except KeyError:
            raise ValueError(
                f"reference '{self.ref}' does not resolve to a valid object "
                f"from scope '{scope}'"
            )

    @classmethod
    def _from_v1_1(cls: type[Self], parameter_ref: xtce_1_1.ParameterRefType) -> Self:
        return cls(ref=XtcePath(parameter_ref.parameter_ref))

    @classmethod
    def _from_v1_2(cls: type[Self], parameter_ref: xtce_1_2.ParameterRefType) -> Self:
        return cls(ref=XtcePath(parameter_ref.parameter_ref))

    @classmethod
    def _from_v1_3(cls: type[Self], parameter_ref: xtce_1_3.ParameterRefType) -> Self:
        return cls(ref=XtcePath(parameter_ref.parameter_ref))

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create a ParameterRef from an xsdata-generated
        ParameterRefType object of any version.
        """
        match version:
            case XtceVersion.V1_1:
                return cls._from_v1_1(raw_obj)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.ParameterRefType:
        return xtce_1_1.ParameterRefType(parameter_ref=str(self.ref))

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ParameterRefType:
        return xtce_1_2.ParameterRefType(parameter_ref=str(self.ref))

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ParameterRefType:
        return xtce_1_3.ParameterRefType(parameter_ref=str(self.ref))

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> (
        xtce_1_1.ParameterRefType
        | xtce_1_2.ParameterRefType
        | xtce_1_3.ParameterRefType
    ):
        """Convert this ParameterRef to an xsdata-generated ParameterRefType object of
        the specified version.
        """
        match version:
            case XtceVersion.V1_1:
                return self._to_v1_1(policy)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)


class OutputParameterRef(ParameterRef):
    """A reference to a parameter that is the output of an algorithm."""

    output_name: str | None = Field(default=None)
    """An optional 'friendly' name for the output parameter."""

    def validate_semantics(self, registry: XtceRegistry, scope: XtcePath) -> None:
        """Validate this object's semantics.

        Rules:
            - The reference must not contain an array index or aggregate member.
            - The reference must exist.
            - The reference must be an instance of Parameter.

        """
        # TODO make sure this isn't supposed to be an array or aggregate
        if self.ref.contains_array or self.ref.contains_aggregate:
            raise ValueError(
                f"reference '{self.ref}' contains an array index or aggregate member, "
                f"but an OutputParameterRef must reference a parameter only."
            )

        from .parameter import Parameter

        try:
            result = registry.resolve(self.ref, scope)
            if not isinstance(result.target, Parameter):
                raise ValueError(
                    f"reference '{self.ref}' resolved to a "
                    f"'{type(result.target).__name__}' type, "
                    f"but a 'Parameter' type was expected."
                )

        except KeyError:
            raise ValueError(
                f"reference '{self.ref}' does not resolve to a valid object "
                f"from scope '{scope}'"
            )

    @classmethod
    def _from_v1_2(
        cls: type[Self], parameter_ref: xtce_1_2.OutputParameterRefType
    ) -> Self:
        return cls(
            ref=XtcePath(parameter_ref.parameter_ref),
            output_name=parameter_ref.output_name,
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], parameter_ref: xtce_1_3.OutputParameterRefType
    ) -> Self:
        return cls(
            ref=XtcePath(parameter_ref.parameter_ref),
            output_name=parameter_ref.output_name,
        )

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create an OutputParameterRef from an xsdata-generated
        OutputParameterRefType object of any version.
        """
        match version:
            case XtceVersion.V1_1:
                raise XtceUnsupportedError(version, cls.__name__)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.OutputParameterRefType:
        return xtce_1_2.OutputParameterRefType(
            parameter_ref=str(self.ref),
            output_name=self.output_name,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.OutputParameterRefType:
        return xtce_1_3.OutputParameterRefType(
            parameter_ref=str(self.ref),
            output_name=self.output_name,
        )

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.OutputParameterRefType | xtce_1_3.OutputParameterRefType:
        """Convert this OutputParameterRef to an xsdata-generated OutputParameterRefType
        object of the specified version.
        """
        match version:
            case XtceVersion.V1_1:
                raise XtceUnsupportedError(version, self.__class__.__name__)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)


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

    def validate_semantics(self, registry: XtceRegistry, scope: XtcePath) -> None:
        """Validate this object's semantics.

        Rules:
            - The reference must exist.
            - The reference must be an instance of Parameter.

        """

        # TODO need parameter type classes to be defined before semantic validation can be implemented

    @classmethod
    def _from_v1_1(
        cls: type[Self], parameter_ref: xtce_1_1.ParameterInstanceRefType
    ) -> Self:
        return cls(
            ref=XtcePath(parameter_ref.parameter_ref),
            instance=parameter_ref.instance,
            use_calibrated_value=parameter_ref.use_calibrated_value,
        )

    @classmethod
    def _from_v1_2(
        cls: type[Self], parameter_ref: xtce_1_2.ParameterInstanceRefType
    ) -> Self:
        return cls(
            ref=XtcePath(parameter_ref.parameter_ref),
            instance=parameter_ref.instance,
            use_calibrated_value=parameter_ref.use_calibrated_value,
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], parameter_ref: xtce_1_3.ParameterInstanceRefType
    ) -> Self:
        return cls(
            ref=XtcePath(parameter_ref.parameter_ref),
            instance=parameter_ref.instance,
            use_calibrated_value=parameter_ref.use_calibrated_value,
        )

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create a ParameterInstanceRef from an xsdata-generated
        ParameterInstanceRefType object of any version.
        """
        match version:
            case XtceVersion.V1_1:
                return cls._from_v1_1(raw_obj)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.ParameterInstanceRefType:
        return xtce_1_1.ParameterInstanceRefType(
            parameter_ref=str(self.ref),
            instance=self.instance,
            use_calibrated_value=self.use_calibrated_value,
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ParameterInstanceRefType:
        return xtce_1_2.ParameterInstanceRefType(
            parameter_ref=str(self.ref),
            instance=self.instance,
            use_calibrated_value=self.use_calibrated_value,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ParameterInstanceRefType:
        return xtce_1_3.ParameterInstanceRefType(
            parameter_ref=str(self.ref),
            instance=self.instance,
            use_calibrated_value=self.use_calibrated_value,
        )

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> (
        xtce_1_1.ParameterInstanceRefType
        | xtce_1_2.ParameterInstanceRefType
        | xtce_1_3.ParameterInstanceRefType
    ):
        """Convert this ParameterInstanceRef to an xsdata-generated
        ParameterInstanceRefType object of the specified version.
        """
        match version:
            case XtceVersion.V1_1:
                return self._to_v1_1(policy)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)


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

    @classmethod
    def _from_v1_2(
        cls: type[Self], argument_ref: xtce_1_2.ArgumentInstanceRefType
    ) -> Self:
        return cls(
            ref=argument_ref.argument_ref,
            use_calibrated_value=argument_ref.use_calibrated_value,
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], argument_ref: xtce_1_3.ArgumentInstanceRefType
    ) -> Self:
        return cls(
            ref=argument_ref.argument_ref,
            use_calibrated_value=argument_ref.use_calibrated_value,
        )

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create a ParameterInstanceRef from an xsdata-generated
        ParameterInstanceRefType object of any version.
        """
        match version:
            case XtceVersion.V1_1:
                raise XtceUnsupportedError(version, cls.__name__)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ArgumentInstanceRefType:
        return xtce_1_2.ArgumentInstanceRefType(
            argument_ref=str(self.ref),
            use_calibrated_value=self.use_calibrated_value,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ArgumentInstanceRefType:
        return xtce_1_3.ArgumentInstanceRefType(
            argument_ref=str(self.ref),
            use_calibrated_value=self.use_calibrated_value,
        )

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ArgumentInstanceRefType | xtce_1_3.ArgumentInstanceRefType:
        """Convert this ArgumentInstanceRef to an xsdata-generated
        ArgumentInstanceRefType object of the specified version.
        """
        match version:
            case XtceVersion.V1_1:
                raise XtceUnsupportedError(version, self.__class__.__name__)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)


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

    @classmethod
    def _from_v1_2(
        cls: type[Self], parameter_ref: xtce_1_2.InputParameterInstanceRefType
    ) -> Self:
        return cls(
            ref=XtcePath(parameter_ref.parameter_ref),
            input_name=parameter_ref.input_name,
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], parameter_ref: xtce_1_3.InputParameterInstanceRefType
    ) -> Self:
        return cls(
            ref=XtcePath(parameter_ref.parameter_ref),
            input_name=parameter_ref.input_name,
        )

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create an InputParameterInstanceRef from an xsdata-
        generated InputParameterInstanceRefType object of any version.
        """
        match version:
            case XtceVersion.V1_1:
                raise XtceUnsupportedError(version, cls.__name__)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.InputParameterInstanceRefType:
        return xtce_1_2.InputParameterInstanceRefType(
            parameter_ref=str(self.ref),
            input_name=self.input_name,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.InputParameterInstanceRefType:
        return xtce_1_3.InputParameterInstanceRefType(
            parameter_ref=str(self.ref),
            input_name=self.input_name,
        )

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> (
        xtce_1_2.InputParameterInstanceRefType | xtce_1_3.InputParameterInstanceRefType
    ):
        """Convert this InputParameterInstanceRef to an xsdata-generated
        InputParameterInstanceRefType object of the specified version.
        """
        match version:
            case XtceVersion.V1_1:
                raise XtceUnsupportedError(version, self.__class__.__name__)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)


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

    def validate_semantics(self, registry: XtceRegistry, scope: XtcePath) -> None:
        """Validate this object's semantics.

        Rules:
            - The reference must not contain an array index or aggregate member.
            - The reference must exist.
            - The reference must be an instance of SequenceContainer.

        """
        if self.ref.contains_array or self.ref.contains_aggregate:
            raise ValueError(
                f"reference '{self.ref}' contains an array index or aggregate member, "
                f"but a ContainerRef must reference a sequence container only."
            )

        from .container import SequenceContainer

        try:
            result = registry.resolve(self.ref, scope)
            if not isinstance(result.target, SequenceContainer):
                raise ValueError(
                    f"reference '{self.ref}' resolved to a "
                    f"'{type(result.target).__name__}' type, "
                    f"but a 'SequenceContainer' type was expected."
                )

        except KeyError:
            raise ValueError(
                f"reference '{self.ref}' does not resolve to a valid object "
                f"from scope '{scope}'"
            )

    @classmethod
    def _from_v1_1(cls: type[Self], container_ref: xtce_1_1.ContainerRefType) -> Self:
        return cls(ref=XtcePath(container_ref.container_ref))

    @classmethod
    def _from_v1_2(cls: type[Self], container_ref: xtce_1_2.ContainerRefType) -> Self:
        return cls(ref=XtcePath(container_ref.container_ref))

    @classmethod
    def _from_v1_3(cls: type[Self], container_ref: xtce_1_3.ContainerRefType) -> Self:
        return cls(ref=XtcePath(container_ref.container_ref))

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create a ContainerRef from an xsdata-generated
        ContainerRefType object of any version.
        """
        match version:
            case XtceVersion.V1_1:
                return cls._from_v1_1(raw_obj)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.ContainerRefType:
        return xtce_1_1.ContainerRefType(container_ref=str(self.ref))

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ContainerRefType:
        return xtce_1_2.ContainerRefType(container_ref=str(self.ref))

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ContainerRefType:
        return xtce_1_3.ContainerRefType(container_ref=str(self.ref))

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> (
        xtce_1_1.ContainerRefType
        | xtce_1_2.ContainerRefType
        | xtce_1_3.ContainerRefType
    ):
        """Convert this ContainerRef to an xsdata-generated ContainerRefType object of
        the specified version.
        """
        match version:
            case XtceVersion.V1_1:
                return self._to_v1_1(policy)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)


class ServiceRef(XtceBaseModel):
    """A reference to a service."""

    ref: Annotated[XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))] = Field(
        ...,
        examples=[
            "/SimpleSat/PowerService",
            "../ThermalService",
            "CommandService",
        ],
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to a service."""

    def validate_semantics(self, registry: XtceRegistry, scope: XtcePath) -> None:
        """Validate this object's semantics.

        Rules:
            - The reference must not contain an array index or aggregate member.
            - The reference must exist.
            - The reference must be an instance of Service.

        """
        if self.ref.contains_array or self.ref.contains_aggregate:
            raise ValueError(
                f"reference '{self.ref}' contains an array index or aggregate member, "
                f"but a ServiceRef must reference a service only."
            )

        from .space_system import Service

        try:
            result = registry.resolve(self.ref, scope)
            if not isinstance(result.target, Service):
                raise ValueError(
                    f"reference '{self.ref}' resolved to a "
                    f"'{type(result.target).__name__}' type, "
                    f"but a 'Service' type was expected."
                )

        except KeyError:
            raise ValueError(
                f"reference '{self.ref}' does not resolve to a valid object "
                f"from scope '{scope}'"
            )

    @classmethod
    def _from_v1_1(cls: type[Self], service_ref: xtce_1_1.ServiceRefType) -> Self:
        return cls(ref=XtcePath(service_ref.service_ref))

    @classmethod
    def _from_v1_2(cls: type[Self], service_ref: xtce_1_2.ServiceRefType) -> Self:
        return cls(ref=XtcePath(service_ref.service_ref))

    @classmethod
    def _from_v1_3(cls: type[Self], service_ref: xtce_1_3.ServiceRefType) -> Self:
        return cls(ref=XtcePath(service_ref.service_ref))

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create a ServiceRef from an xsdata-generated ServiceRefType
        object of any version.
        """
        match version:
            case XtceVersion.V1_1:
                return cls._from_v1_1(raw_obj)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.ServiceRefType:
        return xtce_1_1.ServiceRefType(service_ref=str(self.ref))

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ServiceRefType:
        return xtce_1_2.ServiceRefType(service_ref=str(self.ref))

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ServiceRefType:
        return xtce_1_3.ServiceRefType(service_ref=str(self.ref))

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.ServiceRefType | xtce_1_2.ServiceRefType | xtce_1_3.ServiceRefType:
        """Convert this ServiceRef to an xsdata-generated ServiceRefType object of the
        specified version.
        """
        match version:
            case XtceVersion.V1_1:
                return self._to_v1_1(policy)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)


class StreamRef(XtceBaseModel):
    """A reference to a stream."""

    ref: Annotated[XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))] = Field(
        ...,
        examples=[
            "/SimpleSat/PowerStream",
            "../ThermalStream",
            "CommandStream",
        ],
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to a stream."""

    def validate_semantics(self, registry: XtceRegistry, scope: XtcePath) -> None:
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
                f"but a StreamRef must reference a stream only."
            )

        from .stream import CustomStream, FixedFrameStream, VariableFrameStream

        try:
            result = registry.resolve(self.ref, scope)
            if not isinstance(
                result.target, (CustomStream, FixedFrameStream, VariableFrameStream)
            ):
                raise ValueError(
                    f"reference '{self.ref}' resolved to a "
                    f"'{type(result.target).__name__}' type, "
                    f"but a 'CustomStream', 'FixedFrameStream' or "
                    f"'VariableFrameStream' type was expected."
                )

        except KeyError:
            raise ValueError(
                f"reference '{self.ref}' does not resolve to a valid object "
                f"from scope '{scope}'"
            )

    @classmethod
    def _from_v1_1(cls: type[Self], stream_ref: xtce_1_1.StreamRefType) -> Self:
        return cls(ref=XtcePath(stream_ref.stream_ref))

    @classmethod
    def _from_v1_2(cls: type[Self], stream_ref: xtce_1_2.StreamRefType) -> Self:
        return cls(ref=XtcePath(stream_ref.stream_ref))

    @classmethod
    def _from_v1_3(cls: type[Self], stream_ref: xtce_1_3.StreamRefType) -> Self:
        return cls(ref=XtcePath(stream_ref.stream_ref))

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create a StreamRef from an xsdata-generated StreamRefType
        object of any version.
        """
        match version:
            case XtceVersion.V1_1:
                return cls._from_v1_1(raw_obj)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.StreamRefType:
        return xtce_1_1.StreamRefType(stream_ref=str(self.ref))

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.StreamRefType:
        return xtce_1_2.StreamRefType(stream_ref=str(self.ref))

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.StreamRefType:
        return xtce_1_3.StreamRefType(stream_ref=str(self.ref))

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.StreamRefType | xtce_1_2.StreamRefType | xtce_1_3.StreamRefType:
        """Convert this StreamRef to an xsdata-generated StreamRefType object of the
        specified version.
        """
        match version:
            case XtceVersion.V1_1:
                return self._to_v1_1(policy)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)
