"""Test alarm models."""

from __future__ import annotations

import pytest

from xtce_lib import (
    DowngradePolicy,
    XtceDowngradeError,
    XtcePath,
    XtceUnsupportedError,
    XtceVersion,
    xtce,
)

ALL_VERSIONS = [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3]
BASE_VERSIONS = [XtceVersion.V1_2, XtceVersion.V1_3]


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
    """Build a reusable AlarmConditions for use in an Alarm's `alarm` field."""
    return xtce.AlarmConditions(watch_alarm=_make_match_criteria())


def _make_context_match() -> xtce.ContextMatch:
    """Build a reusable context match."""
    return xtce.ContextMatch(criteria=_make_comparison())


def _make_float_range(min_inclusive: float = 0.0) -> xtce.FloatRange:
    """Build a reusable float range."""
    return xtce.FloatRange(min_inclusive=min_inclusive)


class TestAlarmConditions:
    """Test AlarmConditions model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip alarm conditions through every supported version."""
        original = xtce.AlarmConditions(
            watch_alarm=_make_match_criteria(),
            warning_alarm=_make_match_criteria(),
            distress_alarm=_make_match_criteria(),
            critical_alarm=_make_match_criteria(),
            severe_alarm=_make_match_criteria(),
        )

        round_tripped = xtce.AlarmConditions.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip alarm conditions with no alarms set."""
        original = xtce.AlarmConditions()

        round_tripped = xtce.AlarmConditions.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestCustomAlarm:
    """Test CustomAlarm model."""

    @pytest.mark.parametrize("version", BASE_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a custom alarm through XTCE 1.2 and 1.3."""
        original = xtce.CustomAlarm(
            name="MyCustomAlarm",
            input_algorithm=xtce.InputAlgorithm(name="MyAlgorithm"),
        )

        round_tripped = xtce.CustomAlarm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_v1_1_is_unsupported(self) -> None:
        """XTCE 1.1 import/export is unsupported for CustomAlarm."""
        with pytest.raises(XtceUnsupportedError):
            xtce.CustomAlarm(
                input_algorithm=xtce.InputAlgorithm(name="MyAlgorithm")
            ).to_xsdata(XtceVersion.V1_1)


class TestAlarm:
    """Test shared Alarm behavior, exercised through the BooleanAlarm subclass."""

    def test_min_conformances_defaults_to_min_violations(self) -> None:
        """min_conformances should default to min_violations when unset."""
        model = xtce.BooleanAlarm(min_violations=3)

        assert model.min_conformances == 3

    def test_min_conformances_can_be_set_explicitly(self) -> None:
        """min_conformances should retain an explicitly provided value."""
        model = xtce.BooleanAlarm(min_violations=3, min_conformances=5)

        assert model.min_conformances == 5

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_alarm_conditions(self, version: XtceVersion) -> None:
        """Round-trip an alarm with AlarmConditions through every version."""
        original = xtce.BooleanAlarm(
            alarm=_make_alarm_conditions(),
            min_violations=2,
        )

        round_tripped = xtce.BooleanAlarm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", BASE_VERSIONS)
    def test_round_trip_with_custom_alarm(self, version: XtceVersion) -> None:
        """Round-trip an alarm with a CustomAlarm through XTCE 1.2 and 1.3."""
        original = xtce.BooleanAlarm(
            alarm=xtce.CustomAlarm(
                input_algorithm=xtce.InputAlgorithm(name="MyAlgorithm")
            ),
            min_violations=1,
        )

        round_tripped = xtce.BooleanAlarm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_to_v1_2_strict_rejects_disabled(self) -> None:
        """Exporting disabled=True to XTCE 1.2 should raise in strict mode."""
        model = xtce.BooleanAlarm(disabled=True)

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_2, DowngradePolicy.STRICT)

    def test_to_v1_2_lenient_drops_disabled(self) -> None:
        """Exporting disabled=True to XTCE 1.2 should succeed under WARN policy."""
        model = xtce.BooleanAlarm(disabled=True)

        raw_obj = model.to_xsdata(XtceVersion.V1_2, DowngradePolicy.WARN)

        assert raw_obj is not None

    @pytest.mark.parametrize("version", BASE_VERSIONS)
    def test_round_trip_disabled(self, version: XtceVersion) -> None:
        """Round-trip the disabled flag through XTCE 1.3."""
        original = xtce.BooleanAlarm(disabled=True)

        round_tripped = xtce.BooleanAlarm.from_xsdata(
            original.to_xsdata(XtceVersion.V1_3), XtceVersion.V1_3
        )

        assert round_tripped == original


class TestAlarmRanges:
    """Test AlarmRanges model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip alarm ranges through every supported version."""
        original = xtce.AlarmRanges(
            watch_range=_make_float_range(1.0),
            warning_range=_make_float_range(2.0),
            distress_range=_make_float_range(3.0),
            critical_range=_make_float_range(4.0),
            severe_range=_make_float_range(5.0),
        )

        round_tripped = xtce.AlarmRanges.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", BASE_VERSIONS)
    def test_round_trip_with_name_and_range_form(self, version: XtceVersion) -> None:
        """Round-trip name, description, and a non-default range_form on 1.2+."""
        original = xtce.AlarmRanges(
            name="MyAlarm",
            description="A description",
            watch_range=_make_float_range(1.0),
            range_form=xtce.RangeForm.INSIDE,
        )

        round_tripped = xtce.AlarmRanges.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_to_v1_1_strict_rejects_non_default_range_form(self) -> None:
        """A non-default range_form cannot be represented in XTCE 1.1."""
        model = xtce.AlarmRanges(
            watch_range=_make_float_range(1.0), range_form=xtce.RangeForm.INSIDE
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.STRICT)

    def test_to_v1_1_strict_rejects_name(self) -> None:
        """A name cannot be represented in XTCE 1.1 for AlarmRanges."""
        model = xtce.AlarmRanges(name="MyAlarm", watch_range=_make_float_range(1.0))

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.STRICT)


class TestChangeAlarmRanges:
    """Test ChangeAlarmRanges model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip change alarm ranges through every supported version."""
        original = xtce.ChangeAlarmRanges(
            watch_range=_make_float_range(1.0),
            change_type=xtce.ChangeSpan.CHANGE_PER_SAMPLE,
            change_basis=xtce.ChangeBasis.PERCENTAGE_CHANGE,
            span_of_interest_samples=5,
            span_of_interest_seconds=2.5,
        )

        round_tripped = xtce.ChangeAlarmRanges.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestTimeAlarmRanges:
    """Test TimeAlarmRanges model."""

    @pytest.mark.parametrize("version", BASE_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip time alarm ranges through XTCE 1.2 and 1.3."""
        original = xtce.TimeAlarmRanges(
            watch_range=_make_float_range(1.0),
            time_units=xtce.TimeUnits.SECONDS,
        )

        round_tripped = xtce.TimeAlarmRanges.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_round_trip_v1_3_only_time_unit(self) -> None:
        """Round-trip a time unit that XTCE 1.2 does not support."""
        original = xtce.TimeAlarmRanges(
            watch_range=_make_float_range(1.0),
            time_units=xtce.TimeUnits.MINUTES,
        )

        round_tripped = xtce.TimeAlarmRanges.from_xsdata(
            original.to_xsdata(XtceVersion.V1_3), XtceVersion.V1_3
        )

        assert round_tripped == original

    def test_v1_1_is_unsupported(self) -> None:
        """XTCE 1.1 import/export is unsupported for TimeAlarmRanges directly."""
        with pytest.raises(XtceUnsupportedError):
            xtce.TimeAlarmRanges(watch_range=_make_float_range(1.0)).to_xsdata(
                XtceVersion.V1_1
            )


class TestAlarmMultiRanges:
    """Test AlarmMultiRanges model."""

    @pytest.mark.parametrize("version", BASE_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip alarm multi-ranges through XTCE 1.2 and 1.3."""
        original = xtce.AlarmMultiRanges(
            ranges=[
                xtce.MultiRange(
                    min_inclusive=1.0,
                    level=xtce.ConcernLevel.WARNING,
                    range_form=xtce.RangeForm.OUTSIDE,
                ),
                xtce.MultiRange(
                    max_inclusive=10.0,
                    level=xtce.ConcernLevel.CRITICAL,
                    range_form=xtce.RangeForm.INSIDE,
                ),
            ]
        )

        round_tripped = xtce.AlarmMultiRanges.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_v1_1_is_unsupported(self) -> None:
        """XTCE 1.1 import/export is unsupported for AlarmMultiRanges."""
        with pytest.raises(XtceUnsupportedError):
            xtce.AlarmMultiRanges().to_xsdata(XtceVersion.V1_1)


class TestStringAlarmLevel:
    """Test StringAlarmLevel model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    @pytest.mark.parametrize(
        "level",
        [
            xtce.ConcernLevel.NORMAL,
            xtce.ConcernLevel.WATCH,
            xtce.ConcernLevel.WARNING,
            xtce.ConcernLevel.DISTRESS,
            xtce.ConcernLevel.CRITICAL,
            xtce.ConcernLevel.SEVERE,
        ],
    )
    def test_round_trip(self, version: XtceVersion, level: xtce.ConcernLevel) -> None:
        """Round-trip every concern level through every supported version."""
        original = xtce.StringAlarmLevel(level=level, match_pattern="^ARMED$")

        round_tripped = xtce.StringAlarmLevel.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestEnumerationAlarmLevel:
    """Test EnumerationAlarmLevel model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    @pytest.mark.parametrize(
        "level",
        [
            xtce.ConcernLevel.NORMAL,
            xtce.ConcernLevel.WATCH,
            xtce.ConcernLevel.WARNING,
            xtce.ConcernLevel.DISTRESS,
            xtce.ConcernLevel.CRITICAL,
            xtce.ConcernLevel.SEVERE,
        ],
    )
    def test_round_trip(self, version: XtceVersion, level: xtce.ConcernLevel) -> None:
        """Round-trip every concern level through every supported version."""
        original = xtce.EnumerationAlarmLevel(level=level, enumeration_label="ARMED")

        round_tripped = xtce.EnumerationAlarmLevel.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestNumericAlarm:
    """Test NumericAlarm model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_static_and_change_ranges(
        self, version: XtceVersion
    ) -> None:
        """Round-trip static and change alarm ranges through every version."""
        original = xtce.NumericAlarm(
            static_alarm_ranges=xtce.AlarmRanges(watch_range=_make_float_range(1.0)),
            change_alarm_ranges=xtce.ChangeAlarmRanges(
                watch_range=_make_float_range(2.0)
            ),
            min_violations=2,
        )

        round_tripped = xtce.NumericAlarm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", BASE_VERSIONS)
    def test_round_trip_with_alarm_multi_ranges(self, version: XtceVersion) -> None:
        """Round-trip alarm_multi_ranges through XTCE 1.2 and 1.3."""
        original = xtce.NumericAlarm(
            alarm_multi_ranges=xtce.AlarmMultiRanges(
                ranges=[
                    xtce.MultiRange(min_inclusive=1.0, level=xtce.ConcernLevel.WARNING)
                ]
            ),
        )

        round_tripped = xtce.NumericAlarm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_to_v1_1_strict_rejects_alarm_multi_ranges(self) -> None:
        """alarm_multi_ranges cannot be represented in XTCE 1.1."""
        model = xtce.NumericAlarm(
            alarm_multi_ranges=xtce.AlarmMultiRanges(
                ranges=[
                    xtce.MultiRange(min_inclusive=1.0, level=xtce.ConcernLevel.WARNING)
                ]
            ),
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.STRICT)


class TestStringAlarm:
    """Test StringAlarm model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a string alarm's levels and default level."""
        original = xtce.StringAlarm(
            alarms=[
                xtce.StringAlarmLevel(
                    level=xtce.ConcernLevel.WARNING, match_pattern="^WARN.*"
                ),
                xtce.StringAlarmLevel(
                    level=xtce.ConcernLevel.CRITICAL, match_pattern="^CRIT.*"
                ),
            ],
            default_level=xtce.ConcernLevel.WATCH,
            min_violations=1,
        )

        round_tripped = xtce.StringAlarm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestBinaryAlarm:
    """Test BinaryAlarm model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a minimal binary alarm through every supported version."""
        original = xtce.BinaryAlarm(
            alarm=_make_alarm_conditions(),
            min_violations=3,
        )

        round_tripped = xtce.BinaryAlarm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestBooleanAlarm:
    """Test BooleanAlarm model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a minimal boolean alarm through every supported version."""
        original = xtce.BooleanAlarm(
            alarm=_make_alarm_conditions(),
            min_violations=1,
        )

        round_tripped = xtce.BooleanAlarm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestEnumerationAlarm:
    """Test EnumerationAlarm model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip an enumeration alarm's levels and default level."""
        original = xtce.EnumerationAlarm(
            alarms=[
                xtce.EnumerationAlarmLevel(
                    level=xtce.ConcernLevel.WARNING, enumeration_label="ARMED"
                ),
                xtce.EnumerationAlarmLevel(
                    level=xtce.ConcernLevel.SEVERE, enumeration_label="FAULT"
                ),
            ],
            default_alarm_level=xtce.ConcernLevel.DISTRESS,
        )

        round_tripped = xtce.EnumerationAlarm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_v1_1_from_xsdata_reads_default_alarm_level(self) -> None:
        """Verify importing XTCE 1.1 reads the defaultAlarmLevel attribute."""
        from xtce_lib.generated import xtce_1_1

        raw_obj = xtce_1_1.EnumerationAlarmType(
            enumeration_alarm_list=xtce_1_1.EnumerationAlarmType.EnumerationAlarmList(
                enumeration_alarm=[
                    xtce_1_1.EnumerationAlarmType.EnumerationAlarmList.EnumerationAlarm(
                        alarm_level=xtce_1_1.AlarmLevels.WARNING,
                        enumeration_value="ARMED",
                    )
                ]
            ),
            default_alarm_level=xtce_1_1.AlarmLevels.CRITICAL,
        )

        model = xtce.EnumerationAlarm.from_xsdata(raw_obj, XtceVersion.V1_1)

        assert model.default_alarm_level == xtce.ConcernLevel.CRITICAL


class TestTimeAlarm:
    """Test TimeAlarm model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a time alarm's static and change ranges."""
        original = xtce.TimeAlarm(
            static_alarm_ranges=xtce.TimeAlarmRanges(
                watch_range=_make_float_range(1.0),
                time_units=xtce.TimeUnits.SECONDS,
            ),
            change_per_second_alarm_ranges=xtce.TimeAlarmRanges(
                critical_range=_make_float_range(2.0),
                time_units=xtce.TimeUnits.DAYS,
            ),
        )

        round_tripped = xtce.TimeAlarm.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    def test_round_trip_v1_3_only_time_unit(self) -> None:
        """Round-trip a time unit that only XTCE 1.3 supports."""
        original = xtce.TimeAlarm(
            static_alarm_ranges=xtce.TimeAlarmRanges(
                watch_range=_make_float_range(1.0),
                time_units=xtce.TimeUnits.MINUTES,
            ),
        )

        round_tripped = xtce.TimeAlarm.from_xsdata(
            original.to_xsdata(XtceVersion.V1_3), XtceVersion.V1_3
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a time alarm with no ranges set."""
        original = xtce.TimeAlarm(alarm=_make_alarm_conditions())

        round_tripped = xtce.TimeAlarm.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original


class TestNumericContextAlarm:
    """Test NumericContextAlarm model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a numeric context alarm through every supported version."""
        original = xtce.NumericContextAlarm(
            context_match=_make_context_match(),
            static_alarm_ranges=xtce.AlarmRanges(watch_range=_make_float_range(1.0)),
        )

        round_tripped = xtce.NumericContextAlarm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestStringContextAlarm:
    """Test StringContextAlarm model."""

    @pytest.mark.parametrize("version", BASE_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a string context alarm through XTCE 1.2 and 1.3."""
        original = xtce.StringContextAlarm(
            context_match=_make_context_match(),
            alarms=[
                xtce.StringAlarmLevel(
                    level=xtce.ConcernLevel.WARNING, match_pattern="^WARN.*"
                )
            ],
        )

        round_tripped = xtce.StringContextAlarm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_v1_1_is_unsupported(self) -> None:
        """XTCE 1.1 import/export is unsupported for StringContextAlarm."""
        with pytest.raises(XtceUnsupportedError):
            xtce.StringContextAlarm(context_match=_make_context_match()).to_xsdata(
                XtceVersion.V1_1
            )


class TestBinaryContextAlarm:
    """Test BinaryContextAlarm model."""

    @pytest.mark.parametrize("version", BASE_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a binary context alarm through XTCE 1.2 and 1.3."""
        original = xtce.BinaryContextAlarm(
            context_match=_make_context_match(),
            min_violations=2,
        )

        round_tripped = xtce.BinaryContextAlarm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_v1_1_is_unsupported(self) -> None:
        """XTCE 1.1 import/export is unsupported for BinaryContextAlarm."""
        with pytest.raises(XtceUnsupportedError):
            xtce.BinaryContextAlarm(context_match=_make_context_match()).to_xsdata(
                XtceVersion.V1_1
            )

        with pytest.raises(XtceUnsupportedError):
            xtce.BinaryContextAlarm.from_xsdata(object(), XtceVersion.V1_1)


class TestBooleanContextAlarm:
    """Test BooleanContextAlarm model."""

    @pytest.mark.parametrize("version", BASE_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a boolean context alarm through XTCE 1.2 and 1.3."""
        original = xtce.BooleanContextAlarm(
            context_match=_make_context_match(),
            min_violations=1,
        )

        round_tripped = xtce.BooleanContextAlarm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestEnumerationContextAlarm:
    """Test EnumerationContextAlarm model."""

    @pytest.mark.parametrize("version", BASE_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip an enumeration context alarm through XTCE 1.2 and 1.3."""
        original = xtce.EnumerationContextAlarm(
            context_match=_make_context_match(),
            alarms=[
                xtce.EnumerationAlarmLevel(
                    level=xtce.ConcernLevel.SEVERE, enumeration_label="FAULT"
                )
            ],
            default_alarm_level=xtce.ConcernLevel.NORMAL,
        )

        round_tripped = xtce.EnumerationContextAlarm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestTimeContextAlarm:
    """Test TimeContextAlarm model."""

    @pytest.mark.parametrize("version", BASE_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a time context alarm through XTCE 1.2 and 1.3."""
        original = xtce.TimeContextAlarm(
            context_match=_make_context_match(),
            static_alarm_ranges=xtce.TimeAlarmRanges(
                watch_range=_make_float_range(1.0)
            ),
        )

        round_tripped = xtce.TimeContextAlarm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_v1_1_is_unsupported(self) -> None:
        """XTCE 1.1 import/export is unsupported for TimeContextAlarm."""
        with pytest.raises(XtceUnsupportedError):
            xtce.TimeContextAlarm(context_match=_make_context_match()).to_xsdata(
                XtceVersion.V1_1
            )

        with pytest.raises(XtceUnsupportedError):
            xtce.TimeContextAlarm.from_xsdata(object(), XtceVersion.V1_1)
