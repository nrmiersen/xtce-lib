"""Test common models."""

import pytest
from pydantic import ValidationError

from xtce_lib.common.xtce_path import XTCE_NAME_REFERENCE_WITH_PATH_PATTERN, XtcePath
from xtce_lib.models.common import (
    EXPANDED_NAME_REFERENCE_NO_PATH_PATTERN,
    EXPANDED_NAME_REFERENCE_WITH_PATH_PATTERN,
    ExpandedNameReferenceNoPath,
    ExpandedNameReferenceWithPath,
    NameReferenceNoPath,
    NameReferenceWithPath,
)


class TestNameReferenceWithPath:
    """Test NameReferenceWithPath model."""

    def test_accepts_string_and_stores_xtce_path(self) -> None:
        """String inputs should be coerced and stored as XtcePath."""
        model = NameReferenceWithPath(name="SimpleSat/Bus/EPDS/BatteryOne/Voltage")  # type: ignore

        assert isinstance(model.name, XtcePath)
        assert model.name == XtcePath("SimpleSat/Bus/EPDS/BatteryOne/Voltage")

    def test_accepts_xtce_path_input(self) -> None:
        """XtcePath inputs should validate and be preserved."""
        model = NameReferenceWithPath(
            name=XtcePath("SimpleSat/Bus/EPDS/BatteryOne/Voltage")
        )

        assert isinstance(model.name, XtcePath)
        assert model.name == XtcePath("SimpleSat/Bus/EPDS/BatteryOne/Voltage")

    def test_accepts_absolute_and_relative_qualified_references(self) -> None:
        """Both absolute and relative qualified paths should validate."""
        absolute_model = NameReferenceWithPath(name="/SimpleSat/Bus/Voltage")  # type: ignore
        relative_model = NameReferenceWithPath(name="../Bus/Voltage")  # type: ignore

        assert str(absolute_model.name) == "/SimpleSat/Bus/Voltage"
        assert str(relative_model.name) == "../Bus/Voltage"

    @pytest.mark.parametrize(
        "invalid_name",
        [
            ".",
            "..",
            "SimpleSat:Bus/Voltage",
            "SimpleSat/Bus[0]/Voltage",
            "SimpleSat/Bus.Value",
            "SimpleSat/Bus/Voltage Name",
            "SimpleSat/Bus/\tVoltage",
        ],
    )
    def test_rejects_invalid_xtce_name_reference_paths(self, invalid_name: str) -> None:
        """Reserved characters and invalid terminal segments should fail."""
        with pytest.raises(ValidationError, match="valid XTCE name reference path"):
            NameReferenceWithPath(name=invalid_name)  # type: ignore

    def test_rejects_unsupported_input_types(self) -> None:
        """Inputs that are neither strings nor XtcePath should fail."""
        with pytest.raises(
            ValidationError, match="XtcePath must be a string or XtcePath"
        ):
            NameReferenceWithPath(name=123)  # type: ignore

    def test_serializes_name_as_normalized_string(self) -> None:
        """Model dumps should serialize custom path values as strings."""
        model = NameReferenceWithPath(name=XtcePath("//SimpleSat///Bus/Voltage"))

        assert model.model_dump() == {"name": "/SimpleSat/Bus/Voltage"}

    def test_json_schema_exposes_pattern_for_name_field(self) -> None:
        """Schema should include regex metadata for name field validation."""
        schema = NameReferenceWithPath.model_json_schema()

        assert (
            schema["properties"]["name"]["pattern"]
            == XTCE_NAME_REFERENCE_WITH_PATH_PATTERN
        )


class TestNameReferenceNoPath:
    """Test NameReferenceNoPath model."""

    def test_accepts_simple_name(self) -> None:
        """Plain no-path references should validate."""
        model = NameReferenceNoPath(name="Voltage")

        assert model.name == "Voltage"

    @pytest.mark.parametrize(
        "invalid_name",
        ["Bus/Voltage", "Voltage[0]", "Bus.Voltage", "Voltage Name", "."],
    )
    def test_rejects_path_or_expansion_syntax(self, invalid_name: str) -> None:
        """No-path references should reject path, array, and aggregate syntax."""
        with pytest.raises(ValidationError, match="valid XTCE name reference"):
            NameReferenceNoPath(name=invalid_name)


class TestExpandedNameReferenceNoPath:
    """Test ExpandedNameReferenceNoPath model."""

    @pytest.mark.parametrize(
        "valid_name",
        [
            "Voltage",
            "Voltage[0]",
            "Voltage[12].raw",
            "Voltage[12].raw[3].leaf",
        ],
    )
    def test_accepts_array_and_aggregate_syntax(self, valid_name: str) -> None:
        """Expanded no-path references should allow array and aggregate access."""
        model = ExpandedNameReferenceNoPath(name=valid_name)

        assert model.name == valid_name

    @pytest.mark.parametrize(
        "invalid_name",
        ["Bus/Voltage", ".", "..", "Voltage[]", "Voltage.[0]", "Voltage Name"],
    )
    def test_rejects_invalid_expanded_name_syntax(self, invalid_name: str) -> None:
        """Expanded no-path references should still reject paths and malformed syntax."""
        with pytest.raises(ValidationError, match="valid XTCE name reference"):
            ExpandedNameReferenceNoPath(name=invalid_name)

    def test_json_schema_exposes_expanded_pattern(self) -> None:
        """Schema should expose the expanded no-path regex pattern."""
        schema = ExpandedNameReferenceNoPath.model_json_schema()

        assert (
            schema["properties"]["name"]["pattern"]
            == EXPANDED_NAME_REFERENCE_NO_PATH_PATTERN
        )


class TestExpandedNameReferenceWithPath:
    """Test ExpandedNameReferenceWithPath model."""

    @pytest.mark.parametrize(
        "valid_name",
        [
            "Voltage",
            "/SimpleSat/Bus/Voltage[0]",
            "../Bus/Voltage.raw",
            "SimpleSat/Bus/Voltage[12].raw[3].leaf",
        ],
    )
    def test_accepts_path_array_and_aggregate_syntax(self, valid_name: str) -> None:
        """Expanded path references should allow qualified paths with expansions."""
        model = ExpandedNameReferenceWithPath(name=valid_name)

        assert model.name == valid_name

    @pytest.mark.parametrize(
        "invalid_name",
        [
            ".",
            "..",
            "SimpleSat/Bus/Voltage/",
            "SimpleSat/Bus[0]/Voltage",
            "SimpleSat:Bus/Voltage",
            "SimpleSat/Bus/Voltage[]",
            "SimpleSat/Bus/Voltage.[0]",
            "SimpleSat/Bus/Voltage Name",
        ],
    )
    def test_rejects_invalid_path_or_expansion_syntax(self, invalid_name: str) -> None:
        """Expanded path references should reject malformed path and expansion syntax."""
        with pytest.raises(ValidationError, match="valid XTCE name reference path"):
            ExpandedNameReferenceWithPath(name=invalid_name)

    def test_json_schema_exposes_expanded_with_path_pattern(self) -> None:
        """Schema should expose the expanded with-path regex pattern."""
        schema = ExpandedNameReferenceWithPath.model_json_schema()

        assert (
            schema["properties"]["name"]["pattern"]
            == EXPANDED_NAME_REFERENCE_WITH_PATH_PATTERN
        )
