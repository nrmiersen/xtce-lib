"""Top-level classes relevant to the SpaceSystem."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Any

from pydantic import AfterValidator, Field

from xtce_lib.common.validation import ValidationReport, XtceSemanticError
from xtce_lib.common.xtce_path import XtcePath, require_regex
from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3
from xtce_lib.xtce._pattern import NAME_REF_W_PATH

from ._base import XtceBaseModel
from .command import CommandMetadata
from .common import NameDescriptionBase
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

    classification_instructions: str | None = None
    """Contains an optional additional instructions attribute to be interpreted by
    programs that use this attribute.
    """

    validation_status: ValidationStatus = ValidationStatus.UNKNOWN
    """Contains a flag describing the state of this document in the evolution of the
    project using it.
    """

    _v1_1_type = xtce_1_1.HeaderType
    _v1_2_type = xtce_1_2.HeaderType
    _v1_3_type = xtce_1_3.HeaderType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.HeaderType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["authors"] = (
            [a for a in obj.author_set.author] if obj.author_set is not None else []
        )
        kwargs["notes"] = (
            [n for n in obj.note_set.note] if obj.note_set is not None else []
        )
        kwargs["history"] = (
            [h for h in obj.history_set.history] if obj.history_set is not None else []
        )
        kwargs["version"] = obj.version
        kwargs["date"] = obj.date
        kwargs["classification"] = obj.classification
        kwargs["classification_instructions"] = obj.classification_instructions
        kwargs["validation_status"] = ValidationStatus(obj.validation_status.value)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.HeaderType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["authors"] = (
            [a for a in obj.author_set.author] if obj.author_set is not None else []
        )
        kwargs["notes"] = (
            [n for n in obj.note_set.note] if obj.note_set is not None else []
        )
        kwargs["history"] = (
            [h for h in obj.history_set.history] if obj.history_set is not None else []
        )
        kwargs["version"] = obj.version
        kwargs["date"] = obj.date
        kwargs["classification"] = obj.classification
        kwargs["classification_instructions"] = obj.classification_instructions
        kwargs["validation_status"] = ValidationStatus(obj.validation_status.value)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.HeaderType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["authors"] = (
            [a for a in obj.author_set.author] if obj.author_set is not None else []
        )
        kwargs["notes"] = (
            [n for n in obj.note_set.note] if obj.note_set is not None else []
        )
        kwargs["history"] = (
            [h for h in obj.history_set.history] if obj.history_set is not None else []
        )
        kwargs["version"] = obj.version
        kwargs["date"] = obj.date
        kwargs["classification"] = obj.classification
        kwargs["classification_instructions"] = obj.classification_instructions
        kwargs["validation_status"] = ValidationStatus(obj.validation_status.value)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["author_set"] = self._build_set(
            items=self.authors,
            set_class=xtce_1_1.HeaderType.AuthorSet,
            kwarg_name="author",
            converter=lambda a: a,
        )
        kwargs["note_set"] = self._build_set(
            items=self.notes,
            set_class=xtce_1_1.HeaderType.NoteSet,
            kwarg_name="note",
            converter=lambda n: n,
        )
        kwargs["history_set"] = self._build_set(
            items=self.history,
            set_class=xtce_1_1.HeaderType.HistorySet,
            kwarg_name="history",
            converter=lambda h: h,
        )
        kwargs["version"] = self.version
        kwargs["date"] = self.date
        kwargs["classification"] = self.classification
        kwargs["classification_instructions"] = self.classification_instructions
        kwargs["validation_status"] = xtce_1_1.HeaderTypeValidationStatus(
            self.validation_status.value
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["author_set"] = self._build_set(
            items=self.authors,
            set_class=xtce_1_2.AuthorSetType,
            kwarg_name="author",
            converter=lambda a: a,
        )
        kwargs["note_set"] = self._build_set(
            items=self.notes,
            set_class=xtce_1_2.NoteSetType,
            kwarg_name="note",
            converter=lambda n: n,
        )
        kwargs["history_set"] = self._build_set(
            items=self.history,
            set_class=xtce_1_2.HistorySetType,
            kwarg_name="history",
            converter=lambda h: h,
        )
        kwargs["version"] = self.version
        kwargs["date"] = self.date
        kwargs["classification"] = self.classification
        kwargs["classification_instructions"] = self.classification_instructions
        kwargs["validation_status"] = xtce_1_2.ValidationStatusType(
            self.validation_status.value
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["author_set"] = self._build_set(
            items=self.authors,
            set_class=xtce_1_3.AuthorSetType,
            kwarg_name="author",
            converter=lambda a: a,
        )
        kwargs["note_set"] = self._build_set(
            items=self.notes,
            set_class=xtce_1_3.NoteSetType,
            kwarg_name="note",
            converter=lambda n: n,
        )
        kwargs["history_set"] = self._build_set(
            items=self.history,
            set_class=xtce_1_3.HistorySetType,
            kwarg_name="history",
            converter=lambda h: h,
        )
        kwargs["version"] = self.version
        kwargs["date"] = self.date
        kwargs["classification"] = self.classification
        kwargs["classification_instructions"] = self.classification_instructions
        kwargs["validation_status"] = xtce_1_3.ValidationStatusType(
            self.validation_status.value
        )
        return kwargs


class MessageRef(XtceBaseModel):
    """Holds a reference to a message."""

    ref: Annotated[XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))] = Field(
        ...,
        examples=[
            "/BusMessages/HkSummary",
            "../FlightSoftware/EventMessage",
            "Payload/FrameStatus",
        ],
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to a message."""

    _v1_1_type = xtce_1_1.MessageRefType
    _v1_2_type = xtce_1_2.MessageRefType
    _v1_3_type = xtce_1_3.MessageRefType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.MessageRefType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.message_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.MessageRefType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.message_ref)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.MessageRefType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.message_ref)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["message_ref"] = str(self.ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["message_ref"] = str(self.ref)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["message_ref"] = str(self.ref)
        return kwargs


class Service(NameDescriptionBase):
    """Holds a set of services, logical groups of containers OR messages."""

    refs: list[MessageRef] | list[ContainerRef] = Field(default_factory=list)

    _v1_1_type = xtce_1_1.ServiceType
    _v1_2_type = xtce_1_2.ServiceType
    _v1_3_type = xtce_1_3.ServiceType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.ServiceType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["refs"] = (
            [MessageRef._from_v1_1(ref) for ref in obj.choice.message_ref]
            if isinstance(obj.choice, xtce_1_1.ServiceType.MessageRefSet)
            else [ContainerRef._from_v1_1(ref) for ref in obj.choice.container_ref]
            if isinstance(obj.choice, xtce_1_1.ServiceType.ContainerRefSet)
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ServiceType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["refs"] = (
            [MessageRef._from_v1_2(ref) for ref in obj.choice.message_ref]
            if isinstance(obj.choice, xtce_1_2.MessageRefSetType)
            else [ContainerRef._from_v1_2(ref) for ref in obj.choice.container_ref]
            if isinstance(obj.choice, xtce_1_2.ContainerRefSetType)
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ServiceType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["refs"] = (
            [MessageRef._from_v1_3(ref) for ref in obj.choice.message_ref]
            if isinstance(obj.choice, xtce_1_3.MessageRefSetType)
            else [ContainerRef._from_v1_3(ref) for ref in obj.choice.container_ref]
            if isinstance(obj.choice, xtce_1_3.ContainerRefSetType)
            else []
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["choice"] = (
            self._build_set(
                items=self.refs,
                set_class=xtce_1_1.ServiceType.MessageRefSet,
                kwarg_name="message_ref",
                converter=lambda ref: ref._to_v1_1(policy),
            )
            if self.refs and all(isinstance(ref, MessageRef) for ref in self.refs)
            else self._build_set(
                items=self.refs,
                set_class=xtce_1_1.ServiceType.ContainerRefSet,
                kwarg_name="container_ref",
                converter=lambda ref: ref._to_v1_1(policy),
            )
            if self.refs and all(isinstance(ref, ContainerRef) for ref in self.refs)
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = (
            self._build_set(
                items=self.refs,
                set_class=xtce_1_2.MessageRefSetType,
                kwarg_name="message_ref",
                converter=lambda ref: ref._to_v1_2(policy),
            )
            if self.refs and all(isinstance(ref, MessageRef) for ref in self.refs)
            else self._build_set(
                items=self.refs,
                set_class=xtce_1_2.ContainerRefSetType,
                kwarg_name="container_ref",
                converter=lambda ref: ref._to_v1_2(policy),
            )
            if self.refs and all(isinstance(ref, ContainerRef) for ref in self.refs)
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = (
            self._build_set(
                items=self.refs,
                set_class=xtce_1_3.MessageRefSetType,
                kwarg_name="message_ref",
                converter=lambda ref: ref._to_v1_3(policy),
            )
            if self.refs and all(isinstance(ref, MessageRef) for ref in self.refs)
            else self._build_set(
                items=self.refs,
                set_class=xtce_1_3.ContainerRefSetType,
                kwarg_name="container_ref",
                converter=lambda ref: ref._to_v1_3(policy),
            )
            if self.refs and all(isinstance(ref, ContainerRef) for ref in self.refs)
            else None
        )
        return kwargs


class SpaceSystem(NameDescriptionBase):
    """A collection of SpaceSystem(s).

    Each SpaceSystem may include space assets, ground assets, multi-satellite systems
    and sub-systems. A SpaceSystem is the root element for the set of data necessary to
    monitor and command an arbitrary space device - this includes the binary
    decomposition the data streams going into and out of a device.

    """

    header: Header | None = None
    """The Header element contains optional descriptive information about this
    SpaceSystem or the document as a whole when specified at the root SpaceSystem.
    """

    telemetry_metadata: TelemetryMetadata | None = None
    """This element contains descriptions of the telemetry created on the space
    asset/device and sent to other data consumers.
    """

    command_metadata: CommandMetadata | None = None
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

    system_type: SystemType = SystemType.UNKNOWN
    """Type of the space system.

    Represents what from a space enterprise this SpaceSystem element represents. See the
    individual enumeration descriptions in SystemType.

    Applicable since: XTCE 1.3

    """

    asset_type: str = Field(
        default="unknown",
        examples=["spacecraft", "aircraft", "device"],
    )
    """Broad name for the type of asset.

    Applicable since: XTCE 1.3

    """

    operational_status: str | None = Field(
        default=None,
        examples=["operational", "non-operational"],
    )
    """Optional descriptive attribute for document owner convenience."""

    base: str | None = None
    """Applicable since: XTCE 1.3."""

    def validate_semantics(
        self,
        report: ValidationReport[XtceSemanticError],
        registry: XtceRegistry,
        scope: XtcePath,
    ) -> None:
        """Validate this object's semantics."""

        # TODO call all child validate_semantics methods

    _v1_1_type = xtce_1_1.SpaceSystem
    _v1_2_type = xtce_1_2.SpaceSystem
    _v1_3_type = xtce_1_3.SpaceSystem

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.SpaceSystemType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["header"] = (
            Header._from_v1_1(obj.header) if obj.header is not None else None
        )
        kwargs["telemetry_metadata"] = (
            TelemetryMetadata._from_v1_1(obj.telemetry_meta_data)
            if obj.telemetry_meta_data is not None
            else None
        )
        kwargs["command_metadata"] = (
            CommandMetadata._from_v1_1(obj.command_meta_data)
            if obj.command_meta_data is not None
            else None
        )
        kwargs["services"] = (
            [Service._from_v1_1(s) for s in obj.service_set.service]
            if obj.service_set is not None
            else []
        )
        kwargs["space_systems"] = [SpaceSystem._from_v1_1(s) for s in obj.space_system]
        kwargs["operational_status"] = obj.operational_status
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.SpaceSystemType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["header"] = (
            Header._from_v1_2(obj.header) if obj.header is not None else None
        )
        kwargs["telemetry_metadata"] = (
            TelemetryMetadata._from_v1_2(obj.telemetry_meta_data)
            if obj.telemetry_meta_data is not None
            else None
        )
        kwargs["command_metadata"] = (
            CommandMetadata._from_v1_2(obj.command_meta_data)
            if obj.command_meta_data is not None
            else None
        )
        kwargs["services"] = (
            [Service._from_v1_2(s) for s in obj.service_set.service]
            if obj.service_set is not None
            else []
        )
        kwargs["space_systems"] = [SpaceSystem._from_v1_2(s) for s in obj.space_system]
        kwargs["operational_status"] = obj.operational_status
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.SpaceSystemType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["header"] = (
            Header._from_v1_3(obj.header) if obj.header is not None else None
        )
        kwargs["telemetry_metadata"] = (
            TelemetryMetadata._from_v1_3(obj.telemetry_meta_data)
            if obj.telemetry_meta_data is not None
            else None
        )
        kwargs["command_metadata"] = (
            CommandMetadata._from_v1_3(obj.command_meta_data)
            if obj.command_meta_data is not None
            else None
        )
        kwargs["services"] = (
            [Service._from_v1_3(s) for s in obj.service_set.service]
            if obj.service_set is not None
            else []
        )
        kwargs["space_systems"] = [SpaceSystem._from_v1_3(s) for s in obj.space_system]
        kwargs["system_type"] = SystemType(obj.system_type.value)
        kwargs["asset_type"] = obj.asset_type
        kwargs["operational_status"] = obj.operational_status
        kwargs["base"] = obj.base
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
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

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["header"] = (
            self.header._to_v1_1(policy) if self.header is not None else None
        )
        kwargs["telemetry_meta_data"] = (
            self.telemetry_metadata._to_v1_1(policy)
            if self.telemetry_metadata is not None
            else None
        )
        kwargs["command_meta_data"] = (
            self.command_metadata._to_v1_1(policy)
            if self.command_metadata is not None
            else None
        )
        kwargs["service_set"] = self._build_set(
            items=self.services,
            set_class=xtce_1_1.SpaceSystemType.ServiceSet,
            kwarg_name="service",
            converter=lambda s: s._to_v1_1(policy),
        )
        kwargs["space_system"] = [s._to_v1_1(policy) for s in self.space_systems]
        kwargs["operational_status"] = self.operational_status
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
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

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["header"] = (
            self.header._to_v1_2(policy) if self.header is not None else None
        )
        kwargs["telemetry_meta_data"] = (
            self.telemetry_metadata._to_v1_2(policy)
            if self.telemetry_metadata is not None
            else None
        )
        kwargs["command_meta_data"] = (
            self.command_metadata._to_v1_2(policy)
            if self.command_metadata is not None
            else None
        )
        kwargs["service_set"] = self._build_set(
            items=self.services,
            set_class=xtce_1_2.ServiceSetType,
            kwarg_name="service",
            converter=lambda s: s._to_v1_2(policy),
        )
        kwargs["space_system"] = [s._to_v1_2(policy) for s in self.space_systems]
        kwargs["operational_status"] = self.operational_status
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["header"] = (
            self.header._to_v1_3(policy) if self.header is not None else None
        )
        kwargs["telemetry_meta_data"] = (
            self.telemetry_metadata._to_v1_3(policy)
            if self.telemetry_metadata is not None
            else None
        )
        kwargs["command_meta_data"] = (
            self.command_metadata._to_v1_3(policy)
            if self.command_metadata is not None
            else None
        )
        kwargs["service_set"] = self._build_set(
            items=self.services,
            set_class=xtce_1_3.ServiceSetType,
            kwarg_name="service",
            converter=lambda s: s._to_v1_3(policy),
        )
        kwargs["space_system"] = [s._to_v1_3(policy) for s in self.space_systems]
        kwargs["system_type"] = xtce_1_3.SystemTypeType(self.system_type.value)
        kwargs["asset_type"] = self.asset_type
        kwargs["operational_status"] = self.operational_status
        kwargs["base"] = self.base
        return kwargs
