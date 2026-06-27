"""Top-level classes relevant to the SpaceSystem."""

from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING, Any, Self

from pydantic import Field
from typing_extensions import assert_never

from xtce_lib.common.validation import ValidationReport, XtceSemanticError
from xtce_lib.common.xtce_path import XtcePath
from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from .command import CommandMetadata
from .common import Alias, AncillaryData, NameDescriptionBase
from .enum import SystemType, ValidationStatus
from .reference import ContainerRef
from .telemetry import TelemetryMetadata

if TYPE_CHECKING:
    from xtce_lib.common.xtce_registry import XtceRegistry


class Header(XtceBaseModel):
    """Schema for a Header record.

    A header contains general information about the system or subsystem.

    """

    authors: list[str] = Field(
        default_factory=list,
        examples=[
            "John Spacecraft",
            "Jane Satellite",
            "Cletus",
        ],
    )
    """Contains optional contact information for this document."""

    notes: list[str] = Field(
        default_factory=list,
        examples=[
            "This XTCE is intended for use with CONKSAT-1.",
            "This XTCE contains separate SpaceSystems for each subsystem.",
            "For operator safety, do not read line 42.",
        ],
    )
    """Contains optional technical information related to the content of this
    document.
    """

    history: list[str] = Field(
        default_factory=list,
        examples=[
            "Initial release",
            "Removed self destruct command.",
            "Re-added self destruct command after realizing it was actually needed.",
        ],
    )
    """Contains optional evolutionary information for data contained in this
    document.
    """

    version: str | None = Field(default=None, examples=["1.0", "2.0", "3.0"])
    """Contains an optional version descriptor for this document."""

    date: str | None = Field(
        default=None,
        examples=["2026-01-01", "December 6, 2000", "Feb 31, 2032"],
    )
    """Contains an optional date to be associated with this document."""

    classification: str = Field(
        default="NotClassified",
        examples=[
            "CUI",
            "Secret",
            "Top Secret",
        ],
    )
    """Contains optional classification status for use by programs for which that is
    applicable.
    """

    classification_instructions: str | None = Field(default=None)
    """Contains an optional additional instructions attribute to be interpreted by
    programs that use this attribute.
    """

    validation_status: ValidationStatus = Field(default=ValidationStatus.UNKNOWN)
    """Contains a flag describing the state of this document in the evolution of the
    project using it.
    """


class MessageRef(XtceBaseModel):
    """Holds a reference to a message."""

    ref: str = Field(
        ...,
        pattern=r"^(?:/?(?:\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+$",
        examples=[
            "/BusMessages/HkSummary",
            "../FlightSoftware/EventMessage",
            "Payload/FrameStatus",
        ],
    )
    """Name of message."""


class Service(NameDescriptionBase):
    """Holds a set of services, logical groups of containers OR messages."""

    refs: list[MessageRef] | list[ContainerRef] = Field(
        default_factory=list,
        min_length=1,
    )


class SpaceSystem(NameDescriptionBase):
    """A collection of SpaceSystem(s).

    Each SpaceSystem may include space assets, ground assets, multi-satellite systems
    and sub-systems. A SpaceSystem is the root element for the set of data necessary to
    monitor and command an arbitrary space device - this includes the binary
    decomposition the data streams going into and out of a device.

    """

    header: Header | None = Field(default=None)
    """The Header element contains optional descriptive information about this
    SpaceSystem or the document as a whole when specified at the root SpaceSystem.
    """

    telemetry_metadata: TelemetryMetadata | None = Field(default=None)
    """This element contains descriptions of the telemetry created on the space
    asset/device and sent to other data consumers.
    """

    command_metadata: CommandMetadata | None = Field(default=None)
    """This element contains descriptions of the commands and their associated
    constraints and verifications that can be sent to the space asset/device.
    """

    services: list[Service] = Field(default_factory=list)
    """A logical grouping of container and/or messages."""

    space_systems: list["SpaceSystem"] = Field(default_factory=list)
    """Additional SpaceSystem elements may be used like namespaces to segregate portions
    of the space asset/device into convenient groupings or may be used to specialize a
    product line generic SpaceSystem to a specific asset instance.
    """

    system_type: SystemType = Field(default=SystemType.UNKNOWN)
    """Type of the space system.

    Represents what from a space enterprise this SpaceSystem element represents. See the
    individual enumeration descriptions in SystemType.

    Applicable since: XTCE 1.3.

    """

    asset_type: str = Field(
        default="unknown",
        examples=["spacecraft", "aircraft", "device"],
    )
    """Broad name for the type of asset.

    Applicable since: XTCE 1.3.

    """

    operational_status: str | None = Field(
        default=None,
        examples=["operational", "non-operational"],
    )
    """Optional descriptive attribute for document owner convenience."""

    base: str | None = Field(default=None)
    """Applicable since: XTCE 1.3."""

    def validate_semantics(
        self,
        report: ValidationReport[XtceSemanticError],
        registry: XtceRegistry,
        scope: XtcePath,
    ) -> None:
        """Validate this object's semantics."""
        # TODO call all child validate_semantics methods

    @classmethod
    def _from_v1_1(cls: type[Self], space_system: xtce_1_1.SpaceSystem) -> Self:
        version = XtceVersion.V1_1

        kwargs = {
            f.name: getattr(space_system, f.name)
            for f in dataclasses.fields(space_system)
        }

        if space_system.alias_set:
            kwargs["alias_set"] = [
                Alias.from_xsdata(alias, version)
                for alias in space_system.alias_set.alias
            ]
        if space_system.ancillary_data_set:
            kwargs["ancillary_data_set"] = [
                AncillaryData.from_xsdata(ancillary_data, version)
                for ancillary_data in space_system.ancillary_data_set.ancillary_data
            ]
        if space_system.header:
            kwargs["header"] = Header.from_xsdata(
                space_system.header,
                version,
            )
        if space_system.telemetry_meta_data:
            kwargs["telemetry_metadata"] = TelemetryMetadata.from_xsdata(
                space_system.telemetry_meta_data,
                version,
            )
        if space_system.command_meta_data:
            kwargs["command_metadata"] = CommandMetadata.from_xsdata(
                space_system.command_meta_data,
                version,
            )
        if space_system.service_set:
            kwargs["services"] = [
                Service.from_xsdata(service, version)
                for service in space_system.service_set.service
            ]
        if space_system.space_system:
            kwargs["space_system"] = [
                cls._from_v1_1(subsystem) for subsystem in space_system.space_system
            ]

        return cls(**kwargs)

    @classmethod
    def _from_v1_2(cls: type[Self], space_system: xtce_1_2.SpaceSystem) -> Self:
        version = XtceVersion.V1_2

        kwargs = {
            f.name: getattr(space_system, f.name)
            for f in dataclasses.fields(space_system)
        }

        if space_system.alias_set:
            kwargs["alias_set"] = [
                Alias.from_xsdata(alias, version)
                for alias in space_system.alias_set.alias
            ]
        if space_system.ancillary_data_set:
            kwargs["ancillary_data_set"] = [
                AncillaryData.from_xsdata(ancillary_data, version)
                for ancillary_data in space_system.ancillary_data_set.ancillary_data
            ]
        if space_system.header:
            kwargs["header"] = Header.from_xsdata(
                space_system.header,
                version,
            )
        if space_system.telemetry_meta_data:
            kwargs["telemetry_metadata"] = TelemetryMetadata.from_xsdata(
                space_system.telemetry_meta_data,
                version,
            )
        if space_system.command_meta_data:
            kwargs["command_metadata"] = CommandMetadata.from_xsdata(
                space_system.command_meta_data,
                version,
            )
        if space_system.service_set:
            kwargs["services"] = [
                Service.from_xsdata(service, version)
                for service in space_system.service_set.service
            ]
        if space_system.space_system:
            kwargs["space_system"] = [
                cls._from_v1_2(subsystem) for subsystem in space_system.space_system
            ]

        return cls(**kwargs)

    @classmethod
    def _from_v1_3(cls: type[Self], space_system: xtce_1_3.SpaceSystem) -> Self:
        version = XtceVersion.V1_3

        kwargs = {
            f.name: getattr(space_system, f.name)
            for f in dataclasses.fields(space_system)
        }

        if space_system.alias_set:
            kwargs["alias_set"] = [
                Alias.from_xsdata(alias, version)
                for alias in space_system.alias_set.alias
            ]
        if space_system.ancillary_data_set:
            kwargs["ancillary_data_set"] = [
                AncillaryData.from_xsdata(ancillary_data, version)
                for ancillary_data in space_system.ancillary_data_set.ancillary_data
            ]
        if space_system.header:
            kwargs["header"] = Header.from_xsdata(
                space_system.header,
                version,
            )
        if space_system.telemetry_meta_data:
            kwargs["telemetry_metadata"] = TelemetryMetadata.from_xsdata(
                space_system.telemetry_meta_data,
                version,
            )
        if space_system.command_meta_data:
            kwargs["command_metadata"] = CommandMetadata.from_xsdata(
                space_system.command_meta_data,
                version,
            )
        if space_system.service_set:
            kwargs["services"] = [
                Service.from_xsdata(service, version)
                for service in space_system.service_set.service
            ]
        if space_system.space_system:
            kwargs["space_system"] = [
                cls._from_v1_3(subsystem) for subsystem in space_system.space_system
            ]
        if space_system.system_type:
            kwargs["system_type"] = SystemType(space_system.system_type.value)

        return cls(**kwargs)

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create a SpaceSystem from an xsdata-generated SpaceSystem
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
    ) -> xtce_1_1.SpaceSystem:
        version = XtceVersion.V1_1

        self._enforce_unsupported_field(
            field_name="system_type",
            current_value=self.system_type,
            empty_value=SystemType.UNKNOWN,
            target_version=version,
            policy=policy,
        )
        self._enforce_unsupported_field(
            field_name="asset_type",
            current_value=self.asset_type,
            empty_value="unknown",
            target_version=version,
            policy=policy,
        )
        self._enforce_unsupported_field(
            field_name="base",
            current_value=self.base,
            empty_value=None,
            target_version=version,
            policy=policy,
        )

        return xtce_1_1.SpaceSystem(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=xtce_1_1.AliasSetType(
                alias=[alias.to_xsdata(version=version) for alias in self.aliases]
            )
            if self.aliases
            else None,
            ancillary_data_set=xtce_1_1.DescriptionType.AncillaryDataSet(
                ancillary_data=[
                    ancillary_data.to_xsdata(version=version)
                    for ancillary_data in self.ancillary_data
                ]
            )
            if self.ancillary_data
            else None,
            header=self.header.to_xsdata(version=version) if self.header else None,
            telemetry_meta_data=self.telemetry_metadata.to_xsdata(version=version)
            if self.telemetry_metadata
            else None,
            command_meta_data=self.command_metadata.to_xsdata(version=version)
            if self.command_metadata
            else None,
            service_set=xtce_1_1.SpaceSystemType.ServiceSet(
                service=[
                    service.to_xsdata(version=version) for service in self.services
                ]
            )
            if self.services
            else None,
            space_system=[
                subsystem._to_v1_1(policy) for subsystem in self.space_systems
            ],
            operational_status=self.operational_status,
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.SpaceSystem:
        version = XtceVersion.V1_2

        self._enforce_unsupported_field(
            field_name="system_type",
            current_value=self.system_type,
            empty_value=SystemType.UNKNOWN,
            target_version=version,
            policy=policy,
        )
        self._enforce_unsupported_field(
            field_name="asset_type",
            current_value=self.asset_type,
            empty_value="unknown",
            target_version=version,
            policy=policy,
        )
        self._enforce_unsupported_field(
            field_name="base",
            current_value=self.base,
            empty_value=None,
            target_version=version,
            policy=policy,
        )

        return xtce_1_2.SpaceSystem(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=xtce_1_2.AliasSetType(
                alias=[alias.to_xsdata(version=version) for alias in self.aliases]
            )
            if self.aliases
            else None,
            ancillary_data_set=xtce_1_2.AncillaryDataSetType(
                ancillary_data=[
                    ancillary_data.to_xsdata(version=version)
                    for ancillary_data in self.ancillary_data
                ]
            )
            if self.ancillary_data
            else None,
            header=self.header.to_xsdata(version=version) if self.header else None,
            telemetry_meta_data=self.telemetry_metadata.to_xsdata(version=version)
            if self.telemetry_metadata
            else None,
            command_meta_data=self.command_metadata.to_xsdata(version=version)
            if self.command_metadata
            else None,
            service_set=xtce_1_2.ServiceSetType(
                service=[
                    service.to_xsdata(version=version) for service in self.services
                ]
            )
            if self.services
            else None,
            space_system=[
                subsystem._to_v1_2(policy) for subsystem in self.space_systems
            ],
            operational_status=self.operational_status,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.SpaceSystem:
        version = XtceVersion.V1_3

        return xtce_1_3.SpaceSystem(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=xtce_1_3.AliasSetType(
                alias=[alias.to_xsdata(version=version) for alias in self.aliases]
            )
            if self.aliases
            else None,
            ancillary_data_set=xtce_1_3.AncillaryDataSetType(
                ancillary_data=[
                    ancillary_data.to_xsdata(version=version)
                    for ancillary_data in self.ancillary_data
                ]
            )
            if self.ancillary_data
            else None,
            header=self.header.to_xsdata(version=version) if self.header else None,
            telemetry_meta_data=self.telemetry_metadata.to_xsdata(version=version)
            if self.telemetry_metadata
            else None,
            command_meta_data=self.command_metadata.to_xsdata(version=version)
            if self.command_metadata
            else None,
            service_set=xtce_1_3.ServiceSetType(
                service=[
                    service.to_xsdata(version=version) for service in self.services
                ]
            )
            if self.services
            else None,
            space_system=[
                subsystem._to_v1_3(policy) for subsystem in self.space_systems
            ],
            system_type=xtce_1_3.SystemTypeType(self.system_type.value),
            asset_type=self.asset_type,
            operational_status=self.operational_status,
            base=self.base,
        )

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.SpaceSystem | xtce_1_2.SpaceSystem | xtce_1_3.SpaceSystem:
        """Convert this SpaceSystem to an xsdata-generated SpaceSystem object of the
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
