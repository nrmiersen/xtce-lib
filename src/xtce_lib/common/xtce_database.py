"""XTCE database object."""

import itertools
import logging
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

from .validation import (
    ValidationReport,
    XtceSchemaError,
    XtceSemanticError,
    validate_xml,
)
from .xtce_file import XtceFile
from .xtce_path import XtcePath
from .xtce_registry import XtceRegistry

log = logging.getLogger(__name__)


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
            log.info("No registry found, creating a new one")
            self._build_registry()
        assert self._registry is not None
        return self._registry

    def rebuild_registry(self) -> None:
        """Force a rebuild of the registry."""
        self._build_registry()

    @validate_call
    def validate_schema(
        self,
        xtce_version: XtceVersion,
        *,
        downgrade_policy: DowngradePolicy = DowngradePolicy.STRICT,
        **kwargs: Any,
    ) -> ValidationReport[XtceSchemaError]:
        """Validate this database against the XSD schema."""
        xml = self._render_xml(xtce_version, downgrade_policy, **kwargs)
        return validate_xml(xml.encode("utf-8"), xtce_version)

    def validate_semantics(self) -> ValidationReport[XtceSemanticError]:
        """Perform semantic validation of this database."""
        report = ValidationReport[XtceSemanticError](title="Semantic Validation")
        self.rebuild_registry()  # Ensure registry is up to date before validation
        self.root_system._run_semantic_validation(
            report,
            self.registry,
            XtcePath("/") / self.root_system.name,
        )
        return report

    @validate_call
    def validate(
        self,
        xtce_version: XtceVersion,
        *,
        semantic: bool = True,
        downgrade_policy: DowngradePolicy = DowngradePolicy.STRICT,
        **kwargs: Any,
    ) -> ValidationReport[XtceSchemaError | XtceSemanticError]:
        """Validate this database against the XSD schema and, optionally, semantics."""
        report = ValidationReport[XtceSchemaError | XtceSemanticError](
            title="Validation"
        )

        schema_report = self.validate_schema(
            xtce_version, downgrade_policy=downgrade_policy, **kwargs
        )
        report.errors.extend(schema_report.errors)

        if semantic:
            report.errors.extend(self.validate_semantics().errors)

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
        xml = self._render_xml(xtce_version, downgrade_policy, **kwargs)
        path.write_text(xml, encoding="utf-8")

        return XtceFile(path)

    def to_xsdata(
        self,
        version: XtceVersion,
        policy: DowngradePolicy = DowngradePolicy.STRICT,
    ) -> Any:
        """Convert this model to the xsdata equivalent."""
        return self._root_system.to_xsdata(version=version, policy=policy)

    def _build_registry(self) -> None:
        log.info("Building the registry")
        self._registry = XtceRegistry()
        self._index_space_system(self.root_system, XtcePath("/"), self._registry)
        log.info("Registry build complete")

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

    def _render_xml(
        self,
        xtce_version: XtceVersion,
        downgrade_policy: DowngradePolicy,
        **kwargs: Any,
    ) -> str:
        """Translate and serialize the database to an XML string."""
        space_system = self._root_system.to_xsdata(
            version=xtce_version,
            policy=downgrade_policy,
        )

        config_kwargs: dict[str, Any] = {
            "indent": "    ",
        }
        config_kwargs.update(kwargs)
        serializer = XmlSerializer(config=SerializerConfig(**config_kwargs))

        return serializer.render(  # type: ignore[reportUnknownMemberType]
            space_system,
            ns_map={"xtce": xtce_version.value.namespace},
        )
