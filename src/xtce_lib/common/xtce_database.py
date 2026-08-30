"""XTCE database object."""

import itertools
from pathlib import Path
from typing import Any, Iterable, Self

from pydantic import validate_call
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.xtce._type_aliases_ext import ReferenceableXtceObject
from xtce_lib.xtce.command import CommandMetadata, MetaCommandRef
from xtce_lib.xtce.common import Alias, AncillaryData
from xtce_lib.xtce.enum import SystemType
from xtce_lib.xtce.reference import ParameterRef
from xtce_lib.xtce.space_system import Header, Service, SpaceSystem
from xtce_lib.xtce.telemetry import TelemetryMetadata

from .validation import ValidationReport, XtceSemanticError
from .xtce_file import XtceFile
from .xtce_path import XtcePath
from .xtce_registry import XtceRegistry


class XtceDatabase:
    """An XTCE database."""

    @validate_call
    def __init__(self, name: str) -> None:
        """Initialize a new XTCE database."""
        self._root_system = SpaceSystem(name=name)
        self._registry: XtceRegistry | None = None

    @classmethod
    @validate_call
    def from_space_system(cls, space_system: SpaceSystem) -> Self:
        """Create a new XTCE database from an existing SpaceSystem."""
        # Bypass __init__
        instance = cls.__new__(cls)
        instance._root_system = space_system
        instance._registry = None
        return instance

    # TODO maybe from_file(), not sure how to handle XtceFile vs XtceDatabase yet

    # The below methods allow for accessing the properties of the root SpaceSystem
    # directly from the database, makes for a slightly cleaner API

    @property
    def name(self) -> str:
        """The name of the SpaceSystem."""
        return self._root_system.name

    @name.setter
    def name(self, value: str) -> None:
        self._root_system.name = value

    @property
    def short_description(self) -> str | None:
        """The short description of the SpaceSystem."""
        return self._root_system.short_description

    @short_description.setter
    def short_description(self, value: str | None) -> None:
        self._root_system.short_description = value

    @property
    def long_description(self) -> str | None:
        """The long description of the SpaceSystem."""
        return self._root_system.long_description

    @long_description.setter
    def long_description(self, value: str | None) -> None:
        self._root_system.long_description = value

    @property
    def aliases(self) -> list[Alias]:
        """The aliases of the SpaceSystem."""
        return self._root_system.aliases

    @aliases.setter
    def aliases(self, value: list[Alias]) -> None:
        self._root_system.aliases = value

    @property
    def ancillary_data(self) -> list[AncillaryData]:
        """The ancillary data of the SpaceSystem."""
        return self._root_system.ancillary_data

    @ancillary_data.setter
    def ancillary_data(self, value: list[AncillaryData]) -> None:
        self._root_system.ancillary_data = value

    @property
    def header(self) -> Header | None:
        """The header of the SpaceSystem."""
        return self._root_system.header

    @header.setter
    def header(self, value: Header | None) -> None:
        self._root_system.header = value

    @property
    def telemetry_metadata(self) -> TelemetryMetadata | None:
        """The telemetry metadata of the SpaceSystem."""
        return self._root_system.telemetry_metadata

    @telemetry_metadata.setter
    def telemetry_metadata(self, value: TelemetryMetadata | None) -> None:
        self._root_system.telemetry_metadata = value

    @property
    def command_metadata(self) -> CommandMetadata | None:
        """The command metadata of the SpaceSystem."""
        return self._root_system.command_metadata

    @command_metadata.setter
    def command_metadata(self, value: CommandMetadata | None) -> None:
        self._root_system.command_metadata = value

    @property
    def services(self) -> list[Service]:
        """The services of the SpaceSystem."""
        return self._root_system.services

    @services.setter
    def services(self, value: list[Service]) -> None:
        self._root_system.services = value

    @property
    def space_systems(self) -> list[SpaceSystem]:
        """The child SpaceSystems of the SpaceSystem."""
        return self._root_system.space_systems

    @space_systems.setter
    def space_systems(self, value: list[SpaceSystem]) -> None:
        self._root_system.space_systems = value

    @property
    def system_type(self) -> SystemType:
        """The system type of the SpaceSystem."""
        return self._root_system.system_type

    @system_type.setter
    def system_type(self, value: SystemType) -> None:
        self._root_system.system_type = value

    @property
    def asset_type(self) -> str:
        """The asset type of the SpaceSystem."""
        return self._root_system.asset_type

    @asset_type.setter
    def asset_type(self, value: str) -> None:
        self._root_system.asset_type = value

    @property
    def operational_status(self) -> str | None:
        """The operational status of the SpaceSystem."""
        return self._root_system.operational_status

    @operational_status.setter
    def operational_status(self, value: str | None) -> None:
        self._root_system.operational_status = value

    @property
    def base(self) -> str | None:
        """The base of the SpaceSystem."""
        return self._root_system.base

    @base.setter
    def base(self, value: str | None) -> None:
        self._root_system.base = value

    @property
    def root_system(self) -> SpaceSystem:
        """The root SpaceSystem of the database."""
        return self._root_system

    @property
    def registry(self) -> XtceRegistry:
        """Get the registry of all XTCE objects in this database."""
        if self._registry is None:
            self._registry = XtceRegistry()
            self._index_space_system(self.root_system, XtcePath("/"), self._registry)
        return self._registry

    def rebuild_registry(self) -> None:
        """Force a rebuild of the registry."""
        new_registry = XtceRegistry()
        self._index_space_system(self.root_system, XtcePath("/"), new_registry)
        self._registry = new_registry

    def validate(self) -> ValidationReport[XtceSemanticError]:
        """Perform semantic validation of this database."""
        report = ValidationReport[XtceSemanticError](title="Semantic Validation")
        self.rebuild_registry()  # Ensure registry is up to date before validation
        self.root_system.validate_semantics(report, self.registry, XtcePath("/"))
        return report

    @validate_call
    def to_file(
        self,
        path: Path,
        xtce_version: XtceVersion,
        *,
        downgrade_policy: DowngradePolicy = DowngradePolicy.STRICT,
        **kwargs: Any,
    ) -> XtceFile:
        """Write the database to an XTCE XML file.

        Any keyword arguments override the default serializer configuration.
        """
        # Translate the SpaceSystem
        space_system = self._root_system.to_xsdata(
            version=xtce_version,
            policy=downgrade_policy,
        )

        # Serialize to file
        config_kwargs: dict[str, Any] = {
            "indent": "    ",
        }
        config_kwargs.update(kwargs)
        config = SerializerConfig(**config_kwargs)
        serializer = XmlSerializer(config=config)

        with path.open("w", encoding="utf-8") as f:
            serializer.write(  # type: ignore[reportUnknownMemberType]
                f,
                space_system,
                ns_map={"xtce": xtce_version.value.namespace},
            )

        return XtceFile(path)

    def _index_space_system(
        self,
        space_system: SpaceSystem,
        parent_path: XtcePath,
        registry: XtceRegistry,
    ) -> None:
        """Recursively walk the SpaceSystem hierarchy and index all elements."""
        current_path = parent_path / space_system.name
        registry.register(current_path, space_system)

        collections_to_index: list[Iterable[ReferenceableXtceObject] | None] = []

        if space_system.command_metadata:
            cmd = space_system.command_metadata
            collections_to_index.extend(
                [
                    cmd.argument_types,
                    [
                        meta_command
                        for meta_command in cmd.meta_commands
                        if not isinstance(meta_command, MetaCommandRef)
                    ],
                ]
            )

        if space_system.telemetry_metadata:
            tlm = space_system.telemetry_metadata
            collections_to_index.extend(
                [
                    tlm.parameter_types,
                    [
                        parameter
                        for parameter in tlm.parameters
                        if not isinstance(parameter, ParameterRef)
                    ],
                    tlm.containers,
                    tlm.message_set.messages if tlm.message_set else None,
                ]
            )

        # Iterate through all objects and register in one pass
        valid_collections = (c for c in collections_to_index if c)
        for item in itertools.chain.from_iterable(valid_collections):
            registry.register(current_path / item.name, item)

        # Recurse into child SpaceSystems
        for child in space_system.space_systems:
            self._index_space_system(child, current_path, registry)
