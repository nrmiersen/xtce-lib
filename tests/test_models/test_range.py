"""Test range models."""

import pytest
from pydantic import ValidationError

from xtce_lib import XtceUnsupportedError, XtceVersion, xtce
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3


class TestIntegerRange:
    """Test IntegerRange model."""

    @pytest.mark.parametrize(
        ("min_inclusive", "max_inclusive"),
        [
            (0, 10),
            ("0x10", "0x20"),
            (None, 10),
            (-5, None),
        ],
    )
    def test_accepts_valid_ranges(
        self,
        min_inclusive: int | str | None,
        max_inclusive: int | str | None,
    ) -> None:
        """Integer ranges should accept valid min/max combinations."""
        model = xtce.IntegerRange(
            min_inclusive=min_inclusive, max_inclusive=max_inclusive
        )

        assert model.min_inclusive == min_inclusive
        assert model.max_inclusive == max_inclusive

    def test_rejects_missing_both_bounds(self) -> None:
        """At least one bound must be provided."""
        with pytest.raises(ValidationError) as exc_info:
            xtce.IntegerRange()

        assert "at least one of min_inclusive or max_inclusive must be set" in str(
            exc_info.value
        )

    def test_rejects_min_greater_than_max(self) -> None:
        """Minimum cannot exceed maximum after integer coercion."""
        with pytest.raises(ValidationError) as exc_info:
            xtce.IntegerRange(min_inclusive="0x20", max_inclusive="0x10")

        assert "minimum value (32) cannot be greater than maximum value (16)" in str(
            exc_info.value
        )

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_1,
                xtce_1_1.IntegerRangeType(min_inclusive="0x10", max_inclusive="0x20"),
            ),
            (
                XtceVersion.V1_2,
                xtce_1_2.IntegerRangeType(min_inclusive=16, max_inclusive=32),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.IntegerRangeType(min_inclusive=16, max_inclusive=32),
            ),
        ],
    )
    def test_from_xsdata_for_each_version(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should map versioned IntegerRangeType objects."""
        model = xtce.IntegerRange.from_xsdata(raw_obj, version)

        assert isinstance(model, xtce.IntegerRange)
        assert model.min_inclusive == 16
        assert model.max_inclusive == 32

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_1, xtce_1_1.IntegerRangeType),
            (XtceVersion.V1_2, xtce_1_2.IntegerRangeType),
            (XtceVersion.V1_3, xtce_1_3.IntegerRangeType),
        ],
    )
    def test_to_xsdata_for_each_version(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the expected versioned IntegerRangeType."""
        model = xtce.IntegerRange(min_inclusive="0x10", max_inclusive="0x20")

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        if version == XtceVersion.V1_1:
            assert raw_obj.min_inclusive == "0x10"
            assert raw_obj.max_inclusive == "0x20"
        else:
            assert raw_obj.min_inclusive == 16
            assert raw_obj.max_inclusive == 32

    @pytest.mark.parametrize(
        "version",
        [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3],
    )
    def test_round_trip_through_xsdata_preserves_bounds(
        self,
        version: XtceVersion,
    ) -> None:
        """Converting to xsdata and back should preserve equivalent bounds."""
        original = xtce.IntegerRange(min_inclusive=1, max_inclusive=10)

        round_tripped = xtce.IntegerRange.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestValidIntegerRange:
    """Test ValidIntegerRange model."""

    def test_accepts_applies_to_calibrated_field(self) -> None:
        """ValidIntegerRange should include applies_to_calibrated."""
        model = xtce.ValidIntegerRange(
            min_inclusive=0,
            max_inclusive=100,
            applies_to_calibrated=False,
        )

        assert model.min_inclusive == 0
        assert model.max_inclusive == 100
        assert model.applies_to_calibrated is False

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_2,
                xtce_1_2.IntegerDataType.ValidRange(
                    min_inclusive=5,
                    max_inclusive=15,
                    valid_range_applies_to_calibrated=False,
                ),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.IntegerDataType.ValidRange(
                    min_inclusive=5,
                    max_inclusive=15,
                    valid_range_applies_to_calibrated=False,
                ),
            ),
        ],
    )
    def test_from_xsdata_for_supported_versions(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should map supported versions to ValidIntegerRange."""
        model = xtce.ValidIntegerRange.from_xsdata(raw_obj, version)

        assert isinstance(model, xtce.ValidIntegerRange)
        assert model.min_inclusive == 5
        assert model.max_inclusive == 15
        assert model.applies_to_calibrated is False

    def test_from_xsdata_rejects_v1_1(self) -> None:
        """v1.1 does not support ValidIntegerRange."""
        with pytest.raises(XtceUnsupportedError):
            xtce.ValidIntegerRange.from_xsdata(
                xtce_1_2.IntegerDataType.ValidRange(
                    min_inclusive=1,
                    max_inclusive=2,
                    valid_range_applies_to_calibrated=True,
                ),
                XtceVersion.V1_1,
            )

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_2, xtce_1_2.IntegerDataType.ValidRange),
            (XtceVersion.V1_3, xtce_1_3.IntegerDataType.ValidRange),
        ],
    )
    def test_to_xsdata_for_supported_versions(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the expected supported valid integer type."""
        model = xtce.ValidIntegerRange(
            min_inclusive="0x10",
            max_inclusive="0x20",
            applies_to_calibrated=True,
        )

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert raw_obj.min_inclusive == 16
        assert raw_obj.max_inclusive == 32
        assert raw_obj.valid_range_applies_to_calibrated is True

    def test_to_xsdata_rejects_v1_1(self) -> None:
        """v1.1 export should fail for ValidIntegerRange."""
        model = xtce.ValidIntegerRange(
            min_inclusive=1,
            max_inclusive=2,
            applies_to_calibrated=True,
        )

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_1)

    @pytest.mark.parametrize("version", [XtceVersion.V1_2, XtceVersion.V1_3])
    def test_round_trip_through_xsdata_preserves_fields(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve all fields."""
        original = xtce.ValidIntegerRange(
            min_inclusive=1,
            max_inclusive=10,
            applies_to_calibrated=False,
        )

        round_tripped = xtce.ValidIntegerRange.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original


class TestValidIntegerRanges:
    """Test ValidIntegerRanges model."""

    def test_rejects_empty_ranges(self) -> None:
        """At least one valid range is required."""
        with pytest.raises(ValidationError):
            xtce.ValidIntegerRanges(valid_ranges=[])

    def test_accepts_multiple_ranges(self) -> None:
        """Multiple non-contiguous valid integer ranges should be supported."""
        model = xtce.ValidIntegerRanges(
            valid_ranges=[
                xtce.IntegerRange(min_inclusive=1, max_inclusive=5),
                xtce.IntegerRange(min_inclusive=10, max_inclusive=20),
            ],
            applies_to_calibrated=False,
        )

        assert len(model.valid_ranges) == 2
        assert model.applies_to_calibrated is False

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_2,
                xtce_1_2.ValidIntegerRangeSetType(
                    valid_range=[
                        xtce_1_2.IntegerRangeType(min_inclusive=1, max_inclusive=5),
                        xtce_1_2.IntegerRangeType(min_inclusive=10, max_inclusive=20),
                    ],
                    valid_range_applies_to_calibrated=False,
                ),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.ValidIntegerRangeSetType(
                    valid_range=[
                        xtce_1_3.IntegerRangeType(min_inclusive=1, max_inclusive=5),
                        xtce_1_3.IntegerRangeType(min_inclusive=10, max_inclusive=20),
                    ],
                    valid_range_applies_to_calibrated=False,
                ),
            ),
        ],
    )
    def test_from_xsdata_for_supported_versions(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should map supported versions to ValidIntegerRanges."""
        model = xtce.ValidIntegerRanges.from_xsdata(raw_obj, version)

        assert isinstance(model, xtce.ValidIntegerRanges)
        assert len(model.valid_ranges) == 2
        assert model.valid_ranges[0].min_inclusive == 1
        assert model.valid_ranges[0].max_inclusive == 5
        assert model.valid_ranges[1].min_inclusive == 10
        assert model.valid_ranges[1].max_inclusive == 20
        assert model.applies_to_calibrated is False

    def test_from_xsdata_rejects_v1_1(self) -> None:
        """v1.1 does not support ValidIntegerRanges."""
        with pytest.raises(XtceUnsupportedError):
            xtce.ValidIntegerRanges.from_xsdata(
                xtce_1_2.ValidIntegerRangeSetType(
                    valid_range=[
                        xtce_1_2.IntegerRangeType(min_inclusive=1, max_inclusive=2),
                    ],
                    valid_range_applies_to_calibrated=True,
                ),
                XtceVersion.V1_1,
            )

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_2, xtce_1_2.ValidIntegerRangeSetType),
            (XtceVersion.V1_3, xtce_1_3.ValidIntegerRangeSetType),
        ],
    )
    def test_to_xsdata_for_supported_versions(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the expected supported range-set type."""
        model = xtce.ValidIntegerRanges(
            valid_ranges=[
                xtce.IntegerRange(min_inclusive="0x1", max_inclusive="0x5"),
                xtce.IntegerRange(min_inclusive=10, max_inclusive=20),
            ],
            applies_to_calibrated=True,
        )

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert len(raw_obj.valid_range) == 2
        assert raw_obj.valid_range[0].min_inclusive == 1
        assert raw_obj.valid_range[0].max_inclusive == 5
        assert raw_obj.valid_range[1].min_inclusive == 10
        assert raw_obj.valid_range[1].max_inclusive == 20
        assert raw_obj.valid_range_applies_to_calibrated is True

    def test_to_xsdata_rejects_v1_1(self) -> None:
        """v1.1 export should fail for ValidIntegerRanges."""
        model = xtce.ValidIntegerRanges(
            valid_ranges=[xtce.IntegerRange(min_inclusive=1, max_inclusive=2)],
            applies_to_calibrated=True,
        )

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_1)

    @pytest.mark.parametrize("version", [XtceVersion.V1_2, XtceVersion.V1_3])
    def test_round_trip_through_xsdata_preserves_fields(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve all fields."""
        original = xtce.ValidIntegerRanges(
            valid_ranges=[
                xtce.IntegerRange(min_inclusive=1, max_inclusive=2),
                xtce.IntegerRange(min_inclusive=5, max_inclusive=6),
            ],
            applies_to_calibrated=False,
        )

        round_tripped = xtce.ValidIntegerRanges.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original


class TestFloatRange:
    """Test FloatRange model."""

    @pytest.mark.parametrize(
        ("kwargs",),
        [
            ({"min_inclusive": 1.0, "max_inclusive": 2.0},),
            ({"min_exclusive": 1.0, "max_inclusive": 2.0},),
            ({"min_inclusive": 1.0, "max_exclusive": 2.0},),
            ({"max_inclusive": 2.0},),
            ({"min_exclusive": -1.0},),
        ],
    )
    def test_accepts_valid_ranges(self, kwargs: dict[str, float]) -> None:
        """Float ranges should accept valid inclusive/exclusive combinations."""
        model = xtce.FloatRange(**kwargs)

        for key, value in kwargs.items():
            assert getattr(model, key) == value

    def test_rejects_both_min_bounds(self) -> None:
        """Only one minimum bound option may be set."""
        with pytest.raises(ValidationError) as exc_info:
            xtce.FloatRange(min_inclusive=1.0, min_exclusive=1.1, max_inclusive=2.0)

        assert "only one of min_inclusive and min_exclusive can be set" in str(
            exc_info.value
        )

    def test_rejects_both_max_bounds(self) -> None:
        """Only one maximum bound option may be set."""
        with pytest.raises(ValidationError) as exc_info:
            xtce.FloatRange(min_inclusive=1.0, max_inclusive=2.0, max_exclusive=1.9)

        assert "only one of max_inclusive and max_exclusive can be set" in str(
            exc_info.value
        )

    def test_rejects_missing_both_sides(self) -> None:
        """At least one minimum or maximum bound must be provided."""
        with pytest.raises(ValidationError) as exc_info:
            xtce.FloatRange()

        assert "at least one of the minimum or maximum values must be set" in str(
            exc_info.value
        )

    def test_rejects_min_greater_than_max(self) -> None:
        """Minimum bound cannot exceed maximum bound."""
        with pytest.raises(ValidationError) as exc_info:
            xtce.FloatRange(min_exclusive=10.0, max_inclusive=1.0)

        assert "minimum value (10.0) cannot be greater than maximum value (1.0)" in str(
            exc_info.value
        )

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_1,
                xtce_1_1.FloatRangeType(
                    min_inclusive=1.0,
                    min_exclusive=None,
                    max_inclusive=2.0,
                    max_exclusive=None,
                ),
            ),
            (
                XtceVersion.V1_2,
                xtce_1_2.FloatRangeType(
                    min_inclusive=1.0,
                    min_exclusive=None,
                    max_inclusive=2.0,
                    max_exclusive=None,
                ),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.FloatRangeType(
                    min_inclusive=1.0,
                    min_exclusive=None,
                    max_inclusive=2.0,
                    max_exclusive=None,
                ),
            ),
        ],
    )
    def test_from_xsdata_for_each_version(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should map versioned FloatRangeType objects."""
        model = xtce.FloatRange.from_xsdata(raw_obj, version)

        assert isinstance(model, xtce.FloatRange)
        assert model.min_inclusive == 1.0
        assert model.max_inclusive == 2.0
        assert model.min_exclusive is None
        assert model.max_exclusive is None

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_1, xtce_1_1.FloatRangeType),
            (XtceVersion.V1_2, xtce_1_2.FloatRangeType),
            (XtceVersion.V1_3, xtce_1_3.FloatRangeType),
        ],
    )
    def test_to_xsdata_for_each_version(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the expected versioned FloatRangeType."""
        model = xtce.FloatRange(min_exclusive=0.5, max_exclusive=1.5)

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert raw_obj.min_exclusive == 0.5
        assert raw_obj.max_exclusive == 1.5
        assert raw_obj.min_inclusive is None
        assert raw_obj.max_inclusive is None

    @pytest.mark.parametrize(
        "version",
        [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3],
    )
    def test_round_trip_through_xsdata_preserves_bounds(
        self,
        version: XtceVersion,
    ) -> None:
        """Converting to xsdata and back should preserve bounds."""
        original = xtce.FloatRange(min_inclusive=-1.25, max_exclusive=4.5)

        round_tripped = xtce.FloatRange.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestValidFloatRange:
    """Test ValidFloatRange model."""

    def test_accepts_applies_to_calibrated_field(self) -> None:
        """ValidFloatRange should include applies_to_calibrated."""
        model = xtce.ValidFloatRange(
            min_inclusive=0.0,
            max_inclusive=100.0,
            applies_to_calibrated=False,
        )

        assert model.min_inclusive == 0.0
        assert model.max_inclusive == 100.0
        assert model.applies_to_calibrated is False

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_2,
                xtce_1_2.FloatDataType.ValidRange(
                    min_inclusive=1.0,
                    min_exclusive=None,
                    max_inclusive=None,
                    max_exclusive=5.0,
                    valid_range_applies_to_calibrated=False,
                ),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.FloatDataType.ValidRange(
                    min_inclusive=1.0,
                    min_exclusive=None,
                    max_inclusive=None,
                    max_exclusive=5.0,
                    valid_range_applies_to_calibrated=False,
                ),
            ),
        ],
    )
    def test_from_xsdata_for_supported_versions(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should map supported versions to ValidFloatRange."""
        model = xtce.ValidFloatRange.from_xsdata(raw_obj, version)

        assert isinstance(model, xtce.ValidFloatRange)
        assert model.min_inclusive == 1.0
        assert model.max_exclusive == 5.0
        assert model.applies_to_calibrated is False

    def test_from_xsdata_rejects_v1_1(self) -> None:
        """v1.1 does not support ValidFloatRange."""
        with pytest.raises(XtceUnsupportedError):
            xtce.ValidFloatRange.from_xsdata(
                xtce_1_2.FloatDataType.ValidRange(
                    min_inclusive=1.0,
                    min_exclusive=None,
                    max_inclusive=2.0,
                    max_exclusive=None,
                    valid_range_applies_to_calibrated=True,
                ),
                XtceVersion.V1_1,
            )

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_2, xtce_1_2.FloatDataType.ValidRange),
            (XtceVersion.V1_3, xtce_1_3.FloatDataType.ValidRange),
        ],
    )
    def test_to_xsdata_for_supported_versions(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the expected supported valid float type."""
        model = xtce.ValidFloatRange(
            min_exclusive=1.5,
            max_inclusive=10.0,
            applies_to_calibrated=True,
        )

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert raw_obj.min_exclusive == 1.5
        assert raw_obj.max_inclusive == 10.0
        assert raw_obj.valid_range_applies_to_calibrated is True

    def test_to_xsdata_rejects_v1_1(self) -> None:
        """v1.1 export should fail for ValidFloatRange."""
        model = xtce.ValidFloatRange(min_inclusive=1.0, max_inclusive=2.0)

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_1)

    @pytest.mark.parametrize("version", [XtceVersion.V1_2, XtceVersion.V1_3])
    def test_round_trip_through_xsdata_preserves_fields(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve all fields."""
        original = xtce.ValidFloatRange(
            min_inclusive=-5.0,
            max_exclusive=1.0,
            applies_to_calibrated=False,
        )

        round_tripped = xtce.ValidFloatRange.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original


class TestValidFloatRanges:
    """Test ValidFloatRanges model."""

    def test_rejects_empty_ranges(self) -> None:
        """At least one valid range is required."""
        with pytest.raises(ValidationError):
            xtce.ValidFloatRanges(valid_ranges=[])

    def test_accepts_multiple_ranges(self) -> None:
        """Multiple non-contiguous valid float ranges should be supported."""
        model = xtce.ValidFloatRanges(
            valid_ranges=[
                xtce.FloatRange(min_inclusive=0.0, max_inclusive=1.0),
                xtce.FloatRange(min_exclusive=5.0, max_exclusive=6.0),
            ],
            applies_to_calibrated=False,
        )

        assert len(model.valid_ranges) == 2
        assert model.applies_to_calibrated is False

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_2,
                xtce_1_2.ValidFloatRangeSetType(
                    valid_range=[
                        xtce_1_2.FloatRangeType(
                            min_inclusive=0.0,
                            min_exclusive=None,
                            max_inclusive=1.0,
                            max_exclusive=None,
                        ),
                        xtce_1_2.FloatRangeType(
                            min_inclusive=None,
                            min_exclusive=5.0,
                            max_inclusive=None,
                            max_exclusive=6.0,
                        ),
                    ],
                    valid_range_applies_to_calibrated=False,
                ),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.ValidFloatRangeSetType(
                    valid_range=[
                        xtce_1_3.FloatRangeType(
                            min_inclusive=0.0,
                            min_exclusive=None,
                            max_inclusive=1.0,
                            max_exclusive=None,
                        ),
                        xtce_1_3.FloatRangeType(
                            min_inclusive=None,
                            min_exclusive=5.0,
                            max_inclusive=None,
                            max_exclusive=6.0,
                        ),
                    ],
                    valid_range_applies_to_calibrated=False,
                ),
            ),
        ],
    )
    def test_from_xsdata_for_supported_versions(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should map supported versions to ValidFloatRanges."""
        model = xtce.ValidFloatRanges.from_xsdata(raw_obj, version)

        assert isinstance(model, xtce.ValidFloatRanges)
        assert len(model.valid_ranges) == 2
        assert model.valid_ranges[0].min_inclusive == 0.0
        assert model.valid_ranges[0].max_inclusive == 1.0
        assert model.valid_ranges[1].min_exclusive == 5.0
        assert model.valid_ranges[1].max_exclusive == 6.0
        assert model.applies_to_calibrated is False

    def test_from_xsdata_rejects_v1_1(self) -> None:
        """v1.1 does not support ValidFloatRanges."""
        with pytest.raises(XtceUnsupportedError):
            xtce.ValidFloatRanges.from_xsdata(
                xtce_1_2.ValidFloatRangeSetType(
                    valid_range=[
                        xtce_1_2.FloatRangeType(
                            min_inclusive=1.0,
                            min_exclusive=None,
                            max_inclusive=2.0,
                            max_exclusive=None,
                        ),
                    ],
                    valid_range_applies_to_calibrated=True,
                ),
                XtceVersion.V1_1,
            )

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_2, xtce_1_2.ValidFloatRangeSetType),
            (XtceVersion.V1_3, xtce_1_3.ValidFloatRangeSetType),
        ],
    )
    def test_to_xsdata_for_supported_versions(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the expected supported float range-set type."""
        model = xtce.ValidFloatRanges(
            valid_ranges=[
                xtce.FloatRange(min_inclusive=0.0, max_inclusive=1.0),
                xtce.FloatRange(min_exclusive=5.0, max_exclusive=6.0),
            ],
            applies_to_calibrated=True,
        )

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert len(raw_obj.valid_range) == 2
        assert raw_obj.valid_range[0].min_inclusive == 0.0
        assert raw_obj.valid_range[0].max_inclusive == 1.0
        assert raw_obj.valid_range[1].min_exclusive == 5.0
        assert raw_obj.valid_range[1].max_exclusive == 6.0
        assert raw_obj.valid_range_applies_to_calibrated is True

    def test_to_xsdata_rejects_v1_1(self) -> None:
        """v1.1 export should fail for ValidFloatRanges."""
        model = xtce.ValidFloatRanges(
            valid_ranges=[xtce.FloatRange(min_inclusive=1.0, max_inclusive=2.0)],
            applies_to_calibrated=True,
        )

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_1)

    @pytest.mark.parametrize("version", [XtceVersion.V1_2, XtceVersion.V1_3])
    def test_round_trip_through_xsdata_preserves_fields(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve all fields."""
        original = xtce.ValidFloatRanges(
            valid_ranges=[
                xtce.FloatRange(min_inclusive=0.0, max_inclusive=1.0),
                xtce.FloatRange(min_exclusive=2.0, max_exclusive=3.0),
            ],
            applies_to_calibrated=False,
        )

        round_tripped = xtce.ValidFloatRanges.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original


class TestMultiRange:
    """Test MultiRange model."""

    def test_accepts_fields_and_defaults(self) -> None:
        """MultiRange should accept level and default range_form to OUTSIDE."""
        model = xtce.MultiRange(
            min_inclusive=0.0, max_inclusive=1.0, level=xtce.ConcernLevel.WARNING
        )

        assert model.min_inclusive == 0.0
        assert model.max_inclusive == 1.0
        assert model.range_form == xtce.RangeForm.OUTSIDE
        assert model.level == xtce.ConcernLevel.WARNING

    def test_accepts_explicit_range_form(self) -> None:
        """MultiRange should support explicit range_form values."""
        model = xtce.MultiRange(
            min_exclusive=1.0,
            max_exclusive=2.0,
            range_form=xtce.RangeForm.INSIDE,
            level=xtce.ConcernLevel.CRITICAL,
        )

        assert model.range_form == xtce.RangeForm.INSIDE
        assert model.level == xtce.ConcernLevel.CRITICAL

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (
                XtceVersion.V1_2,
                xtce_1_2.MultiRangeType(
                    min_inclusive=None,
                    min_exclusive=1.0,
                    max_inclusive=None,
                    max_exclusive=2.0,
                    range_form=xtce_1_2.RangeFormType.INSIDE,
                    level=xtce_1_2.ConcernLevelsType.WARNING,
                ),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.MultiRangeType(
                    min_inclusive=None,
                    min_exclusive=1.0,
                    max_inclusive=None,
                    max_exclusive=2.0,
                    range_form=xtce_1_3.RangeFormType.INSIDE,
                    level=xtce_1_3.ConcernLevelsType.WARNING,
                ),
            ),
        ],
    )
    def test_from_xsdata_for_supported_versions(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should map supported versions to MultiRange."""
        model = xtce.MultiRange.from_xsdata(raw_obj, version)

        assert isinstance(model, xtce.MultiRange)
        assert model.min_exclusive == 1.0
        assert model.max_exclusive == 2.0
        assert model.range_form == xtce.RangeForm.INSIDE
        assert model.level == xtce.ConcernLevel.WARNING

    def test_from_xsdata_rejects_v1_1(self) -> None:
        """v1.1 does not support MultiRange."""
        with pytest.raises(XtceUnsupportedError):
            xtce.MultiRange.from_xsdata(
                xtce_1_2.MultiRangeType(
                    min_inclusive=0.0,
                    min_exclusive=None,
                    max_inclusive=1.0,
                    max_exclusive=None,
                    range_form=xtce_1_2.RangeFormType.OUTSIDE,
                    level=xtce_1_2.ConcernLevelsType.CRITICAL,
                ),
                XtceVersion.V1_1,
            )

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_2, xtce_1_2.MultiRangeType),
            (XtceVersion.V1_3, xtce_1_3.MultiRangeType),
        ],
    )
    def test_to_xsdata_for_supported_versions(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the expected supported MultiRangeType."""
        model = xtce.MultiRange(
            min_inclusive=0.0,
            max_inclusive=1.0,
            range_form=xtce.RangeForm.OUTSIDE,
            level=xtce.ConcernLevel.DISTRESS,
        )

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert raw_obj.min_inclusive == 0.0
        assert raw_obj.max_inclusive == 1.0
        assert raw_obj.range_form.value == xtce.RangeForm.OUTSIDE.value
        assert xtce.unwrap(raw_obj.level).value == xtce.ConcernLevel.DISTRESS.value

    def test_to_xsdata_rejects_v1_1(self) -> None:
        """v1.1 export should fail for MultiRange."""
        model = xtce.MultiRange(
            min_inclusive=0.0, max_inclusive=1.0, level=xtce.ConcernLevel.WARNING
        )

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_1)

    @pytest.mark.parametrize("version", [XtceVersion.V1_2, XtceVersion.V1_3])
    def test_round_trip_through_xsdata_preserves_fields(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve all fields."""
        original = xtce.MultiRange(
            min_exclusive=-1.0,
            max_exclusive=5.0,
            range_form=xtce.RangeForm.INSIDE,
            level=xtce.ConcernLevel.CRITICAL,
        )

        round_tripped = xtce.MultiRange.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original
