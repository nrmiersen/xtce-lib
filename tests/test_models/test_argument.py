"""Test argument models."""

from __future__ import annotations

import datetime

import pytest

from xtce_lib import XtceDowngradeError, XtcePath, XtceVersion, xtce

ALL_VERSIONS = [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3]
BASE_VERSIONS = [XtceVersion.V1_2, XtceVersion.V1_3]


def _make_integer_encoding() -> xtce.IntegerDataEncoding:
    """Build a reusable integer data encoding.

    Uses an explicit byte_order list rather than an Endian value, since XTCE 1.1
    expands Endian into an explicit list on export.

    """
    return xtce.IntegerDataEncoding(size_in_bits=16, byte_order=[1, 0])


def _make_time_encoding() -> xtce.TimeEncoding:
    """Build a reusable time encoding."""
    return xtce.TimeEncoding(encoding_type=_make_integer_encoding())


class TestIntegerArgument:
    """Test IntegerArgument model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal integer argument with no valid ranges."""
        original = xtce.IntegerArgument(name="MyInt", encoding_type=None)

        round_tripped = xtce.IntegerArgument.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_valid_ranges(self, version: XtceVersion) -> None:
        """Round-trip an integer argument with multiple valid ranges."""
        original = xtce.IntegerArgument(
            name="MyInt",
            encoding_type=_make_integer_encoding(),
            valid_ranges=xtce.ValidIntegerRanges(
                valid_ranges=[
                    xtce.IntegerRange(min_inclusive=0, max_inclusive=10),
                    xtce.IntegerRange(min_inclusive=20, max_inclusive=30),
                ],
                applies_to_calibrated=False,
            ),
        )

        round_tripped = xtce.IntegerArgument.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestFloatArgument:
    """Test FloatArgument model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal float argument with no valid ranges."""
        original = xtce.FloatArgument(name="MyFloat", encoding_type=None)

        round_tripped = xtce.FloatArgument.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_valid_ranges(self, version: XtceVersion) -> None:
        """Round-trip a float argument with multiple valid ranges."""
        original = xtce.FloatArgument(
            name="MyFloat",
            encoding_type=None,
            valid_ranges=xtce.ValidFloatRanges(
                valid_ranges=[
                    xtce.FloatRange(min_inclusive=0.0, max_inclusive=1.0),
                    xtce.FloatRange(min_exclusive=5.0, max_exclusive=6.0),
                ],
                applies_to_calibrated=False,
            ),
        )

        round_tripped = xtce.FloatArgument.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestStringArgument:
    """Test StringArgument model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal string argument."""
        original = xtce.StringArgument(name="MyString", encoding_type=None)

        round_tripped = xtce.StringArgument.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_all_fields(self, version: XtceVersion) -> None:
        """Round-trip a string argument with every field set."""
        original = xtce.StringArgument(
            name="MyString",
            encoding_type=xtce.ArgumentStringDataEncoding(allocation_size=64),
            initial_value="hello",
            restriction_pattern="[a-z]+",
            character_width=8,
        )

        round_tripped = xtce.StringArgument.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestBinaryArgument:
    """Test BinaryArgument model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal binary argument."""
        original = xtce.BinaryArgument(name="MyBinary", encoding_type=None)

        round_tripped = xtce.BinaryArgument.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_initial_value(self, version: XtceVersion) -> None:
        """Round-trip a binary argument with an initial value."""
        original = xtce.BinaryArgument(
            name="MyBinary",
            encoding_type=xtce.ArgumentBinaryDataEncoding(size_in_bits=32),
            initial_value=b"\xab\x12",
        )

        round_tripped = xtce.BinaryArgument.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestBooleanArgument:
    """Test BooleanArgument model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal boolean argument."""
        original = xtce.BooleanArgument(name="MyBool", encoding_type=None)

        round_tripped = xtce.BooleanArgument.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_all_fields(self, version: XtceVersion) -> None:
        """Round-trip a boolean argument with every field set."""
        original = xtce.BooleanArgument(
            name="MyBool",
            encoding_type=_make_integer_encoding(),
            initial_value="true",
            one_string_value="On",
            zero_string_value="Off",
        )

        round_tripped = xtce.BooleanArgument.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestEnumeratedArgument:
    """Test EnumeratedArgument model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal enumerated argument with a single enumeration."""
        original = xtce.EnumeratedArgument(
            name="MyEnum",
            encoding_type=None,
            enumerations=[xtce.ValueEnumeration(value=1, label="Label")],
        )

        round_tripped = xtce.EnumeratedArgument.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_multiple_enumerations(self, version: XtceVersion) -> None:
        """Round-trip an enumerated argument with multiple enumerations."""
        original = xtce.EnumeratedArgument(
            name="MyEnum",
            encoding_type=_make_integer_encoding(),
            enumerations=[
                xtce.ValueEnumeration(value=0, label="Off"),
                xtce.ValueEnumeration(value=1, label="On"),
            ],
            initial_value="Off",
        )

        round_tripped = xtce.EnumeratedArgument.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestArrayArgument:
    """Test ArrayArgument model."""

    @pytest.mark.parametrize("version", BASE_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip an array argument through XTCE 1.2/1.3.

        Uses a path-less reference since XTCE 1.2 only supports NameReferenceType
        (no path) for array_type_ref.

        """
        original = xtce.ArrayArgument(
            name="MyArray",
            array_type_ref=XtcePath("ElementType"),
            dimensions=[xtce.ArgumentDimension(start_index=0, end_index=3)],
        )

        round_tripped = xtce.ArrayArgument.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_round_trip_v1_1_preserves_dimension_count(self) -> None:
        """XTCE 1.1 only preserves the number of dimensions, not their bounds.

        v1.1's ArrayDataTypeType has no per-dimension bound information, so the
        dimensions are reconstructed as placeholders on import.

        """
        original = xtce.ArrayArgument(
            name="MyArray",
            array_type_ref=XtcePath("ElementType"),
            dimensions=[xtce.ArgumentDimension(start_index=0, end_index=3)],
        )

        round_tripped = xtce.ArrayArgument.from_xsdata(
            original.to_xsdata(XtceVersion.V1_1), XtceVersion.V1_1
        )

        assert len(round_tripped.dimensions) == len(original.dimensions)


class TestAggregateArgument:
    """Test AggregateArgument model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal aggregate argument with a single member."""
        original = xtce.AggregateArgument(
            name="MyAggregate",
            members=[
                xtce.Member(name="voltage", type_ref=XtcePath("FloatType")),
            ],
        )

        round_tripped = xtce.AggregateArgument.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_round_trip_v1_3_with_initial_value(self) -> None:
        """Round-trip a v1.3 aggregate argument with an initial value.

        Only XTCE 1.3 supports an initial value for aggregates.

        """
        original = xtce.AggregateArgument(
            name="MyAggregate",
            members=[xtce.Member(name="voltage", type_ref=XtcePath("FloatType"))],
            initial_value={"voltage": 1.5},
        )

        round_tripped = xtce.AggregateArgument.from_xsdata(
            original.to_xsdata(XtceVersion.V1_3), XtceVersion.V1_3
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", [XtceVersion.V1_1, XtceVersion.V1_2])
    def test_v1_1_and_v1_2_reject_initial_value(self, version: XtceVersion) -> None:
        """XTCE 1.1/1.2 do not support an initial value for aggregates."""
        model = xtce.AggregateArgument(
            name="MyAggregate",
            members=[xtce.Member(name="voltage", type_ref=XtcePath("FloatType"))],
            initial_value={"voltage": 1.5},
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(version)


class TestRelativeTimeArgument:
    """Test RelativeTimeArgument model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal relative time argument."""
        original = xtce.RelativeTimeArgument(
            name="MyTime", encoding=_make_time_encoding()
        )

        round_tripped = xtce.RelativeTimeArgument.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_initial_value(self, version: XtceVersion) -> None:
        """Round-trip a relative time argument with an initial value.

        XTCE 1.1 has no ArgumentRelativeTimeDataType, so this casts to
        RelativeTimeDataType.

        """
        original = xtce.RelativeTimeArgument(
            name="MyTime",
            encoding=_make_time_encoding(),
            initial_value=datetime.timedelta(seconds=30),
        )

        round_tripped = xtce.RelativeTimeArgument.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestAbsoluteTimeArgument:
    """Test AbsoluteTimeArgument model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal absolute time argument."""
        original = xtce.AbsoluteTimeArgument(
            name="MyTime", encoding=_make_time_encoding()
        )

        round_tripped = xtce.AbsoluteTimeArgument.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_initial_value(self, version: XtceVersion) -> None:
        """Round-trip an absolute time argument with an initial value.

        XTCE 1.1 has no ArgumentAbsoluteTimeDataType, so this casts to
        AbsoluteTimeDataType.

        """
        original = xtce.AbsoluteTimeArgument(
            name="MyTime",
            encoding=_make_time_encoding(),
            initial_value=datetime.datetime(2024, 1, 2, 3, 4, 5),
        )

        round_tripped = xtce.AbsoluteTimeArgument.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original
