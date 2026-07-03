"""Test enum models."""

import pytest

from xtce_lib import (
    DowngradePolicy,
    XtceDowngradeError,
    XtceUnsupportedError,
    XtceVersion,
    xtce,
)
from xtce_lib.generated import xtce_1_2, xtce_1_3


class TestTimeUnits:
    """Tests for TimeUnits enum conversion behavior."""

    @pytest.mark.parametrize(
        ("raw_value", "expected"),
        [
            (xtce_1_2.TimeUnitsType.SECONDS, xtce.TimeUnits.SECONDS),
            (xtce_1_2.TimeUnitsType.PICO_SECONDS, xtce.TimeUnits.PICOSECONDS),
            (xtce_1_2.TimeUnitsType.DAYS, xtce.TimeUnits.DAYS),
            (xtce_1_2.TimeUnitsType.MONTHS, xtce.TimeUnits.MONTHS),
            (xtce_1_2.TimeUnitsType.YEARS, xtce.TimeUnits.YEARS),
        ],
    )
    def test_from_xsdata_v1_2(
        self, raw_value: object, expected: xtce.TimeUnits
    ) -> None:
        """XTCE 1.2 time-unit enums should map to unified TimeUnits."""
        result = xtce.TimeUnits.from_xsdata(raw_value, XtceVersion.V1_2)

        assert result == expected

    @pytest.mark.parametrize(
        ("raw_value", "expected"),
        [
            (xtce_1_3.TimeUnitsType.SECONDS, xtce.TimeUnits.SECONDS),
            (xtce_1_3.TimeUnitsType.MILLISECONDS, xtce.TimeUnits.MILLISECONDS),
            (xtce_1_3.TimeUnitsType.HOURS, xtce.TimeUnits.HOURS),
        ],
    )
    def test_from_xsdata_v1_3(
        self, raw_value: object, expected: xtce.TimeUnits
    ) -> None:
        """XTCE 1.3 time-unit enums should map to unified TimeUnits."""
        result = xtce.TimeUnits.from_xsdata(raw_value, XtceVersion.V1_3)

        assert result == expected

    def test_from_xsdata_v1_1_unsupported(self) -> None:
        """XTCE 1.1 import is unsupported for TimeUnits."""
        with pytest.raises(XtceUnsupportedError):
            xtce.TimeUnits.from_xsdata(xtce_1_2.TimeUnitsType.SECONDS, XtceVersion.V1_1)

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (xtce.TimeUnits.SECONDS, xtce_1_2.TimeUnitsType.SECONDS),
            (xtce.TimeUnits.PICOSECONDS, xtce_1_2.TimeUnitsType.PICO_SECONDS),
            (xtce.TimeUnits.DAYS, xtce_1_2.TimeUnitsType.DAYS),
        ],
    )
    def test_to_xsdata_v1_2_supported(
        self,
        value: xtce.TimeUnits,
        expected: xtce_1_2.TimeUnitsType,
    ) -> None:
        """Supported TimeUnits values should export directly to XTCE 1.2."""
        result = value.to_xsdata(XtceVersion.V1_2)

        assert result == expected

    def test_to_xsdata_v1_2_strict_raises_for_unmapped(self) -> None:
        """Unsupported XTCE 1.2 values should raise in strict downgrade mode."""
        with pytest.raises(XtceDowngradeError):
            xtce.TimeUnits.HOURS.to_xsdata(XtceVersion.V1_2, DowngradePolicy.STRICT)

    def test_to_xsdata_v1_2_non_strict_falls_back(self) -> None:
        """Unsupported XTCE 1.2 values should fall back in non-strict mode."""
        result = xtce.TimeUnits.HOURS.to_xsdata(
            XtceVersion.V1_2, DowngradePolicy.IGNORE
        )

        assert result == xtce_1_2.TimeUnitsType.SECONDS

    @pytest.mark.parametrize(
        "value",
        [
            xtce.TimeUnits.SECONDS,
            xtce.TimeUnits.MILLISECONDS,
            xtce.TimeUnits.HOURS,
            xtce.TimeUnits.MONTHS,
        ],
    )
    def test_to_xsdata_v1_3_round_trip(self, value: xtce.TimeUnits) -> None:
        """All TimeUnits values should export to XTCE 1.3 by value."""
        result = value.to_xsdata(XtceVersion.V1_3)

        assert result == xtce_1_3.TimeUnitsType(value.value)


class TestTimeAssociationUnits:
    """Tests for TimeAssociationUnits enum conversion behavior."""

    @pytest.mark.parametrize(
        ("raw_value", "expected"),
        [
            (
                xtce_1_2.TimeAssociationUnitType.SI_SECOND,
                xtce.TimeAssociationUnits.SECONDS,
            ),
            (
                xtce_1_2.TimeAssociationUnitType.SI_MILLSECOND,
                xtce.TimeAssociationUnits.MILLISECONDS,
            ),
            (
                xtce_1_2.TimeAssociationUnitType.MINUTE,
                xtce.TimeAssociationUnits.MINUTES,
            ),
            (
                xtce_1_2.TimeAssociationUnitType.JULIAN_YEAR,
                xtce.TimeAssociationUnits.YEARS,
            ),
        ],
    )
    def test_from_xsdata_v1_2(
        self,
        raw_value: object,
        expected: xtce.TimeAssociationUnits,
    ) -> None:
        """XTCE 1.2 time-association unit enums should map to unified enum values."""
        result = xtce.TimeAssociationUnits.from_xsdata(raw_value, XtceVersion.V1_2)

        assert result == expected

    @pytest.mark.parametrize(
        ("raw_value", "expected"),
        [
            (
                xtce_1_3.TimeAssociationUnitType.SECONDS,
                xtce.TimeAssociationUnits.SECONDS,
            ),
            (
                xtce_1_3.TimeAssociationUnitType.MICROSECONDS,
                xtce.TimeAssociationUnits.MICROSECONDS,
            ),
            (xtce_1_3.TimeAssociationUnitType.HOURS, xtce.TimeAssociationUnits.HOURS),
        ],
    )
    def test_from_xsdata_v1_3(
        self,
        raw_value: object,
        expected: xtce.TimeAssociationUnits,
    ) -> None:
        """XTCE 1.3 time-association unit enums should map to unified enum values."""
        result = xtce.TimeAssociationUnits.from_xsdata(raw_value, XtceVersion.V1_3)

        assert result == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (
                xtce.TimeAssociationUnits.SECONDS,
                xtce_1_2.TimeAssociationUnitType.SI_SECOND,
            ),
            (
                xtce.TimeAssociationUnits.NANOSECONDS,
                xtce_1_2.TimeAssociationUnitType.SI_NANOSECOND,
            ),
            (
                xtce.TimeAssociationUnits.MINUTES,
                xtce_1_2.TimeAssociationUnitType.MINUTE,
            ),
        ],
    )
    def test_to_xsdata_v1_2_supported(
        self,
        value: xtce.TimeAssociationUnits,
        expected: xtce_1_2.TimeAssociationUnitType,
    ) -> None:
        """Supported TimeAssociationUnits values should export directly to XTCE 1.2."""
        result = value.to_xsdata(XtceVersion.V1_2)

        assert result == expected

    def test_to_xsdata_v1_2_strict_raises_for_unmapped(self) -> None:
        """Unsupported XTCE 1.2 time-association values should raise in strict mode."""
        with pytest.raises(XtceDowngradeError):
            xtce.TimeAssociationUnits.HOURS.to_xsdata(
                XtceVersion.V1_2,
                DowngradePolicy.STRICT,
            )

    def test_to_xsdata_v1_2_non_strict_falls_back(self) -> None:
        """Unsupported XTCE 1.2 time-association values should fall back in non-strict mode."""
        result = xtce.TimeAssociationUnits.HOURS.to_xsdata(
            XtceVersion.V1_2,
            DowngradePolicy.IGNORE,
        )

        assert result == xtce_1_2.TimeAssociationUnitType.SI_SECOND

    @pytest.mark.parametrize(
        "value",
        [
            xtce.TimeAssociationUnits.SECONDS,
            xtce.TimeAssociationUnits.MILLISECONDS,
            xtce.TimeAssociationUnits.HOURS,
            xtce.TimeAssociationUnits.YEARS,
        ],
    )
    def test_to_xsdata_v1_3_round_trip(self, value: xtce.TimeAssociationUnits) -> None:
        """All TimeAssociationUnits values should export to XTCE 1.3 by value."""
        result = value.to_xsdata(XtceVersion.V1_3)

        assert result == xtce_1_3.TimeAssociationUnitType(value.value)
