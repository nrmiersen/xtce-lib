"""Test parameter models."""

from __future__ import annotations

import datetime

import pytest
from pydantic import ValidationError

from xtce_lib import (
    DowngradePolicy,
    XtceDowngradeError,
    XtcePath,
    XtceVersion,
    xtce,
)

ALL_VERSIONS = [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3]
MODERN_VERSIONS = [XtceVersion.V1_2, XtceVersion.V1_3]


def _make_integer_encoding() -> xtce.IntegerDataEncoding:
    """Build a reusable integer data encoding."""
    return xtce.IntegerDataEncoding(size_in_bits=16, byte_order=[1, 0])


def _make_time_encoding() -> xtce.TimeEncoding:
    """Build a reusable time encoding."""
    return xtce.TimeEncoding(encoding_type=_make_integer_encoding())


def _make_comparison(value: object = 1) -> xtce.Comparison:
    """Build a reusable comparison for match criteria."""
    return xtce.Comparison(
        ref=XtcePath("/TestSystem/ParameterA"),
        instance=1,
        use_calibrated_value=True,
        comparison_operator=xtce.ComparisonOperator.GT,
        value=value,  # type: ignore[arg-type]
    )


def _make_match_criteria() -> xtce.MatchCriteria:
    """Build a reusable match criteria."""
    return xtce.MatchCriteria(criteria=_make_comparison())


def _make_alarm_conditions() -> xtce.AlarmConditions:
    """Build reusable AlarmConditions."""
    return xtce.AlarmConditions(watch_alarm=_make_match_criteria())


def _make_context_match() -> xtce.ContextMatch:
    """Build a reusable context match."""
    return xtce.ContextMatch(criteria=_make_comparison())


def _make_numeric_alarm() -> xtce.NumericAlarm:
    """Build a reusable numeric alarm."""
    return xtce.NumericAlarm(
        alarm=_make_alarm_conditions(),
        min_violations=2,
    )


def _make_numeric_context_alarm() -> xtce.NumericContextAlarm:
    """Build a reusable numeric context alarm."""
    return xtce.NumericContextAlarm(
        context_match=_make_context_match(),
        alarm=_make_alarm_conditions(),
        min_violations=3,
    )


class TestIntegerParameter:
    """Test IntegerParameter model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal IntegerParameter."""
        original = xtce.IntegerParameter(name="MyInt", encoding_type=None)

        round_tripped = xtce.IntegerParameter.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_alarms(self, version: XtceVersion) -> None:
        """Round-trip IntegerParameter with default and context alarms."""
        original = xtce.IntegerParameter(
            name="MyInt",
            encoding_type=_make_integer_encoding(),
            default_alarm=_make_numeric_alarm(),
            context_alarms=[_make_numeric_context_alarm()],
        )

        round_tripped = xtce.IntegerParameter.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestFloatParameter:
    """Test FloatParameter model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal FloatParameter."""
        original = xtce.FloatParameter(name="MyFloat", encoding_type=None)

        round_tripped = xtce.FloatParameter.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_alarms(self, version: XtceVersion) -> None:
        """Round-trip FloatParameter with default and context alarms."""
        original = xtce.FloatParameter(
            name="MyFloat",
            encoding_type=None,
            default_alarm=_make_numeric_alarm(),
            context_alarms=[_make_numeric_context_alarm()],
        )

        round_tripped = xtce.FloatParameter.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestStringParameter:
    """Test StringParameter model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal StringParameter."""
        original = xtce.StringParameter(name="MyStr", encoding_type=None)

        round_tripped = xtce.StringParameter.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_alarms(self, version: XtceVersion) -> None:
        """Round-trip StringParameter with default and context alarms."""
        string_alarm = xtce.StringAlarm(
            alarm=_make_alarm_conditions(),
            alarms=[
                xtce.StringAlarmLevel(
                    match_pattern="ERROR",
                    level=xtce.ConcernLevel.CRITICAL,
                )
            ],
            default_level=xtce.ConcernLevel.NORMAL,
        )
        context_alarm = xtce.StringContextAlarm(
            context_match=_make_context_match(),
            alarm=_make_alarm_conditions(),
            alarms=[
                xtce.StringAlarmLevel(
                    match_pattern="WARN",
                    level=xtce.ConcernLevel.WARNING,
                )
            ],
            default_level=xtce.ConcernLevel.NORMAL,
        )
        original = xtce.StringParameter(
            name="MyStr",
            encoding_type=None,
            default_alarm=string_alarm,
            context_alarms=[context_alarm],
        )

        round_tripped = xtce.StringParameter.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestBinaryParameter:
    """Test BinaryParameter model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal BinaryParameter."""
        original = xtce.BinaryParameter(name="MyBin", encoding_type=None)

        round_tripped = xtce.BinaryParameter.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_alarms(self, version: XtceVersion) -> None:
        """Round-trip BinaryParameter with default and context alarms."""
        binary_alarm = xtce.BinaryAlarm(alarm=_make_alarm_conditions())
        context_alarm = xtce.BinaryContextAlarm(
            context_match=_make_context_match(),
            alarm=_make_alarm_conditions(),
        )
        original = xtce.BinaryParameter(
            name="MyBin",
            encoding_type=None,
            default_alarm=binary_alarm,
            context_alarms=[context_alarm],
        )

        round_tripped = xtce.BinaryParameter.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestBooleanParameter:
    """Test BooleanParameter model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal BooleanParameter."""
        original = xtce.BooleanParameter(name="MyBool", encoding_type=None)

        round_tripped = xtce.BooleanParameter.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_alarms(self, version: XtceVersion) -> None:
        """Round-trip BooleanParameter with default and context alarms."""
        boolean_alarm = xtce.BooleanAlarm(alarm=_make_alarm_conditions())
        context_alarm = xtce.BooleanContextAlarm(
            context_match=_make_context_match(),
            alarm=_make_alarm_conditions(),
        )
        original = xtce.BooleanParameter(
            name="MyBool",
            encoding_type=None,
            default_alarm=boolean_alarm,
            context_alarms=[context_alarm],
        )

        round_tripped = xtce.BooleanParameter.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestEnumeratedParameter:
    """Test EnumeratedParameter model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal EnumeratedParameter."""
        original = xtce.EnumeratedParameter(
            name="MyEnum",
            encoding_type=None,
            enumerations=[
                xtce.ValueEnumeration(value=0, label="OFF"),
                xtce.ValueEnumeration(value=1, label="ON"),
            ],
        )

        round_tripped = xtce.EnumeratedParameter.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_alarms(self, version: XtceVersion) -> None:
        """Round-trip EnumeratedParameter with default and single context alarm."""
        original = xtce.EnumeratedParameter(
            name="MyEnum",
            encoding_type=None,
            enumerations=[
                xtce.ValueEnumeration(value=0, label="OFF"),
                xtce.ValueEnumeration(value=1, label="ON"),
            ],
            default_alarm=xtce.EnumerationAlarm(
                alarm=_make_alarm_conditions(),
                alarms=[
                    xtce.EnumerationAlarmLevel(
                        enumeration_label="OFF",
                        level=xtce.ConcernLevel.WARNING,
                    )
                ],
                default_alarm_level=xtce.ConcernLevel.NORMAL,
            ),
            context_alarms=[
                xtce.EnumerationContextAlarm(
                    context_match=_make_context_match(),
                    alarm=_make_alarm_conditions(),
                    alarms=[
                        xtce.EnumerationAlarmLevel(
                            enumeration_label="OFF",
                            level=xtce.ConcernLevel.CRITICAL,
                        )
                    ],
                    default_alarm_level=xtce.ConcernLevel.NORMAL,
                )
            ],
        )

        round_tripped = xtce.EnumeratedParameter.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_v1_1_downgrade_policy_multiple_context_alarms(self) -> None:
        """Test v1.1 downgrade policy behavior when multiple context alarms are present."""
        context_alarm = xtce.EnumerationContextAlarm(
            context_match=_make_context_match(),
            alarm=_make_alarm_conditions(),
        )
        original = xtce.EnumeratedParameter(
            name="MyEnum",
            encoding_type=None,
            enumerations=[xtce.ValueEnumeration(value=0, label="OFF")],
            context_alarms=[context_alarm, context_alarm],
        )

        with pytest.raises(XtceDowngradeError):
            original.to_xsdata(XtceVersion.V1_1, policy=DowngradePolicy.STRICT)

        exported = original.to_xsdata(XtceVersion.V1_1, policy=DowngradePolicy.IGNORE)
        assert exported.context_alarm_list is not None


class TestArrayParameter:
    """Test ArrayParameter model."""

    @pytest.mark.parametrize("version", MODERN_VERSIONS)
    def test_round_trip_modern(self, version: XtceVersion) -> None:
        """Round-trip ArrayParameter with dimensions in v1.2/v1.3."""
        original = xtce.ArrayParameter(
            name="MyArray",
            array_type_ref=XtcePath("ElementType"),
            dimensions=[
                xtce.Dimension(start_index=0, end_index=10),
                xtce.Dimension(start_index=0, end_index=5),
            ],
        )

        round_tripped = xtce.ArrayParameter.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_round_trip_v1_1(self) -> None:
        """Test ArrayParameter dimension count preservation in v1.1."""
        original = xtce.ArrayParameter(
            name="MyArray",
            array_type_ref=XtcePath("ElementType"),
            dimensions=[
                xtce.Dimension(start_index=0, end_index=10),
                xtce.Dimension(start_index=0, end_index=5),
            ],
        )

        raw = original.to_xsdata(XtceVersion.V1_1)
        assert raw.number_of_dimensions == 2

        imported = xtce.ArrayParameter.from_xsdata(raw, XtceVersion.V1_1)
        assert len(imported.dimensions) == 2


class TestAggregateParameter:
    """Test AggregateParameter model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip AggregateParameter with members."""
        original = xtce.AggregateParameter(
            name="MyAggregate",
            members=[
                xtce.Member(name="MemberA", type_ref=XtcePath("TypeA")),
                xtce.Member(name="MemberB", type_ref=XtcePath("TypeB")),
            ],
        )

        round_tripped = xtce.AggregateParameter.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestRelativeTimeParameter:
    """Test RelativeTimeParameter model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal RelativeTimeParameter."""
        original = xtce.RelativeTimeParameter(
            name="MyRelTime",
            encoding=_make_time_encoding(),
            reference_time=xtce.ReferenceTime(epoch=xtce.EpochTime.TAI),
        )

        round_tripped = xtce.RelativeTimeParameter.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_alarms(self, version: XtceVersion) -> None:
        """Round-trip RelativeTimeParameter with default and context alarms."""
        original = xtce.RelativeTimeParameter(
            name="MyRelTime",
            encoding=_make_time_encoding(),
            reference_time=xtce.ReferenceTime(epoch=xtce.EpochTime.TAI),
            default_alarm=xtce.TimeAlarm(
                alarm=_make_alarm_conditions(),
            ),
            context_alarms=[
                xtce.TimeContextAlarm(
                    context_match=_make_context_match(),
                    alarm=_make_alarm_conditions(),
                )
            ],
        )

        round_tripped = xtce.RelativeTimeParameter.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestAbsoluteTimeParameter:
    """Test AbsoluteTimeParameter model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip AbsoluteTimeParameter."""
        original = xtce.AbsoluteTimeParameter(
            name="MyAbsTime",
            encoding=_make_time_encoding(),
            reference_time=xtce.ReferenceTime(epoch=xtce.EpochTime.TAI),
        )

        round_tripped = xtce.AbsoluteTimeParameter.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestPhysicalAddress:
    """Test PhysicalAddress model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip empty/minimal PhysicalAddress."""
        original = xtce.PhysicalAddress()

        round_tripped = xtce.PhysicalAddress.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_full(self, version: XtceVersion) -> None:
        """Round-trip PhysicalAddress with all fields and nested sub_address."""
        original = xtce.PhysicalAddress(
            source_name="RAM",
            source_address="0x1000",
            sub_address=xtce.PhysicalAddress(
                source_name="PART_A",
                source_address="0x04",
            ),
        )

        round_tripped = xtce.PhysicalAddress.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestParameterProperties:
    """Test ParameterProperties model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip default ParameterProperties."""
        original = xtce.ParameterProperties()

        round_tripped = xtce.ParameterProperties.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_full(self, version: XtceVersion) -> None:
        """Round-trip ParameterProperties with common fields."""
        original = xtce.ParameterProperties(
            system_name="SYS1",
            validity_condition=_make_match_criteria(),
            physical_addresses=[
                xtce.PhysicalAddress(source_name="BUS", source_address="0x20")
            ],
            time_association=xtce.TimeAssociation(
                ref=XtcePath("/TestSystem/TimeParam"),
            ),
            data_source=xtce.TelemetryDataSource.TELEMETERED,
            read_only=True,
            persistence=True,
        )

        round_tripped = xtce.ParameterProperties.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_v1_1_persistence_downgrade_policy(self) -> None:
        """Test v1.1 rejects persistence=False under STRICT."""
        props = xtce.ParameterProperties(persistence=False)

        with pytest.raises(XtceDowngradeError):
            props.to_xsdata(XtceVersion.V1_1, policy=DowngradePolicy.STRICT)

        exported = props.to_xsdata(XtceVersion.V1_1, policy=DowngradePolicy.IGNORE)
        assert exported is not None

    @pytest.mark.parametrize("version", MODERN_VERSIONS)
    def test_ground_data_source_modern(self, version: XtceVersion) -> None:
        """Test TelemetryDataSource.GROUND is supported in v1.2/v1.3."""
        props = xtce.ParameterProperties(data_source=xtce.TelemetryDataSource.GROUND)

        round_tripped = xtce.ParameterProperties.from_xsdata(
            props.to_xsdata(version), version
        )

        assert round_tripped == props

    def test_v1_1_ground_data_source_downgrade(self) -> None:
        """Test TelemetryDataSource.GROUND raises in v1.1 under STRICT."""
        props = xtce.ParameterProperties(data_source=xtce.TelemetryDataSource.GROUND)

        with pytest.raises(XtceDowngradeError):
            props.to_xsdata(XtceVersion.V1_1, policy=DowngradePolicy.STRICT)

        exported = props.to_xsdata(XtceVersion.V1_1, policy=DowngradePolicy.IGNORE)
        assert exported.data_source is None


class TestParameter:
    """Test Parameter model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal Parameter."""
        original = xtce.Parameter(
            name="Voltage",
            parameter_type_ref=XtcePath("/TestSystem/VoltageType"),
        )

        round_tripped = xtce.Parameter.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    @pytest.mark.parametrize(
        "initial_value",
        [
            42,
            3.14,
            "ACTIVE",
            True,
            b"\xde\xad\xbe\xef",
            datetime.timedelta(seconds=10),
            datetime.datetime(2026, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc),
        ],
    )
    def test_round_trip_initial_values(
        self, version: XtceVersion, initial_value: object
    ) -> None:
        """Round-trip Parameter with various scalar initial values."""
        original = xtce.Parameter(
            name="ParamWithInit",
            parameter_type_ref=XtcePath("/TestSystem/MyType"),
            initial_value=initial_value,  # type: ignore[arg-type]
        )

        round_tripped = xtce.Parameter.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_properties(self, version: XtceVersion) -> None:
        """Round-trip Parameter with full ParameterProperties."""
        original = xtce.Parameter(
            name="Voltage",
            parameter_type_ref=XtcePath("/TestSystem/VoltageType"),
            properties=xtce.ParameterProperties(
                system_name="SYS1",
                data_source=xtce.TelemetryDataSource.DERIVED,
                read_only=True,
                persistence=True,
            ),
        )

        round_tripped = xtce.Parameter.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    def test_invalid_parameter_type_ref_pattern(self) -> None:
        """Parameter rejects invalid parameter_type_ref patterns."""
        with pytest.raises(ValidationError):
            xtce.Parameter(
                name="Voltage",
                parameter_type_ref=XtcePath(""),
            )
