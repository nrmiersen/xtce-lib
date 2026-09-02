"""Test data type models."""

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
from xtce_lib.generated import xtce_1_1

ALL_VERSIONS = [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3]
BASE_VERSIONS = [XtceVersion.V1_2, XtceVersion.V1_3]


def _make_integer_encoding() -> xtce.IntegerDataEncoding:
    """Build a reusable integer data encoding.

    Uses an explicit byte_order list rather than an Endian value, since XTCE 1.1
    expands Endian into an explicit list on export.

    """
    return xtce.IntegerDataEncoding(size_in_bits=16, byte_order=[1, 0])


def _make_float_encoding() -> xtce.FloatDataEncoding:
    """Build a reusable float data encoding.

    Uses an explicit byte_order list rather than an Endian value, since XTCE 1.1
    expands Endian into an explicit list on export.

    """
    return xtce.FloatDataEncoding(size_in_bits=32, byte_order=[3, 2, 1, 0])


def _make_string_encoding() -> xtce.StringDataEncoding:
    """Build a reusable fixed-length string data encoding."""
    return xtce.StringDataEncoding(allocation_size=64)


def _make_binary_encoding() -> xtce.BinaryDataEncoding:
    """Build a reusable binary data encoding."""
    return xtce.BinaryDataEncoding(size_in_bits=32)


def _make_argument_string_encoding() -> xtce.ArgumentStringDataEncoding:
    """Build a reusable fixed-length argument string data encoding."""
    return xtce.ArgumentStringDataEncoding(allocation_size=64)


def _make_argument_binary_encoding() -> xtce.ArgumentBinaryDataEncoding:
    """Build a reusable argument binary data encoding."""
    return xtce.ArgumentBinaryDataEncoding(size_in_bits=32)


def _make_unit(symbol: str = "m/s^2") -> xtce.Unit:
    """Build a reusable unit."""
    return xtce.Unit(symbol=symbol)


def _make_value_enumeration(
    value: int = 1, label: str = "Label"
) -> xtce.ValueEnumeration:
    """Build a reusable value enumeration."""
    return xtce.ValueEnumeration(value=value, label=label)


def _make_number_format() -> xtce.NumberFormat:
    """Build a reusable number format."""
    return xtce.NumberFormat()


def _make_to_string() -> xtce.ToString:
    """Build a reusable to-string, using a NumberFormat for cross-version support."""
    return xtce.ToString(number_format=_make_number_format())


def _make_reference_time() -> xtce.ReferenceTime:
    """Build a reusable reference time, using an epoch for cross-version support.

    XTCE 1.1's epoch enum only supports TAI (unlike 1.2/1.3, which add J2000/UNIX/GPS).

    """
    return xtce.ReferenceTime(epoch=xtce.EpochTime.TAI)


def _make_time_encoding() -> xtce.TimeEncoding:
    """Build a reusable time encoding."""
    return xtce.TimeEncoding(encoding_type=_make_integer_encoding())


class TestUnit:
    """Test Unit model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal unit through every supported version."""
        original = _make_unit()

        round_tripped = xtce.Unit.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    @pytest.mark.parametrize("version", BASE_VERSIONS)
    def test_round_trip_with_all_fields(self, version: XtceVersion) -> None:
        """Round-trip a unit with every field set."""
        original = xtce.Unit(
            symbol="m/s^2",
            factor="2",
            power=2.0,
            form=xtce.UnitForm.RAW,
            description="A description.",
        )

        round_tripped = xtce.Unit.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    def test_v1_1_drops_non_default_form(self) -> None:
        """XTCE 1.1 has no form field, so a non-default form must be rejected."""
        model = xtce.Unit(symbol="V", form=xtce.UnitForm.RAW)

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_1)

        raw_obj = model.to_xsdata(XtceVersion.V1_1, policy=DowngradePolicy.IGNORE)

        assert isinstance(raw_obj, xtce_1_1.UnitType)

    def test_v1_1_accepts_default_form(self) -> None:
        """XTCE 1.1 should accept a unit with the default calibrated form."""
        model = xtce.Unit(symbol="V")

        raw_obj = model.to_xsdata(XtceVersion.V1_1)

        assert isinstance(raw_obj, xtce_1_1.UnitType)


class TestValueEnumeration:
    """Test ValueEnumeration model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal value enumeration through every supported version."""
        original = _make_value_enumeration()

        round_tripped = xtce.ValueEnumeration.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", BASE_VERSIONS)
    def test_round_trip_with_all_fields(self, version: XtceVersion) -> None:
        """Round-trip a value enumeration with every field set."""
        original = xtce.ValueEnumeration(
            value=1,
            max_value=5,
            label="Label",
            short_description="A short description.",
        )

        round_tripped = xtce.ValueEnumeration.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_v1_1_drops_max_value_and_short_description(self) -> None:
        """XTCE 1.1 has no max_value or short_description fields."""
        model = xtce.ValueEnumeration(
            value=1, max_value=5, label="Label", short_description="A description."
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_1)

        raw_obj = model.to_xsdata(XtceVersion.V1_1, policy=DowngradePolicy.IGNORE)

        assert isinstance(raw_obj, xtce_1_1.ValueEnumerationType)


class TestBaseData:
    """Test BaseData model (instantiated directly, not through a leaf subclass)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal base data with no encoding, units, or base type."""
        original = xtce.BaseData(name="MyType", encoding_type=None)

        round_tripped = xtce.BaseData.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_encoding_and_units(self, version: XtceVersion) -> None:
        """Round-trip a base data with an encoding type and units."""
        original = xtce.BaseData(
            name="MyType",
            encoding_type=_make_integer_encoding(),
            units=[_make_unit()],
        )

        round_tripped = xtce.BaseData.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_base_type(self, version: XtceVersion) -> None:
        """Round-trip a base data that derives from another data type.

        Uses a path-less reference since XTCE 1.1/1.2 only support NameReferenceType
        (no path) for base_type.

        """
        original = xtce.BaseData(
            name="MyType",
            encoding_type=None,
            base_type=XtcePath("OtherType"),
        )

        round_tripped = xtce.BaseData.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_all_encoding_types(self, version: XtceVersion) -> None:
        """Round-trip a base data with every encoding type variant."""
        for encoding_type in (
            _make_integer_encoding(),
            _make_float_encoding(),
            _make_string_encoding(),
            _make_binary_encoding(),
        ):
            original = xtce.BaseData(name="MyType", encoding_type=encoding_type)

            round_tripped = xtce.BaseData.from_xsdata(
                original.to_xsdata(version), version
            )

            assert round_tripped == original


class TestArgumentBaseData:
    """Test ArgumentBaseData model (instantiated directly)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal argument base data."""
        original = xtce.ArgumentBaseData(name="MyType", encoding_type=None)

        round_tripped = xtce.ArgumentBaseData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_base_type(self, version: XtceVersion) -> None:
        """Round-trip an argument base data that derives from another data type."""
        original = xtce.ArgumentBaseData(
            name="MyType",
            encoding_type=None,
            base_type=XtcePath("OtherType"),
        )

        round_tripped = xtce.ArgumentBaseData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_integer_encoding(self, version: XtceVersion) -> None:
        """Round-trip an argument base data with an integer encoding.

        Integer/float encodings are shared between plain and Argument data types.

        """
        original = xtce.ArgumentBaseData(
            name="MyType",
            encoding_type=_make_integer_encoding(),
            units=[_make_unit()],
        )

        round_tripped = xtce.ArgumentBaseData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_argument_string_encoding(
        self, version: XtceVersion
    ) -> None:
        """Round-trip an argument base data with an argument string encoding."""
        original = xtce.ArgumentBaseData(
            name="MyType",
            encoding_type=_make_argument_string_encoding(),
        )

        round_tripped = xtce.ArgumentBaseData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_argument_binary_encoding(
        self, version: XtceVersion
    ) -> None:
        """Round-trip an argument base data with an argument binary encoding."""
        original = xtce.ArgumentBaseData(
            name="MyType",
            encoding_type=_make_argument_binary_encoding(),
        )

        round_tripped = xtce.ArgumentBaseData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestNumberFormat:
    """Test NumberFormat model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_defaults(self, version: XtceVersion) -> None:
        """Round-trip a number format with default values."""
        original = _make_number_format()

        round_tripped = xtce.NumberFormat.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_all_fields(self, version: XtceVersion) -> None:
        """Round-trip a number format with every field set."""
        original = xtce.NumberFormat(
            number_base=xtce.Radix.HEXADECIMAL,
            minimum_fraction_digits=1,
            maximum_fraction_digits=3,
            minimum_integer_digits=2,
            maximum_integer_digits=5,
            negative_prefix="(",
            positive_prefix="+",
            negative_suffix=")",
            positive_suffix="",
            show_thousands_grouping=True,
            notation=xtce.FloatingPointNotation.SCIENTIFIC,
        )

        round_tripped = xtce.NumberFormat.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestToString:
    """Test ToString model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_number_format(self, version: XtceVersion) -> None:
        """Round-trip a to-string wrapping a number format."""
        original = _make_to_string()

        round_tripped = xtce.ToString.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    def test_round_trip_v1_1_with_value_enumeration(self) -> None:
        """Round-trip a v1.1 to-string wrapping a value enumeration."""
        original = xtce.ToString(number_format=_make_value_enumeration())

        round_tripped = xtce.ToString.from_xsdata(
            original.to_xsdata(XtceVersion.V1_1), XtceVersion.V1_1
        )

        assert round_tripped == original

    def test_round_trip_v1_1_with_float_range(self) -> None:
        """Round-trip a v1.1 to-string wrapping a float range."""
        original = xtce.ToString(number_format=xtce.FloatRange(min_inclusive=0.0))

        round_tripped = xtce.ToString.from_xsdata(
            original.to_xsdata(XtceVersion.V1_1), XtceVersion.V1_1
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", BASE_VERSIONS)
    def test_base_versions_reject_value_enumeration(self, version: XtceVersion) -> None:
        """XTCE 1.2/1.3 only support NumberFormat for number_format."""
        model = xtce.ToString(number_format=_make_value_enumeration())

        with pytest.raises((XtceDowngradeError, TypeError)):
            model.to_xsdata(version)


class TestIntegerData:
    """Test IntegerData model (instantiated directly)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_external_dynamic_size(self, version: XtceVersion) -> None:
        """Round-trip the external dynamic-size sentinel."""
        original = xtce.IntegerData(name="MyInt", encoding_type=None, size_in_bits=-1)

        round_tripped = xtce.IntegerData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal integer data with only defaults."""
        original = xtce.IntegerData(name="MyInt", encoding_type=None)

        round_tripped = xtce.IntegerData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_all_fields(self, version: XtceVersion) -> None:
        """Round-trip an integer data with every field set."""
        original = xtce.IntegerData(
            name="MyInt",
            encoding_type=_make_integer_encoding(),
            to_string=_make_to_string(),
            valid_range=xtce.ValidIntegerRange(
                min_inclusive=0, max_inclusive=100, applies_to_calibrated=True
            ),
            initial_value=5,
            size_in_bits=16,
            signed=False,
        )

        round_tripped = xtce.IntegerData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_hex_initial_value(self, version: XtceVersion) -> None:
        """Round-trip an integer data with a hex string initial value.

        XTCE 1.2/1.3 coerce hex initial values to base-10 integers on export, so this
        only round-trips exactly for XTCE 1.1.

        """
        original = xtce.IntegerData(
            name="MyInt", encoding_type=None, initial_value="0x10"
        )

        raw_obj = original.to_xsdata(version)
        round_tripped = xtce.IntegerData.from_xsdata(raw_obj, version)

        if version == XtceVersion.V1_1:
            assert round_tripped == original
        else:
            assert round_tripped.initial_value == 16


class TestArgumentIntegerData:
    """Test ArgumentIntegerData model (instantiated directly)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_external_dynamic_size(self, version: XtceVersion) -> None:
        """Round-trip the external dynamic-size sentinel."""
        original = xtce.ArgumentIntegerData(
            name="MyInt", encoding_type=None, size_in_bits=-1
        )

        round_tripped = xtce.ArgumentIntegerData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal argument integer data."""
        original = xtce.ArgumentIntegerData(name="MyInt", encoding_type=None)

        round_tripped = xtce.ArgumentIntegerData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_round_trip_v1_1_with_valid_range(self) -> None:
        """Round-trip a v1.1 argument integer data with a valid range."""
        original = xtce.ArgumentIntegerData(
            name="MyInt",
            encoding_type=None,
            valid_range=xtce.ValidIntegerRange(
                min_inclusive=0, max_inclusive=100, applies_to_calibrated=True
            ),
        )

        round_tripped = xtce.ArgumentIntegerData.from_xsdata(
            original.to_xsdata(XtceVersion.V1_1), XtceVersion.V1_1
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", BASE_VERSIONS)
    def test_base_versions_reject_valid_range(self, version: XtceVersion) -> None:
        """XTCE 1.2/1.3 do not support valid_range on ArgumentIntegerData."""
        model = xtce.ArgumentIntegerData(
            name="MyInt",
            encoding_type=None,
            valid_range=xtce.ValidIntegerRange(min_inclusive=0, max_inclusive=100),
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(version)


class TestFloatData:
    """Test FloatData model (instantiated directly)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal float data."""
        original = xtce.FloatData(name="MyFloat", encoding_type=None)

        round_tripped = xtce.FloatData.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_all_fields(self, version: XtceVersion) -> None:
        """Round-trip a float data with every field set."""
        original = xtce.FloatData(
            name="MyFloat",
            encoding_type=_make_float_encoding(),
            to_string=_make_to_string(),
            valid_range=xtce.ValidFloatRange(
                min_inclusive=0.0, max_inclusive=100.0, applies_to_calibrated=True
            ),
            initial_value=1.5,
            size_in_bits=64,
        )

        round_tripped = xtce.FloatData.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original


class TestArgumentFloatData:
    """Test ArgumentFloatData model (instantiated directly)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal argument float data."""
        original = xtce.ArgumentFloatData(name="MyFloat", encoding_type=None)

        round_tripped = xtce.ArgumentFloatData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_round_trip_v1_1_with_valid_range(self) -> None:
        """Round-trip a v1.1 argument float data with a valid range."""
        original = xtce.ArgumentFloatData(
            name="MyFloat",
            encoding_type=None,
            valid_range=xtce.ValidFloatRange(min_inclusive=0.0, max_inclusive=100.0),
        )

        round_tripped = xtce.ArgumentFloatData.from_xsdata(
            original.to_xsdata(XtceVersion.V1_1), XtceVersion.V1_1
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", BASE_VERSIONS)
    def test_base_versions_reject_valid_range(self, version: XtceVersion) -> None:
        """XTCE 1.2/1.3 do not support valid_range on ArgumentFloatData."""
        model = xtce.ArgumentFloatData(
            name="MyFloat",
            encoding_type=None,
            valid_range=xtce.ValidFloatRange(min_inclusive=0.0, max_inclusive=100.0),
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(version)


class TestStringData:
    """Test StringData model (instantiated directly)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal string data."""
        original = xtce.StringData(name="MyString", encoding_type=None)

        round_tripped = xtce.StringData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_all_fields(self, version: XtceVersion) -> None:
        """Round-trip a string data with every field set."""
        original = xtce.StringData(
            name="MyString",
            encoding_type=_make_string_encoding(),
            size_range_in_characters=xtce.IntegerRange(
                min_inclusive=0, max_inclusive=64
            ),
            initial_value="hello",
            restriction_pattern="[a-z]+",
            character_width=8,
        )

        round_tripped = xtce.StringData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestArgumentStringData:
    """Test ArgumentStringData model (instantiated directly)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal argument string data."""
        original = xtce.ArgumentStringData(name="MyString", encoding_type=None)

        round_tripped = xtce.ArgumentStringData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_all_fields(self, version: XtceVersion) -> None:
        """Round-trip an argument string data with every field set."""
        original = xtce.ArgumentStringData(
            name="MyString",
            encoding_type=_make_argument_string_encoding(),
            size_range_in_characters=xtce.IntegerRange(
                min_inclusive=0, max_inclusive=64
            ),
            initial_value="hello",
            restriction_pattern="[a-z]+",
            character_width=16,
        )

        round_tripped = xtce.ArgumentStringData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestBinaryData:
    """Test BinaryData model (instantiated directly)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal binary data."""
        original = xtce.BinaryData(name="MyBinary", encoding_type=None)

        round_tripped = xtce.BinaryData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_initial_value(self, version: XtceVersion) -> None:
        """Round-trip a binary data with an initial value."""
        original = xtce.BinaryData(
            name="MyBinary",
            encoding_type=_make_binary_encoding(),
            initial_value=b"\xab\x12",
        )

        round_tripped = xtce.BinaryData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestArgumentBinaryData:
    """Test ArgumentBinaryData model (instantiated directly)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal argument binary data."""
        original = xtce.ArgumentBinaryData(name="MyBinary", encoding_type=None)

        round_tripped = xtce.ArgumentBinaryData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_initial_value(self, version: XtceVersion) -> None:
        """Round-trip an argument binary data with an initial value."""
        original = xtce.ArgumentBinaryData(
            name="MyBinary",
            encoding_type=_make_argument_binary_encoding(),
            initial_value=b"\xab\x12",
        )

        round_tripped = xtce.ArgumentBinaryData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestBooleanData:
    """Test BooleanData model (instantiated directly)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal boolean data."""
        original = xtce.BooleanData(name="MyBool", encoding_type=None)

        round_tripped = xtce.BooleanData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_all_fields(self, version: XtceVersion) -> None:
        """Round-trip a boolean data with every field set."""
        original = xtce.BooleanData(
            name="MyBool",
            encoding_type=_make_integer_encoding(),
            initial_value="true",
            one_string_value="On",
            zero_string_value="Off",
        )

        round_tripped = xtce.BooleanData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestArgumentBooleanData:
    """Test ArgumentBooleanData model (instantiated directly)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal argument boolean data."""
        original = xtce.ArgumentBooleanData(name="MyBool", encoding_type=None)

        round_tripped = xtce.ArgumentBooleanData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_all_fields(self, version: XtceVersion) -> None:
        """Round-trip an argument boolean data with every field set."""
        original = xtce.ArgumentBooleanData(
            name="MyBool",
            encoding_type=None,
            initial_value="true",
            one_string_value="On",
            zero_string_value="Off",
        )

        round_tripped = xtce.ArgumentBooleanData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestEnumeratedData:
    """Test EnumeratedData model (instantiated directly)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal enumerated data with a single enumeration."""
        original = xtce.EnumeratedData(
            name="MyEnum",
            encoding_type=None,
            enumerations=[_make_value_enumeration()],
        )

        round_tripped = xtce.EnumeratedData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_multiple_enumerations(self, version: XtceVersion) -> None:
        """Round-trip an enumerated data with multiple enumerations and an initial
        value.
        """
        original = xtce.EnumeratedData(
            name="MyEnum",
            encoding_type=_make_integer_encoding(),
            enumerations=[
                _make_value_enumeration(value=0, label="Off"),
                _make_value_enumeration(value=1, label="On"),
            ],
            initial_value="Off",
        )

        round_tripped = xtce.EnumeratedData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_rejects_empty_enumerations(self) -> None:
        """At least one enumeration is required."""
        with pytest.raises(ValidationError):
            xtce.EnumeratedData(name="MyEnum", encoding_type=None, enumerations=[])


class TestArgumentEnumeratedData:
    """Test ArgumentEnumeratedData model (instantiated directly)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal argument enumerated data."""
        original = xtce.ArgumentEnumeratedData(
            name="MyEnum",
            encoding_type=None,
            enumerations=[_make_value_enumeration()],
        )

        round_tripped = xtce.ArgumentEnumeratedData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_rejects_empty_enumerations(self) -> None:
        """At least one enumeration is required."""
        with pytest.raises(ValidationError):
            xtce.ArgumentEnumeratedData(
                name="MyEnum", encoding_type=None, enumerations=[]
            )


class _ArrayDataForTest(xtce.ArrayData):
    """Concrete subclass exposing number_of_dimensions for v1.1 export.

    A real leaf subclass (e.g. a future ArrayParameter/ArrayArgument) is expected to
    supply this the same way, since ArrayData itself has no way to derive it.

    """

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, object]:
        return super()._to_v1_1_kwargs(policy, number_of_dimensions=1)


class TestArrayData:
    """Test ArrayData model (instantiated through a minimal concrete subclass)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal array data with no initial value.

        Uses a path-less reference since XTCE 1.1/1.2 only support NameReferenceType
        (no path) for array_type_ref.

        """
        original = _ArrayDataForTest(
            name="MyArray", array_type_ref=XtcePath("ElementType")
        )

        round_tripped = _ArrayDataForTest.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_round_trip_v1_3_with_initial_value(self) -> None:
        """Round-trip a v1.3 array data with an initial value.

        Only XTCE 1.3 supports an initial value for arrays.

        """
        original = _ArrayDataForTest(
            name="MyArray",
            array_type_ref=XtcePath("ElementType"),
            initial_value=[1, 2, 3],
        )

        round_tripped = _ArrayDataForTest.from_xsdata(
            original.to_xsdata(XtceVersion.V1_3), XtceVersion.V1_3
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", [XtceVersion.V1_1, XtceVersion.V1_2])
    def test_v1_1_and_v1_2_reject_initial_value(self, version: XtceVersion) -> None:
        """XTCE 1.1/1.2 do not support an initial value for arrays."""
        model = _ArrayDataForTest(
            name="MyArray",
            array_type_ref=XtcePath("ElementType"),
            initial_value=[1, 2, 3],
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(version)


class TestMember:
    """Test Member model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal member with no initial value."""
        original = xtce.Member(name="voltage", type_ref=XtcePath("FloatType"))

        round_tripped = xtce.Member.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    @pytest.mark.parametrize("version", BASE_VERSIONS)
    def test_round_trip_with_initial_value(self, version: XtceVersion) -> None:
        """Round-trip a member with an initial value.

        Only XTCE 1.2/1.3 support an initial value for aggregate members.

        """
        original = xtce.Member(
            name="voltage",
            type_ref=XtcePath("FloatType"),
            initial_value=1.5,
        )

        round_tripped = xtce.Member.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    def test_v1_1_rejects_initial_value(self) -> None:
        """XTCE 1.1 does not support an initial value for aggregate members."""
        model = xtce.Member(
            name="voltage",
            type_ref=XtcePath("FloatType"),
            initial_value=1.5,
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_1)

    def test_v1_1_rejects_short_description(self) -> None:
        """XTCE 1.1's Member type has no NameDescriptionType fields."""
        model = xtce.Member(
            name="voltage",
            type_ref=XtcePath("FloatType"),
            short_description="A description.",
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_1)


class TestAggregateData:
    """Test AggregateData model (instantiated directly)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal aggregate data with a single member."""
        original = xtce.AggregateData(
            name="MyAggregate",
            members=[xtce.Member(name="voltage", type_ref=XtcePath("FloatType"))],
        )

        round_tripped = xtce.AggregateData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_round_trip_v1_3_with_initial_value(self) -> None:
        """Round-trip a v1.3 aggregate data with an initial value.

        Only XTCE 1.3 supports an initial value for aggregates.

        """
        original = xtce.AggregateData(
            name="MyAggregate",
            members=[xtce.Member(name="voltage", type_ref=XtcePath("FloatType"))],
            initial_value={"voltage": 1.5},
        )

        round_tripped = xtce.AggregateData.from_xsdata(
            original.to_xsdata(XtceVersion.V1_3), XtceVersion.V1_3
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", [XtceVersion.V1_1, XtceVersion.V1_2])
    def test_v1_1_and_v1_2_reject_initial_value(self, version: XtceVersion) -> None:
        """XTCE 1.1/1.2 do not support an initial value for aggregates."""
        model = xtce.AggregateData(
            name="MyAggregate",
            members=[xtce.Member(name="voltage", type_ref=XtcePath("FloatType"))],
            initial_value={"voltage": 1.5},
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(version)

    def test_rejects_empty_members(self) -> None:
        """At least one member is required."""
        with pytest.raises(ValidationError):
            xtce.AggregateData(name="MyAggregate", members=[])


class TestBaseTimeData:
    """Test BaseTimeData model (instantiated directly)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal time data with only an encoding."""
        original = xtce.BaseTimeData(name="MyTime", encoding=_make_time_encoding())

        round_tripped = xtce.BaseTimeData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_reference_time(self, version: XtceVersion) -> None:
        """Round-trip a time data with a reference time."""
        original = xtce.BaseTimeData(
            name="MyTime",
            encoding=_make_time_encoding(),
            reference_time=_make_reference_time(),
        )

        round_tripped = xtce.BaseTimeData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", BASE_VERSIONS)
    def test_round_trip_with_base_type(self, version: XtceVersion) -> None:
        """Round-trip a time data with a base type.

        Only XTCE 1.2/1.3 support base_type on time data types.

        """
        original = xtce.BaseTimeData(
            name="MyTime",
            encoding=_make_time_encoding(),
            base_type=XtcePath("/TestSystem/OtherTimeType"),
        )

        round_tripped = xtce.BaseTimeData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_v1_1_rejects_base_type(self) -> None:
        """XTCE 1.1 does not support base_type on time data types."""
        model = xtce.BaseTimeData(
            name="MyTime",
            encoding=_make_time_encoding(),
            base_type=XtcePath("/TestSystem/OtherTimeType"),
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_1)


class TestArgumentBaseTimeData:
    """Test ArgumentBaseTimeData model (instantiated directly)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal argument time data with only an encoding."""
        original = xtce.ArgumentBaseTimeData(
            name="MyTime", encoding=_make_time_encoding()
        )

        round_tripped = xtce.ArgumentBaseTimeData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_reference_time(self, version: XtceVersion) -> None:
        """Round-trip an argument time data with a reference time."""
        original = xtce.ArgumentBaseTimeData(
            name="MyTime",
            encoding=_make_time_encoding(),
            reference_time=_make_reference_time(),
        )

        round_tripped = xtce.ArgumentBaseTimeData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestRelativeTimeData:
    """Test RelativeTimeData model (instantiated directly)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal relative time data with no initial value."""
        original = xtce.RelativeTimeData(name="MyTime", encoding=_make_time_encoding())

        round_tripped = xtce.RelativeTimeData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_initial_value(self, version: XtceVersion) -> None:
        """Round-trip a relative time data with an initial value."""
        original = xtce.RelativeTimeData(
            name="MyTime",
            encoding=_make_time_encoding(),
            initial_value=datetime.timedelta(days=1, seconds=5),
        )

        round_tripped = xtce.RelativeTimeData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestArgumentRelativeTimeData:
    """Test ArgumentRelativeTimeData model (instantiated directly)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal argument relative time data."""
        original = xtce.ArgumentRelativeTimeData(
            name="MyTime", encoding=_make_time_encoding()
        )

        round_tripped = xtce.ArgumentRelativeTimeData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_initial_value(self, version: XtceVersion) -> None:
        """Round-trip an argument relative time data with an initial value.

        XTCE 1.1 has no ArgumentRelativeTimeDataType, so this casts to
        RelativeTimeDataType.

        """
        original = xtce.ArgumentRelativeTimeData(
            name="MyTime",
            encoding=_make_time_encoding(),
            initial_value=datetime.timedelta(seconds=30),
        )

        round_tripped = xtce.ArgumentRelativeTimeData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestAbsoluteTimeData:
    """Test AbsoluteTimeData model (instantiated directly)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal absolute time data with no initial value."""
        original = xtce.AbsoluteTimeData(name="MyTime", encoding=_make_time_encoding())

        round_tripped = xtce.AbsoluteTimeData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_initial_value(self, version: XtceVersion) -> None:
        """Round-trip an absolute time data with an initial value."""
        original = xtce.AbsoluteTimeData(
            name="MyTime",
            encoding=_make_time_encoding(),
            initial_value=datetime.datetime(2024, 1, 2, 3, 4, 5),
        )

        round_tripped = xtce.AbsoluteTimeData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestArgumentAbsoluteTimeData:
    """Test ArgumentAbsoluteTimeData model (instantiated directly)."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal argument absolute time data."""
        original = xtce.ArgumentAbsoluteTimeData(
            name="MyTime", encoding=_make_time_encoding()
        )

        round_tripped = xtce.ArgumentAbsoluteTimeData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_initial_value(self, version: XtceVersion) -> None:
        """Round-trip an argument absolute time data with an initial value.

        XTCE 1.1 has no ArgumentAbsoluteTimeDataType, so this casts to
        AbsoluteTimeDataType.

        """
        original = xtce.ArgumentAbsoluteTimeData(
            name="MyTime",
            encoding=_make_time_encoding(),
            initial_value=datetime.datetime(2024, 1, 2, 3, 4, 5),
        )

        round_tripped = xtce.ArgumentAbsoluteTimeData.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original
