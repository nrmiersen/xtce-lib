"""Test reference models."""

import pytest
from pydantic import ValidationError

from xtce_lib import XtceDatabase, XtcePath, XtceVersion, xtce
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3
from xtce_lib.xtce._pattern import EXPD_NAME_REF_W_PATH
from xtce_lib.xtce.reference import ParameterRef


@pytest.fixture
def db_and_scope() -> tuple[XtceDatabase, XtcePath]:
    """Build a concrete database and scope for semantic reference checks."""
    space_system = xtce.SpaceSystem(
        name="TestSystem",
        telemetry_metadata=xtce.TelemetryMetadata(
            parameters=[
                xtce.Parameter(name="TestParam1", parameter_type_ref="IntParamType1"),
                xtce.Parameter(name="TestParam2", parameter_type_ref="IntParamType1"),
            ],
            parameter_types=[
                xtce.IntegerParameter(
                    name="IntParamType1",
                    size_in_bits=32,
                    encoding_type=xtce.IntegerDataEncoding(),
                ),
            ],
        ),
    )

    db = XtceDatabase(root_system=space_system)
    scope = XtcePath("/TestSystem")
    return db, scope


class TestParameterRef:
    """Test ParameterRef model."""

    @pytest.mark.parametrize(
        "valid_ref",
        [
            "SimpleSat",
            "/SimpleSat/Bus/BatteryVoltage",
            XtcePath("/SimpleSat/Bus/BatteryVoltage"),
            XtcePath("../Bus/BatteryVoltage"),
            XtcePath("../Payload/Camera/ExposureTime"),
        ],
    )
    def test_accepts_valid_parameter_references(
        self,
        valid_ref: str | XtcePath,
    ) -> None:
        """Valid parameter reference strings and XtcePath objects should be accepted."""
        model = ParameterRef(ref=valid_ref)  # type: ignore[arg-type]

        assert model.ref == valid_ref

    @pytest.mark.parametrize(
        "invalid_ref",
        [
            ".",
            "..",
            "...",
            "/",
            "\t",
        ],
    )
    def test_rejects_invalid_parameter_references(self, invalid_ref: str) -> None:
        """Malformed parameter references should fail validation."""
        with pytest.raises(ValidationError):
            ParameterRef(ref=XtcePath(invalid_ref))

    def test_rejects_non_string_reference_values(self) -> None:
        """Reference values must be strings or XtcePath objects."""
        with pytest.raises(ValidationError):
            ParameterRef(ref=123)  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_1,
                xtce_1_1.ParameterRefType(parameter_ref="/SimpleSat/Bus/Voltage"),
            ),
            (
                XtceVersion.V1_2,
                xtce_1_2.ParameterRefType(parameter_ref="/SimpleSat/Bus/Voltage"),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.ParameterRefType(parameter_ref="/SimpleSat/Bus/Voltage"),
            ),
        ],
    )
    def test_from_xsdata_for_each_version(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should map versioned ParameterRefType objects to ParameterRef."""
        model = ParameterRef.from_xsdata(raw_obj, version)

        assert isinstance(model, ParameterRef)
        assert model.ref == "/SimpleSat/Bus/Voltage"

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_1, xtce_1_1.ParameterRefType),
            (XtceVersion.V1_2, xtce_1_2.ParameterRefType),
            (XtceVersion.V1_3, xtce_1_3.ParameterRefType),
        ],
    )
    def test_to_xsdata_for_each_version(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the appropriate versioned ParameterRefType."""
        model = ParameterRef(ref=XtcePath("/SimpleSat/Bus/Voltage"))

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert raw_obj.parameter_ref == "/SimpleSat/Bus/Voltage"

    @pytest.mark.parametrize(
        "version",
        [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3],
    )
    def test_round_trip_through_xsdata_preserves_ref(
        self,
        version: XtceVersion,
    ) -> None:
        """Converting to xsdata and back should preserve the reference string."""
        original = ParameterRef(ref=XtcePath("/SimpleSat/Bus/Voltage"))

        round_tripped = ParameterRef.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    def test_json_schema_exposes_pattern_and_examples(self) -> None:
        """Schema should expose regex and examples for API/documentation tooling."""
        schema = ParameterRef.model_json_schema()

        assert schema["properties"]["ref"]["pattern"] == EXPD_NAME_REF_W_PATH
        assert schema["properties"]["ref"]["examples"] == [
            "/SimpleSat/Bus/BatteryVoltage",
            "../Bus/BatteryVoltage",
            "../Payload/Camera/ExposureTime",
        ]

    def test_validate_semantics_accepts_resolvable_parameter(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
    ) -> None:
        """validate_semantics should pass for a resolvable Parameter target."""
        db, scope = db_and_scope
        model = ParameterRef(ref=XtcePath("/TestSystem/TestParam1"))

        assert model.validate_semantics(db.registry, scope) is None

    @pytest.mark.parametrize(
        "bad_ref",
        [
            "/TestSystem/TestArray[2]",
            "/TestSystem/Agg.field",
        ],
    )
    def test_validate_semantics_rejects_array_or_aggregate_references(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
        bad_ref: str,
    ) -> None:
        """validate_semantics should reject array and aggregate references."""
        db, scope = db_and_scope
        model = ParameterRef(ref=XtcePath(bad_ref))

        with pytest.raises(
            ValueError,
            match="contains an array index or aggregate member",
        ):
            model.validate_semantics(db.registry, scope)

    def test_validate_semantics_rejects_unresolvable_reference(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
    ) -> None:
        """validate_semantics should fail when the reference does not resolve."""
        db, scope = db_and_scope
        model = ParameterRef(ref=XtcePath("/TestSystem/DoesNotExist"))

        with pytest.raises(ValueError, match="does not resolve to a valid object"):
            model.validate_semantics(db.registry, scope)

    def test_validate_semantics_rejects_non_parameter_target(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
    ) -> None:
        """validate_semantics should fail when the target is not a Parameter."""
        db, scope = db_and_scope
        model = ParameterRef(ref=XtcePath("/TestSystem/IntParamType1"))

        with pytest.raises(ValueError, match="but a 'Parameter' type was expected"):
            model.validate_semantics(db.registry, scope)
