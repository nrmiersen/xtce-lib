"""Test reference models."""

import pytest
from pydantic import ValidationError

from xtce_lib import XtceDatabase, XtcePath, XtceVersion, xtce
from xtce_lib.exceptions import XtceUnsupportedError
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3
from xtce_lib.xtce._pattern import (
    EXPD_NAME_REF_NO_PATH,
    EXPD_NAME_REF_W_PATH,
    NAME_REF_W_PATH,
)
from xtce_lib.xtce.reference import (
    ArgumentInstanceRef,
    ContainerRef,
    InputParameterInstanceRef,
    OutputParameterRef,
    ParameterInstanceRef,
    ParameterRef,
    ServiceRef,
    StreamRef,
)


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
            containers=[
                xtce.SequenceContainer(name="TestContainer", entries=[]),
            ],
            streams=[
                xtce.FixedFrameStream(
                    name="TestStream",
                    frame_length_in_bits=32,
                    sync_strategy=xtce.FixedFrameSyncStrategy(
                        sync_pattern=xtce.SyncPattern(
                            pattern=b"\xaa",
                            pattern_length_in_bits=8,
                        )
                    ),
                )
            ],
        ),
        services=[
            xtce.Service(
                name="TestService",
                refs=[xtce.ContainerRef(ref=XtcePath("/TestSystem/TestContainer"))],
            )
        ],
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


class TestOutputParameterRef:
    """Test OutputParameterRef model."""

    @pytest.mark.parametrize(
        "valid_ref",
        [
            "SimpleSat",
            "/SimpleSat/Bus/BatteryVoltage",
            XtcePath("/SimpleSat/Bus/BatteryVoltage"),
            XtcePath("../Bus/BatteryVoltage"),
        ],
    )
    def test_accepts_valid_output_parameter_references(
        self,
        valid_ref: str | XtcePath,
    ) -> None:
        """Valid output parameter reference values should be accepted."""
        model = OutputParameterRef(ref=valid_ref)  # type: ignore[arg-type]

        assert model.ref == valid_ref

    @pytest.mark.parametrize("output_name", [None, "BatteryVoltageOut"])
    def test_accepts_optional_output_name(self, output_name: str | None) -> None:
        """output_name should support both omitted and explicit values."""
        model = OutputParameterRef(
            ref=XtcePath("/SimpleSat/Bus/BatteryVoltage"),
            output_name=output_name,
        )

        assert model.output_name == output_name

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
    def test_rejects_invalid_output_parameter_references(
        self,
        invalid_ref: str,
    ) -> None:
        """Malformed output parameter references should fail validation."""
        with pytest.raises(ValidationError):
            OutputParameterRef(ref=XtcePath(invalid_ref))

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_2,
                xtce_1_2.OutputParameterRefType(
                    parameter_ref="/SimpleSat/Bus/Voltage",
                    output_name="OutVoltage",
                ),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.OutputParameterRefType(
                    parameter_ref="/SimpleSat/Bus/Voltage",
                    output_name="OutVoltage",
                ),
            ),
        ],
    )
    def test_from_xsdata_for_supported_versions(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should map supported versions to OutputParameterRef."""
        model = OutputParameterRef.from_xsdata(raw_obj, version)

        assert isinstance(model, OutputParameterRef)
        assert model.ref == "/SimpleSat/Bus/Voltage"
        assert model.output_name == "OutVoltage"

    def test_from_xsdata_rejects_v1_1(self) -> None:
        """v1.1 does not support OutputParameterRef."""
        with pytest.raises(XtceUnsupportedError):
            OutputParameterRef.from_xsdata(
                xtce_1_1.ParameterRefType(parameter_ref="/SimpleSat/Bus/Voltage"),
                XtceVersion.V1_1,
            )

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_2, xtce_1_2.OutputParameterRefType),
            (XtceVersion.V1_3, xtce_1_3.OutputParameterRefType),
        ],
    )
    def test_to_xsdata_for_supported_versions(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the expected supported output reference type."""
        model = OutputParameterRef(
            ref=XtcePath("/SimpleSat/Bus/Voltage"),
            output_name="OutVoltage",
        )

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert raw_obj.parameter_ref == "/SimpleSat/Bus/Voltage"
        assert raw_obj.output_name == "OutVoltage"

    def test_to_xsdata_rejects_v1_1(self) -> None:
        """v1.1 export should fail for OutputParameterRef."""
        model = OutputParameterRef(
            ref=XtcePath("/SimpleSat/Bus/Voltage"),
            output_name="OutVoltage",
        )

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_1)

    @pytest.mark.parametrize("version", [XtceVersion.V1_2, XtceVersion.V1_3])
    def test_round_trip_through_xsdata_preserves_fields(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve ref and output_name."""
        original = OutputParameterRef(
            ref=XtcePath("/SimpleSat/Bus/Voltage"),
            output_name="OutVoltage",
        )

        round_tripped = OutputParameterRef.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    def test_json_schema_exposes_pattern_and_examples(self) -> None:
        """Schema should include pattern and examples inherited from ParameterRef."""
        schema = OutputParameterRef.model_json_schema()

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
        model = OutputParameterRef(ref=XtcePath("/TestSystem/TestParam1"))

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
        model = OutputParameterRef(ref=XtcePath(bad_ref))

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
        model = OutputParameterRef(ref=XtcePath("/TestSystem/DoesNotExist"))

        with pytest.raises(ValueError, match="does not resolve to a valid object"):
            model.validate_semantics(db.registry, scope)

    def test_validate_semantics_rejects_non_parameter_target(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
    ) -> None:
        """validate_semantics should fail when the target is not a Parameter."""
        db, scope = db_and_scope
        model = OutputParameterRef(ref=XtcePath("/TestSystem/IntParamType1"))

        with pytest.raises(ValueError, match="but a 'Parameter' type was expected"):
            model.validate_semantics(db.registry, scope)


class TestParameterInstanceRef:
    """Test ParameterInstanceRef model."""

    def test_accepts_fields(self) -> None:
        """Parameter instance references should accept all explicit fields."""
        model = ParameterInstanceRef(
            ref=XtcePath("/SimpleSat/Bus/BatteryVoltage"),
            instance=-1,
            use_calibrated_value=False,
        )

        assert model.ref == "/SimpleSat/Bus/BatteryVoltage"
        assert model.instance == -1
        assert model.use_calibrated_value is False

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_1,
                xtce_1_1.ParameterInstanceRefType(
                    parameter_ref="/SimpleSat/Bus/Voltage",
                    instance=1,
                    use_calibrated_value=False,
                ),
            ),
            (
                XtceVersion.V1_2,
                xtce_1_2.ParameterInstanceRefType(
                    parameter_ref="/SimpleSat/Bus/Voltage",
                    instance=1,
                    use_calibrated_value=False,
                ),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.ParameterInstanceRefType(
                    parameter_ref="/SimpleSat/Bus/Voltage",
                    instance=1,
                    use_calibrated_value=False,
                ),
            ),
        ],
    )
    def test_from_xsdata_for_each_version(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should map versioned parameter instance references."""
        model = ParameterInstanceRef.from_xsdata(raw_obj, version)

        assert isinstance(model, ParameterInstanceRef)
        assert model.ref == "/SimpleSat/Bus/Voltage"
        assert model.instance == 1
        assert model.use_calibrated_value is False

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_1, xtce_1_1.ParameterInstanceRefType),
            (XtceVersion.V1_2, xtce_1_2.ParameterInstanceRefType),
            (XtceVersion.V1_3, xtce_1_3.ParameterInstanceRefType),
        ],
    )
    def test_to_xsdata_for_each_version(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the expected versioned parameter instance type."""
        model = ParameterInstanceRef(
            ref=XtcePath("/SimpleSat/Bus/Voltage"),
            instance=-2,
            use_calibrated_value=True,
        )

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert raw_obj.parameter_ref == "/SimpleSat/Bus/Voltage"
        assert raw_obj.instance == -2
        assert raw_obj.use_calibrated_value is True

    @pytest.mark.parametrize(
        "version",
        [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3],
    )
    def test_round_trip_through_xsdata_preserves_fields(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve all fields."""
        original = ParameterInstanceRef(
            ref=XtcePath("/SimpleSat/Bus/Voltage"),
            instance=3,
            use_calibrated_value=False,
        )

        round_tripped = ParameterInstanceRef.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    def test_validate_semantics_todo(self) -> None:
        """TODO: add semantic tests when ParameterInstanceRef.validate_semantics is implemented."""


class TestArgumentInstanceRef:
    """Test ArgumentInstanceRef model."""

    @pytest.mark.parametrize(
        "valid_ref",
        [
            "Arg1",
            "CommandArg",
            "payload_arg_12",
        ],
    )
    def test_accepts_valid_argument_references(self, valid_ref: str) -> None:
        """Valid argument names should be accepted."""
        model = ArgumentInstanceRef(ref=valid_ref)

        assert model.ref == valid_ref

    @pytest.mark.parametrize(
        "invalid_ref",
        [
            ".",
            "..",
            "/",
            ":",
            "\t",
        ],
    )
    def test_rejects_invalid_argument_references(self, invalid_ref: str) -> None:
        """Malformed argument names should fail validation."""
        with pytest.raises(ValidationError):
            ArgumentInstanceRef(ref=invalid_ref)

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_2,
                xtce_1_2.ArgumentInstanceRefType(
                    argument_ref="Arg1",
                    use_calibrated_value=False,
                ),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.ArgumentInstanceRefType(
                    argument_ref="Arg1",
                    use_calibrated_value=False,
                ),
            ),
        ],
    )
    def test_from_xsdata_for_supported_versions(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should map supported versions to ArgumentInstanceRef."""
        model = ArgumentInstanceRef.from_xsdata(raw_obj, version)

        assert isinstance(model, ArgumentInstanceRef)
        assert model.ref == "Arg1"
        assert model.use_calibrated_value is False

    def test_from_xsdata_rejects_v1_1(self) -> None:
        """v1.1 does not support ArgumentInstanceRef."""
        with pytest.raises(XtceUnsupportedError):
            ArgumentInstanceRef.from_xsdata(
                xtce_1_2.ArgumentInstanceRefType(
                    argument_ref="Arg1",
                    use_calibrated_value=True,
                ),
                XtceVersion.V1_1,
            )

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_2, xtce_1_2.ArgumentInstanceRefType),
            (XtceVersion.V1_3, xtce_1_3.ArgumentInstanceRefType),
        ],
    )
    def test_to_xsdata_for_supported_versions(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the expected supported argument reference type."""
        model = ArgumentInstanceRef(ref="Arg1", use_calibrated_value=False)

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert raw_obj.argument_ref == "Arg1"
        assert raw_obj.use_calibrated_value is False

    def test_to_xsdata_rejects_v1_1(self) -> None:
        """v1.1 export should fail for ArgumentInstanceRef."""
        model = ArgumentInstanceRef(ref="Arg1", use_calibrated_value=True)

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_1)

    @pytest.mark.parametrize("version", [XtceVersion.V1_2, XtceVersion.V1_3])
    def test_round_trip_through_xsdata_preserves_fields(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve argument instance fields."""
        original = ArgumentInstanceRef(ref="Arg1", use_calibrated_value=False)

        round_tripped = ArgumentInstanceRef.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    def test_json_schema_exposes_pattern(self) -> None:
        """Schema should include the argument-name regex pattern."""
        schema = ArgumentInstanceRef.model_json_schema()

        assert schema["properties"]["ref"]["pattern"] == EXPD_NAME_REF_NO_PATH

    def test_validate_semantics_todo(self) -> None:
        """TODO: add semantic tests when ArgumentInstanceRef.validate_semantics is implemented."""


class TestInputParameterInstanceRef:
    """Test InputParameterInstanceRef model."""

    def test_accepts_fields(self) -> None:
        """Input parameter instance references should accept optional input_name."""
        model = InputParameterInstanceRef(
            ref=XtcePath("/SimpleSat/Bus/BatteryVoltage"),
            input_name="InVoltage",
        )

        assert model.ref == "/SimpleSat/Bus/BatteryVoltage"
        assert model.input_name == "InVoltage"

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_2,
                xtce_1_2.InputParameterInstanceRefType(
                    parameter_ref="/SimpleSat/Bus/Voltage",
                    input_name="InVoltage",
                ),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.InputParameterInstanceRefType(
                    parameter_ref="/SimpleSat/Bus/Voltage",
                    input_name="InVoltage",
                ),
            ),
        ],
    )
    def test_from_xsdata_for_supported_versions(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should map supported versions to InputParameterInstanceRef."""
        model = InputParameterInstanceRef.from_xsdata(raw_obj, version)

        assert isinstance(model, InputParameterInstanceRef)
        assert model.ref == "/SimpleSat/Bus/Voltage"
        assert model.input_name == "InVoltage"

    def test_from_xsdata_rejects_v1_1(self) -> None:
        """v1.1 does not support InputParameterInstanceRef."""
        with pytest.raises(XtceUnsupportedError):
            InputParameterInstanceRef.from_xsdata(
                xtce_1_2.InputParameterInstanceRefType(
                    parameter_ref="/SimpleSat/Bus/Voltage",
                    input_name="InVoltage",
                ),
                XtceVersion.V1_1,
            )

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_2, xtce_1_2.InputParameterInstanceRefType),
            (XtceVersion.V1_3, xtce_1_3.InputParameterInstanceRefType),
        ],
    )
    def test_to_xsdata_for_supported_versions(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the expected supported input reference type."""
        model = InputParameterInstanceRef(
            ref=XtcePath("/SimpleSat/Bus/Voltage"),
            input_name="InVoltage",
        )

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert raw_obj.parameter_ref == "/SimpleSat/Bus/Voltage"
        assert raw_obj.input_name == "InVoltage"

    def test_to_xsdata_rejects_v1_1(self) -> None:
        """v1.1 export should fail for InputParameterInstanceRef."""
        model = InputParameterInstanceRef(
            ref=XtcePath("/SimpleSat/Bus/Voltage"),
            input_name="InVoltage",
        )

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_1)

    @pytest.mark.parametrize("version", [XtceVersion.V1_2, XtceVersion.V1_3])
    def test_round_trip_through_xsdata_preserves_fields(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve ref and input_name."""
        original = InputParameterInstanceRef(
            ref=XtcePath("/SimpleSat/Bus/Voltage"),
            input_name="InVoltage",
        )

        round_tripped = InputParameterInstanceRef.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    def test_validate_semantics_todo(self) -> None:
        """TODO: add semantic tests when InputParameterInstanceRef.validate_semantics is implemented."""


class TestContainerRef:
    """Test ContainerRef model."""

    @pytest.mark.parametrize(
        "valid_ref",
        [
            "ContainerA",
            "/Telemetry/Power/PowerStatus",
            XtcePath("/Telemetry/Power/PowerStatus"),
            XtcePath("../Thermal/ThermalStatus"),
        ],
    )
    def test_accepts_valid_container_references(
        self,
        valid_ref: str | XtcePath,
    ) -> None:
        """Valid container references should be accepted."""
        model = ContainerRef(ref=valid_ref)  # type: ignore[arg-type]

        assert model.ref == valid_ref

    @pytest.mark.parametrize("invalid_ref", [".", "..", "...", "/", "\t"])
    def test_rejects_invalid_container_references(self, invalid_ref: str) -> None:
        """Malformed container references should fail validation."""
        with pytest.raises(ValidationError):
            ContainerRef(ref=XtcePath(invalid_ref))

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_1,
                xtce_1_1.ContainerRefType(container_ref="/SimpleSat/PowerStatus"),
            ),
            (
                XtceVersion.V1_2,
                xtce_1_2.ContainerRefType(container_ref="/SimpleSat/PowerStatus"),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.ContainerRefType(container_ref="/SimpleSat/PowerStatus"),
            ),
        ],
    )
    def test_from_xsdata_for_each_version(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should map versioned ContainerRefType objects."""
        model = ContainerRef.from_xsdata(raw_obj, version)

        assert isinstance(model, ContainerRef)
        assert model.ref == "/SimpleSat/PowerStatus"

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_1, xtce_1_1.ContainerRefType),
            (XtceVersion.V1_2, xtce_1_2.ContainerRefType),
            (XtceVersion.V1_3, xtce_1_3.ContainerRefType),
        ],
    )
    def test_to_xsdata_for_each_version(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the expected versioned ContainerRefType."""
        model = ContainerRef(ref=XtcePath("/SimpleSat/PowerStatus"))

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert raw_obj.container_ref == "/SimpleSat/PowerStatus"

    @pytest.mark.parametrize(
        "version",
        [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3],
    )
    def test_round_trip_through_xsdata_preserves_ref(
        self,
        version: XtceVersion,
    ) -> None:
        """Converting to xsdata and back should preserve the container ref."""
        original = ContainerRef(ref=XtcePath("/SimpleSat/PowerStatus"))

        round_tripped = ContainerRef.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    def test_json_schema_exposes_pattern_and_examples(self) -> None:
        """Schema should expose regex and examples for API/documentation tooling."""
        schema = ContainerRef.model_json_schema()

        assert schema["properties"]["ref"]["pattern"] == NAME_REF_W_PATH
        assert schema["properties"]["ref"]["examples"] == [
            "/Telemetry/Power/PowerStatus",
            "../Thermal/ThermalStatus",
            "Command/ExecutionReport",
        ]

    def test_validate_semantics_accepts_resolvable_container(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
    ) -> None:
        """validate_semantics should pass for a resolvable SequenceContainer target."""
        db, scope = db_and_scope
        model = ContainerRef(ref=XtcePath("/TestSystem/TestContainer"))

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
        """Array and aggregate notation should fail field validation for ContainerRef."""
        _db, _scope = db_and_scope

        with pytest.raises(ValidationError):
            ContainerRef(ref=XtcePath(bad_ref))

    def test_validate_semantics_rejects_unresolvable_reference(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
    ) -> None:
        """validate_semantics should fail when the reference does not resolve."""
        db, scope = db_and_scope
        model = ContainerRef(ref=XtcePath("/TestSystem/DoesNotExist"))

        with pytest.raises(ValueError, match="does not resolve to a valid object"):
            model.validate_semantics(db.registry, scope)

    def test_validate_semantics_rejects_non_container_target(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
    ) -> None:
        """validate_semantics should fail when the target is not a SequenceContainer."""
        db, scope = db_and_scope
        model = ContainerRef(ref=XtcePath("/TestSystem/TestParam1"))

        with pytest.raises(
            ValueError,
            match="but a 'SequenceContainer' type was expected",
        ):
            model.validate_semantics(db.registry, scope)


class TestServiceRef:
    """Test ServiceRef model."""

    @pytest.mark.parametrize(
        "valid_ref",
        [
            "ServiceA",
            "/SimpleSat/PowerService",
            XtcePath("/SimpleSat/PowerService"),
            XtcePath("../ThermalService"),
        ],
    )
    def test_accepts_valid_service_references(
        self,
        valid_ref: str | XtcePath,
    ) -> None:
        """Valid service references should be accepted."""
        model = ServiceRef(ref=valid_ref)  # type: ignore[arg-type]

        assert model.ref == valid_ref

    @pytest.mark.parametrize("invalid_ref", [".", "..", "...", "/", "\t"])
    def test_rejects_invalid_service_references(self, invalid_ref: str) -> None:
        """Malformed service references should fail validation."""
        with pytest.raises(ValidationError):
            ServiceRef(ref=XtcePath(invalid_ref))

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_1,
                xtce_1_1.ServiceRefType(service_ref="/SimpleSat/PowerService"),
            ),
            (
                XtceVersion.V1_2,
                xtce_1_2.ServiceRefType(service_ref="/SimpleSat/PowerService"),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.ServiceRefType(service_ref="/SimpleSat/PowerService"),
            ),
        ],
    )
    def test_from_xsdata_for_each_version(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should map versioned ServiceRefType objects."""
        model = ServiceRef.from_xsdata(raw_obj, version)

        assert isinstance(model, ServiceRef)
        assert model.ref == "/SimpleSat/PowerService"

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_1, xtce_1_1.ServiceRefType),
            (XtceVersion.V1_2, xtce_1_2.ServiceRefType),
            (XtceVersion.V1_3, xtce_1_3.ServiceRefType),
        ],
    )
    def test_to_xsdata_for_each_version(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the expected versioned ServiceRefType."""
        model = ServiceRef(ref=XtcePath("/SimpleSat/PowerService"))

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert raw_obj.service_ref == "/SimpleSat/PowerService"

    @pytest.mark.parametrize(
        "version",
        [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3],
    )
    def test_round_trip_through_xsdata_preserves_ref(
        self,
        version: XtceVersion,
    ) -> None:
        """Converting to xsdata and back should preserve the service ref."""
        original = ServiceRef(ref=XtcePath("/SimpleSat/PowerService"))

        round_tripped = ServiceRef.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    def test_json_schema_exposes_pattern_and_examples(self) -> None:
        """Schema should expose regex and examples for API/documentation tooling."""
        schema = ServiceRef.model_json_schema()

        assert schema["properties"]["ref"]["pattern"] == NAME_REF_W_PATH
        assert schema["properties"]["ref"]["examples"] == [
            "/SimpleSat/PowerService",
            "../ThermalService",
            "CommandService",
        ]

    def test_validate_semantics_accepts_resolvable_service_todo(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
    ) -> None:
        """TODO: add a passing ServiceRef semantic test once service entries are indexed in the registry."""

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
        """Array and aggregate notation should fail field validation for ServiceRef."""
        _db, _scope = db_and_scope

        with pytest.raises(ValidationError):
            ServiceRef(ref=XtcePath(bad_ref))

    def test_validate_semantics_rejects_unresolvable_reference(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
    ) -> None:
        """validate_semantics should fail when the reference does not resolve."""
        db, scope = db_and_scope
        model = ServiceRef(ref=XtcePath("/TestSystem/DoesNotExist"))

        with pytest.raises(ValueError, match="does not resolve to a valid object"):
            model.validate_semantics(db.registry, scope)

    def test_validate_semantics_rejects_non_service_target(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
    ) -> None:
        """validate_semantics should fail when the target is not a Service."""
        db, scope = db_and_scope
        model = ServiceRef(ref=XtcePath("/TestSystem/TestParam1"))

        with pytest.raises(ValueError, match="but a 'Service' type was expected"):
            model.validate_semantics(db.registry, scope)


class TestStreamRef:
    """Test StreamRef model."""

    @pytest.mark.parametrize(
        "valid_ref",
        [
            "StreamA",
            "/SimpleSat/PowerStream",
            XtcePath("/SimpleSat/PowerStream"),
            XtcePath("../ThermalStream"),
        ],
    )
    def test_accepts_valid_stream_references(
        self,
        valid_ref: str | XtcePath,
    ) -> None:
        """Valid stream references should be accepted."""
        model = StreamRef(ref=valid_ref)  # type: ignore[arg-type]

        assert model.ref == valid_ref

    @pytest.mark.parametrize("invalid_ref", [".", "..", "...", "/", "\t"])
    def test_rejects_invalid_stream_references(self, invalid_ref: str) -> None:
        """Malformed stream references should fail validation."""
        with pytest.raises(ValidationError):
            StreamRef(ref=XtcePath(invalid_ref))

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_1,
                xtce_1_1.StreamRefType(stream_ref="/SimpleSat/PowerStream"),
            ),
            (
                XtceVersion.V1_2,
                xtce_1_2.StreamRefType(stream_ref="/SimpleSat/PowerStream"),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.StreamRefType(stream_ref="/SimpleSat/PowerStream"),
            ),
        ],
    )
    def test_from_xsdata_for_each_version(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should map versioned StreamRefType objects."""
        model = StreamRef.from_xsdata(raw_obj, version)

        assert isinstance(model, StreamRef)
        assert model.ref == "/SimpleSat/PowerStream"

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_1, xtce_1_1.StreamRefType),
            (XtceVersion.V1_2, xtce_1_2.StreamRefType),
            (XtceVersion.V1_3, xtce_1_3.StreamRefType),
        ],
    )
    def test_to_xsdata_for_each_version(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the expected versioned StreamRefType."""
        model = StreamRef(ref=XtcePath("/SimpleSat/PowerStream"))

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert raw_obj.stream_ref == "/SimpleSat/PowerStream"

    @pytest.mark.parametrize(
        "version",
        [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3],
    )
    def test_round_trip_through_xsdata_preserves_ref(
        self,
        version: XtceVersion,
    ) -> None:
        """Converting to xsdata and back should preserve the stream ref."""
        original = StreamRef(ref=XtcePath("/SimpleSat/PowerStream"))

        round_tripped = StreamRef.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    def test_json_schema_exposes_pattern_and_examples(self) -> None:
        """Schema should expose regex and examples for API/documentation tooling."""
        schema = StreamRef.model_json_schema()

        assert schema["properties"]["ref"]["pattern"] == NAME_REF_W_PATH
        assert schema["properties"]["ref"]["examples"] == [
            "/SimpleSat/PowerStream",
            "../ThermalStream",
            "CommandStream",
        ]

    def test_validate_semantics_accepts_resolvable_stream_todo(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
    ) -> None:
        """TODO: add a passing StreamRef semantic test once stream entries are indexed in the registry."""

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
        """Array and aggregate notation should fail field validation for StreamRef."""
        _db, _scope = db_and_scope

        with pytest.raises(ValidationError):
            StreamRef(ref=XtcePath(bad_ref))

    def test_validate_semantics_rejects_unresolvable_reference(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
    ) -> None:
        """validate_semantics should fail when the reference does not resolve."""
        db, scope = db_and_scope
        model = StreamRef(ref=XtcePath("/TestSystem/DoesNotExist"))

        with pytest.raises(ValueError, match="does not resolve to a valid object"):
            model.validate_semantics(db.registry, scope)

    def test_validate_semantics_rejects_non_stream_target(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
    ) -> None:
        """validate_semantics should fail when the target is not a stream type."""
        db, scope = db_and_scope
        model = StreamRef(ref=XtcePath("/TestSystem/TestParam1"))

        with pytest.raises(
            ValueError,
            match="but a 'CustomStream', 'FixedFrameStream' or 'VariableFrameStream' type was expected",
        ):
            model.validate_semantics(db.registry, scope)
