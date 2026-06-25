"""Reference models."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Any, Self, assert_never

from pydantic import AfterValidator, Field

from xtce_lib.common.xtce_path import XtcePath, require_regex
from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from ._pattern import EXPD_NAME_REF_W_PATH

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


class ParameterInstanceRef(ParameterRef):
    instance: int = Field(default=0)
    use_calibrated_value: bool = Field(default=True)


class ContainerRef(XtceBaseModel):
    """Holds a reference to a container."""

    ref: str = Field(
        ...,
        pattern=r"^(?:/?(?:\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+$",
        examples=[
            "/Telemetry/Power/PowerStatus",
            "../Thermal/ThermalStatus",
            "Command/ExecutionReport",
        ],
    )
    """Name of container."""


class ServiceRef(XtceBaseModel):
    service_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )


class StreamRef(XtceBaseModel):
    stream_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )


class InputParameterInstanceRef(ParameterInstanceRef):
    input_name: str | None = Field(default=None)


class OutputParameterRef(ParameterRef):
    output_name: str | None = Field(default=None)


class ArgumentInstanceRef(XtceBaseModel):
    argument_ref: str = Field(
        ..., pattern=r"([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)"
    )
    use_calibrated_value: bool = Field(default=True)
