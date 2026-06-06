"""XTCE file object."""

import importlib.resources
import re
import tempfile
from dataclasses import dataclass
from importlib.abc import Traversable
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

from lxml import etree
from xsdata.formats.dataclass.parsers import XmlParser

from .xtce_version import XtceVersion

if TYPE_CHECKING:
    from xtce_lib.generated.xtce_1_1.models import SpaceSystem as SpaceSystem11
    from xtce_lib.generated.xtce_1_2.models import SpaceSystem as SpaceSystem12
    from xtce_lib.generated.xtce_1_3.models import SpaceSystem as SpaceSystem13

    AnySpaceSystem = SpaceSystem11 | SpaceSystem12 | SpaceSystem13
else:
    AnySpaceSystem = Any


@dataclass
class XtceValidationError:
    """Represents a single XTCE schema validation error."""

    line: int
    message: str


@dataclass
class ValidationResult:
    """The result of an XTCE file validation."""

    is_valid: bool
    errors: list[XtceValidationError]


class XtceFile:
    """XTCE file manager for parsing and validation."""

    # TODO add unified model

    # Cache at class level
    _schema_cache: ClassVar[dict[XtceVersion, etree.XMLSchema]] = {}
    _NAMESPACE_PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"^\{([^}]+)\}")

    def __init__(self, file_path: str | Path) -> None:
        """Initialize the XTCE file object."""
        self._file_path = Path(file_path)

        self._namespace = self.get_namespace(self._file_path)
        self._version = XtceVersion.from_namespace(self._namespace)
        self._raw_model: AnySpaceSystem | None = None

        self._schema_resource, self._xml_resource = self._get_xsd_resources()

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

    def validate(self) -> ValidationResult:
        """Validate the XTCE file against its corresponding XSD schema.

        Returns:
            ValidationResult: The result of the validation.

        Raises:
            ValueError: If the XML file is invalid or if validation fails.

        """
        validator = self._get_validator()

        try:
            xml_doc = etree.parse(self._file_path)
            is_valid = validator.validate(xml_doc)

            if is_valid:
                return ValidationResult(is_valid=True, errors=[])

            errors: list[XtceValidationError] = []
            for error in validator.error_log:
                # Strip the namespace
                clean_message = re.sub(r"\{(?:http|urn)[^}]+\}", "", error.message)

                errors.append(
                    XtceValidationError(line=error.line, message=clean_message)
                )

            return ValidationResult(is_valid=False, errors=errors)

        except etree.XMLSyntaxError as e:
            # Catastrophic syntax error
            syntax_error = XtceValidationError(line=e.lineno or 0, message=str(e))
            return ValidationResult(is_valid=False, errors=[syntax_error])

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

    def _get_validator(self) -> etree.XMLSchema:
        """Get the XMLSchema validator for the XTCE version of this file."""
        if self._version in self._schema_cache:
            return self._schema_cache[self._version]

        try:
            # Write the XSD resources to a temporary directory so that relative paths
            # like xml.xsd are resolved correctly
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)

                schema_path = temp_path / self._schema_resource.name
                xml_xsd_path = temp_path / self._xml_resource.name

                schema_path.write_bytes(self._schema_resource.read_bytes())
                xml_xsd_path.write_bytes(self._xml_resource.read_bytes())

                schema_doc = etree.parse(schema_path)
                xmlschema = etree.XMLSchema(schema_doc)

                self.__class__._schema_cache[self._version] = xmlschema
                return xmlschema

        except etree.XMLSchemaParseError as e:
            raise ValueError(
                f"Failed to compile XSD schema for version {self._version}: {e}"
            )

    def _get_xsd_resources(self) -> tuple[Traversable, Traversable]:
        """Get schema resources for the XTCE version of this file."""
        files = importlib.resources.files("xtce_lib.xsd")
        schema_file = files / self._version.value.xsd_name
        xsd_file = files / "xml.xsd"

        return schema_file, xsd_file
