"""Stream models."""

from abc import ABC
from typing import Annotated, Any

from pydantic import AfterValidator, Field

from xtce_lib.common.xtce_path import XtcePath, require_regex
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3
from xtce_lib.xtce._pattern import NAME_REF_NO_PATH, NAME_REF_W_PATH

from ._base import XtceBaseModel
from ._util import unwrap
from .algorithm import InputAlgorithm, InputOutputAlgorithm
from .common import NameDescriptionBase
from .enum import Basis, FlagBit, PcmType
from .reference import ContainerRef, ServiceRef, StreamRef


class PcmStream(NameDescriptionBase, ABC):
    """Base class for all PCM streams."""

    bit_rate_bps: float | None = None
    """Bit rate of the PCM stream in bits per second."""

    pcm_type: PcmType = PcmType.NRZL
    """Type of PCM encoding used in the stream."""

    inverted: bool = False
    """Whether the PCM stream is inverted."""

    @classmethod
    def _from_v1_1_kwargs(cls, obj: Any) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["bit_rate_bps"] = obj.bit_rate_in_bps
        kwargs["pcm_type"] = PcmType(obj.pcm_type.value)
        kwargs["inverted"] = obj.inverted
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: Any) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["bit_rate_bps"] = obj.bit_rate_in_bps
        kwargs["pcm_type"] = PcmType(obj.pcm_type.value)
        kwargs["inverted"] = obj.inverted
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: Any) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["bit_rate_bps"] = obj.bit_rate_in_bps
        kwargs["pcm_type"] = PcmType(obj.pcm_type.value)
        kwargs["inverted"] = obj.inverted
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["bit_rate_in_bps"] = self.bit_rate_bps
        kwargs["pcm_type"] = xtce_1_1.PcmstreamTypePcmType(self.pcm_type.value)
        kwargs["inverted"] = self.inverted
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["bit_rate_in_bps"] = self.bit_rate_bps
        kwargs["pcm_type"] = xtce_1_2.Pcmtype(self.pcm_type.value)
        kwargs["inverted"] = self.inverted
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["bit_rate_in_bps"] = self.bit_rate_bps
        kwargs["pcm_type"] = xtce_1_3.Pcmtype(self.pcm_type.value)
        kwargs["inverted"] = self.inverted
        return kwargs


class CustomStream(PcmStream):
    """Define a stream with some level of custom processing (convolutional, encryption,
    compression).
    """

    encoding_algorithm: InputAlgorithm
    """The algorithm used to encode the stream."""

    decoding_algorithm: InputOutputAlgorithm
    """The algorithm used to decode the stream."""

    encoded_stream_ref: StreamRef
    """A Unix-like path to an encoded stream."""

    decoded_stream_ref: StreamRef
    """A Unix-like path to a decoded stream."""

    _v1_1_type = xtce_1_1.CustomStreamType
    _v1_2_type = xtce_1_2.CustomStreamType
    _v1_3_type = xtce_1_3.CustomStreamType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.CustomStreamType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["encoding_algorithm"] = InputAlgorithm._from_v1_1(obj.encoding_algorithm)
        kwargs["decoding_algorithm"] = InputOutputAlgorithm._from_v1_1(
            obj.decoding_algorithm
        )
        kwargs["encoded_stream_ref"] = StreamRef(ref=XtcePath(obj.encoded_stream_ref))
        kwargs["decoded_stream_ref"] = StreamRef(ref=XtcePath(obj.decoded_stream_ref))
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.CustomStreamType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["encoding_algorithm"] = InputAlgorithm._from_v1_2(obj.encoding_algorithm)
        kwargs["decoding_algorithm"] = InputOutputAlgorithm._from_v1_2(
            obj.decoding_algorithm
        )
        kwargs["encoded_stream_ref"] = StreamRef(ref=XtcePath(obj.encoded_stream_ref))
        kwargs["decoded_stream_ref"] = StreamRef(ref=XtcePath(obj.decoded_stream_ref))
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.CustomStreamType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["encoding_algorithm"] = InputAlgorithm._from_v1_3(obj.encoding_algorithm)
        kwargs["decoding_algorithm"] = InputOutputAlgorithm._from_v1_3(
            obj.decoding_algorithm
        )
        kwargs["encoded_stream_ref"] = StreamRef(ref=XtcePath(obj.encoded_stream_ref))
        kwargs["decoded_stream_ref"] = StreamRef(ref=XtcePath(obj.decoded_stream_ref))
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.1 uses type xtce:NameReferenceType
        validator = require_regex(NAME_REF_NO_PATH)
        validator(self.encoded_stream_ref.ref)
        validator(self.decoded_stream_ref.ref)

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["encoding_algorithm"] = self.encoding_algorithm._to_v1_1(policy)
        kwargs["decoding_algorithm"] = self.decoding_algorithm._to_v1_1(policy)
        kwargs["encoded_stream_ref"] = str(self.encoded_stream_ref.ref)
        kwargs["decoded_stream_ref"] = str(self.decoded_stream_ref.ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.2 uses type xtce:NameReferenceType
        validator = require_regex(NAME_REF_NO_PATH)
        validator(self.encoded_stream_ref.ref)
        validator(self.decoded_stream_ref.ref)

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["encoding_algorithm"] = self.encoding_algorithm._to_v1_2(policy)
        kwargs["decoding_algorithm"] = self.decoding_algorithm._to_v1_2(policy)
        kwargs["encoded_stream_ref"] = str(self.encoded_stream_ref.ref)
        kwargs["decoded_stream_ref"] = str(self.decoded_stream_ref.ref)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["encoding_algorithm"] = self.encoding_algorithm._to_v1_3(policy)
        kwargs["decoding_algorithm"] = self.decoding_algorithm._to_v1_3(policy)
        kwargs["encoded_stream_ref"] = str(self.encoded_stream_ref.ref)
        kwargs["decoded_stream_ref"] = str(self.decoded_stream_ref.ref)
        return kwargs


class FrameStream(PcmStream):
    """Define a stream that is frame-based."""

    ref: ContainerRef | ServiceRef
    """A reference to the container or service that is contained in this frame
    stream.
    """

    stream_ref: StreamRef | None = None
    """An optional reference to a connecting stream."""

    _v1_1_type = xtce_1_1.FrameStreamType
    _v1_2_type = xtce_1_2.FrameStreamType
    _v1_3_type = xtce_1_3.FrameStreamType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.FrameStreamType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["ref"] = (
            ContainerRef._from_v1_1(obj.choice)
            if isinstance(obj.choice, xtce_1_1.ContainerRefType)
            else ServiceRef._from_v1_1(unwrap(obj.choice))
        )
        kwargs["stream_ref"] = (
            StreamRef._from_v1_1(obj.stream_ref) if obj.stream_ref is not None else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.FrameStreamType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["ref"] = (
            ContainerRef._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.ContainerRefType)
            else ServiceRef._from_v1_2(unwrap(obj.choice))
        )
        kwargs["stream_ref"] = (
            StreamRef._from_v1_2(obj.stream_ref) if obj.stream_ref is not None else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.FrameStreamType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["ref"] = (
            ContainerRef._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.ContainerRefType)
            else ServiceRef._from_v1_3(unwrap(obj.choice))
        )
        kwargs["stream_ref"] = (
            StreamRef._from_v1_3(obj.stream_ref) if obj.stream_ref is not None else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["choice"] = self.ref._to_v1_1(policy)
        kwargs["stream_ref"] = (
            self.stream_ref._to_v1_1(policy) if self.stream_ref is not None else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = self.ref._to_v1_2(policy)
        kwargs["stream_ref"] = (
            self.stream_ref._to_v1_2(policy) if self.stream_ref is not None else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = self.ref._to_v1_3(policy)
        kwargs["stream_ref"] = (
            self.stream_ref._to_v1_3(policy) if self.stream_ref is not None else None
        )
        return kwargs


class AutoInvert(XtceBaseModel):
    """Define the auto-invert behavior for a stream.

    After searching for the frame sync marker for some number of bits, it may be
    desirable to invert the incoming data, and then look for frame sync.

    """

    invert_algorithm: InputAlgorithm | None = None
    """An optional algorithm used to invert the incoming data when auto-invert is
    triggered.
    """

    bad_frames_to_auto_invert: int = Field(default=1024, ge=1)
    """The number of bad frames to encounter before auto-invert is triggered."""

    _v1_1_type = xtce_1_1.SyncStrategyType.AutoInvert
    _v1_2_type = xtce_1_2.AutoInvertType
    _v1_3_type = xtce_1_3.AutoInvertType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.SyncStrategyType.AutoInvert
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["invert_algorithm"] = (
            InputAlgorithm._from_v1_1(obj.invert_algorithm)
            if obj.invert_algorithm is not None
            else None
        )
        kwargs["bad_frames_to_auto_invert"] = obj.bad_frames_to_auto_invert
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.AutoInvertType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["invert_algorithm"] = (
            InputAlgorithm._from_v1_2(obj.invert_algorithm)
            if obj.invert_algorithm is not None
            else None
        )
        kwargs["bad_frames_to_auto_invert"] = obj.bad_frames_to_auto_invert
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.AutoInvertType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["invert_algorithm"] = (
            InputAlgorithm._from_v1_3(obj.invert_algorithm)
            if obj.invert_algorithm is not None
            else None
        )
        kwargs["bad_frames_to_auto_invert"] = obj.bad_frames_to_auto_invert
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["invert_algorithm"] = (
            self.invert_algorithm._to_v1_1(policy)
            if self.invert_algorithm is not None
            else None
        )
        kwargs["bad_frames_to_auto_invert"] = self.bad_frames_to_auto_invert
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["invert_algorithm"] = (
            self.invert_algorithm._to_v1_2(policy)
            if self.invert_algorithm is not None
            else None
        )
        kwargs["bad_frames_to_auto_invert"] = self.bad_frames_to_auto_invert
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["invert_algorithm"] = (
            self.invert_algorithm._to_v1_3(policy)
            if self.invert_algorithm is not None
            else None
        )
        kwargs["bad_frames_to_auto_invert"] = self.bad_frames_to_auto_invert
        return kwargs


class SyncStrategy(XtceBaseModel, ABC):
    """Define the strategy for finding frames within a stream of PCM data.

    The sync strategy is based upon a state machine that begins in the 'search' state
    until the first sync marker is found. Then it goes into the 'verify' state until a
    specified number of successive good sync markers are found. Then the state machine
    goes into the 'lock' state, where frames are considered good.

    Should a sync marker be missed in the 'lock' state, the state machine will
    transition into the 'check' state. If the next sync marker is where it is expected
    within a specified number of frames, then the state machine will transition back
    into the 'lock' state. Otherwise, it will return to the 'search' state.

    """

    auto_invert: AutoInvert | None = None
    """The auto-invert behavior."""

    verify_to_lock_good_frames: int = Field(default=4, ge=0)
    """The number of good frames required to transition from 'verify' to 'lock'
    state.
    """

    check_to_lock_good_frames: int = Field(default=1, ge=0)
    """The number of good frames required to transition from 'check' to 'lock' state."""

    max_bit_errors_in_sync_pattern: int = Field(default=0, ge=0)
    """The maximum number of bit errors allowed in the sync pattern."""

    @classmethod
    def _from_v1_1_kwargs(cls, obj: Any) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["auto_invert"] = (
            AutoInvert._from_v1_1(obj.auto_invert)
            if obj.auto_invert is not None
            else None
        )
        kwargs["verify_to_lock_good_frames"] = obj.verify_to_lock_good_frames
        kwargs["check_to_lock_good_frames"] = obj.check_to_lock_good_frames
        kwargs["max_bit_errors_in_sync_pattern"] = obj.max_bit_errors_in_sync_pattern
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: Any) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["auto_invert"] = (
            AutoInvert._from_v1_2(obj.auto_invert)
            if obj.auto_invert is not None
            else None
        )
        kwargs["verify_to_lock_good_frames"] = obj.verify_to_lock_good_frames
        kwargs["check_to_lock_good_frames"] = obj.check_to_lock_good_frames
        kwargs["max_bit_errors_in_sync_pattern"] = obj.max_bit_errors_in_sync_pattern
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: Any) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["auto_invert"] = (
            AutoInvert._from_v1_3(obj.auto_invert)
            if obj.auto_invert is not None
            else None
        )
        kwargs["verify_to_lock_good_frames"] = obj.verify_to_lock_good_frames
        kwargs["check_to_lock_good_frames"] = obj.check_to_lock_good_frames
        kwargs["max_bit_errors_in_sync_pattern"] = obj.max_bit_errors_in_sync_pattern
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["auto_invert"] = (
            self.auto_invert._to_v1_1(policy) if self.auto_invert is not None else None
        )
        kwargs["verify_to_lock_good_frames"] = self.verify_to_lock_good_frames
        kwargs["check_to_lock_good_frames"] = self.check_to_lock_good_frames
        kwargs["max_bit_errors_in_sync_pattern"] = self.max_bit_errors_in_sync_pattern
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["auto_invert"] = (
            self.auto_invert._to_v1_2(policy) if self.auto_invert is not None else None
        )
        kwargs["verify_to_lock_good_frames"] = self.verify_to_lock_good_frames
        kwargs["check_to_lock_good_frames"] = self.check_to_lock_good_frames
        kwargs["max_bit_errors_in_sync_pattern"] = self.max_bit_errors_in_sync_pattern
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["auto_invert"] = (
            self.auto_invert._to_v1_3(policy) if self.auto_invert is not None else None
        )
        kwargs["verify_to_lock_good_frames"] = self.verify_to_lock_good_frames
        kwargs["check_to_lock_good_frames"] = self.check_to_lock_good_frames
        kwargs["max_bit_errors_in_sync_pattern"] = self.max_bit_errors_in_sync_pattern
        return kwargs


class SyncPattern(XtceBaseModel):
    """Define a sync pattern used to identify the start of a frame within a stream of
    PCM data.
    """

    pattern: bytes = Field(..., min_length=1)
    """The sync pattern as a sequence of bytes."""

    bit_location_from_start_of_container: int = 0
    """The bit location of the sync pattern from the start of the container."""

    mask: bytes | None = None
    """The mask applied to the sync pattern."""

    mask_length_in_bits: int | None = Field(default=None, ge=1)
    """The length of the mask in bits."""

    pattern_length_in_bits: int = Field(..., ge=1)
    """The length of the sync pattern in bits."""

    _v1_1_type = xtce_1_1.FixedFrameStreamType.SyncStrategy.SyncPattern
    _v1_2_type = xtce_1_2.SyncPatternType
    _v1_3_type = xtce_1_3.SyncPatternType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.FixedFrameStreamType.SyncStrategy.SyncPattern
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["pattern"] = obj.pattern
        kwargs["bit_location_from_start_of_container"] = (
            obj.bit_location_from_start_of_container
        )
        kwargs["mask"] = obj.mask
        kwargs["mask_length_in_bits"] = obj.mask_length_in_bits
        kwargs["pattern_length_in_bits"] = obj.pattern_length_in_bits
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.SyncPatternType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["pattern"] = obj.pattern
        kwargs["bit_location_from_start_of_container"] = (
            obj.bit_location_from_start_of_container
        )
        kwargs["mask"] = obj.mask
        kwargs["mask_length_in_bits"] = obj.mask_length_in_bits
        kwargs["pattern_length_in_bits"] = obj.pattern_length_in_bits
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.SyncPatternType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["pattern"] = obj.pattern
        kwargs["bit_location_from_start_of_container"] = (
            obj.bit_location_from_start_of_container
        )
        kwargs["mask"] = obj.mask
        kwargs["mask_length_in_bits"] = obj.mask_length_in_bits
        kwargs["pattern_length_in_bits"] = obj.pattern_length_in_bits
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["pattern"] = self.pattern
        kwargs["bit_location_from_start_of_container"] = (
            self.bit_location_from_start_of_container
        )
        kwargs["mask"] = self.mask
        kwargs["mask_length_in_bits"] = self.mask_length_in_bits
        kwargs["pattern_length_in_bits"] = self.pattern_length_in_bits
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["pattern"] = self.pattern
        kwargs["bit_location_from_start_of_container"] = (
            self.bit_location_from_start_of_container
        )
        kwargs["mask"] = self.mask
        kwargs["mask_length_in_bits"] = self.mask_length_in_bits
        kwargs["pattern_length_in_bits"] = self.pattern_length_in_bits
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["pattern"] = self.pattern
        kwargs["bit_location_from_start_of_container"] = (
            self.bit_location_from_start_of_container
        )
        kwargs["mask"] = self.mask
        kwargs["mask_length_in_bits"] = self.mask_length_in_bits
        kwargs["pattern_length_in_bits"] = self.pattern_length_in_bits
        return kwargs


class FixedFrameSyncStrategy(SyncStrategy):
    """Define a fixed frame synchronization strategy."""

    sync_pattern: SyncPattern
    """The synchronization pattern used for fixed frame synchronization."""

    _v1_1_type = xtce_1_1.FixedFrameStreamType.SyncStrategy
    _v1_2_type = xtce_1_2.FixedFrameSyncStrategyType
    _v1_3_type = xtce_1_3.FixedFrameSyncStrategyType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.FixedFrameStreamType.SyncStrategy
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["sync_pattern"] = SyncPattern._from_v1_1(obj.sync_pattern)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.FixedFrameSyncStrategyType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["sync_pattern"] = SyncPattern._from_v1_2(obj.sync_pattern)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.FixedFrameSyncStrategyType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["sync_pattern"] = SyncPattern._from_v1_3(obj.sync_pattern)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["sync_pattern"] = self.sync_pattern._to_v1_1(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["sync_pattern"] = self.sync_pattern._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["sync_pattern"] = self.sync_pattern._to_v1_3(policy)
        return kwargs


class FixedFrameStream(FrameStream):
    """Define a stream that contains fixed-length frames.

    The frames are found by looking for a frame sync pattern within the stream.

    """

    sync_strategy: FixedFrameSyncStrategy
    """The sync strategy used to locate frames within the stream."""

    sync_aperture_bits: int = Field(default=0, ge=0)
    """The allowed slip (in bits) in either direction for the sync pattern."""

    frame_length_bits: int
    """The length of each frame in bits."""

    _v1_1_type = xtce_1_1.FixedFrameStreamType
    _v1_2_type = xtce_1_2.FixedFrameStreamType
    _v1_3_type = xtce_1_3.FixedFrameStreamType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.FixedFrameStreamType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["sync_strategy"] = FixedFrameSyncStrategy._from_v1_1(obj.sync_strategy)
        kwargs["sync_aperture_bits"] = obj.sync_aperture_in_bits
        kwargs["frame_length_bits"] = obj.frame_length_in_bits
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.FixedFrameStreamType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["sync_strategy"] = FixedFrameSyncStrategy._from_v1_2(obj.sync_strategy)
        kwargs["sync_aperture_bits"] = obj.sync_aperture_in_bits
        kwargs["frame_length_bits"] = obj.frame_length_in_bits
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.FixedFrameStreamType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["sync_strategy"] = FixedFrameSyncStrategy._from_v1_3(obj.sync_strategy)
        kwargs["sync_aperture_bits"] = obj.sync_aperture_in_bits
        kwargs["frame_length_bits"] = obj.frame_length_in_bits
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["sync_strategy"] = self.sync_strategy._to_v1_1(policy)
        kwargs["sync_aperture_in_bits"] = self.sync_aperture_bits
        kwargs["frame_length_in_bits"] = self.frame_length_bits
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["sync_strategy"] = self.sync_strategy._to_v1_2(policy)
        kwargs["sync_aperture_in_bits"] = self.sync_aperture_bits
        kwargs["frame_length_in_bits"] = self.frame_length_bits
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["sync_strategy"] = self.sync_strategy._to_v1_3(policy)
        kwargs["sync_aperture_in_bits"] = self.sync_aperture_bits
        kwargs["frame_length_in_bits"] = self.frame_length_bits
        return kwargs


class Flag(XtceBaseModel):
    """Define a flag used to look for frame synchronization."""

    flag_size_bits: int = Field(default=6, ge=1)
    """The size of the flag in bits."""

    flag_bit_type: FlagBit = Field(default=FlagBit.ONES)
    """The type of bits used in the flag."""

    _v1_1_type = xtce_1_1.VariableFrameStreamType.SyncStrategy.Flag
    _v1_2_type = xtce_1_2.FlagType
    _v1_3_type = xtce_1_3.FlagType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.VariableFrameStreamType.SyncStrategy.Flag
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["flag_size_bits"] = obj.flag_size_in_bits
        kwargs["flag_bit_type"] = FlagBit(obj.flag_bit_type.value)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.FlagType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["flag_size_bits"] = obj.flag_size_in_bits
        kwargs["flag_bit_type"] = FlagBit(obj.flag_bit_type.value)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.FlagType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["flag_size_bits"] = obj.flag_size_in_bits
        kwargs["flag_bit_type"] = FlagBit(obj.flag_bit_type.value)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["flag_size_in_bits"] = self.flag_size_bits
        kwargs["flag_bit_type"] = xtce_1_1.FlagFlagBitType(self.flag_bit_type.value)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["flag_size_in_bits"] = self.flag_size_bits
        kwargs["flag_bit_type"] = xtce_1_2.FlagBitType(self.flag_bit_type.value)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["flag_size_in_bits"] = self.flag_size_bits
        kwargs["flag_bit_type"] = xtce_1_3.FlagBitType(self.flag_bit_type.value)
        return kwargs


class VariableFrameSyncStrategy(SyncStrategy):
    """Define a variable frame synchronization strategy."""

    flag: Flag

    _v1_1_type = xtce_1_1.VariableFrameStreamType.SyncStrategy
    _v1_2_type = xtce_1_2.VariableFrameSyncStrategyType
    _v1_3_type = xtce_1_3.VariableFrameSyncStrategyType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.VariableFrameStreamType.SyncStrategy
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["flag"] = Flag._from_v1_1(obj.flag)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.VariableFrameSyncStrategyType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["flag"] = Flag._from_v1_2(obj.flag)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.VariableFrameSyncStrategyType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["flag"] = Flag._from_v1_3(obj.flag)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["flag"] = self.flag._to_v1_1(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["flag"] = self.flag._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["flag"] = self.flag._to_v1_3(policy)
        return kwargs


class VariableFrameStream(FrameStream):
    """Define a stream that contains variable-length frames.

    The frames are found by looking for a series of one's or zero's within the stream.

    """

    sync_strategy: VariableFrameSyncStrategy
    """The strategy used to identify the start of variable-length frames within the
    stream.
    """

    _v1_1_type = xtce_1_1.VariableFrameStreamType
    _v1_2_type = xtce_1_2.VariableFrameStreamType
    _v1_3_type = xtce_1_3.VariableFrameStreamType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.VariableFrameStreamType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["sync_strategy"] = VariableFrameSyncStrategy._from_v1_1(
            obj.sync_strategy
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.VariableFrameStreamType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["sync_strategy"] = VariableFrameSyncStrategy._from_v1_2(
            obj.sync_strategy
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.VariableFrameStreamType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["sync_strategy"] = VariableFrameSyncStrategy._from_v1_3(
            obj.sync_strategy
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["sync_strategy"] = self.sync_strategy._to_v1_1(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["sync_strategy"] = self.sync_strategy._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["sync_strategy"] = self.sync_strategy._to_v1_3(policy)
        return kwargs


class RateInStream(XtceBaseModel):
    """Define the expected appearance rate of a container in a stream.

    Can be defined as either a rate per second or a rate per container update.

    """

    basis: Basis = Basis.PER_SECOND
    """The basis for the rate of updates."""

    minimum_value: float | None = None
    """The minimum expected rate of appearance."""

    maximum_value: float | None = None
    """The maximum expected rate of appearance."""

    _v1_1_type = xtce_1_1.RateInStreamType
    _v1_2_type = xtce_1_2.RateInStreamType
    _v1_3_type = xtce_1_3.RateInStreamType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.RateInStreamType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["basis"] = Basis(obj.basis.value)
        kwargs["minimum_value"] = obj.minimum_value
        kwargs["maximum_value"] = obj.maximum_value
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.RateInStreamType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["basis"] = Basis(obj.basis.value)
        kwargs["minimum_value"] = obj.minimum_value
        kwargs["maximum_value"] = obj.maximum_value
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.RateInStreamType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["basis"] = Basis(obj.basis.value)
        kwargs["minimum_value"] = obj.minimum_value
        kwargs["maximum_value"] = obj.maximum_value
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["basis"] = xtce_1_1.RateInStreamTypeBasis(self.basis.value)
        kwargs["minimum_value"] = self.minimum_value
        kwargs["maximum_value"] = self.maximum_value
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["basis"] = xtce_1_2.BasisType(self.basis.value)
        kwargs["minimum_value"] = self.minimum_value
        kwargs["maximum_value"] = self.maximum_value
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["basis"] = xtce_1_3.BasisType(self.basis.value)
        kwargs["minimum_value"] = self.minimum_value
        kwargs["maximum_value"] = self.maximum_value
        return kwargs


class RateInStreamWithStreamName(RateInStream):
    """Define the expected appearance rate of a container in a specific stream.

    Can be defined as either a rate per second or a rate per container update.

    """

    stream_ref: Annotated[XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))] = (
        Field(
            ...,
            examples=[],
            json_schema_extra={"pattern": NAME_REF_W_PATH},
        )
    )
    """A Unix-like path to the stream in which this rate applies."""

    _v1_1_type = None
    _v1_2_type = xtce_1_2.RateInStreamWithStreamNameType
    _v1_3_type = xtce_1_3.RateInStreamWithStreamNameType

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.RateInStreamWithStreamNameType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["stream_ref"] = XtcePath(obj.stream_ref)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.RateInStreamWithStreamNameType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["stream_ref"] = XtcePath(obj.stream_ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["stream_ref"] = str(self.stream_ref)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["stream_ref"] = str(self.stream_ref)
        return kwargs
