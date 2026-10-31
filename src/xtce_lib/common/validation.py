"""Common validation utilities."""

import importlib.resources
import re
import tempfile
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Generic, TypeVar

from lxml import etree

from .xtce_path import XtcePath
from .xtce_version import XtceVersion


class BaseValidationError(ABC):
    """Abstract base class for all validation errors."""

    @abstractmethod
    def format(self) -> str:
        """Return a formatted string representation of the error."""
        pass


@dataclass(frozen=True)
class XtceSchemaError(BaseValidationError):
    """An XTCE schema validation error."""

    line: int
    """The line number in the XML where the schema error occurred."""

    message: str
    """The error message describing the schema issue."""

    def format(self) -> str:
        """Return a formatted string representation of the error."""
        return f"Line {self.line}: {self.message}"


@dataclass(frozen=True)
class XtceSemanticError(BaseValidationError):
    """An XTCE semantic validation error."""

    scope: XtcePath
    """The scope (path) within the XTCE model where the error occurred."""

    message: str
    """The error message describing the semantic issue."""

    source: tuple[str, ...] = ()
    """Model types leading to the model that reported the error, outermost first.

    For example ('SpaceSystem', 'CommandMetadata', 'ParameterRef').

    """

    def format(self) -> str:
        """Return a formatted string representation of the error."""
        source = f" {' > '.join(self.source)}:" if self.source else ""
        return f"[{self.scope}]{source} {self.message}"


ErrorType = TypeVar("ErrorType", bound=BaseValidationError)


@dataclass
class ValidationReport(Generic[ErrorType]):
    """A generic report for XTCE validation."""

    title: str
    errors: list[ErrorType] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """True if the validation pass found no errors."""
        return len(self.errors) == 0

    def add_error(self, error: ErrorType) -> None:
        """Append an error to the report."""
        self.errors.append(error)

    def summary(self) -> str:
        """Generate a console-friendly report."""
        if self.is_valid:
            return f"{self.title}: PASSED"

        lines = [f"{self.title}: FAILED with {len(self.errors)} errors"]
        for err in self.errors:
            lines.append(f"  {err.format()}")

        return "\n".join(lines)


_schema_cache: dict[XtceVersion, etree.XMLSchema] = {}


def get_schema_validator(version: XtceVersion) -> etree.XMLSchema:
    """Get the (cached) compiled XSD schema for an XTCE version."""
    if version in _schema_cache:
        return _schema_cache[version]

    files = importlib.resources.files("xtce_lib.xsd")
    schema_resource = files / version.value.xsd_name
    xml_resource = files / "xml.xsd"

    try:
        # Write the XSDs to a temporary directory so that relative paths like
        # xml.xsd are resolved correctly
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            schema_path = temp_path / schema_resource.name
            schema_path.write_bytes(schema_resource.read_bytes())
            (temp_path / xml_resource.name).write_bytes(xml_resource.read_bytes())

            xmlschema = etree.XMLSchema(etree.parse(schema_path))
    except etree.XMLSchemaParseError as e:
        raise ValueError(f"Failed to compile XSD schema for version {version}: {e}")

    _schema_cache[version] = xmlschema
    return xmlschema


def validate_xml(
    source: Path | bytes, version: XtceVersion
) -> ValidationReport[XtceSchemaError]:
    """Validate an XML file (path) or document (UTF-8 bytes) against the XTCE XSD."""
    validator = get_schema_validator(version)
    report = ValidationReport[XtceSchemaError](title="XSD Validation")

    try:
        if isinstance(source, bytes):
            xml_doc = etree.fromstring(source).getroottree()
        else:
            xml_doc = etree.parse(source)
    except etree.XMLSyntaxError as e:
        # Catastrophic syntax error
        report.add_error(XtceSchemaError(line=e.lineno or 0, message=str(e)))
        return report

    if not validator.validate(xml_doc):
        for error in validator.error_log:
            # Strip the namespace
            clean_message = re.sub(r"\{(?:http|urn)[^}]+\}", "", error.message)
            report.add_error(XtceSchemaError(line=error.line, message=clean_message))

    return report
