"""Test container models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from xtce_lib import (
    XtceDowngradeError,
    XtcePath,
    XtceUnsupportedError,
    XtceVersion,
    xtce,
)
from xtce_lib.xtce._base import XtceBaseModel

ALL_VERSIONS = [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3]
MODERN_VERSIONS = [XtceVersion.V1_2, XtceVersion.V1_3]


def _parameter_ref() -> XtcePath:
    return XtcePath("/TestSystem/Parameter")


def _container_ref() -> XtcePath:
    return XtcePath("/TestSystem/Container")


def _stream_ref() -> XtcePath:
    return XtcePath("/TestSystem/Stream")


def _parameter_instance() -> xtce.ParameterInstanceRef:
    return xtce.ParameterInstanceRef(ref=_parameter_ref(), instance=1)


def _match_criteria() -> xtce.MatchCriteria:
    return xtce.MatchCriteria(
        criteria=xtce.Comparison(
            ref=_parameter_ref(),
            comparison_operator=xtce.ComparisonOperator.EQ,
            value=1,
        )
    )


def _argument_match_criteria() -> xtce.ArgumentMatchCriteria:
    return xtce.ArgumentMatchCriteria(
        criteria=xtce.ArgumentComparison(
            instance_ref=xtce.ArgumentInstanceRef(ref="Argument"),
            comparison_operator=xtce.ComparisonOperator.EQ,
            value=1,
        )
    )


def _location() -> xtce.LocationInContainer:
    return xtce.LocationInContainer(
        offset=2,
        reference_location=xtce.ReferenceLocation.CONTAINER_START,
    )


def _argument_location() -> xtce.ArgumentLocationInContainer:
    return xtce.ArgumentLocationInContainer(
        offset=2,
        reference_location=xtce.ReferenceLocation.CONTAINER_START,
    )


def _repeat() -> xtce.Repeat:
    return xtce.Repeat(count=2, offset=1)


def _argument_repeat() -> xtce.ArgumentRepeat:
    return xtce.ArgumentRepeat(count=2, offset=1)


def _dimension() -> xtce.Dimension:
    return xtce.Dimension(start_index=0, end_index=1)


def _argument_dimension() -> xtce.ArgumentDimension:
    return xtce.ArgumentDimension(start_index=0, end_index=1)


@pytest.mark.parametrize("version", ALL_VERSIONS)
@pytest.mark.parametrize(
    "original",
    [
        xtce.Repeat(count=2),
        xtce.Repeat(count=2, offset=1),
        xtce.LocationInContainer(offset=0),
        xtce.LocationInContainer(
            offset=2, reference_location=xtce.ReferenceLocation.CONTAINER_END
        ),
        xtce.ParameterRefEntry(parameter_ref=_parameter_ref()),
        xtce.ParameterSegmentRefEntry(
            parameter_ref=_parameter_ref(), order=1, size_in_bits=8
        ),
        xtce.ContainerRefEntry(container_ref=_container_ref()),
        xtce.ContainerSegmentRefEntry(
            container_ref=_container_ref(), order=1, size_in_bits=8
        ),
        xtce.StreamSegmentEntry(stream_ref=_stream_ref(), order=1, size_in_bits=8),
        xtce.IndirectParameterRefEntry(parameter_instance=_parameter_instance()),
        xtce.ArrayParameterRefEntry(
            parameter_ref=_parameter_ref(), dimensions=[_dimension()]
        ),
        xtce.ArgumentRepeat(count=2),
        xtce.ArgumentLocationInContainer(offset=0),
        xtce.ArgumentParameterRefEntry(parameter_ref=_parameter_ref()),
        xtce.ArgumentParameterSegmentRefEntry(
            parameter_ref=_parameter_ref(), order=1, size_in_bits=8
        ),
        xtce.ArgumentContainerRefEntry(container_ref=_container_ref()),
        xtce.ArgumentContainerSegmentRefEntry(
            container_ref=_container_ref(), order=1, size_in_bits=8
        ),
        xtce.ArgumentStreamSegmentEntry(
            stream_ref=_stream_ref(), order=1, size_in_bits=8
        ),
        xtce.ArgumentIndirectParameterRefEntry(
            parameter_instance=_parameter_instance()
        ),
        xtce.ArgumentArrayParameterRefEntry(
            parameter_ref=_parameter_ref(), dimensions=[_dimension()]
        ),
        xtce.ArgumentArgumentRefEntry(argument_ref=XtcePath("Argument")),
        xtce.ArgumentArrayArgumentRefEntry(
            argument_ref=XtcePath("ArrayArgument"), dimensions=[_argument_dimension()]
        ),
        xtce.ArgumentFixedValueEntry(binary_value=b"\xaa", size_in_bits=8),
        xtce.RestrictionCriteria(criteria=_match_criteria().criteria),
        xtce.BaseContainer(
            container_ref=_container_ref(),
            restriction_criteria=xtce.RestrictionCriteria(
                criteria=_match_criteria().criteria
            ),
        ),
    ],
)
def test_round_trip_simple_models(
    original: XtceBaseModel, version: XtceVersion
) -> None:
    """Round-trip each container leaf model through every available version."""
    round_tripped = type(original).from_xsdata(original.to_xsdata(version), version)

    assert round_tripped == original


class TestSequenceEntry:
    """Test shared telemetry sequence-entry properties."""

    @pytest.mark.parametrize("version", MODERN_VERSIONS)
    def test_round_trip_with_all_shared_fields(self, version: XtceVersion) -> None:
        """Preserve every shared modern sequence-entry field."""
        original = xtce.ParameterRefEntry(
            parameter_ref=_parameter_ref(),
            location_in_container=_location(),
            repeat_entry=_repeat(),
            include_condition=_match_criteria(),
            time_association=xtce.TimeAssociation(ref=_parameter_ref()),
            ancillary_data=[xtce.AncillaryData(name="source", value="test")],
            short_description="A parameter entry",
        )

        round_tripped = xtce.ParameterRefEntry.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_v1_1_rejects_modern_shared_fields(self) -> None:
        """Reject fields which XTCE v1.1 cannot represent."""
        original = xtce.ParameterRefEntry(
            parameter_ref=_parameter_ref(),
            time_association=xtce.TimeAssociation(ref=_parameter_ref()),
        )

        with pytest.raises(XtceDowngradeError):
            original.to_xsdata(XtceVersion.V1_1)


class TestArgumentSequenceEntry:
    """Test shared command sequence-entry properties."""

    @pytest.mark.parametrize("version", MODERN_VERSIONS)
    def test_round_trip_with_all_shared_fields(self, version: XtceVersion) -> None:
        """Preserve every shared modern command sequence-entry field."""
        original = xtce.ArgumentParameterRefEntry(
            parameter_ref=_parameter_ref(),
            location_in_container=_argument_location(),
            repeat_entry=_argument_repeat(),
            include_condition=_argument_match_criteria(),
            ancillary_data=[xtce.AncillaryData(name="source", value="test")],
            short_description="An argument entry",
        )

        round_tripped = xtce.ArgumentParameterRefEntry.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_v1_1_rejects_modern_shared_fields(self) -> None:
        """Reject command entry ancillary data unavailable in XTCE v1.1."""
        original = xtce.ArgumentParameterRefEntry(
            parameter_ref=_parameter_ref(),
            ancillary_data=[xtce.AncillaryData(name="source", value="test")],
        )

        with pytest.raises(XtceDowngradeError):
            original.to_xsdata(XtceVersion.V1_1)


class TestContainerBinaryDataEncoding:
    """Test XTCE v1.3 container binary data encoding."""

    def test_round_trip(self) -> None:
        """Round-trip every container binary encoding field through XTCE v1.3."""
        original = xtce.ContainerBinaryDataEncoding(
            error_detect_correct=[
                xtce.Checksum(name=xtce.ChecksumType.SUM8),
                xtce.XOR(),
            ],
            size_in_bits=32,
            from_binary_transform_algorithm=xtce.InputAlgorithm(name="Decode"),
            to_binary_transform_algorithm=xtce.InputAlgorithm(name="Encode"),
        )

        round_tripped = xtce.ContainerBinaryDataEncoding.from_xsdata(
            original.to_xsdata(XtceVersion.V1_3), XtceVersion.V1_3
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", [XtceVersion.V1_1, XtceVersion.V1_2])
    def test_older_versions_are_unsupported(self, version: XtceVersion) -> None:
        """Container binary encoding exists only in XTCE v1.3."""
        original = xtce.ContainerBinaryDataEncoding(size_in_bits=32)

        with pytest.raises(XtceUnsupportedError):
            original.to_xsdata(version)


class TestSequenceContainer:
    """Test telemetry sequence containers."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_every_entry_type(self, version: XtceVersion) -> None:
        """Round-trip every telemetry entry variant in a sequence container."""
        original = xtce.SequenceContainer(
            name="Telemetry",
            entries=[
                xtce.ParameterRefEntry(parameter_ref=_parameter_ref()),
                xtce.ParameterSegmentRefEntry(
                    parameter_ref=_parameter_ref(), order=1, size_in_bits=8
                ),
                xtce.ContainerRefEntry(container_ref=_container_ref()),
                xtce.ContainerSegmentRefEntry(
                    container_ref=_container_ref(), order=1, size_in_bits=8
                ),
                xtce.StreamSegmentEntry(
                    stream_ref=_stream_ref(), order=1, size_in_bits=8
                ),
                xtce.IndirectParameterRefEntry(
                    parameter_instance=_parameter_instance(), alias_name_space="Alias"
                ),
                xtce.ArrayParameterRefEntry(
                    parameter_ref=_parameter_ref(), dimensions=[_dimension()]
                ),
            ],
            base_container=xtce.BaseContainer(
                container_ref=_container_ref(),
                restriction_criteria=xtce.RestrictionCriteria(
                    criteria=_match_criteria().criteria
                ),
            ),
            abstract=True,
            idle_pattern=0xAA,
        )

        round_tripped = xtce.SequenceContainer.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", MODERN_VERSIONS)
    def test_round_trip_container_fields(self, version: XtceVersion) -> None:
        """Preserve rates and v1.3-specific binary encoding when supported."""
        original = xtce.SequenceContainer(
            name="Telemetry",
            entries=[xtce.ParameterRefEntry(parameter_ref=_parameter_ref())],
            default_rate_in_stream=xtce.RateInStream(minimum_value=1.0),
            rate_in_streams=[
                xtce.RateInStreamWithStreamName(
                    stream_ref=_stream_ref(), maximum_value=2.0
                )
            ],
        )
        if version == XtceVersion.V1_3:
            original.binary_encoding = xtce.ContainerBinaryDataEncoding(size_in_bits=8)

        round_tripped = xtce.SequenceContainer.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestCommandContainer:
    """Test command containers."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_every_entry_type(self, version: XtceVersion) -> None:
        """Round-trip every command entry variant in a command container."""
        original = xtce.CommandContainer(
            name="Command",
            entries=[
                xtce.ArgumentParameterRefEntry(parameter_ref=_parameter_ref()),
                xtce.ArgumentParameterSegmentRefEntry(
                    parameter_ref=_parameter_ref(), order=1, size_in_bits=8
                ),
                xtce.ArgumentContainerRefEntry(container_ref=_container_ref()),
                xtce.ArgumentContainerSegmentRefEntry(
                    container_ref=_container_ref(), order=1, size_in_bits=8
                ),
                xtce.ArgumentStreamSegmentEntry(
                    stream_ref=_stream_ref(), order=1, size_in_bits=8
                ),
                xtce.ArgumentIndirectParameterRefEntry(
                    parameter_instance=_parameter_instance(), alias_name_space="Alias"
                ),
                xtce.ArgumentArrayParameterRefEntry(
                    parameter_ref=_parameter_ref(), dimensions=[_dimension()]
                ),
                xtce.ArgumentArgumentRefEntry(argument_ref=XtcePath("Argument")),
                xtce.ArgumentArrayArgumentRefEntry(
                    argument_ref=XtcePath("ArrayArgument"),
                    dimensions=[_argument_dimension()],
                ),
                xtce.ArgumentFixedValueEntry(binary_value=b"\xaa", size_in_bits=8),
            ],
        )

        round_tripped = xtce.CommandContainer.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", MODERN_VERSIONS)
    def test_round_trip_with_base_container(self, version: XtceVersion) -> None:
        """Preserve optional base-container inheritance on modern versions."""
        original = xtce.CommandContainer(
            name="Command",
            entries=[xtce.ArgumentParameterRefEntry(parameter_ref=_parameter_ref())],
            base_container=xtce.BaseContainer(container_ref=_container_ref()),
        )

        round_tripped = xtce.CommandContainer.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


def test_repeat_rejects_negative_offset() -> None:
    """Repeat offsets may be zero but cannot be negative."""
    with pytest.raises(ValidationError):
        xtce.Repeat(count=1, offset=-1)


def test_argument_repeat_rejects_negative_offset() -> None:
    """Argument repeat offsets may be zero but cannot be negative."""
    with pytest.raises(ValidationError):
        xtce.ArgumentRepeat(count=1, offset=-1)
