"""Top-level classes relevant to the SpaceSystem."""

from pydantic import Field

from ._base import XtceBaseModel
from .commands import CommandMetadata
from .common import NameDescriptionBase
from .enums import SystemType, ValidationStatus
from .telemetry import TelemetryMetadata


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

    space_system: list["SpaceSystem"] = Field(default_factory=list)
    """Additional SpaceSystem elements may be used like namespaces to segregate portions
    of the space asset/device into convenient groupings or may be used to specialize a
    product line generic SpaceSystem to a specific asset instance.
    """

    system_type: SystemType = Field(default=SystemType.UNKNOWN)
    """Type of the space system.

    Represents what from a space enterprise this SpaceSystem element represents. See the
    individual enumeration descriptions in SystemType.
    """

    asset_type: str = Field(
        default="unknown",
        examples=["spacecraft", "aircraft", "device"],
    )
    """Broad name for the type of asset."""

    operational_status: str | None = Field(
        default=None,
        examples=["operational", "non-operational"],
    )
    """Optional descriptive attribute for document owner convenience."""

    base: str | None = Field(default=None)
