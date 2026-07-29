"""Test common models."""

import pytest
from pydantic import ValidationError

from xtce_lib import XtceVersion, xtce
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3


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

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_1,
                xtce_1_1.DescriptionType(
                    short_description="Battery voltage in volts",
                    long_description="Measured battery voltage.",
                ),
            ),
            (
                XtceVersion.V1_2,
                xtce_1_2.DescriptionType(
                    short_description="Battery voltage in volts",
                    long_description="Measured battery voltage.",
                ),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.DescriptionType(
                    short_description="Battery voltage in volts",
                    long_description="Measured battery voltage.",
                ),
            ),
        ],
    )
    def test_from_xsdata_for_each_version(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should map versioned description objects to DescriptionBase."""
        model = xtce.DescriptionBase.from_xsdata(raw_obj, version)

        assert isinstance(model, xtce.DescriptionBase)
        assert model.short_description == "Battery voltage in volts"
        assert model.long_description == "Measured battery voltage."

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_1, xtce_1_1.DescriptionType),
            (XtceVersion.V1_2, xtce_1_2.DescriptionType),
            (XtceVersion.V1_3, xtce_1_3.DescriptionType),
        ],
    )
    def test_to_xsdata_for_each_version(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the expected versioned description type."""
        model = xtce.DescriptionBase(
            short_description="Battery voltage in volts",
            long_description="Measured battery voltage.",
        )

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert raw_obj.short_description == "Battery voltage in volts"
        assert raw_obj.long_description == "Measured battery voltage."

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
        """Round-trip conversion should preserve description fields."""
        original = xtce.DescriptionBase(
            short_description="Battery voltage in volts",
            long_description="Measured battery voltage.",
        )

        round_tripped = xtce.DescriptionBase.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


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

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (XtceVersion.V1_1, xtce_1_1.NameDescriptionType(name="BatteryVoltage")),
            (XtceVersion.V1_2, xtce_1_2.NameDescriptionType(name="BatteryVoltage")),
            (XtceVersion.V1_3, xtce_1_3.NameDescriptionType(name="BatteryVoltage")),
        ],
    )
    def test_from_xsdata_for_each_version(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should map versioned name-description objects to NameDescriptionBase."""
        model = xtce.NameDescriptionBase.from_xsdata(raw_obj, version)

        assert isinstance(model, xtce.NameDescriptionBase)
        assert model.name == "BatteryVoltage"

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_1, xtce_1_1.NameDescriptionType),
            (XtceVersion.V1_2, xtce_1_2.NameDescriptionType),
            (XtceVersion.V1_3, xtce_1_3.NameDescriptionType),
        ],
    )
    def test_to_xsdata_for_each_version(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the expected versioned name-description type."""
        model = xtce.NameDescriptionBase(name="BatteryVoltage")

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert raw_obj.name == "BatteryVoltage"

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
        """Round-trip conversion should preserve the name field."""
        original = xtce.NameDescriptionBase(name="BatteryVoltage")

        round_tripped = xtce.NameDescriptionBase.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


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

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_1,
                xtce_1_1.OptionalNameDescriptionType(name="SpeedCommandVerifier"),
            ),
            (
                XtceVersion.V1_2,
                xtce_1_2.OptionalNameDescriptionType(name="SpeedCommandVerifier"),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.OptionalNameDescriptionType(name="SpeedCommandVerifier"),
            ),
        ],
    )
    def test_from_xsdata_for_each_version(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should map versioned optional-name objects to OptionalNameDescriptionBase."""
        model = xtce.OptionalNameDescriptionBase.from_xsdata(raw_obj, version)

        assert isinstance(model, xtce.OptionalNameDescriptionBase)
        assert model.name == "SpeedCommandVerifier"

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_1, xtce_1_1.OptionalNameDescriptionType),
            (XtceVersion.V1_2, xtce_1_2.OptionalNameDescriptionType),
            (XtceVersion.V1_3, xtce_1_3.OptionalNameDescriptionType),
        ],
    )
    def test_to_xsdata_for_each_version(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the expected versioned optional-name type."""
        model = xtce.OptionalNameDescriptionBase(name="SpeedCommandVerifier")

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert raw_obj.name == "SpeedCommandVerifier"

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
        """Round-trip conversion should preserve the optional name field."""
        original = xtce.OptionalNameDescriptionBase(name="SpeedCommandVerifier")

        round_tripped = xtce.OptionalNameDescriptionBase.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original
