"""XTCE database object."""

from pathlib import Path

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

    @classmethod
    def create_new(cls, name: str) -> "XtceDatabase":
        """Create a new XTCE database with a root SpaceSystem."""
        root_system = SpaceSystem(name=name)
        return cls(root_system=root_system)

    @property
    def name(self) -> str:
        """Get the name of the root SpaceSystem."""
        return self.root_system.name

    def validate(self):
        """Perform semantic validation of this SpaceSystem."""
        # TODO define dataclasses for validation return types
        # TODO iteratively validate all sub elements
        pass

    def to_file(self, file_path: str | Path) -> XtceFile:
        """Write this SpaceSystem to an XTCE file."""
        file_path = Path(file_path)
        # TODO maybe use Pydantic validate_call
        # TODO probably want to allow passthru arguments for the file writing (pretty print, encoding, etc.)
        # TODO write to file
        return XtceFile(file_path)
