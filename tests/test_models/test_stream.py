"""Test stream models."""

from __future__ import annotations

import pytest

from xtce_lib import (
    XtcePath,
    XtceUnsupportedError,
    XtceVersion,
    xtce,
)

SUPPORTED_ALL_VERSIONS = [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3]
SUPPORTED_BASE_VERSIONS = [XtceVersion.V1_2, XtceVersion.V1_3]


def _make_sync_pattern() -> xtce.SyncPattern:
    """Build a reusable sync pattern for stream tests."""
    return xtce.SyncPattern(pattern=b"\xaa", pattern_length_in_bits=8)


def _make_fixed_frame_sync_strategy() -> xtce.FixedFrameSyncStrategy:
    """Build a reusable fixed-frame sync strategy for stream tests."""
    return xtce.FixedFrameSyncStrategy(sync_pattern=_make_sync_pattern())


def _make_variable_frame_sync_strategy() -> xtce.VariableFrameSyncStrategy:
    """Build a reusable variable-frame sync strategy for stream tests."""
    return xtce.VariableFrameSyncStrategy(flag=xtce.Flag())


class TestCustomStream:
    """Test CustomStream model."""

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a custom stream through each supported version."""
        original = xtce.CustomStream(
            name="MyCustomStream",
            bit_rate_bps=1000.0,
            pcm_type=xtce.PcmType.NRZL,
            inverted=False,
            encoding_algorithm=xtce.InputAlgorithm(name="EncodingAlgorithm"),
            decoding_algorithm=xtce.InputOutputAlgorithm(name="DecodingAlgorithm"),
            encoded_stream_ref=xtce.StreamRef(ref=XtcePath("EncodedStream")),
            decoded_stream_ref=xtce.StreamRef(ref=XtcePath("DecodedStream")),
        )

        round_tripped = xtce.CustomStream.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestFrameStream:
    """Test FrameStream model."""

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip_with_container_ref(self, version: XtceVersion) -> None:
        """Round-trip a frame stream referencing a container."""
        original = xtce.FrameStream(
            name="MyFrameStream",
            ref=xtce.ContainerRef(ref=XtcePath("/TestSystem/TestContainer")),
            stream_ref=xtce.StreamRef(ref=XtcePath("/TestSystem/OtherStream")),
        )

        round_tripped = xtce.FrameStream.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip_with_service_ref(self, version: XtceVersion) -> None:
        """Round-trip a frame stream referencing a service, with no stream_ref."""
        original = xtce.FrameStream(
            name="MyFrameStream",
            ref=xtce.ServiceRef(ref=XtcePath("/TestSystem/TestService")),
        )

        round_tripped = xtce.FrameStream.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestAutoInvert:
    """Test AutoInvert model."""

    def test_defaults(self) -> None:
        """Default bad_frames_to_auto_invert should be 1024."""
        model = xtce.AutoInvert()

        assert model.invert_algorithm is None
        assert model.bad_frames_to_auto_invert == 1024

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip_without_algorithm(self, version: XtceVersion) -> None:
        """Round-trip an auto-invert with no invert algorithm."""
        original = xtce.AutoInvert(bad_frames_to_auto_invert=512)

        round_tripped = xtce.AutoInvert.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip_with_algorithm(self, version: XtceVersion) -> None:
        """Round-trip an auto-invert with an invert algorithm."""
        original = xtce.AutoInvert(
            invert_algorithm=xtce.InputAlgorithm(name="InvertAlgorithm"),
            bad_frames_to_auto_invert=256,
        )

        round_tripped = xtce.AutoInvert.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestSyncPattern:
    """Test SyncPattern model."""

    def test_accepts_fields(self) -> None:
        """SyncPattern should accept pattern and mask fields."""
        model = xtce.SyncPattern(
            pattern=b"\xaa",
            bit_location_from_start_of_container=4,
            mask=b"\xff",
            mask_length_in_bits=8,
            pattern_length_in_bits=8,
        )

        assert model.pattern == b"\xaa"
        assert model.mask == b"\xff"

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a sync pattern through each supported version."""
        original = xtce.SyncPattern(
            pattern=b"\xaa\xbb",
            bit_location_from_start_of_container=4,
            mask=b"\xff\xff",
            mask_length_in_bits=16,
            pattern_length_in_bits=16,
        )

        round_tripped = xtce.SyncPattern.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestFixedFrameSyncStrategy:
    """Test FixedFrameSyncStrategy model."""

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a fixed-frame sync strategy through each supported version."""
        original = xtce.FixedFrameSyncStrategy(
            verify_to_lock_good_frames=5,
            check_to_lock_good_frames=2,
            max_bit_errors_in_sync_pattern=1,
            sync_pattern=_make_sync_pattern(),
        )

        round_tripped = xtce.FixedFrameSyncStrategy.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip_with_auto_invert(self, version: XtceVersion) -> None:
        """Round-trip a fixed-frame sync strategy that includes auto-invert."""
        original = xtce.FixedFrameSyncStrategy(
            auto_invert=xtce.AutoInvert(bad_frames_to_auto_invert=128),
            sync_pattern=_make_sync_pattern(),
        )

        round_tripped = xtce.FixedFrameSyncStrategy.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestFixedFrameStream:
    """Test FixedFrameStream model."""

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a fixed-frame stream through each supported version."""
        original = xtce.FixedFrameStream(
            name="MyFixedFrameStream",
            ref=xtce.ContainerRef(ref=XtcePath("/TestSystem/TestContainer")),
            sync_strategy=_make_fixed_frame_sync_strategy(),
            sync_aperture_bits=2,
            frame_length_bits=1024,
        )

        round_tripped = xtce.FixedFrameStream.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestFlag:
    """Test Flag model."""

    def test_defaults(self) -> None:
        """Default flag_size_bits should be 6 and flag_bit_type should be ONES."""
        model = xtce.Flag()

        assert model.flag_size_bits == 6
        assert model.flag_bit_type == xtce.FlagBit.ONES

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a flag through each supported version."""
        original = xtce.Flag(flag_size_bits=8, flag_bit_type=xtce.FlagBit.ZEROS)

        round_tripped = xtce.Flag.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original


class TestVariableFrameSyncStrategy:
    """Test VariableFrameSyncStrategy model."""

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a variable-frame sync strategy through each supported version."""
        original = xtce.VariableFrameSyncStrategy(
            verify_to_lock_good_frames=3,
            check_to_lock_good_frames=1,
            max_bit_errors_in_sync_pattern=2,
            flag=xtce.Flag(flag_size_bits=8, flag_bit_type=xtce.FlagBit.ZEROS),
        )

        round_tripped = xtce.VariableFrameSyncStrategy.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip_with_auto_invert(self, version: XtceVersion) -> None:
        """Round-trip a variable-frame sync strategy that includes auto-invert."""
        original = xtce.VariableFrameSyncStrategy(
            auto_invert=xtce.AutoInvert(bad_frames_to_auto_invert=64),
            flag=xtce.Flag(),
        )

        round_tripped = xtce.VariableFrameSyncStrategy.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestVariableFrameStream:
    """Test VariableFrameStream model."""

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a variable-frame stream through each supported version."""
        original = xtce.VariableFrameStream(
            name="MyVariableFrameStream",
            ref=xtce.ContainerRef(ref=XtcePath("/TestSystem/TestContainer")),
            sync_strategy=_make_variable_frame_sync_strategy(),
        )

        round_tripped = xtce.VariableFrameStream.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestRateInStream:
    """Test RateInStream model."""

    def test_defaults(self) -> None:
        """Default basis should be PER_SECOND."""
        model = xtce.RateInStream()

        assert model.basis == xtce.Basis.PER_SECOND
        assert model.minimum_value is None
        assert model.maximum_value is None

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a rate-in-stream through each supported version."""
        original = xtce.RateInStream(
            basis=xtce.Basis.PER_CONTAINER_UPDATE,
            minimum_value=1.0,
            maximum_value=10.0,
        )

        round_tripped = xtce.RateInStream.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestRateInStreamWithStreamName:
    """Test RateInStreamWithStreamName model."""

    def test_from_v1_1_is_unsupported(self) -> None:
        """XTCE 1.1 import is unsupported for RateInStreamWithStreamName."""
        with pytest.raises(XtceUnsupportedError):
            xtce.RateInStreamWithStreamName.from_xsdata(object(), XtceVersion.V1_1)

    def test_to_v1_1_is_unsupported(self) -> None:
        """XTCE 1.1 export is unsupported for RateInStreamWithStreamName."""
        model = xtce.RateInStreamWithStreamName(
            stream_ref=XtcePath("/TestSystem/TestStream")
        )

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_1)

    @pytest.mark.parametrize("version", SUPPORTED_BASE_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a rate-in-stream-with-name through XTCE 1.2 and 1.3."""
        original = xtce.RateInStreamWithStreamName(
            basis=xtce.Basis.PER_CONTAINER_UPDATE,
            minimum_value=1.0,
            maximum_value=10.0,
            stream_ref=XtcePath("/TestSystem/TestStream"),
        )

        round_tripped = xtce.RateInStreamWithStreamName.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original
