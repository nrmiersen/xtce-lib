"""Test common models."""

import pytest
from pydantic import ValidationError

from xtce_lib import XtcePath, XtceVersion, xtce
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3
from xtce_lib.xtce._pattern import (
    EXPD_NAME_REF_NO_PATH,
    EXPD_NAME_REF_W_PATH,
    NAME_REF_NO_PATH,
)


class TestAlias:
    """Test Alias model."""

    def test_accepts_fields(self) -> None:
        """Alias should accept namespace and alias fields."""
        model = xtce.Alias(namespace="Bus", alias="BatteryVoltage")

        assert model.namespace == "Bus"
        assert model.alias == "BatteryVoltage"

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_1,
                xtce_1_1.AliasSetType.Alias(name_space="Bus", alias="BatteryVoltage"),
            ),
            (
                XtceVersion.V1_2,
                xtce_1_2.AliasType(name_space="Bus", alias="BatteryVoltage"),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.AliasType(name_space="Bus", alias="BatteryVoltage"),
            ),
        ],
    )
    def test_from_xsdata_for_each_version(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should map versioned alias objects to Alias."""
        model = xtce.Alias.from_xsdata(raw_obj, version)

        assert isinstance(model, xtce.Alias)
        assert model.namespace == "Bus"
        assert model.alias == "BatteryVoltage"

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_1, xtce_1_1.AliasSetType.Alias),
            (XtceVersion.V1_2, xtce_1_2.AliasType),
            (XtceVersion.V1_3, xtce_1_3.AliasType),
        ],
    )
    def test_to_xsdata_for_each_version(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the expected versioned alias object."""
        model = xtce.Alias(namespace="Bus", alias="BatteryVoltage")

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert raw_obj.name_space == "Bus"
        assert raw_obj.alias == "BatteryVoltage"

    @pytest.mark.parametrize(
        "version",
        [
            XtceVersion.V1_1,
            XtceVersion.V1_2,
            XtceVersion.V1_3,
        ],
    )
    def test_round_trip_through_xsdata_preserves_fields(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve namespace and alias."""
        original = xtce.Alias(namespace="Bus", alias="BatteryVoltage")

        round_tripped = xtce.Alias.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    def test_json_schema_exposes_examples(self) -> None:
        """Schema should expose example values for both fields."""
        schema = xtce.Alias.model_json_schema()

        assert schema["properties"]["namespace"]["examples"] == [
            "Bus",
            "Payload",
            "Ground",
        ]
        assert schema["properties"]["alias"]["examples"] == [
            "BatteryVoltage",
            "BusBatteryVoltage",
            "BattVolt",
        ]


class TestAncillaryData:
    """Test AncillaryData model."""

    def test_accepts_fields(self) -> None:
        """AncillaryData should accept the standard fields."""
        model = xtce.AncillaryData(
            name="ContainerSize",
            value="123 bytes",
            mime_type="text/plain",
            href="http://example.com/data",
        )

        assert model.name == "ContainerSize"
        assert model.value == "123 bytes"
        assert model.mime_type == "text/plain"
        assert model.href == "http://example.com/data"

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_1,
                xtce_1_1.DescriptionType.AncillaryDataSet.AncillaryData(
                    name="ContainerSize",
                    value="123 bytes",
                    mime_type="text/plain",
                    href="http://example.com/data",
                ),
            ),
            (
                XtceVersion.V1_2,
                xtce_1_2.AncillaryDataType(
                    name="ContainerSize",
                    value="123 bytes",
                    mime_type="text/plain",
                    href="http://example.com/data",
                ),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.AncillaryDataType(
                    name="ContainerSize",
                    value="123 bytes",
                    mime_type="text/plain",
                    href="http://example.com/data",
                ),
            ),
        ],
    )
    def test_from_xsdata_for_each_version(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should map versioned ancillary data objects to AncillaryData."""
        model = xtce.AncillaryData.from_xsdata(raw_obj, version)

        assert isinstance(model, xtce.AncillaryData)
        assert model.name == "ContainerSize"
        assert model.value == "123 bytes"
        assert model.mime_type == "text/plain"
        assert model.href == "http://example.com/data"

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_1, xtce_1_1.DescriptionType.AncillaryDataSet.AncillaryData),
            (XtceVersion.V1_2, xtce_1_2.AncillaryDataType),
            (XtceVersion.V1_3, xtce_1_3.AncillaryDataType),
        ],
    )
    def test_to_xsdata_for_each_version(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the expected versioned ancillary data type."""
        model = xtce.AncillaryData(
            name="ContainerSize",
            value="123 bytes",
            mime_type="application/json",
            href="http://example.com/data",
        )

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert raw_obj.name == "ContainerSize"
        assert raw_obj.value == "123 bytes"
        assert raw_obj.mime_type == "application/json"
        assert raw_obj.href == "http://example.com/data"

    @pytest.mark.parametrize(
        "version",
        [
            XtceVersion.V1_1,
            XtceVersion.V1_2,
            XtceVersion.V1_3,
        ],
    )
    def test_round_trip_through_xsdata_preserves_fields(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve all fields."""
        original = xtce.AncillaryData(
            name="ContainerSize",
            value="123 bytes",
            mime_type="application/xml",
            href="http://example.com/data",
        )

        round_tripped = xtce.AncillaryData.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    def test_json_schema_exposes_examples(self) -> None:
        """Schema should expose example values for the ancillary data fields."""
        schema = xtce.AncillaryData.model_json_schema()

        assert schema["properties"]["name"]["examples"] == [
            "ContainerSize",
            "SizeRangeDict",
            "SizeRangeXml",
        ]
        assert schema["properties"]["value"]["examples"] == [
            "123 bytes",
            '{"min_size": 1, "max_size": 10}',
            "<SizeRange><MinSize>1</MinSize><MaxSize>10</MaxSize></SizeRange>",
        ]
        assert schema["properties"]["mime_type"]["examples"] == [
            "text/plain",
            "application/json",
            "application/xml",
        ]


class TestDescriptionBase:
    """Test DescriptionBase model."""

    def test_accepts_description_fields(self) -> None:
        """DescriptionBase should accept descriptions and nested collections."""
        model = xtce.DescriptionBase(
            short_description="Battery voltage in volts",
            long_description="Measured battery voltage.",
            aliases=[xtce.Alias(namespace="Bus", alias="BatteryVoltage")],
            ancillary_data=[
                xtce.AncillaryData(
                    name="ContainerSize",
                    value="123 bytes",
                    mime_type="text/plain",
                )
            ],
        )

        assert model.short_description == "Battery voltage in volts"
        assert model.long_description == "Measured battery voltage."
        assert len(model.aliases) == 1
        assert len(model.ancillary_data) == 1

    def test_rejects_empty_aliases(self) -> None:
        """Aliases must contain at least one entry when provided."""
        with pytest.raises(ValidationError):
            xtce.DescriptionBase(
                aliases=[],
                ancillary_data=[xtce.AncillaryData(name="ContainerSize")],
            )

    def test_rejects_empty_ancillary_data(self) -> None:
        """ancillary_data must contain at least one entry when provided."""
        with pytest.raises(ValidationError):
            xtce.DescriptionBase(
                aliases=[xtce.Alias(namespace="Bus", alias="BatteryVoltage")],
                ancillary_data=[],
            )


class TestNameDescriptionBase:
    """Test NameDescriptionBase model."""

    def test_accepts_valid_name_and_descriptions(self) -> None:
        """NameDescriptionBase should accept a valid name and descriptions."""
        model = xtce.NameDescriptionBase(name="BatteryVoltage")

        assert model.name == "BatteryVoltage"

    @pytest.mark.parametrize(
        "invalid_name",
        [
            ".",
            "..",
            "/",
            "Battery Voltage",
            "Battery:Voltage",
        ],
    )
    def test_rejects_invalid_names(self, invalid_name: str) -> None:
        """Names should match the strict name pattern."""
        with pytest.raises(ValidationError):
            xtce.NameDescriptionBase(name=invalid_name)

    def test_json_schema_exposes_pattern_and_examples(self) -> None:
        """Schema should expose the strict name pattern and examples."""
        schema = xtce.NameDescriptionBase.model_json_schema()

        assert schema["properties"]["name"]["pattern"] == r"^[^./:\[\] ]+$"
        assert schema["properties"]["name"]["examples"] == [
            "BatteryVoltage",
            "setSpeed",
            "uint8",
        ]


class TestOptionalNameDescriptionBase:
    """Test OptionalNameDescriptionBase model."""

    def test_accepts_missing_name(self) -> None:
        """The optional name may be omitted."""
        model = xtce.OptionalNameDescriptionBase()

        assert model.name is None

    @pytest.mark.parametrize(
        "name",
        [
            None,
            "SpeedCommandVerifier",
            "LogMessageSet",
        ],
    )
    def test_accepts_valid_optional_name(self, name: str | None) -> None:
        """OptionalNameDescriptionBase should accept None and valid names."""
        model = xtce.OptionalNameDescriptionBase(name=name)

        assert model.name == name

    @pytest.mark.parametrize(
        "invalid_name",
        [
            ".",
            "..",
            "/",
            "Speed Command Verifier",
            "Speed:Command",
        ],
    )
    def test_rejects_invalid_optional_names(self, invalid_name: str) -> None:
        """Optional names should still follow the strict optional-name pattern."""
        with pytest.raises(ValidationError):
            xtce.OptionalNameDescriptionBase(name=invalid_name)

    def test_json_schema_exposes_pattern_and_examples(self) -> None:
        """Schema should expose the optional-name pattern and examples."""
        schema = xtce.OptionalNameDescriptionBase.model_json_schema()

        assert (
            schema["properties"]["name"]["anyOf"][0]["pattern"] == r"^[^.\[\]:/ \t]+$"
        )
        assert schema["properties"]["name"]["examples"] == [
            "SpeedCommandVerifier",
            "LogMessageSet",
        ]


class TestNameReferenceNoPath:
    """Test NameReferenceNoPath model."""

    @pytest.mark.parametrize(
        "valid_name",
        [
            "Voltage",
            "BatteryVoltage",
            "uint8",
        ],
    )
    def test_accepts_valid_names(self, valid_name: str) -> None:
        """Name references without a path should accept valid names."""
        model = xtce.NameReferenceNoPath(name=valid_name)

        assert model.name == valid_name

    @pytest.mark.parametrize(
        "invalid_name",
        [
            ".",
            "..",
            "/",
        ],
    )
    def test_rejects_invalid_names(self, invalid_name: str) -> None:
        """Name references without a path should reject malformed names."""
        with pytest.raises(ValidationError):
            xtce.NameReferenceNoPath(name=invalid_name)

    def test_json_schema_exposes_pattern_and_examples(self) -> None:
        """Schema should expose the no-path name pattern and examples."""
        schema = xtce.NameReferenceNoPath.model_json_schema()

        assert schema["properties"]["name"]["pattern"] == NAME_REF_NO_PATH
        assert schema["properties"]["name"]["examples"] == ["Voltage"]


class TestExpandedNameReferenceNoPath:
    """Test ExpandedNameReferenceNoPath model."""

    @pytest.mark.parametrize(
        "valid_name",
        [
            "Voltage",
            "Voltage[1]",
            "Battery Voltage",
        ],
    )
    def test_accepts_valid_names(self, valid_name: str) -> None:
        """Expanded name references without a path should accept array and aggregate syntax."""
        model = xtce.ExpandedNameReferenceNoPath(name=valid_name)

        assert model.name == valid_name

    @pytest.mark.parametrize(
        "invalid_name",
        [
            ".",
            "..",
            "/",
        ],
    )
    def test_rejects_invalid_names(self, invalid_name: str) -> None:
        """Expanded name references without a path should reject malformed names."""
        with pytest.raises(ValidationError):
            xtce.ExpandedNameReferenceNoPath(name=invalid_name)

    def test_json_schema_exposes_pattern_and_examples(self) -> None:
        """Schema should expose the expanded no-path pattern and examples."""
        schema = xtce.ExpandedNameReferenceNoPath.model_json_schema()

        assert schema["properties"]["name"]["pattern"] == EXPD_NAME_REF_NO_PATH
        assert schema["properties"]["name"]["examples"] == ["Voltage[12].raw[3]"]


class TestNameReferenceWithPath:
    """Test NameReferenceWithPath model."""

    @pytest.mark.parametrize(
        "valid_name",
        [
            "Voltage",
            "/ConkSat/Bus/BatteryVoltage",
            XtcePath("../Bus/BatteryVoltage"),
            XtcePath("../Payload/Camera/ExposureTime"),
        ],
    )
    def test_accepts_valid_names(self, valid_name: str | XtcePath) -> None:
        """Path-based name references should accept valid path references."""
        model = xtce.NameReferenceWithPath(name=valid_name)  # type: ignore

        assert model.name == valid_name

    @pytest.mark.parametrize(
        "invalid_name",
        [
            ".",
            "..",
            "/",
            "Battery Voltage",
        ],
    )
    def test_rejects_invalid_names(self, invalid_name: str) -> None:
        """Path-based name references should reject malformed references."""
        with pytest.raises(ValidationError):
            xtce.NameReferenceWithPath(name=XtcePath(invalid_name))

    def test_json_schema_exposes_pattern_and_examples(self) -> None:
        """Schema should expose the path-based name pattern and examples."""
        schema = xtce.NameReferenceWithPath.model_json_schema()

        assert schema["properties"]["name"]["pattern"] == EXPD_NAME_REF_W_PATH
        assert schema["properties"]["name"]["examples"] == [
            "/ConkSat/Bus/BatteryVoltage",
            "../Bus/BatteryVoltage",
            "../Payload/Camera/ExposureTime",
        ]


class TestExpandedNameReferenceWithPath:
    """Test ExpandedNameReferenceWithPath model."""

    @pytest.mark.parametrize(
        "valid_name",
        [
            "Voltage",
            "/ConkSat/Bus/Battery[2].voltage",
            XtcePath("ConkSat/Bus/BatteryVoltage[3]"),
            XtcePath("../Bus/BatteryVoltage[3].raw"),
        ],
    )
    def test_accepts_valid_names(self, valid_name: str | XtcePath) -> None:
        """Expanded path-based name references should accept array and aggregate syntax."""
        model = xtce.ExpandedNameReferenceWithPath(name=valid_name)  # type: ignore

        assert model.name == valid_name

    @pytest.mark.parametrize(
        "invalid_name",
        [
            ".",
            "..",
            "/",
            "Battery Voltage",
        ],
    )
    def test_rejects_invalid_names(self, invalid_name: str) -> None:
        """Expanded path-based name references should reject malformed references."""
        with pytest.raises(ValidationError):
            xtce.ExpandedNameReferenceWithPath(name=XtcePath(invalid_name))

    def test_json_schema_exposes_pattern_and_examples(self) -> None:
        """Schema should expose the expanded path-based name pattern and examples."""
        schema = xtce.ExpandedNameReferenceWithPath.model_json_schema()

        assert schema["properties"]["name"]["pattern"] == EXPD_NAME_REF_W_PATH
        assert schema["properties"]["name"]["examples"] == [
            "ConkSat/Bus/Battery.voltage",
            "ConkSat/Bus/Battery[2].voltage",
            "ConkSat/Bus/BatteryVoltage[3]",
        ]
