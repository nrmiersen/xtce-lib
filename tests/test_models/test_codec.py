"""Test codec models."""

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

VERSIONS = [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3]
SUPPORTED_BASE_VERSIONS = [XtceVersion.V1_2, XtceVersion.V1_3]
RESTRICTED_LENGTH_VERSIONS = [XtceVersion.V1_1, XtceVersion.V1_2]


def _make_parameter_instance_ref(
    ref: str = "/TestSystem/ParameterA",
) -> xtce.ParameterInstanceRef:
    """Build a reusable parameter instance reference."""
    return xtce.ParameterInstanceRef(ref=XtcePath(ref), instance=0)


def _make_argument_instance_ref(ref: str = "ArgumentA") -> xtce.ArgumentInstanceRef:
    """Build a reusable argument instance reference."""
    return xtce.ArgumentInstanceRef(ref=ref)


def _make_calibrator() -> xtce.Calibrator:
    """Build a reusable simple calibrator."""
    return xtce.Calibrator(
        calibrator_type=xtce.PolynomialCalibrator(
            terms=[xtce.Term(coefficient=1.0, exponent=0)]
        )
    )


def _make_context_calibrator() -> xtce.ContextCalibrator:
    """Build a reusable context calibrator."""
    return xtce.ContextCalibrator(
        context_match=xtce.ContextMatch(
            criteria=xtce.Comparison(
                ref=XtcePath("/TestSystem/ParameterB"),
                instance=0,
                use_calibrated_value=True,
                comparison_operator=xtce.ComparisonOperator.EQ,
                value=1,
            )
        ),
        calibrator=_make_calibrator(),
    )


class TestDynamicValue:
    """Test DynamicValue model."""

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a dynamic value with no linear adjustment."""
        original = xtce.DynamicValue(instance=_make_parameter_instance_ref())

        round_tripped = xtce.DynamicValue.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_with_linear_adjustment(self, version: XtceVersion) -> None:
        """Round-trip a dynamic value with a linear adjustment."""
        original = xtce.DynamicValue(
            instance=_make_parameter_instance_ref(),
            linear_adjustment=xtce.LinearAdjustment(slope=2.0, intercept=1.5),
        )

        round_tripped = xtce.DynamicValue.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestArgumentDynamicValue:
    """Test ArgumentDynamicValue model."""

    def test_round_trip_v1_1_with_parameter_instance_ref(self) -> None:
        """Round-trip cast to XTCE 1.1's IntegerValueType.DynamicValue.

        XTCE 1.1 has no argument instance references, so the instance must be
        restricted to a parameter instance reference.

        """
        original = xtce.ArgumentDynamicValue(instance=_make_parameter_instance_ref())

        round_tripped = xtce.ArgumentDynamicValue.from_xsdata(
            original.to_xsdata(XtceVersion.V1_1), XtceVersion.V1_1
        )

        assert round_tripped == original

    def test_v1_1_strict_rejects_argument_instance_ref(self) -> None:
        """An ArgumentInstanceRef instance cannot be cast down to XTCE 1.1."""
        model = xtce.ArgumentDynamicValue(instance=_make_argument_instance_ref())

        with pytest.raises((XtceDowngradeError, TypeError)):
            model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.STRICT)

    @pytest.mark.parametrize("version", SUPPORTED_BASE_VERSIONS)
    def test_round_trip_with_parameter_instance_ref(self, version: XtceVersion) -> None:
        """Round-trip with a parameter instance reference through 1.2/1.3."""
        original = xtce.ArgumentDynamicValue(instance=_make_parameter_instance_ref())

        round_tripped = xtce.ArgumentDynamicValue.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_BASE_VERSIONS)
    def test_round_trip_with_argument_instance_ref(self, version: XtceVersion) -> None:
        """Round-trip with an argument instance reference through 1.2/1.3."""
        original = xtce.ArgumentDynamicValue(instance=_make_argument_instance_ref())

        round_tripped = xtce.ArgumentDynamicValue.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_with_linear_adjustment(self, version: XtceVersion) -> None:
        """Round-trip with a linear adjustment through every supported version."""
        original = xtce.ArgumentDynamicValue(
            instance=_make_parameter_instance_ref(),
            linear_adjustment=xtce.LinearAdjustment(slope=2.0, intercept=1.5),
        )

        round_tripped = xtce.ArgumentDynamicValue.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestLeadingSize:
    """Test LeadingSize model."""

    def test_default(self) -> None:
        """The default size_in_bits should be 16."""
        assert xtce.LeadingSize().size_in_bits == 16

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a leading size through each supported version."""
        original = xtce.LeadingSize(size_in_bits=8)

        round_tripped = xtce.LeadingSize.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestDataEncodingCommonFields:
    """Test DataEncoding's shared fields via the concrete IntegerDataEncoding
    subclass, since DataEncoding itself is abstract.
    """

    @pytest.mark.parametrize("version", VERSIONS)
    def test_error_detect_correct_none_round_trip(self, version: XtceVersion) -> None:
        """A None error_detect_correct should round-trip through every version."""
        original = xtce.IntegerDataEncoding(size_in_bits=16, byte_order=[1, 0])

        round_tripped = xtce.IntegerDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original
        assert round_tripped.error_detect_correct is None

    @pytest.mark.parametrize("version", SUPPORTED_BASE_VERSIONS)
    def test_error_detect_correct_single_entry_round_trip(
        self, version: XtceVersion
    ) -> None:
        """A single error_detect_correct entry should round-trip through 1.2/1.3."""
        original = xtce.IntegerDataEncoding(
            size_in_bits=16,
            error_detect_correct=[xtce.Checksum(name=xtce.ChecksumType.SUM8)],
        )

        round_tripped = xtce.IntegerDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_error_detect_correct_round_trip_v1_3_multiple_entries(self) -> None:
        """XTCE 1.3 allows more than one error_detect_correct entry, of any type."""
        original = xtce.IntegerDataEncoding(
            size_in_bits=16,
            error_detect_correct=[
                xtce.Checksum(name=xtce.ChecksumType.SUM8),
                xtce.CRC(polynomial=b"\x07", width=8),
                xtce.Parity(parity_form=xtce.ParityForm.EVEN),
                xtce.XOR(),
            ],
        )

        round_tripped = xtce.IntegerDataEncoding.from_xsdata(
            original.to_xsdata(XtceVersion.V1_3), XtceVersion.V1_3
        )

        assert round_tripped == original

    def test_error_detect_correct_is_unsupported_in_v1_1(self) -> None:
        """Checksum/CRC/Parity/XOR all lack XTCE 1.1 support, so export raises."""
        model = xtce.IntegerDataEncoding(
            size_in_bits=16,
            error_detect_correct=[xtce.Checksum(name=xtce.ChecksumType.SUM8)],
        )

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_1)

    @pytest.mark.parametrize("version", RESTRICTED_LENGTH_VERSIONS)
    def test_error_detect_correct_too_long_strict_raises(
        self, version: XtceVersion
    ) -> None:
        """More than one entry is not allowed in v1.1/v1.2 under STRICT policy."""
        model = xtce.IntegerDataEncoding(
            size_in_bits=16,
            error_detect_correct=[
                xtce.Checksum(name=xtce.ChecksumType.SUM8),
                xtce.Parity(parity_form=xtce.ParityForm.EVEN),
            ],
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(version, DowngradePolicy.STRICT)

    def test_error_detect_correct_too_long_ignore_uses_first_entry_v1_2(self) -> None:
        """Under IGNORE, only the first entry is kept when there are too many."""
        model = xtce.IntegerDataEncoding(
            size_in_bits=16,
            error_detect_correct=[
                xtce.Checksum(name=xtce.ChecksumType.SUM8),
                xtce.Parity(parity_form=xtce.ParityForm.EVEN),
            ],
        )

        raw_obj = model.to_xsdata(XtceVersion.V1_2, DowngradePolicy.IGNORE)

        round_tripped = xtce.IntegerDataEncoding.from_xsdata(raw_obj, XtceVersion.V1_2)
        assert round_tripped.error_detect_correct == [
            xtce.Checksum(name=xtce.ChecksumType.SUM8)
        ]

    @pytest.mark.parametrize("version", VERSIONS)
    def test_bit_order_round_trip(self, version: XtceVersion) -> None:
        """A non-default bit_order should round-trip through every version."""
        original = xtce.IntegerDataEncoding(
            size_in_bits=16,
            bit_order=xtce.BitOrder.LEAST_SIGNIFICANT_BIT_FIRST,
            byte_order=[1, 0],
        )

        round_tripped = xtce.IntegerDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_BASE_VERSIONS)
    def test_byte_order_endian_round_trip(self, version: XtceVersion) -> None:
        """An Endian byte_order should round-trip through 1.2/1.3.

        XTCE 1.1 has no big/little endian shortcut - see
        ``test_byte_order_endian_expands_to_explicit_list_in_v1_1``.

        """
        original = xtce.IntegerDataEncoding(
            size_in_bits=32, byte_order=xtce.Endian.LITTLE
        )

        round_tripped = xtce.IntegerDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", VERSIONS)
    def test_byte_order_custom_list_round_trip(self, version: XtceVersion) -> None:
        """A custom byte_order list should round-trip through every version."""
        original = xtce.IntegerDataEncoding(size_in_bits=32, byte_order=[0, 1, 2, 3])

        round_tripped = xtce.IntegerDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_byte_order_endian_expands_to_explicit_list_in_v1_1(self) -> None:
        """XTCE 1.1 has no Endian shortcut - it is expanded to an explicit byte list.

        This means an Endian byte_order does not round-trip identically through
        v1.1 (it comes back as the equivalent explicit list instead).

        """
        original = xtce.IntegerDataEncoding(size_in_bits=32, byte_order=xtce.Endian.BIG)

        round_tripped = xtce.IntegerDataEncoding.from_xsdata(
            original.to_xsdata(XtceVersion.V1_1), XtceVersion.V1_1
        )

        assert round_tripped.byte_order == [3, 2, 1, 0]


class TestIntegerDataEncoding:
    """Test IntegerDataEncoding model."""

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_with_external_dynamic_size(self, version: XtceVersion) -> None:
        """Round-trip the external dynamic-size sentinel."""
        original = xtce.IntegerDataEncoding(size_in_bits=-1)

        round_tripped = xtce.IntegerDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped.size_in_bits == -1

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal integer data encoding.

        Uses an explicit byte_order list rather than the default Endian value,
        since XTCE 1.1 expands Endian into an explicit list (see
        ``TestDataEncodingCommonFields.test_byte_order_endian_expands_to_explicit_list_in_v1_1``).

        """
        original = xtce.IntegerDataEncoding(byte_order=[0])

        round_tripped = xtce.IntegerDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_full(self, version: XtceVersion) -> None:
        """Round-trip an integer data encoding with a calibrator and context
        calibrators.
        """
        original = xtce.IntegerDataEncoding(
            encoding=xtce.IntegerEncoding.TWOS_COMPLEMENT,
            size_in_bits=32,
            byte_order=[3, 2, 1, 0],
            default_calibrator=_make_calibrator(),
            context_calibrators=[_make_context_calibrator()],
        )

        round_tripped = xtce.IntegerDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_BASE_VERSIONS)
    def test_round_trip_with_change_threshold(self, version: XtceVersion) -> None:
        """Round-trip a change_threshold through 1.2/1.3."""
        original = xtce.IntegerDataEncoding(size_in_bits=16, change_threshold=5)

        round_tripped = xtce.IntegerDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_to_v1_1_strict_rejects_change_threshold(self) -> None:
        """change_threshold is not supported in XTCE 1.1 and should raise in strict
        mode.
        """
        model = xtce.IntegerDataEncoding(size_in_bits=16, change_threshold=5)

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.STRICT)

    def test_from_v1_1_always_has_none_change_threshold(self) -> None:
        """XTCE 1.1 has no change_threshold, so it always comes back as None."""
        original = xtce.IntegerDataEncoding(size_in_bits=16)

        round_tripped = xtce.IntegerDataEncoding.from_xsdata(
            original.to_xsdata(XtceVersion.V1_1), XtceVersion.V1_1
        )

        assert round_tripped.change_threshold is None


class TestFloatDataEncoding:
    """Test FloatDataEncoding model."""

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal float data encoding."""
        original = xtce.FloatDataEncoding(byte_order=[3, 2, 1, 0])

        round_tripped = xtce.FloatDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_full(self, version: XtceVersion) -> None:
        """Round-trip a float data encoding with a calibrator and context
        calibrators.
        """
        original = xtce.FloatDataEncoding(
            encoding=xtce.FloatEncoding.IEEE754_1985,
            size_in_bits=64,
            byte_order=[7, 6, 5, 4, 3, 2, 1, 0],
            default_calibrator=_make_calibrator(),
            context_calibrators=[_make_context_calibrator()],
        )

        round_tripped = xtce.FloatDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_BASE_VERSIONS)
    def test_round_trip_with_change_threshold(self, version: XtceVersion) -> None:
        """Round-trip a change_threshold through 1.2/1.3."""
        original = xtce.FloatDataEncoding(size_in_bits=32, change_threshold=0.5)

        round_tripped = xtce.FloatDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_to_v1_1_strict_rejects_change_threshold(self) -> None:
        """change_threshold is not supported in XTCE 1.1 and should raise in strict
        mode.
        """
        model = xtce.FloatDataEncoding(size_in_bits=32, change_threshold=0.5)

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.STRICT)

    def test_to_v1_1_strict_rejects_unmapped_encoding(self) -> None:
        """XTCE 1.1 only supports IEEE754_1985/MILSTD_1750A - IEEE754 should raise
        in strict mode rather than crash with a raw ValueError.
        """
        model = xtce.FloatDataEncoding(
            size_in_bits=32, encoding=xtce.FloatEncoding.IEEE754
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.STRICT)

    def test_to_v1_1_ignore_falls_back_for_unmapped_encoding(self) -> None:
        """Under IGNORE, an unmapped encoding falls back to IEEE754_1985."""
        model = xtce.FloatDataEncoding(
            size_in_bits=32, encoding=xtce.FloatEncoding.IEEE754
        )

        raw_obj = model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.IGNORE)

        assert raw_obj.encoding.value == "IEEE754_1985"


class TestStringDataEncoding:
    """Test StringDataEncoding model."""

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_fixed_length_plain(self, version: XtceVersion) -> None:
        """Round-trip a fixed-length string with no terminator or leading size."""
        original = xtce.StringDataEncoding(allocation_size=64)

        round_tripped = xtce.StringDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_BASE_VERSIONS)
    def test_round_trip_fixed_length_with_termination_character(
        self, version: XtceVersion
    ) -> None:
        """Round-trip a fixed-length string with a termination character.

        XTCE 1.1 cannot combine a fixed size with a termination character (its
        SizeInBits choice is mutually exclusive), so only 1.2/1.3 are tested here.

        """
        original = xtce.StringDataEncoding(
            allocation_size=64, termination_character=b"\x00"
        )

        round_tripped = xtce.StringDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_BASE_VERSIONS)
    def test_round_trip_fixed_length_with_leading_size(
        self, version: XtceVersion
    ) -> None:
        """Round-trip a fixed-length string with a leading size.

        XTCE 1.1 cannot combine a fixed size with a leading size (its SizeInBits
        choice is mutually exclusive), so only 1.2/1.3 are tested here.

        """
        original = xtce.StringDataEncoding(
            allocation_size=64,
            leading_size=xtce.LeadingSize(size_in_bits=8),
            encoding=xtce.StringEncoding.UTF_16,
        )

        round_tripped = xtce.StringDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_to_v1_1_strict_rejects_termination_character_on_fixed_length(
        self,
    ) -> None:
        """A fixed-length string with a termination character cannot be cast down
        to XTCE 1.1.
        """
        model = xtce.StringDataEncoding(
            allocation_size=64, termination_character=b"\x00"
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.STRICT)

    def test_round_trip_variable_length_v1_1_with_termination_character(self) -> None:
        """XTCE 1.1 variable strings have no max_size_in_bits concept."""
        original = xtce.StringDataEncoding(
            allocation_size=None, termination_character=b"\x00"
        )

        round_tripped = xtce.StringDataEncoding.from_xsdata(
            original.to_xsdata(XtceVersion.V1_1), XtceVersion.V1_1
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_BASE_VERSIONS)
    def test_round_trip_variable_length_with_dynamic_value(
        self, version: XtceVersion
    ) -> None:
        """Round-trip a variable-length string with a dynamic allocation size."""
        original = xtce.StringDataEncoding(
            allocation_size=xtce.DynamicValue(instance=_make_parameter_instance_ref()),
            leading_size=xtce.LeadingSize(size_in_bits=8),
            max_size_in_bits=2048,
        )

        round_tripped = xtce.StringDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_round_trip_variable_length_with_discrete_lookup_list_v1_2(self) -> None:
        """Round-trip a variable-length string with a discrete lookup allocation
        size through XTCE 1.2 (no default_value support).
        """
        original = xtce.StringDataEncoding(
            allocation_size=xtce.DiscreteLookupList(
                lookups=[
                    xtce.DiscreteLookup(
                        criteria=xtce.Comparison(
                            ref=XtcePath("/TestSystem/ParameterA"),
                            instance=0,
                            use_calibrated_value=True,
                            comparison_operator=xtce.ComparisonOperator.EQ,
                            value=1,
                        ),
                        value=64,
                    )
                ]
            ),
            termination_character=b"\x00",
            max_size_in_bits=2048,
        )

        round_tripped = xtce.StringDataEncoding.from_xsdata(
            original.to_xsdata(XtceVersion.V1_2), XtceVersion.V1_2
        )

        assert round_tripped == original

    def test_round_trip_variable_length_with_discrete_lookup_list_v1_3(self) -> None:
        """Round-trip a variable-length string with a discrete lookup allocation
        size through XTCE 1.3 (default_value is required).
        """
        original = xtce.StringDataEncoding(
            allocation_size=xtce.DiscreteLookupList(
                lookups=[
                    xtce.DiscreteLookup(
                        criteria=xtce.Comparison(
                            ref=XtcePath("/TestSystem/ParameterA"),
                            instance=0,
                            use_calibrated_value=True,
                            comparison_operator=xtce.ComparisonOperator.EQ,
                            value=1,
                        ),
                        value=64,
                    )
                ],
                default_value=32,
            ),
            termination_character=b"\x00",
            max_size_in_bits=2048,
        )

        round_tripped = xtce.StringDataEncoding.from_xsdata(
            original.to_xsdata(XtceVersion.V1_3), XtceVersion.V1_3
        )

        assert round_tripped == original

    def test_to_v1_1_strict_rejects_max_size_in_bits(self) -> None:
        """max_size_in_bits is not supported in XTCE 1.1 and should raise in strict
        mode.
        """
        model = xtce.StringDataEncoding(
            allocation_size=None,
            termination_character=b"\x00",
            max_size_in_bits=1024,
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.STRICT)

    def test_to_v1_2_strict_rejects_unset_allocation_size(self) -> None:
        """XTCE 1.2 does not allow allocation_size to be left unset."""
        model = xtce.StringDataEncoding(
            allocation_size=None,
            termination_character=b"\x00",
            max_size_in_bits=1024,
        )

        with pytest.raises((XtceDowngradeError, TypeError)):
            model.to_xsdata(XtceVersion.V1_2, DowngradePolicy.STRICT)

    def test_validation_rejects_both_termination_character_and_leading_size(
        self,
    ) -> None:
        """A string cannot define both a termination character and a leading size."""
        with pytest.raises(ValueError):
            xtce.StringDataEncoding(
                allocation_size=64,
                termination_character=b"\x00",
                leading_size=xtce.LeadingSize(),
            )

    def test_validation_rejects_variable_string_without_terminator_or_leading_size(
        self,
    ) -> None:
        """A variable-length string must define a terminator or leading size."""
        with pytest.raises(ValueError):
            xtce.StringDataEncoding(allocation_size=None, max_size_in_bits=1024)


class TestArgumentStringDataEncoding:
    """Test ArgumentStringDataEncoding model."""

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_fixed_length_plain(self, version: XtceVersion) -> None:
        """Round-trip a fixed-length string with no terminator or leading size."""
        original = xtce.ArgumentStringDataEncoding(allocation_size=64)

        round_tripped = xtce.ArgumentStringDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_BASE_VERSIONS)
    def test_round_trip_fixed_length_with_termination_character(
        self, version: XtceVersion
    ) -> None:
        """Round-trip a fixed-length string with a termination character.

        XTCE 1.1 cannot combine a fixed size with a termination character (its
        SizeInBits choice is mutually exclusive), so only 1.2/1.3 are tested here.

        """
        original = xtce.ArgumentStringDataEncoding(
            allocation_size=64, termination_character=b"\x00"
        )

        round_tripped = xtce.ArgumentStringDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_BASE_VERSIONS)
    def test_round_trip_variable_length_with_argument_dynamic_value(
        self, version: XtceVersion
    ) -> None:
        """Round-trip a variable-length string with an argument dynamic allocation
        size, referencing an argument instance.

        This exercises the fix for a bug where ``_from_v1_3_kwargs`` constructed
        the non-Argument ``DynamicValue``/``DiscreteLookupList`` classes instead of
        the Argument variants.

        """
        original = xtce.ArgumentStringDataEncoding(
            allocation_size=xtce.ArgumentDynamicValue(
                instance=_make_argument_instance_ref()
            ),
            leading_size=xtce.LeadingSize(size_in_bits=8),
            max_size_in_bits=2048,
        )

        round_tripped = xtce.ArgumentStringDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_round_trip_variable_length_with_argument_discrete_lookup_list_v1_2(
        self,
    ) -> None:
        """Round-trip an argument discrete lookup allocation size through XTCE 1.2
        (no default_value support).
        """
        original = xtce.ArgumentStringDataEncoding(
            allocation_size=xtce.ArgumentDiscreteLookupList(
                lookups=[
                    xtce.ArgumentDiscreteLookup(
                        criteria=xtce.ArgumentComparison(
                            instance_ref=_make_argument_instance_ref(),
                            comparison_operator=xtce.ComparisonOperator.EQ,
                            value=1,
                        ),
                        value=64,
                    )
                ]
            ),
            termination_character=b"\x00",
            max_size_in_bits=2048,
        )

        round_tripped = xtce.ArgumentStringDataEncoding.from_xsdata(
            original.to_xsdata(XtceVersion.V1_2), XtceVersion.V1_2
        )

        assert round_tripped == original

    def test_round_trip_variable_length_with_argument_discrete_lookup_list_v1_3(
        self,
    ) -> None:
        """Round-trip an argument discrete lookup allocation size through XTCE 1.3
        (default_value is required).
        """
        original = xtce.ArgumentStringDataEncoding(
            allocation_size=xtce.ArgumentDiscreteLookupList(
                lookups=[
                    xtce.ArgumentDiscreteLookup(
                        criteria=xtce.ArgumentComparison(
                            instance_ref=_make_argument_instance_ref(),
                            comparison_operator=xtce.ComparisonOperator.EQ,
                            value=1,
                        ),
                        value=64,
                    )
                ],
                default_value=32,
            ),
            termination_character=b"\x00",
            max_size_in_bits=2048,
        )

        round_tripped = xtce.ArgumentStringDataEncoding.from_xsdata(
            original.to_xsdata(XtceVersion.V1_3), XtceVersion.V1_3
        )

        assert round_tripped == original

    def test_v1_1_strict_rejects_leading_size_with_dynamic_value(self) -> None:
        """XTCE 1.1 cannot combine a dynamic allocation size with a leading size.

        The model requires a leading_size/termination_character whenever
        allocation_size isn't a plain int, but XTCE 1.1's SizeInBits choice cannot
        represent a dynamic size alongside either marker - so this is always
        rejected when exporting to XTCE 1.1.

        """
        model = xtce.ArgumentStringDataEncoding(
            allocation_size=xtce.ArgumentDynamicValue(
                instance=_make_parameter_instance_ref()
            ),
            leading_size=xtce.LeadingSize(size_in_bits=8),
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.STRICT)

    def test_v1_1_strict_rejects_argument_backed_dynamic_value(self) -> None:
        """A dynamic allocation size referencing an argument cannot be cast down to
        XTCE 1.1.
        """
        model = xtce.ArgumentStringDataEncoding(
            allocation_size=xtce.ArgumentDynamicValue(
                instance=_make_argument_instance_ref()
            ),
            leading_size=xtce.LeadingSize(size_in_bits=8),
        )

        with pytest.raises((XtceDowngradeError, TypeError)):
            model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.STRICT)


class TestBinaryDataEncoding:
    """Test BinaryDataEncoding model."""

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_with_external_dynamic_size(self, version: XtceVersion) -> None:
        """Round-trip the external dynamic-size sentinel."""
        original = xtce.BinaryDataEncoding(size_in_bits=-1)

        round_tripped = xtce.BinaryDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_fixed_size(self, version: XtceVersion) -> None:
        """Round-trip a fixed-size binary data encoding."""
        original = xtce.BinaryDataEncoding(size_in_bits=64)

        round_tripped = xtce.BinaryDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_with_dynamic_value_size(self, version: XtceVersion) -> None:
        """Round-trip a binary data encoding with a dynamic size."""
        original = xtce.BinaryDataEncoding(
            size_in_bits=xtce.DynamicValue(instance=_make_parameter_instance_ref())
        )

        round_tripped = xtce.BinaryDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_with_transform_algorithms(self, version: XtceVersion) -> None:
        """Round-trip a binary data encoding with transform algorithms."""
        original = xtce.BinaryDataEncoding(
            size_in_bits=32,
            from_binary_transform_algorithm=xtce.InputAlgorithm(name="FromBinary"),
            to_binary_transform_algorithm=xtce.InputAlgorithm(name="ToBinary"),
        )

        round_tripped = xtce.BinaryDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestArgumentBinaryDataEncoding:
    """Test ArgumentBinaryDataEncoding model."""

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_with_external_dynamic_size(self, version: XtceVersion) -> None:
        """Round-trip the external dynamic-size sentinel."""
        original = xtce.ArgumentBinaryDataEncoding(size_in_bits=-1)

        round_tripped = xtce.ArgumentBinaryDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_fixed_size(self, version: XtceVersion) -> None:
        """Round-trip a fixed-size argument binary data encoding."""
        original = xtce.ArgumentBinaryDataEncoding(size_in_bits=64)

        round_tripped = xtce.ArgumentBinaryDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_with_parameter_backed_dynamic_value_size(
        self, version: XtceVersion
    ) -> None:
        """Round-trip a dynamic size referencing a parameter through every version.

        This exercises the fix for ``parse_argument_integer_value_v1_1`` (which
        previously always raised via the unsupported ``ArgumentDynamicValue``).

        """
        original = xtce.ArgumentBinaryDataEncoding(
            size_in_bits=xtce.ArgumentDynamicValue(
                instance=_make_parameter_instance_ref()
            )
        )

        round_tripped = xtce.ArgumentBinaryDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_BASE_VERSIONS)
    def test_round_trip_with_argument_backed_dynamic_value_size(
        self, version: XtceVersion
    ) -> None:
        """Round-trip a dynamic size referencing an argument through 1.2/1.3."""
        original = xtce.ArgumentBinaryDataEncoding(
            size_in_bits=xtce.ArgumentDynamicValue(
                instance=_make_argument_instance_ref()
            )
        )

        round_tripped = xtce.ArgumentBinaryDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_v1_1_strict_rejects_argument_backed_dynamic_value_size(self) -> None:
        """A dynamic size referencing an argument cannot be cast down to XTCE 1.1."""
        model = xtce.ArgumentBinaryDataEncoding(
            size_in_bits=xtce.ArgumentDynamicValue(
                instance=_make_argument_instance_ref()
            )
        )

        with pytest.raises((XtceDowngradeError, TypeError)):
            model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.STRICT)

    def test_round_trip_with_discrete_lookup_list_size_v1_2(self) -> None:
        """Round-trip an argument discrete-lookup-based size through XTCE 1.2 (no
        default_value support).
        """
        original = xtce.ArgumentBinaryDataEncoding(
            size_in_bits=xtce.ArgumentDiscreteLookupList(
                lookups=[
                    xtce.ArgumentDiscreteLookup(
                        criteria=xtce.ArgumentComparison(
                            instance_ref=_make_argument_instance_ref(),
                            comparison_operator=xtce.ComparisonOperator.EQ,
                            value=1,
                        ),
                        value=64,
                    )
                ]
            )
        )

        round_tripped = xtce.ArgumentBinaryDataEncoding.from_xsdata(
            original.to_xsdata(XtceVersion.V1_2), XtceVersion.V1_2
        )

        assert round_tripped == original

    def test_round_trip_with_discrete_lookup_list_size_v1_3(self) -> None:
        """Round-trip an argument discrete-lookup-based size through XTCE 1.3
        (default_value is required).
        """
        original = xtce.ArgumentBinaryDataEncoding(
            size_in_bits=xtce.ArgumentDiscreteLookupList(
                lookups=[
                    xtce.ArgumentDiscreteLookup(
                        criteria=xtce.ArgumentComparison(
                            instance_ref=_make_argument_instance_ref(),
                            comparison_operator=xtce.ComparisonOperator.EQ,
                            value=1,
                        ),
                        value=64,
                    )
                ],
                default_value=32,
            )
        )

        round_tripped = xtce.ArgumentBinaryDataEncoding.from_xsdata(
            original.to_xsdata(XtceVersion.V1_3), XtceVersion.V1_3
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_with_transform_algorithms(self, version: XtceVersion) -> None:
        """Round-trip an argument binary data encoding with transform algorithms.

        This exercises the fix where ``_from_v1_x_kwargs`` previously constructed
        plain ``InputAlgorithm`` instances instead of ``ArgumentInputAlgorithm``.

        """
        original = xtce.ArgumentBinaryDataEncoding(
            size_in_bits=32,
            from_binary_transform_algorithm=xtce.ArgumentInputAlgorithm(
                name="FromBinary"
            ),
            to_binary_transform_algorithm=xtce.ArgumentInputAlgorithm(name="ToBinary"),
        )

        round_tripped = xtce.ArgumentBinaryDataEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestTimeEncoding:
    """Test TimeEncoding model."""

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_with_integer_encoding(self, version: XtceVersion) -> None:
        """Round-trip a time encoding wrapping an integer data encoding.

        Uses an explicit byte_order list rather than an Endian value, since XTCE 1.1
        expands Endian into an explicit list (see
        ``test_byte_order_endian_expands_to_explicit_list_in_v1_1``).

        """
        original = xtce.TimeEncoding(
            encoding_type=xtce.IntegerDataEncoding(
                size_in_bits=32, byte_order=[3, 2, 1, 0]
            ),
            units=xtce.TimeUnits.SECONDS,
            scale=2.0,
            offset=1.5,
        )

        round_tripped = xtce.TimeEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_with_float_encoding(self, version: XtceVersion) -> None:
        """Round-trip a time encoding wrapping a float data encoding."""
        original = xtce.TimeEncoding(
            encoding_type=xtce.FloatDataEncoding(
                size_in_bits=64, byte_order=[7, 6, 5, 4, 3, 2, 1, 0]
            )
        )

        round_tripped = xtce.TimeEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_with_string_encoding(self, version: XtceVersion) -> None:
        """Round-trip a time encoding wrapping a fixed-length string encoding.

        Uses a plain fixed-length string with no terminator, since XTCE 1.1 cannot
        combine a fixed size with a termination character.

        """
        original = xtce.TimeEncoding(
            encoding_type=xtce.StringDataEncoding(allocation_size=64)
        )

        round_tripped = xtce.TimeEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_with_binary_encoding(self, version: XtceVersion) -> None:
        """Round-trip a time encoding wrapping a binary data encoding."""
        original = xtce.TimeEncoding(
            encoding_type=xtce.BinaryDataEncoding(size_in_bits=32)
        )

        round_tripped = xtce.TimeEncoding.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original
