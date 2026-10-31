"""XTCE file object."""

import importlib
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

from lxml import etree
from xsdata.formats.dataclass.parsers import XmlParser

from xtce_lib.xtce.space_system import SpaceSystem

from .validation import ValidationReport, XtceSchemaError, validate_xml
from .xtce_version import XtceVersion

if TYPE_CHECKING:
    from xtce_lib.generated.xtce_1_1.models import SpaceSystem as SpaceSystem11
    from xtce_lib.generated.xtce_1_2.models import SpaceSystem as SpaceSystem12
    from xtce_lib.generated.xtce_1_3.models import SpaceSystem as SpaceSystem13

    from .xtce_database import XtceDatabase

    AnySpaceSystem = SpaceSystem11 | SpaceSystem12 | SpaceSystem13
else:
    AnySpaceSystem = Any


class XtceFile:
    """XTCE file manager for parsing and validation."""

    # TODO add unified model

    _NAMESPACE_PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"^\{([^}]+)\}")

    def __init__(self, file_path: str | Path) -> None:
        """Initialize the XTCE file object."""
        self._file_path = Path(file_path).resolve()

        self._namespace = self.get_namespace(self._file_path)
        self._version = XtceVersion.from_namespace(self._namespace)
        self._raw_model: AnySpaceSystem | None = None

    @property
    def file_path(self) -> Path:
        """Get the XTCE file path."""
        return self._file_path

    @property
    def namespace(self) -> str:
        """Get the XML namespace of the XTCE file."""
        return self._namespace

    @property
    def version(self) -> str:
        """Get the XTCE version of the file."""
        return self._version.value.version

    @property
    def database(self) -> "XtceDatabase":
        """Get the XTCE database object for this file."""
        if self._raw_model is None:
            self.parse_raw()

        from .xtce_database import XtceDatabase

        return XtceDatabase.from_space_system(
            SpaceSystem.from_xsdata(self._raw_model, self._version)
        )

    @property
    def raw_model(self) -> Any:
        """Get the raw parsed model of the XTCE file."""
        if self._raw_model is None:
            self.parse_raw()
        return self._raw_model

    @staticmethod
    def get_namespace(file_path: str | Path) -> str:
        """Extract the namespace from the file path.

        Args:
            file_path (str | Path): The path to the XTCE XML file.

        Returns:
            str: The namespace of the XTCE XML file.

        Raises:
            ValueError: If the XML file is invalid or if no namespace is found.

        """
        file_path = Path(file_path)
        try:
            for _, element in etree.iterparse(file_path, events=["start"]):
                if isinstance(element.tag, str):
                    match = XtceFile._NAMESPACE_PATTERN.match(element.tag)
                    if match:
                        return match.group(1)

        except etree.XMLSyntaxError as e:
            raise ValueError(f"Invalid XML file: {file_path}: {e}")

        raise ValueError(f"No namespace found in XML file: {file_path}")

    def validate(self) -> ValidationReport[XtceSchemaError]:
        """Validate the XTCE file against its corresponding XSD schema.

        Returns:
            ValidationReport[XtceSchemaError]: The result of the validation.

        Raises:
            ValueError: If the XML file is invalid or if validation fails.

        """
        return validate_xml(self._file_path, self._version)

    def parse_raw(self, strict: bool = False) -> None:
        """Parse the XML file into the version-specific xsdata dataclasses.

        Args:
            strict: If True, validates the file against the schema before parsing.

        Raises:
            ValueError: If validation fails in strict mode or if parsing fails.

        """
        if strict:
            result = self.validate()
            if not result.is_valid:
                raise ValueError(
                    f"Cannot parse invalid XTCE file: {result.errors[0].message}"
                )

        # Import the correct generated module based on the XTCE version
        module_path = f"xtce_lib.generated.{self._version.value.module_name}.models"
        models_module = importlib.import_module(module_path)

        # Parse XML into the SpaceSystem root class
        root_class = getattr(models_module, "SpaceSystem")
        parser = XmlParser()
        self._raw_model = parser.parse(str(self._file_path), root_class)

        # TODO catch exceptions?
