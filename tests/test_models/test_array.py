"""Test array models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from xtce_lib import (
    DowngradePolicy,
    XtceDowngradeError,
    XtcePath,
    XtceVersion,
    xtce,
)

SUPPORTED_ARRAY_VERSIONS = [XtceVersion.V1_2, XtceVersion.V1_3]
SUPPORTED_DIMENSION_VERSIONS = [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3]


def _make_parameter_instance_ref() -> xtce.ParameterInstanceRef:
    """Build a reusable parameter instance reference for array tests."""
    return xtce.ParameterInstanceRef(
        ref=XtcePath("/TestSystem/ParameterA"),
        instance=0,
        use_calibrated_value=True,
    )


def _make_argument_instance_ref() -> xtce.ArgumentInstanceRef:
    """Build a reusable argument instance reference for array tests."""
    return xtce.ArgumentInstanceRef(ref="ArgumentA", use_calibrated_value=False)


def _make_dynamic_value() -> xtce.DynamicValue:
    """Build a reusable dynamic value for array tests."""
    return xtce.DynamicValue(
        instance=_make_parameter_instance_ref(),
        linear_adjustment=xtce.LinearAdjustment(slope=2.5, intercept=1.0),
    )


def _make_argument_dynamic_value() -> xtce.ArgumentDynamicValue:
    """Build a reusable argument dynamic value for array tests."""
    return xtce.ArgumentDynamicValue(
        instance=_make_argument_instance_ref(),
        linear_adjustment=xtce.LinearAdjustment(slope=0.5, intercept=-2.0),
    )


def _make_discrete_lookup_list(default_value: int) -> xtce.DiscreteLookupList:
    """Build a reusable discrete lookup list for array tests."""
    return xtce.DiscreteLookupList(
        lookups=[
            xtce.DiscreteLookup(
                criteria=xtce.Comparison(
                    ref=XtcePath("/TestSystem/ParameterB"),
                    instance=0,
                    use_calibrated_value=True,
                    comparison_operator=xtce.ComparisonOperator.EQ,
                    value=1,
                ),
                value=7,
            )
        ],
        default_value=default_value,
    )


def _make_argument_discrete_lookup_list(
    default_value: int,
) -> xtce.ArgumentDiscreteLookupList:
    """Build a reusable argument discrete lookup list for array tests."""
    return xtce.ArgumentDiscreteLookupList(
        lookups=[
            xtce.ArgumentDiscreteLookup(
                criteria=xtce.ArgumentComparison(
                    instance_ref=_make_argument_instance_ref(),
                    comparison_operator=xtce.ComparisonOperator.GT,
                    value=1,
                ),
                value=7,
            )
        ],
        default_value=default_value,
    )


class TestDimension:
    """Test Dimension model."""

    @pytest.mark.parametrize("version", SUPPORTED_DIMENSION_VERSIONS)
    def test_round_trip_with_integer_indexes(self, version: XtceVersion) -> None:
        """Round-trip Dimension with static integer bounds."""
        original = xtce.Dimension(start_index=1, end_index=4)

        round_tripped = xtce.Dimension.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_ARRAY_VERSIONS)
    def test_round_trip_with_dynamic_indexes(self, version: XtceVersion) -> None:
        """Round-trip Dimension with a dynamic start index."""
        original = xtce.Dimension.model_construct(
            start_index=_make_dynamic_value(),
            end_index=6,
        )

        round_tripped = xtce.Dimension.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_ARRAY_VERSIONS)
    def test_round_trip_with_lookup_list_indexes(self, version: XtceVersion) -> None:
        """Round-trip Dimension with discrete lookup list bounds."""
        original = xtce.Dimension.model_construct(
            start_index=_make_discrete_lookup_list(0),
            end_index=_make_discrete_lookup_list(0),
        )

        if version == XtceVersion.V1_2:
            with pytest.raises(XtceDowngradeError):
                original.to_xsdata(version, DowngradePolicy.STRICT)

            return

        round_tripped = xtce.Dimension.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    def test_lookup_list_default_value_is_rejected_on_v1_2(self) -> None:
        """Reject Dimension downgrade when the lookup default would be lost."""
        original = xtce.Dimension.model_construct(
            start_index=_make_discrete_lookup_list(3),
            end_index=5,
        )

        with pytest.raises(XtceDowngradeError):
            original.to_xsdata(XtceVersion.V1_2, DowngradePolicy.STRICT)

    def test_round_trip_with_dynamic_index_on_v1_1(self) -> None:
        """Round-trip Dimension with a dynamic start index through XTCE v1.1."""
        original = xtce.Dimension.model_construct(
            start_index=_make_dynamic_value(),
            end_index=6,
        )

        round_tripped = xtce.Dimension.from_xsdata(
            original.to_xsdata(XtceVersion.V1_1),
            XtceVersion.V1_1,
        )

        assert round_tripped == original

    def test_rejects_descending_static_indexes(self) -> None:
        """Reject Dimension instances whose static bounds are inverted."""
        with pytest.raises(ValidationError):
            xtce.Dimension(start_index=4, end_index=3)


class TestArgumentDimension:
    """Test ArgumentDimension model."""

    @pytest.mark.parametrize("version", SUPPORTED_DIMENSION_VERSIONS)
    def test_round_trip_with_integer_indexes(self, version: XtceVersion) -> None:
        """Round-trip ArgumentDimension with static integer bounds."""
        original = xtce.ArgumentDimension(start_index=2, end_index=7)

        round_tripped = xtce.ArgumentDimension.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_ARRAY_VERSIONS)
    def test_round_trip_with_dynamic_indexes(self, version: XtceVersion) -> None:
        """Round-trip ArgumentDimension with a dynamic start index."""
        original = xtce.ArgumentDimension.model_construct(
            start_index=_make_argument_dynamic_value(),
            end_index=8,
        )

        round_tripped = xtce.ArgumentDimension.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_ARRAY_VERSIONS)
    def test_round_trip_with_lookup_list_indexes(self, version: XtceVersion) -> None:
        """Round-trip ArgumentDimension with discrete lookup list bounds."""
        original = xtce.ArgumentDimension.model_construct(
            start_index=_make_argument_discrete_lookup_list(0),
            end_index=_make_argument_discrete_lookup_list(0),
        )

        if version == XtceVersion.V1_2:
            with pytest.raises(XtceDowngradeError):
                original.to_xsdata(version, DowngradePolicy.STRICT)

            return

        round_tripped = xtce.ArgumentDimension.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    def test_lookup_list_default_value_is_rejected_on_v1_2(self) -> None:
        """Reject ArgumentDimension downgrade when the lookup default would be lost."""
        original = xtce.ArgumentDimension.model_construct(
            start_index=_make_argument_discrete_lookup_list(3),
            end_index=5,
        )

        with pytest.raises(XtceDowngradeError):
            original.to_xsdata(XtceVersion.V1_2, DowngradePolicy.STRICT)

    def test_round_trip_with_dynamic_index_on_v1_1(self) -> None:
        """Round-trip ArgumentDimension with a dynamic index through XTCE v1.1.

        v1.1 has no argument-specific dynamic value type, so the dynamic value must
        reference a parameter instance rather than an argument instance.
        """
        original = xtce.ArgumentDimension.model_construct(
            start_index=xtce.ArgumentDynamicValue(instance=_make_parameter_instance_ref()),
            end_index=8,
        )

        round_tripped = xtce.ArgumentDimension.from_xsdata(
            original.to_xsdata(XtceVersion.V1_1),
            XtceVersion.V1_1,
        )

        assert round_tripped == original

    def test_rejects_descending_static_indexes(self) -> None:
        """Reject ArgumentDimension instances whose static bounds are inverted."""
        with pytest.raises(ValidationError):
            xtce.ArgumentDimension(start_index=4, end_index=3)
