"""Test trigger models."""

import pytest
from pydantic import ValidationError

from xtce_lib import (
    ValidationReport,
    XtceDatabase,
    XtcePath,
    XtceSemanticError,
    XtceVersion,
    xtce,
)
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3
from xtce_lib.xtce._pattern import EXPD_NAME_REF_W_PATH, NAME_REF_W_PATH


@pytest.fixture
def db_and_scope() -> tuple[XtceDatabase, XtcePath]:
    """Build a concrete database and scope for semantic trigger checks."""
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


def validate_semantics(
    model: object,
    db_and_scope: tuple[XtceDatabase, XtcePath],
) -> ValidationReport[XtceSemanticError]:
    """Run semantic validation and return the collected report."""
    db, scope = db_and_scope
    report = ValidationReport[XtceSemanticError](title="Semantic Validation")
    model.validate_semantics(report, db.registry, scope)  # type: ignore[attr-defined]
    return report


class TestOnParameterUpdateTrigger:
    """Test OnParameterUpdateTrigger model."""

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
    def test_accepts_valid_parameter_update_trigger_refs(
        self,
        valid_ref: str | XtcePath,
    ) -> None:
        """Valid parameter references should be accepted."""
        trigger = xtce.OnParameterUpdateTrigger(ref=valid_ref)  # type: ignore[arg-type]
        assert trigger.ref is not None

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
    def test_rejects_invalid_parameter_update_trigger_refs(
        self, invalid_ref: str
    ) -> None:
        """Invalid parameter references should be rejected."""
        with pytest.raises(ValidationError):
            xtce.OnParameterUpdateTrigger(ref=invalid_ref)  # type: ignore[arg-type]

    def test_rejects_non_string_reference_values(self) -> None:
        """Reference values must be strings or XtcePath objects."""
        with pytest.raises(ValidationError):
            xtce.OnParameterUpdateTrigger(ref=123)  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_1,
                xtce_1_1.TriggerSetType.OnParameterUpdateTrigger(
                    parameter_ref="/SimpleSat/Bus/Voltage"
                ),
            ),
            (
                XtceVersion.V1_2,
                xtce_1_2.OnParameterUpdateTriggerType(
                    parameter_ref="/SimpleSat/Bus/Voltage"
                ),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.OnParameterUpdateTriggerType(
                    parameter_ref="/SimpleSat/Bus/Voltage"
                ),
            ),
        ],
    )
    def test_from_xsdata_for_each_version(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """Test conversion from xsdata models for each XTCE version."""
        if version == XtceVersion.V1_1:
            trigger = xtce.OnParameterUpdateTrigger._from_v1_1(raw_obj)  # type: ignore[arg-type]
        elif version == XtceVersion.V1_2:
            trigger = xtce.OnParameterUpdateTrigger._from_v1_2(raw_obj)  # type: ignore[arg-type]
        else:
            trigger = xtce.OnParameterUpdateTrigger._from_v1_3(raw_obj)  # type: ignore[arg-type]

        assert str(trigger.ref) == "/SimpleSat/Bus/Voltage"

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_1, xtce_1_1.TriggerSetType.OnParameterUpdateTrigger),
            (XtceVersion.V1_2, xtce_1_2.OnParameterUpdateTriggerType),
            (XtceVersion.V1_3, xtce_1_3.OnParameterUpdateTriggerType),
        ],
    )
    def test_to_xsdata_for_each_version(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """Test conversion to xsdata models for each XTCE version."""
        trigger = xtce.OnParameterUpdateTrigger(ref=XtcePath("/SimpleSat/Bus/Voltage"))

        if version == XtceVersion.V1_1:
            result = trigger._to_v1_1()
        elif version == XtceVersion.V1_2:
            result = trigger._to_v1_2()
        else:
            result = trigger._to_v1_3()

        assert isinstance(result, expected_type)
        assert result.parameter_ref == "/SimpleSat/Bus/Voltage"

    @pytest.mark.parametrize(
        "version",
        [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3],
    )
    def test_round_trip_through_xsdata_preserves_ref(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve the reference."""
        original_ref = "/SimpleSat/Bus/Voltage"
        trigger = xtce.OnParameterUpdateTrigger(ref=XtcePath(original_ref))

        if version == XtceVersion.V1_1:
            xsdata_obj = trigger._to_v1_1()
            restored = xtce.OnParameterUpdateTrigger._from_v1_1(xsdata_obj)
        elif version == XtceVersion.V1_2:
            xsdata_obj = trigger._to_v1_2()
            restored = xtce.OnParameterUpdateTrigger._from_v1_2(xsdata_obj)
        else:
            xsdata_obj = trigger._to_v1_3()
            restored = xtce.OnParameterUpdateTrigger._from_v1_3(xsdata_obj)

        assert str(restored.ref) == original_ref

    def test_json_schema_exposes_pattern_and_examples(self) -> None:
        """Schema should expose regex and examples for API/documentation tooling."""
        schema = xtce.OnParameterUpdateTrigger.model_json_schema()

        assert schema["properties"]["ref"]["pattern"] == EXPD_NAME_REF_W_PATH
        assert schema["properties"]["ref"]["examples"] == [
            "/ConkSat/Bus/BatteryVoltage",
            "../Bus/BatteryVoltage",
            "../Payload/Camera/ExposureTime",
        ]

    def test_validate_semantics_accepts_resolvable_parameter(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
    ) -> None:
        """validate_semantics should pass for a resolvable Parameter target."""
        trigger = xtce.OnParameterUpdateTrigger(ref=XtcePath("/TestSystem/TestParam1"))

        report = validate_semantics(trigger, db_and_scope)

        assert report.is_valid

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
        """validate_semantics should reject array or aggregate references."""
        trigger = xtce.OnParameterUpdateTrigger(ref=XtcePath(bad_ref))

        report = validate_semantics(trigger, db_and_scope)

        assert not report.is_valid

    def test_validate_semantics_rejects_unresolvable_reference(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
    ) -> None:
        """validate_semantics should fail when the reference does not resolve."""
        trigger = xtce.OnParameterUpdateTrigger(
            ref=XtcePath("/TestSystem/DoesNotExist")
        )

        report = validate_semantics(trigger, db_and_scope)

        assert [error.message for error in report.errors] == [
            "reference '/TestSystem/DoesNotExist' does not resolve to a valid object from scope '/TestSystem'",
        ]

    def test_validate_semantics_rejects_non_parameter_target(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
    ) -> None:
        """validate_semantics should fail when the target is not a Parameter."""
        trigger = xtce.OnParameterUpdateTrigger(
            ref=XtcePath("/TestSystem/IntParamType1")
        )

        report = validate_semantics(trigger, db_and_scope)

        assert [error.message for error in report.errors] == [
            "reference '/TestSystem/IntParamType1' resolved to a 'IntegerParameter' type, but a 'Parameter' type was expected",
        ]


class TestOnContainerUpdateTrigger:
    """Test OnContainerUpdateTrigger model."""

    @pytest.mark.parametrize(
        "valid_ref",
        [
            "TestContainer",
            "/SimpleSat/PowerStatus",
            XtcePath("/SimpleSat/PowerStatus"),
            XtcePath("../Thermal/ThermalStatus"),
        ],
    )
    def test_accepts_valid_container_update_trigger_refs(
        self,
        valid_ref: str | XtcePath,
    ) -> None:
        """Valid container references should be accepted."""
        trigger = xtce.OnContainerUpdateTrigger(ref=valid_ref)  # type: ignore[arg-type]
        assert trigger.ref is not None

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
    def test_rejects_invalid_container_update_trigger_refs(
        self, invalid_ref: str
    ) -> None:
        """Invalid container references should be rejected."""
        with pytest.raises(ValidationError):
            xtce.OnContainerUpdateTrigger(ref=invalid_ref)  # type: ignore[arg-type]

    def test_rejects_non_string_reference_values(self) -> None:
        """Reference values must be strings or XtcePath objects."""
        with pytest.raises(ValidationError):
            xtce.OnContainerUpdateTrigger(ref=456)  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_1,
                xtce_1_1.TriggerSetType.OnContainerUpdateTrigger(
                    container_ref="/SimpleSat/PowerStatus"
                ),
            ),
            (
                XtceVersion.V1_2,
                xtce_1_2.OnContainerUpdateTriggerType(
                    container_ref="/SimpleSat/PowerStatus"
                ),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.OnContainerUpdateTriggerType(
                    container_ref="/SimpleSat/PowerStatus"
                ),
            ),
        ],
    )
    def test_from_xsdata_for_each_version(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """Test conversion from xsdata models for each XTCE version."""
        if version == XtceVersion.V1_1:
            trigger = xtce.OnContainerUpdateTrigger._from_v1_1(raw_obj)  # type: ignore[arg-type]
        elif version == XtceVersion.V1_2:
            trigger = xtce.OnContainerUpdateTrigger._from_v1_2(raw_obj)  # type: ignore[arg-type]
        else:
            trigger = xtce.OnContainerUpdateTrigger._from_v1_3(raw_obj)  # type: ignore[arg-type]

        assert str(trigger.ref) == "/SimpleSat/PowerStatus"

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_1, xtce_1_1.TriggerSetType.OnContainerUpdateTrigger),
            (XtceVersion.V1_2, xtce_1_2.OnContainerUpdateTriggerType),
            (XtceVersion.V1_3, xtce_1_3.OnContainerUpdateTriggerType),
        ],
    )
    def test_to_xsdata_for_each_version(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """Test conversion to xsdata models for each XTCE version."""
        trigger = xtce.OnContainerUpdateTrigger(ref=XtcePath("/SimpleSat/PowerStatus"))

        if version == XtceVersion.V1_1:
            result = trigger._to_v1_1()
        elif version == XtceVersion.V1_2:
            result = trigger._to_v1_2()
        else:
            result = trigger._to_v1_3()

        assert isinstance(result, expected_type)
        assert result.container_ref == "/SimpleSat/PowerStatus"

    @pytest.mark.parametrize(
        "version",
        [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3],
    )
    def test_round_trip_through_xsdata_preserves_ref(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve the reference."""
        original_ref = "/SimpleSat/PowerStatus"
        trigger = xtce.OnContainerUpdateTrigger(ref=XtcePath(original_ref))

        if version == XtceVersion.V1_1:
            xsdata_obj = trigger._to_v1_1()
            restored = xtce.OnContainerUpdateTrigger._from_v1_1(xsdata_obj)
        elif version == XtceVersion.V1_2:
            xsdata_obj = trigger._to_v1_2()
            restored = xtce.OnContainerUpdateTrigger._from_v1_2(xsdata_obj)
        else:
            xsdata_obj = trigger._to_v1_3()
            restored = xtce.OnContainerUpdateTrigger._from_v1_3(xsdata_obj)

        assert str(restored.ref) == original_ref

    def test_json_schema_exposes_pattern_and_examples(self) -> None:
        """Schema should expose regex and examples for API/documentation tooling."""
        schema = xtce.OnContainerUpdateTrigger.model_json_schema()

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
        trigger = xtce.OnContainerUpdateTrigger(
            ref=XtcePath("/TestSystem/TestContainer")
        )

        report = validate_semantics(trigger, db_and_scope)

        assert report.is_valid

    def test_rejects_array_or_aggregate_references_at_validation_time(
        self,
    ) -> None:
        """Array or aggregate references are rejected at validation time."""
        with pytest.raises(ValidationError):
            xtce.OnContainerUpdateTrigger(ref=XtcePath("/TestSystem/TestArray[2]"))

        with pytest.raises(ValidationError):
            xtce.OnContainerUpdateTrigger(ref=XtcePath("/TestSystem/Agg.field"))

    def test_validate_semantics_rejects_unresolvable_reference(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
    ) -> None:
        """validate_semantics should fail when the reference does not resolve."""
        trigger = xtce.OnContainerUpdateTrigger(
            ref=XtcePath("/TestSystem/DoesNotExist")
        )

        report = validate_semantics(trigger, db_and_scope)

        assert [error.message for error in report.errors] == [
            "reference '/TestSystem/DoesNotExist' does not resolve to a valid object from scope '/TestSystem'",
        ]

    def test_validate_semantics_rejects_non_container_target(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
    ) -> None:
        """validate_semantics should fail when the target is not a SequenceContainer."""
        trigger = xtce.OnContainerUpdateTrigger(ref=XtcePath("/TestSystem/TestParam1"))

        report = validate_semantics(trigger, db_and_scope)

        assert [error.message for error in report.errors] == [
            "reference '/TestSystem/TestParam1' resolved to a 'Parameter' type, but a 'SequenceContainer' type was expected",
        ]


class TestOnPeriodicRateTrigger:
    """Test OnPeriodicRateTrigger model."""

    @pytest.mark.parametrize(
        "fire_rate",
        [
            0,
            0.5,
            1.0,
            10.0,
            100.0,
        ],
    )
    def test_accepts_valid_fire_rates(self, fire_rate: float) -> None:
        """Valid fire rates should be accepted."""
        trigger = xtce.OnPeriodicRateTrigger(fire_rate_sec=fire_rate)
        assert trigger.fire_rate_sec == fire_rate

    def test_rejects_negative_fire_rate(self) -> None:
        """Negative fire rates should be rejected."""
        with pytest.raises(ValidationError):
            xtce.OnPeriodicRateTrigger(fire_rate_sec=-1.0)

    def test_rejects_non_numeric_fire_rate(self) -> None:
        """Fire rate must be numeric."""
        with pytest.raises(ValidationError):
            xtce.OnPeriodicRateTrigger(fire_rate_sec="fast")  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_1,
                xtce_1_1.TriggerSetType.OnPeriodicRateTrigger(fire_rate_in_seconds=5),  # type: ignore[arg-type]
            ),
            (
                XtceVersion.V1_2,
                xtce_1_2.OnPeriodicRateTriggerType(fire_rate_in_seconds=5.0),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.OnPeriodicRateTriggerType(fire_rate_in_seconds=5.0),
            ),
        ],
    )
    def test_from_xsdata_for_each_version(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """Test conversion from xsdata models for each XTCE version."""
        if version == XtceVersion.V1_1:
            trigger = xtce.OnPeriodicRateTrigger._from_v1_1(raw_obj)  # type: ignore[arg-type]
        elif version == XtceVersion.V1_2:
            trigger = xtce.OnPeriodicRateTrigger._from_v1_2(raw_obj)  # type: ignore[arg-type]
        else:
            trigger = xtce.OnPeriodicRateTrigger._from_v1_3(raw_obj)  # type: ignore[arg-type]

        assert trigger.fire_rate_sec == 5.0

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_1, xtce_1_1.TriggerSetType.OnPeriodicRateTrigger),
            (XtceVersion.V1_2, xtce_1_2.OnPeriodicRateTriggerType),
            (XtceVersion.V1_3, xtce_1_3.OnPeriodicRateTriggerType),
        ],
    )
    def test_to_xsdata_for_each_version(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """Test conversion to xsdata models for each XTCE version."""
        trigger = xtce.OnPeriodicRateTrigger(fire_rate_sec=10.0)

        if version == XtceVersion.V1_1:
            result = trigger._to_v1_1()
        elif version == XtceVersion.V1_2:
            result = trigger._to_v1_2()
        else:
            result = trigger._to_v1_3()

        assert isinstance(result, expected_type)
        assert result.fire_rate_in_seconds == 10.0

    @pytest.mark.parametrize(
        "version",
        [XtceVersion.V1_2, XtceVersion.V1_3],
    )
    def test_round_trip_through_xsdata_preserves_fire_rate(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve the fire rate (v1.2+)."""
        original_rate = 7.5
        trigger = xtce.OnPeriodicRateTrigger(fire_rate_sec=original_rate)

        if version == XtceVersion.V1_2:
            xsdata_obj = trigger._to_v1_2()
            restored = xtce.OnPeriodicRateTrigger._from_v1_2(xsdata_obj)
        else:
            xsdata_obj = trigger._to_v1_3()
            restored = xtce.OnPeriodicRateTrigger._from_v1_3(xsdata_obj)

        assert restored.fire_rate_sec == original_rate

    def test_round_trip_v1_1_truncates_fire_rate_to_int(
        self,
    ) -> None:
        """v1.1 fire rates are truncated to integers during round-trip."""
        original_rate = 7.5
        trigger = xtce.OnPeriodicRateTrigger(fire_rate_sec=original_rate)

        xsdata_obj = trigger._to_v1_1()
        restored = xtce.OnPeriodicRateTrigger._from_v1_1(xsdata_obj)

        # v1.1 truncates to int
        assert restored.fire_rate_sec == 7.0


class TestTriggerSet:
    """Test TriggerSet model."""

    def test_accepts_empty_trigger_list(self) -> None:
        """Empty trigger sets should be accepted."""
        trigger_set = xtce.TriggerSet(triggers=[])
        assert trigger_set.triggers == []

    def test_accepts_single_parameter_update_trigger(self) -> None:
        """A trigger set with a single parameter update trigger should be accepted."""
        trigger = xtce.OnParameterUpdateTrigger(ref="/System/Param")  # type: ignore[arg-type]
        trigger_set = xtce.TriggerSet(triggers=[trigger])
        assert len(trigger_set.triggers) == 1
        assert isinstance(trigger_set.triggers[0], xtce.OnParameterUpdateTrigger)

    def test_accepts_single_container_update_trigger(self) -> None:
        """A trigger set with a single container update trigger should be accepted."""
        trigger = xtce.OnContainerUpdateTrigger(ref="/System/Container")  # type: ignore[arg-type]
        trigger_set = xtce.TriggerSet(triggers=[trigger])
        assert len(trigger_set.triggers) == 1
        assert isinstance(trigger_set.triggers[0], xtce.OnContainerUpdateTrigger)

    def test_accepts_single_periodic_rate_trigger(self) -> None:
        """A trigger set with a single periodic rate trigger should be accepted."""
        trigger = xtce.OnPeriodicRateTrigger(fire_rate_sec=1.0)
        trigger_set = xtce.TriggerSet(triggers=[trigger])
        assert len(trigger_set.triggers) == 1
        assert isinstance(trigger_set.triggers[0], xtce.OnPeriodicRateTrigger)

    def test_accepts_mixed_trigger_types(self) -> None:
        """A trigger set with mixed trigger types should be accepted."""
        triggers = [
            xtce.OnParameterUpdateTrigger(ref="/System/Param"),  # type: ignore[arg-type]
            xtce.OnContainerUpdateTrigger(ref="/System/Container"),  # type: ignore[arg-type]
            xtce.OnPeriodicRateTrigger(fire_rate_sec=2.0),
        ]
        trigger_set = xtce.TriggerSet(triggers=triggers)
        assert len(trigger_set.triggers) == 3

    def test_accepts_optional_name(self) -> None:
        """Trigger sets with or without a name should be accepted."""
        trigger_set_no_name = xtce.TriggerSet(triggers=[])
        assert trigger_set_no_name.name is None

        trigger_set_with_name = xtce.TriggerSet(triggers=[], name="MyTriggerSet")
        assert trigger_set_with_name.name == "MyTriggerSet"

    def test_accepts_trigger_rate(self) -> None:
        """Trigger sets should accept a non-negative trigger rate."""
        trigger_set = xtce.TriggerSet(triggers=[], trigger_rate=5)
        assert trigger_set.trigger_rate == 5

        trigger_set_no_limit = xtce.TriggerSet(triggers=[], trigger_rate=0)
        assert trigger_set_no_limit.trigger_rate == 0

    def test_rejects_negative_trigger_rate(self) -> None:
        """Negative trigger rates should be rejected."""
        with pytest.raises(ValidationError):
            xtce.TriggerSet(triggers=[], trigger_rate=-1)

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_1,
                xtce_1_1.TriggerSetType(
                    choice=[
                        xtce_1_1.TriggerSetType.OnParameterUpdateTrigger(
                            parameter_ref="/System/Param"  # type: ignore[arg-type]
                        ),
                        xtce_1_1.TriggerSetType.OnPeriodicRateTrigger(
                            fire_rate_in_seconds=5  # type: ignore[arg-type]
                        ),
                    ],
                    name="TestSet",
                    trigger_rate=2,
                ),
            ),
            (
                XtceVersion.V1_2,
                xtce_1_2.TriggerSetType(
                    choice=[
                        xtce_1_2.OnParameterUpdateTriggerType(
                            parameter_ref="/System/Param"
                        ),
                        xtce_1_2.OnPeriodicRateTriggerType(fire_rate_in_seconds=5.0),
                    ],
                    name="TestSet",
                    trigger_rate=2,
                ),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.TriggerSetType(
                    choice=[
                        xtce_1_3.OnParameterUpdateTriggerType(
                            parameter_ref="/System/Param"
                        ),
                        xtce_1_3.OnPeriodicRateTriggerType(fire_rate_in_seconds=5.0),
                    ],
                    name="TestSet",
                    trigger_rate=2,
                ),
            ),
        ],
    )
    def test_from_xsdata_for_each_version(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """Test conversion from xsdata models for each XTCE version."""
        if version == XtceVersion.V1_1:
            trigger_set = xtce.TriggerSet._from_v1_1(raw_obj)  # type: ignore[arg-type]
        elif version == XtceVersion.V1_2:
            trigger_set = xtce.TriggerSet._from_v1_2(raw_obj)  # type: ignore[arg-type]
        else:
            trigger_set = xtce.TriggerSet._from_v1_3(raw_obj)  # type: ignore[arg-type]

        assert len(trigger_set.triggers) == 2
        assert trigger_set.name == "TestSet"
        assert trigger_set.trigger_rate == 2
        assert isinstance(trigger_set.triggers[0], xtce.OnParameterUpdateTrigger)
        assert isinstance(trigger_set.triggers[1], xtce.OnPeriodicRateTrigger)

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_1, xtce_1_1.TriggerSetType),
            (XtceVersion.V1_2, xtce_1_2.TriggerSetType),
            (XtceVersion.V1_3, xtce_1_3.TriggerSetType),
        ],
    )
    def test_to_xsdata_for_each_version(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """Test conversion to xsdata models for each XTCE version."""
        triggers = [
            xtce.OnParameterUpdateTrigger(ref="/System/Param"),  # type: ignore[arg-type]
            xtce.OnPeriodicRateTrigger(fire_rate_sec=5.0),
        ]
        trigger_set = xtce.TriggerSet(
            triggers=triggers,  # type: ignore[arg-type]
            name="TestSet",
            trigger_rate=2,
        )

        if version == XtceVersion.V1_1:
            result = trigger_set._to_v1_1()
        elif version == XtceVersion.V1_2:
            result = trigger_set._to_v1_2()
        else:
            result = trigger_set._to_v1_3()

        assert isinstance(result, expected_type)
        assert len(result.choice) == 2
        assert result.name == "TestSet"
        assert result.trigger_rate == 2

    @pytest.mark.parametrize(
        "version",
        [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3],
    )
    def test_round_trip_through_xsdata_preserves_structure(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve the trigger set structure."""
        original_triggers = [
            xtce.OnParameterUpdateTrigger(ref="/System/Param"),  # type: ignore[arg-type]
            xtce.OnPeriodicRateTrigger(fire_rate_sec=7.5),
        ]
        original_set = xtce.TriggerSet(
            triggers=original_triggers,  # type: ignore[arg-type]
            name="TestSet",
            trigger_rate=3,
        )

        if version == XtceVersion.V1_1:
            xsdata_obj = original_set._to_v1_1()
            restored = xtce.TriggerSet._from_v1_1(xsdata_obj)
        elif version == XtceVersion.V1_2:
            xsdata_obj = original_set._to_v1_2()
            restored = xtce.TriggerSet._from_v1_2(xsdata_obj)
        else:
            xsdata_obj = original_set._to_v1_3()
            restored = xtce.TriggerSet._from_v1_3(xsdata_obj)

        assert len(restored.triggers) == 2
        assert restored.name == "TestSet"
        assert restored.trigger_rate == 3
        assert isinstance(restored.triggers[0], xtce.OnParameterUpdateTrigger)
        assert isinstance(restored.triggers[1], xtce.OnPeriodicRateTrigger)

    def test_validate_semantics_accepts_valid_triggers(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
    ) -> None:
        """validate_semantics should pass for valid triggers."""
        trigger_set = xtce.TriggerSet(
            triggers=[
                xtce.OnParameterUpdateTrigger(ref="/TestSystem/TestParam1"),  # type: ignore[arg-type]
                xtce.OnContainerUpdateTrigger(ref="/TestSystem/TestContainer"),  # type: ignore[arg-type]
                xtce.OnPeriodicRateTrigger(fire_rate_sec=1.0),
            ]
        )

        report = validate_semantics(trigger_set, db_and_scope)

        assert report.is_valid

    def test_validate_semantics_collects_errors_from_all_triggers(
        self,
        db_and_scope: tuple[XtceDatabase, XtcePath],
    ) -> None:
        """validate_semantics should collect errors from all triggers in the set."""
        trigger_set = xtce.TriggerSet(
            triggers=[
                xtce.OnParameterUpdateTrigger(ref="/TestSystem/InvalidParam"),  # type: ignore[arg-type]
                xtce.OnContainerUpdateTrigger(ref="/TestSystem/InvalidContainer"),  # type: ignore[arg-type]
            ]
        )

        report = validate_semantics(trigger_set, db_and_scope)

        assert not report.is_valid
        assert len(report.errors) == 2
