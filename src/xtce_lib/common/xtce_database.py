"""XTCE database object."""

import itertools
from functools import cached_property
from pathlib import Path
from typing import Iterable

from xtce_lib.common.validation import ValidationReport, XtceSemanticError
from xtce_lib.common.xtce_path import XtcePath
from xtce_lib.common.xtce_registry import XtceRegistry
from xtce_lib.xtce._type_aliases import ReferenceableXtceObject
from xtce_lib.xtce.command import MetaCommandRef
from xtce_lib.xtce.reference import ParameterRef
from xtce_lib.xtce.space_system import SpaceSystem

from .xtce_file import XtceFile


class XtceDatabase:
    """The top level object representing an XTCE database."""

    def __init__(self, root_system: SpaceSystem) -> None:
        """Initialize the XTCE database wrapper around an existing SpaceSystem model."""
        if not isinstance(root_system, SpaceSystem):
            raise TypeError(
                f"root_system must be an instance of SpaceSystem, got {type(root_system).__name__}"
            )

        self.root_system = root_system
        self._registry: XtceRegistry | None = None

    @classmethod
    def create_new(cls, name: str) -> "XtceDatabase":
        """Create a new XTCE database with a root SpaceSystem."""
        root_system = SpaceSystem(name=name)
        return cls(root_system=root_system)

    @property
    def name(self) -> str:
        """Get the name of the root SpaceSystem."""
        return self.root_system.name

    @cached_property
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

    def to_file(self, file_path: str | Path) -> XtceFile:
        """Write this SpaceSystem to an XTCE file."""
        file_path = Path(file_path)
        # TODO maybe use Pydantic validate_call
        # TODO probably want to allow passthru arguments for the file writing (pretty print, encoding, etc.)
        # TODO write to file
        return XtceFile(file_path)

    def _index_space_system(
        self, space_system: SpaceSystem, parent_path: XtcePath, registry: XtceRegistry
    ) -> None:
        """Recursively walk the SpaceSystem hierarchy and index all definitions."""
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
