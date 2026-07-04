"""Test time models."""

import datetime

import pytest
from pydantic import ValidationError
from xsdata.models.datatype import XmlDate, XmlDateTime

from xtce_lib import (
    DowngradePolicy,
    XtceDowngradeError,
    XtcePath,
    XtceVersion,
    xtce,
)
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3


class TestTimeAssociation:
    """Test TimeAssociation model."""

    def test_accepts_fields(self) -> None:
        """TimeAssociation should accept supported fields and defaults."""
        model = xtce.TimeAssociation(
            ref=XtcePath("/SimpleSat/Clock/OnboardTime"),
            instance=2,
            use_calibrated_value=False,
            interpolate_time=False,
            offset=1.5,
            unit=xtce.TimeAssociationUnits.SECONDS,
        )

        assert model.ref == "/SimpleSat/Clock/OnboardTime"
        assert model.instance == 2
        assert model.use_calibrated_value is False
        assert model.interpolate_time is False
        assert model.offset == 1.5
        assert model.unit == xtce.TimeAssociationUnits.SECONDS

    @pytest.mark.parametrize(
        ("version", "raw_obj", "expected_offset", "expected_unit"),
        [
            (
                XtceVersion.V1_1,
                xtce_1_1.TimeAssociationType(
                    parameter_ref="/SimpleSat/Clock/OnboardTime",
                    instance=1,
                    use_calibrated_value=False,
                    interpolate_time=False,
                    offset=XmlDate.from_date(datetime.date(2020, 1, 1)),
                ),
                datetime.date(2020, 1, 1),
                xtce.TimeAssociationUnits.SECONDS,
            ),
            (
                XtceVersion.V1_2,
                xtce_1_2.TimeAssociationType(
                    parameter_ref="/SimpleSat/Clock/OnboardTime",
                    instance=1,
                    use_calibrated_value=False,
                    interpolate_time=False,
                    offset=2.5,
                    unit=xtce_1_2.TimeAssociationUnitType.MINUTE,
                ),
                2.5,
                xtce.TimeAssociationUnits.MINUTES,
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.TimeAssociationType(
                    parameter_ref="/SimpleSat/Clock/OnboardTime",
                    instance=1,
                    use_calibrated_value=False,
                    interpolate_time=False,
                    offset=3.5,
                    unit=xtce_1_3.TimeAssociationUnitType.HOURS,
                ),
                3.5,
                xtce.TimeAssociationUnits.HOURS,
            ),
        ],
    )
    def test_from_xsdata_for_each_version(
        self,
        version: XtceVersion,
        raw_obj: object,
        expected_offset: datetime.date | float,
        expected_unit: xtce.TimeAssociationUnits,
    ) -> None:
        """from_xsdata should map versioned TimeAssociationType objects."""
        model = xtce.TimeAssociation.from_xsdata(raw_obj, version)

        assert isinstance(model, xtce.TimeAssociation)
        assert model.ref == "/SimpleSat/Clock/OnboardTime"
        assert model.instance == 1
        assert model.use_calibrated_value is False
        assert model.interpolate_time is False
        assert model.offset == expected_offset
        assert model.unit == expected_unit

    def test_to_xsdata_v1_1(self) -> None:
        """to_xsdata should emit XTCE 1.1 TimeAssociationType."""
        model = xtce.TimeAssociation(
            ref=XtcePath("/SimpleSat/Clock/OnboardTime"),
            instance=1,
            use_calibrated_value=True,
            interpolate_time=True,
            offset=datetime.date(2020, 1, 2),
            unit=xtce.TimeAssociationUnits.SECONDS,
        )

        raw_obj = model.to_xsdata(XtceVersion.V1_1)

        assert isinstance(raw_obj, xtce_1_1.TimeAssociationType)
        assert raw_obj.parameter_ref == "/SimpleSat/Clock/OnboardTime"
        assert raw_obj.instance == 1
        assert raw_obj.use_calibrated_value is True
        assert raw_obj.interpolate_time is True
        assert raw_obj.offset == XmlDate.from_date(datetime.date(2020, 1, 2))

    def test_to_xsdata_v1_2(self) -> None:
        """to_xsdata should emit XTCE 1.2 TimeAssociationType."""
        model = xtce.TimeAssociation(
            ref=XtcePath("/SimpleSat/Clock/OnboardTime"),
            instance=2,
            use_calibrated_value=False,
            interpolate_time=False,
            offset=5.25,
            unit=xtce.TimeAssociationUnits.NANOSECONDS,
        )

        raw_obj = model.to_xsdata(XtceVersion.V1_2)

        assert isinstance(raw_obj, xtce_1_2.TimeAssociationType)
        assert raw_obj.parameter_ref == "/SimpleSat/Clock/OnboardTime"
        assert raw_obj.instance == 2
        assert raw_obj.use_calibrated_value is False
        assert raw_obj.interpolate_time is False
        assert raw_obj.offset == 5.25
        assert raw_obj.unit == xtce_1_2.TimeAssociationUnitType.SI_NANOSECOND

    def test_to_xsdata_v1_3(self) -> None:
        """to_xsdata should emit XTCE 1.3 TimeAssociationType."""
        model = xtce.TimeAssociation(
            ref=XtcePath("/SimpleSat/Clock/OnboardTime"),
            instance=-1,
            use_calibrated_value=True,
            interpolate_time=False,
            offset=7.0,
            unit=xtce.TimeAssociationUnits.MONTHS,
        )

        raw_obj = model.to_xsdata(XtceVersion.V1_3)

        assert isinstance(raw_obj, xtce_1_3.TimeAssociationType)
        assert raw_obj.parameter_ref == "/SimpleSat/Clock/OnboardTime"
        assert raw_obj.instance == -1
        assert raw_obj.use_calibrated_value is True
        assert raw_obj.interpolate_time is False
        assert raw_obj.offset == 7.0
        assert raw_obj.unit == xtce_1_3.TimeAssociationUnitType.MONTHS

    def test_to_xsdata_v1_2_strict_raises_for_unmapped_unit(self) -> None:
        """XTCE 1.2 strict downgrade should fail for unsupported units."""
        model = xtce.TimeAssociation(
            ref=XtcePath("/SimpleSat/Clock/OnboardTime"),
            offset=1.0,
            unit=xtce.TimeAssociationUnits.HOURS,
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_2, DowngradePolicy.STRICT)

    def test_to_xsdata_v1_2_non_strict_uses_unit_fallback(self) -> None:
        """XTCE 1.2 non-strict downgrade should use the documented fallback unit."""
        model = xtce.TimeAssociation(
            ref=XtcePath("/SimpleSat/Clock/OnboardTime"),
            offset=1.0,
            unit=xtce.TimeAssociationUnits.HOURS,
        )

        raw_obj = model.to_xsdata(XtceVersion.V1_2, DowngradePolicy.IGNORE)

        assert raw_obj.unit == xtce_1_2.TimeAssociationUnitType.SI_SECOND

    @pytest.mark.parametrize(
        "version",
        [XtceVersion.V1_2, XtceVersion.V1_3],
    )
    def test_round_trip_through_xsdata_preserves_float_offset(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve float-based time associations."""
        original = xtce.TimeAssociation(
            ref=XtcePath("/SimpleSat/Clock/OnboardTime"),
            instance=3,
            use_calibrated_value=False,
            interpolate_time=True,
            offset=4.5,
            unit=xtce.TimeAssociationUnits.SECONDS,
        )

        round_tripped = xtce.TimeAssociation.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    def test_round_trip_through_xsdata_preserves_date_offset_for_v1_1(self) -> None:
        """Round-trip conversion should preserve date-based v1.1 time associations."""
        original = xtce.TimeAssociation(
            ref=XtcePath("/SimpleSat/Clock/OnboardTime"),
            instance=0,
            use_calibrated_value=True,
            interpolate_time=True,
            offset=datetime.date(2021, 5, 6),
            unit=xtce.TimeAssociationUnits.SECONDS,
        )

        round_tripped = xtce.TimeAssociation.from_xsdata(
            original.to_xsdata(XtceVersion.V1_1),
            XtceVersion.V1_1,
        )

        assert round_tripped == original


class TestReferenceTime:
    """Test ReferenceTime model."""

    def test_accepts_epoch_value(self) -> None:
        """ReferenceTime should accept an epoch value."""
        model = xtce.ReferenceTime(epoch=datetime.date(2020, 1, 1))

        assert model.epoch == datetime.date(2020, 1, 1)
        assert model.offset_from is None

    def test_accepts_offset_from_value(self) -> None:
        """ReferenceTime should accept an offset_from value."""
        model = xtce.ReferenceTime(
            offset_from=xtce.ParameterInstanceRef(
                ref=XtcePath("/SimpleSat/Clock/OnboardTime"),
                instance=-1,
                use_calibrated_value=False,
            )
        )

        assert model.offset_from is not None
        assert model.offset_from.ref == "/SimpleSat/Clock/OnboardTime"
        assert model.epoch is None

    def test_rejects_when_both_epoch_and_offset_from_missing(self) -> None:
        """ReferenceTime requires one of epoch or offset_from."""
        with pytest.raises(ValidationError) as exc_info:
            xtce.ReferenceTime()

        assert "one of 'offset_from' and 'epoch' must be provided" in str(
            exc_info.value
        )

    def test_rejects_when_both_epoch_and_offset_from_provided(self) -> None:
        """ReferenceTime must not accept both epoch and offset_from together."""
        with pytest.raises(ValidationError) as exc_info:
            xtce.ReferenceTime(
                offset_from=xtce.ParameterInstanceRef(
                    ref=XtcePath("/SimpleSat/Clock/OnboardTime")
                ),
                epoch=xtce.EpochTime.UNIX,
            )

        assert "only one of 'offset_from' and 'epoch' can be provided" in str(
            exc_info.value
        )

    @pytest.mark.parametrize(
        ("version", "raw_obj", "expected_epoch"),
        [
            (
                XtceVersion.V1_1,
                xtce_1_1.ReferenceTimeType(
                    choice=XmlDate.from_date(datetime.date(2020, 1, 1))
                ),
                datetime.date(2020, 1, 1),
            ),
            (
                XtceVersion.V1_2,
                xtce_1_2.ReferenceTimeType(
                    choice=XmlDateTime.from_datetime(
                        datetime.datetime(2020, 1, 1, 12, 30, 0)
                    )
                ),
                datetime.datetime(2020, 1, 1, 12, 30, 0),
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.ReferenceTimeType(choice=xtce_1_3.EpochTimeEnumsType.J2000),
                xtce.EpochTime.J2000,
            ),
        ],
    )
    def test_from_xsdata_for_epoch_values(
        self,
        version: XtceVersion,
        raw_obj: object,
        expected_epoch: datetime.date | datetime.datetime | xtce.EpochTime,
    ) -> None:
        """from_xsdata should parse epoch values for each supported version."""
        model = xtce.ReferenceTime.from_xsdata(raw_obj, version)

        assert isinstance(model, xtce.ReferenceTime)
        assert model.offset_from is None
        assert model.epoch == expected_epoch

    @pytest.mark.parametrize(
        ("version", "raw_obj", "expected_type"),
        [
            (
                XtceVersion.V1_1,
                xtce_1_1.ReferenceTimeType(
                    choice=xtce_1_1.ParameterInstanceRefType(
                        parameter_ref="/SimpleSat/Clock/OnboardTime",
                        instance=2,
                        use_calibrated_value=False,
                    )
                ),
                xtce_1_1.ParameterInstanceRefType,
            ),
            (
                XtceVersion.V1_2,
                xtce_1_2.ReferenceTimeType(
                    choice=xtce_1_2.ParameterInstanceRefType(
                        parameter_ref="/SimpleSat/Clock/OnboardTime",
                        instance=2,
                        use_calibrated_value=False,
                    )
                ),
                xtce_1_2.ParameterInstanceRefType,
            ),
            (
                XtceVersion.V1_3,
                xtce_1_3.ReferenceTimeType(
                    choice=xtce_1_3.ParameterInstanceRefType(
                        parameter_ref="/SimpleSat/Clock/OnboardTime",
                        instance=2,
                        use_calibrated_value=False,
                    )
                ),
                xtce_1_3.ParameterInstanceRefType,
            ),
        ],
    )
    def test_from_xsdata_for_offset_from_values(
        self,
        version: XtceVersion,
        raw_obj: object,
        expected_type: type,
    ) -> None:
        """from_xsdata should parse offset-from references for each version."""
        model = xtce.ReferenceTime.from_xsdata(raw_obj, version)

        assert isinstance(model, xtce.ReferenceTime)
        assert model.epoch is None
        assert isinstance(model.offset_from.to_xsdata(version), expected_type)  # type: ignore[union-attr]
        assert model.offset_from.ref == "/SimpleSat/Clock/OnboardTime"  # type: ignore[union-attr]

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_1, xtce_1_1.ReferenceTimeType),
            (XtceVersion.V1_2, xtce_1_2.ReferenceTimeType),
            (XtceVersion.V1_3, xtce_1_3.ReferenceTimeType),
        ],
    )
    def test_to_xsdata_for_epoch_enum_each_version(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should emit versioned reference-time types for epoch enums."""
        model = xtce.ReferenceTime(epoch=xtce.EpochTime.TAI)

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_1, xtce_1_1.ReferenceTimeType),
            (XtceVersion.V1_2, xtce_1_2.ReferenceTimeType),
            (XtceVersion.V1_3, xtce_1_3.ReferenceTimeType),
        ],
    )
    def test_to_xsdata_for_offset_from_each_version(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should emit versioned reference-time types for offset_from."""
        model = xtce.ReferenceTime(
            offset_from=xtce.ParameterInstanceRef(
                ref=XtcePath("/SimpleSat/Clock/OnboardTime"),
                instance=-2,
                use_calibrated_value=False,
            )
        )

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert raw_obj.choice.parameter_ref == "/SimpleSat/Clock/OnboardTime"

    def test_to_xsdata_v1_1_accepts_datetime_epoch_in_strict_mode(self) -> None:
        """XTCE 1.1 export should accept datetime epochs (as date-compatible values)."""
        model = xtce.ReferenceTime(epoch=datetime.datetime(2020, 1, 1, 12, 0, 0))

        raw_obj = model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.STRICT)

        assert isinstance(raw_obj.choice, XmlDate)

    def test_to_xsdata_v1_1_datetime_epoch_allowed_in_ignore_mode(self) -> None:
        """XTCE 1.1 ignore downgrade should allow datetime epoch export."""
        model = xtce.ReferenceTime(epoch=datetime.datetime(2020, 1, 1, 12, 0, 0))

        raw_obj = model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.IGNORE)

        assert isinstance(raw_obj.choice, XmlDate)

    @pytest.mark.parametrize(
        ("version", "raw_obj"),
        [
            (XtceVersion.V1_1, xtce_1_1.ReferenceTimeType(choice=None)),
            (XtceVersion.V1_2, xtce_1_2.ReferenceTimeType(choice=None)),
            (XtceVersion.V1_3, xtce_1_3.ReferenceTimeType(choice=None)),
        ],
    )
    def test_from_xsdata_rejects_missing_choice(
        self,
        version: XtceVersion,
        raw_obj: object,
    ) -> None:
        """from_xsdata should fail when the XML contains neither OffsetFrom nor Epoch."""
        with pytest.raises(ValueError):
            xtce.ReferenceTime.from_xsdata(raw_obj, version)

    def test_round_trip_through_xsdata_preserves_v1_1_date_epoch(self) -> None:
        """Round-trip conversion should preserve v1.1 date epochs."""
        original = xtce.ReferenceTime(epoch=datetime.date(2022, 4, 5))

        round_tripped = xtce.ReferenceTime.from_xsdata(
            original.to_xsdata(XtceVersion.V1_1),
            XtceVersion.V1_1,
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", [XtceVersion.V1_2, XtceVersion.V1_3])
    def test_round_trip_through_xsdata_preserves_datetime_epoch(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve datetime epochs in XTCE 1.2/1.3."""
        original = xtce.ReferenceTime(epoch=datetime.datetime(2022, 4, 5, 6, 7, 8))

        round_tripped = xtce.ReferenceTime.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    @pytest.mark.parametrize(
        "version", [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3]
    )
    def test_round_trip_through_xsdata_preserves_offset_from(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve offset_from references."""
        original = xtce.ReferenceTime(
            offset_from=xtce.ParameterInstanceRef(
                ref=XtcePath("/SimpleSat/Clock/OnboardTime"),
                instance=1,
                use_calibrated_value=False,
            )
        )

        round_tripped = xtce.ReferenceTime.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    def test_time_association_schema_includes_unit_default(self) -> None:
        """Schema should expose unit default for TimeAssociation."""
        schema = xtce.TimeAssociation.model_json_schema()

        assert (
            schema["properties"]["unit"]["default"] == xtce.TimeAssociationUnits.SECONDS
        )

    def test_reference_time_schema_includes_epoch_examples(self) -> None:
        """Schema should expose example values for epoch field."""
        schema = xtce.ReferenceTime.model_json_schema()

        assert len(schema["properties"]["epoch"]["examples"]) == 3
