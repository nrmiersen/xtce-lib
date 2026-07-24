"""Stream models."""

from abc import ABC
from typing import Annotated, Any, Self

from pydantic import AfterValidator, Field

from xtce_lib.common.xtce_path import XtcePath, require_regex
from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy, XtceUnsupportedError
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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.CustomStreamType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_1(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_1(raw_obj.ancillary_data_set),
            bit_rate_bps=raw_obj.bit_rate_in_bps,
            pcm_type=PcmType(raw_obj.pcm_type.value),
            inverted=raw_obj.inverted,
            encoding_algorithm=InputAlgorithm._from_v1_1(raw_obj.encoding_algorithm),
            decoding_algorithm=InputOutputAlgorithm._from_v1_1(
                raw_obj.decoding_algorithm
            ),
            encoded_stream_ref=StreamRef(ref=XtcePath(raw_obj.encoded_stream_ref)),
            decoded_stream_ref=StreamRef(ref=XtcePath(raw_obj.decoded_stream_ref)),
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.CustomStreamType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_2(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_2(raw_obj.ancillary_data_set),
            bit_rate_bps=raw_obj.bit_rate_in_bps,
            pcm_type=PcmType(raw_obj.pcm_type.value),
            inverted=raw_obj.inverted,
            encoding_algorithm=InputAlgorithm._from_v1_2(raw_obj.encoding_algorithm),
            decoding_algorithm=InputOutputAlgorithm._from_v1_2(
                raw_obj.decoding_algorithm
            ),
            encoded_stream_ref=StreamRef(ref=XtcePath(raw_obj.encoded_stream_ref)),
            decoded_stream_ref=StreamRef(ref=XtcePath(raw_obj.decoded_stream_ref)),
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.CustomStreamType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_3(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_3(raw_obj.ancillary_data_set),
            bit_rate_bps=raw_obj.bit_rate_in_bps,
            pcm_type=PcmType(raw_obj.pcm_type.value),
            inverted=raw_obj.inverted,
            encoding_algorithm=InputAlgorithm._from_v1_3(raw_obj.encoding_algorithm),
            decoding_algorithm=InputOutputAlgorithm._from_v1_3(
                raw_obj.decoding_algorithm
            ),
            encoded_stream_ref=StreamRef(ref=XtcePath(raw_obj.encoded_stream_ref)),
            decoded_stream_ref=StreamRef(ref=XtcePath(raw_obj.decoded_stream_ref)),
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.CustomStreamType:
        # XTCE 1.1 uses type xtce:NameReferenceType
        validator = require_regex(NAME_REF_NO_PATH)
        validator(self.encoded_stream_ref.ref)
        validator(self.decoded_stream_ref.ref)

        return xtce_1_1.CustomStreamType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_1(policy),
            ancillary_data_set=self._ancillary_data_to_v1_1(policy),
            bit_rate_in_bps=self.bit_rate_bps,
            pcm_type=xtce_1_1.PcmstreamTypePcmType(self.pcm_type.value),
            inverted=self.inverted,
            encoding_algorithm=self.encoding_algorithm._to_v1_1(policy),
            decoding_algorithm=self.decoding_algorithm._to_v1_1(policy),
            encoded_stream_ref=str(self.encoded_stream_ref.ref),
            decoded_stream_ref=str(self.decoded_stream_ref.ref),
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.CustomStreamType:
        # XTCE 1.2 uses type xtce:NameReferenceType
        validator = require_regex(NAME_REF_NO_PATH)
        validator(self.encoded_stream_ref.ref)
        validator(self.decoded_stream_ref.ref)

        return xtce_1_2.CustomStreamType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_2(policy),
            ancillary_data_set=self._ancillary_data_to_v1_2(policy),
            bit_rate_in_bps=self.bit_rate_bps,
            pcm_type=xtce_1_2.Pcmtype(self.pcm_type.value),
            inverted=self.inverted,
            encoding_algorithm=self.encoding_algorithm._to_v1_2(policy),
            decoding_algorithm=self.decoding_algorithm._to_v1_2(policy),
            encoded_stream_ref=str(self.encoded_stream_ref.ref),
            decoded_stream_ref=str(self.decoded_stream_ref.ref),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.CustomStreamType:
        return xtce_1_3.CustomStreamType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_3(policy),
            ancillary_data_set=self._ancillary_data_to_v1_3(policy),
            bit_rate_in_bps=self.bit_rate_bps,
            pcm_type=xtce_1_3.Pcmtype(self.pcm_type.value),
            inverted=self.inverted,
            encoding_algorithm=self.encoding_algorithm._to_v1_3(policy),
            decoding_algorithm=self.decoding_algorithm._to_v1_3(policy),
            encoded_stream_ref=str(self.encoded_stream_ref.ref),
            decoded_stream_ref=str(self.decoded_stream_ref.ref),
        )


class FrameStream(PcmStream):
    """Define a stream that is frame-based."""

    ref: ContainerRef | ServiceRef
    """A reference to the container or service that is contained in this frame
    stream.
    """

    stream_ref: StreamRef | None = None
    """An optional reference to a connecting stream."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.FrameStreamType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_1(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_1(raw_obj.ancillary_data_set),
            bit_rate_bps=raw_obj.bit_rate_in_bps,
            pcm_type=PcmType(raw_obj.pcm_type.value),
            inverted=raw_obj.inverted,
            ref=ContainerRef._from_v1_1(raw_obj.choice)
            if isinstance(raw_obj.choice, xtce_1_1.ContainerRefType)
            else ServiceRef._from_v1_1(unwrap(raw_obj.choice)),
            stream_ref=StreamRef._from_v1_1(raw_obj.stream_ref)
            if raw_obj.stream_ref is not None
            else None,
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.FrameStreamType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_2(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_2(raw_obj.ancillary_data_set),
            bit_rate_bps=raw_obj.bit_rate_in_bps,
            pcm_type=PcmType(raw_obj.pcm_type.value),
            inverted=raw_obj.inverted,
            ref=ContainerRef._from_v1_2(raw_obj.choice)
            if isinstance(raw_obj.choice, xtce_1_2.ContainerRefType)
            else ServiceRef._from_v1_2(unwrap(raw_obj.choice)),
            stream_ref=StreamRef._from_v1_2(raw_obj.stream_ref)
            if raw_obj.stream_ref is not None
            else None,
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.FrameStreamType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_3(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_3(raw_obj.ancillary_data_set),
            bit_rate_bps=raw_obj.bit_rate_in_bps,
            pcm_type=PcmType(raw_obj.pcm_type.value),
            inverted=raw_obj.inverted,
            ref=ContainerRef._from_v1_3(raw_obj.choice)
            if isinstance(raw_obj.choice, xtce_1_3.ContainerRefType)
            else ServiceRef._from_v1_3(unwrap(raw_obj.choice)),
            stream_ref=StreamRef._from_v1_3(raw_obj.stream_ref)
            if raw_obj.stream_ref is not None
            else None,
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.FrameStreamType:
        return xtce_1_1.FrameStreamType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_1(policy),
            ancillary_data_set=self._ancillary_data_to_v1_1(policy),
            bit_rate_in_bps=self.bit_rate_bps,
            pcm_type=xtce_1_1.PcmstreamTypePcmType(self.pcm_type.value),
            inverted=self.inverted,
            choice=self.ref._to_v1_1(policy),
            stream_ref=self.stream_ref._to_v1_1(policy)
            if self.stream_ref is not None
            else None,
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.FrameStreamType:
        return xtce_1_2.FrameStreamType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_2(policy),
            ancillary_data_set=self._ancillary_data_to_v1_2(policy),
            bit_rate_in_bps=self.bit_rate_bps,
            pcm_type=xtce_1_2.Pcmtype(self.pcm_type.value),
            inverted=self.inverted,
            choice=self.ref._to_v1_2(policy),
            stream_ref=self.stream_ref._to_v1_2(policy)
            if self.stream_ref is not None
            else None,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.FrameStreamType:
        return xtce_1_3.FrameStreamType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_3(policy),
            ancillary_data_set=self._ancillary_data_to_v1_3(policy),
            bit_rate_in_bps=self.bit_rate_bps,
            pcm_type=xtce_1_3.Pcmtype(self.pcm_type.value),
            inverted=self.inverted,
            choice=self.ref._to_v1_3(policy),
            stream_ref=self.stream_ref._to_v1_3(policy)
            if self.stream_ref is not None
            else None,
        )


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

    @classmethod
    def _from_v1_1(
        cls: type[Self], raw_obj: xtce_1_1.SyncStrategyType.AutoInvert
    ) -> Self:
        return cls(
            invert_algorithm=InputAlgorithm._from_v1_1(raw_obj.invert_algorithm)
            if raw_obj.invert_algorithm is not None
            else None,
            bad_frames_to_auto_invert=raw_obj.bad_frames_to_auto_invert,
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.AutoInvertType) -> Self:
        return cls(
            invert_algorithm=InputAlgorithm._from_v1_2(raw_obj.invert_algorithm)
            if raw_obj.invert_algorithm is not None
            else None,
            bad_frames_to_auto_invert=raw_obj.bad_frames_to_auto_invert,
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.AutoInvertType) -> Self:
        return cls(
            invert_algorithm=InputAlgorithm._from_v1_3(raw_obj.invert_algorithm)
            if raw_obj.invert_algorithm is not None
            else None,
            bad_frames_to_auto_invert=raw_obj.bad_frames_to_auto_invert,
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.SyncStrategyType.AutoInvert:
        return xtce_1_1.SyncStrategyType.AutoInvert(
            invert_algorithm=self.invert_algorithm._to_v1_1(policy)
            if self.invert_algorithm is not None
            else None,
            bad_frames_to_auto_invert=self.bad_frames_to_auto_invert,
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.AutoInvertType:
        return xtce_1_2.AutoInvertType(
            invert_algorithm=self.invert_algorithm._to_v1_2(policy)
            if self.invert_algorithm is not None
            else None,
            bad_frames_to_auto_invert=self.bad_frames_to_auto_invert,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.AutoInvertType:
        return xtce_1_3.AutoInvertType(
            invert_algorithm=self.invert_algorithm._to_v1_3(policy)
            if self.invert_algorithm is not None
            else None,
            bad_frames_to_auto_invert=self.bad_frames_to_auto_invert,
        )


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

    @classmethod
    def _from_v1_1(
        cls: type[Self], raw_obj: xtce_1_1.FixedFrameStreamType.SyncStrategy.SyncPattern
    ) -> Self:
        return cls(
            pattern=raw_obj.pattern,
            bit_location_from_start_of_container=raw_obj.bit_location_from_start_of_container,
            mask=raw_obj.mask,
            mask_length_in_bits=raw_obj.mask_length_in_bits,
            pattern_length_in_bits=raw_obj.pattern_length_in_bits,
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.SyncPatternType) -> Self:
        return cls(
            pattern=raw_obj.pattern,
            bit_location_from_start_of_container=raw_obj.bit_location_from_start_of_container,
            mask=raw_obj.mask,
            mask_length_in_bits=raw_obj.mask_length_in_bits,
            pattern_length_in_bits=raw_obj.pattern_length_in_bits,
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.SyncPatternType) -> Self:
        return cls(
            pattern=raw_obj.pattern,
            bit_location_from_start_of_container=raw_obj.bit_location_from_start_of_container,
            mask=raw_obj.mask,
            mask_length_in_bits=raw_obj.mask_length_in_bits,
            pattern_length_in_bits=raw_obj.pattern_length_in_bits,
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.FixedFrameStreamType.SyncStrategy.SyncPattern:
        return xtce_1_1.FixedFrameStreamType.SyncStrategy.SyncPattern(
            pattern=self.pattern,
            bit_location_from_start_of_container=self.bit_location_from_start_of_container,
            mask=self.mask,
            mask_length_in_bits=self.mask_length_in_bits,
            pattern_length_in_bits=self.pattern_length_in_bits,
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.SyncPatternType:
        return xtce_1_2.SyncPatternType(
            pattern=self.pattern,
            bit_location_from_start_of_container=self.bit_location_from_start_of_container,
            mask=self.mask,
            mask_length_in_bits=self.mask_length_in_bits,
            pattern_length_in_bits=self.pattern_length_in_bits,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.SyncPatternType:
        return xtce_1_3.SyncPatternType(
            pattern=self.pattern,
            bit_location_from_start_of_container=self.bit_location_from_start_of_container,
            mask=self.mask,
            mask_length_in_bits=self.mask_length_in_bits,
            pattern_length_in_bits=self.pattern_length_in_bits,
        )


class FixedFrameSyncStrategy(SyncStrategy):
    """Define a fixed frame synchronization strategy."""

    sync_pattern: SyncPattern
    """The synchronization pattern used for fixed frame synchronization."""

    @classmethod
    def _from_v1_1(
        cls: type[Self], raw_obj: xtce_1_1.FixedFrameStreamType.SyncStrategy
    ) -> Self:
        return cls(
            auto_invert=AutoInvert._from_v1_1(raw_obj.auto_invert)
            if raw_obj.auto_invert is not None
            else None,
            verify_to_lock_good_frames=raw_obj.verify_to_lock_good_frames,
            check_to_lock_good_frames=raw_obj.check_to_lock_good_frames,
            max_bit_errors_in_sync_pattern=raw_obj.max_bit_errors_in_sync_pattern,
            sync_pattern=SyncPattern._from_v1_1(raw_obj.sync_pattern),
        )

    @classmethod
    def _from_v1_2(
        cls: type[Self], raw_obj: xtce_1_2.FixedFrameSyncStrategyType
    ) -> Self:
        return cls(
            auto_invert=AutoInvert._from_v1_2(raw_obj.auto_invert)
            if raw_obj.auto_invert is not None
            else None,
            verify_to_lock_good_frames=raw_obj.verify_to_lock_good_frames,
            check_to_lock_good_frames=raw_obj.check_to_lock_good_frames,
            max_bit_errors_in_sync_pattern=raw_obj.max_bit_errors_in_sync_pattern,
            sync_pattern=SyncPattern._from_v1_2(raw_obj.sync_pattern),
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], raw_obj: xtce_1_3.FixedFrameSyncStrategyType
    ) -> Self:
        return cls(
            auto_invert=AutoInvert._from_v1_3(raw_obj.auto_invert)
            if raw_obj.auto_invert is not None
            else None,
            verify_to_lock_good_frames=raw_obj.verify_to_lock_good_frames,
            check_to_lock_good_frames=raw_obj.check_to_lock_good_frames,
            max_bit_errors_in_sync_pattern=raw_obj.max_bit_errors_in_sync_pattern,
            sync_pattern=SyncPattern._from_v1_3(raw_obj.sync_pattern),
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.FixedFrameStreamType.SyncStrategy:
        return xtce_1_1.FixedFrameStreamType.SyncStrategy(
            auto_invert=self.auto_invert._to_v1_1(policy)
            if self.auto_invert is not None
            else None,
            verify_to_lock_good_frames=self.verify_to_lock_good_frames,
            check_to_lock_good_frames=self.check_to_lock_good_frames,
            max_bit_errors_in_sync_pattern=self.max_bit_errors_in_sync_pattern,
            sync_pattern=self.sync_pattern._to_v1_1(policy),
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.FixedFrameSyncStrategyType:
        return xtce_1_2.FixedFrameSyncStrategyType(
            auto_invert=self.auto_invert._to_v1_2(policy)
            if self.auto_invert is not None
            else None,
            verify_to_lock_good_frames=self.verify_to_lock_good_frames,
            check_to_lock_good_frames=self.check_to_lock_good_frames,
            max_bit_errors_in_sync_pattern=self.max_bit_errors_in_sync_pattern,
            sync_pattern=self.sync_pattern._to_v1_2(policy),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.FixedFrameSyncStrategyType:
        return xtce_1_3.FixedFrameSyncStrategyType(
            auto_invert=self.auto_invert._to_v1_3(policy)
            if self.auto_invert is not None
            else None,
            verify_to_lock_good_frames=self.verify_to_lock_good_frames,
            check_to_lock_good_frames=self.check_to_lock_good_frames,
            max_bit_errors_in_sync_pattern=self.max_bit_errors_in_sync_pattern,
            sync_pattern=self.sync_pattern._to_v1_3(policy),
        )


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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.FixedFrameStreamType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_1(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_1(raw_obj.ancillary_data_set),
            bit_rate_bps=raw_obj.bit_rate_in_bps,
            pcm_type=PcmType(raw_obj.pcm_type.value),
            inverted=raw_obj.inverted,
            ref=ContainerRef._from_v1_1(raw_obj.choice)
            if isinstance(raw_obj.choice, xtce_1_1.ContainerRefType)
            else ServiceRef._from_v1_1(unwrap(raw_obj.choice)),
            stream_ref=StreamRef._from_v1_1(raw_obj.stream_ref)
            if raw_obj.stream_ref is not None
            else None,
            sync_strategy=FixedFrameSyncStrategy._from_v1_1(raw_obj.sync_strategy),
            sync_aperture_bits=raw_obj.sync_aperture_in_bits,
            frame_length_bits=raw_obj.frame_length_in_bits,
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.FixedFrameStreamType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_2(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_2(raw_obj.ancillary_data_set),
            bit_rate_bps=raw_obj.bit_rate_in_bps,
            pcm_type=PcmType(raw_obj.pcm_type.value),
            inverted=raw_obj.inverted,
            ref=ContainerRef._from_v1_2(raw_obj.choice)
            if isinstance(raw_obj.choice, xtce_1_2.ContainerRefType)
            else ServiceRef._from_v1_2(unwrap(raw_obj.choice)),
            stream_ref=StreamRef._from_v1_2(raw_obj.stream_ref)
            if raw_obj.stream_ref is not None
            else None,
            sync_strategy=FixedFrameSyncStrategy._from_v1_2(raw_obj.sync_strategy),
            sync_aperture_bits=raw_obj.sync_aperture_in_bits,
            frame_length_bits=raw_obj.frame_length_in_bits,
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.FixedFrameStreamType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_3(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_3(raw_obj.ancillary_data_set),
            bit_rate_bps=raw_obj.bit_rate_in_bps,
            pcm_type=PcmType(raw_obj.pcm_type.value),
            inverted=raw_obj.inverted,
            ref=ContainerRef._from_v1_3(raw_obj.choice)
            if isinstance(raw_obj.choice, xtce_1_3.ContainerRefType)
            else ServiceRef._from_v1_3(unwrap(raw_obj.choice)),
            stream_ref=StreamRef._from_v1_3(raw_obj.stream_ref)
            if raw_obj.stream_ref is not None
            else None,
            sync_strategy=FixedFrameSyncStrategy._from_v1_3(raw_obj.sync_strategy),
            sync_aperture_bits=raw_obj.sync_aperture_in_bits,
            frame_length_bits=raw_obj.frame_length_in_bits,
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.FixedFrameStreamType:
        return xtce_1_1.FixedFrameStreamType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_1(policy),
            ancillary_data_set=self._ancillary_data_to_v1_1(policy),
            bit_rate_in_bps=self.bit_rate_bps,
            pcm_type=xtce_1_1.PcmstreamTypePcmType(self.pcm_type.value),
            inverted=self.inverted,
            choice=self.ref._to_v1_1(policy),
            stream_ref=self.stream_ref._to_v1_1(policy)
            if self.stream_ref is not None
            else None,
            sync_strategy=self.sync_strategy._to_v1_1(policy),
            sync_aperture_in_bits=self.sync_aperture_bits,
            frame_length_in_bits=self.frame_length_bits,
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.FixedFrameStreamType:
        return xtce_1_2.FixedFrameStreamType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_2(policy),
            ancillary_data_set=self._ancillary_data_to_v1_2(policy),
            bit_rate_in_bps=self.bit_rate_bps,
            pcm_type=xtce_1_2.Pcmtype(self.pcm_type.value),
            inverted=self.inverted,
            choice=self.ref._to_v1_2(policy),
            stream_ref=self.stream_ref._to_v1_2(policy)
            if self.stream_ref is not None
            else None,
            sync_strategy=self.sync_strategy._to_v1_2(policy),
            sync_aperture_in_bits=self.sync_aperture_bits,
            frame_length_in_bits=self.frame_length_bits,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.FixedFrameStreamType:
        return xtce_1_3.FixedFrameStreamType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_3(policy),
            ancillary_data_set=self._ancillary_data_to_v1_3(policy),
            bit_rate_in_bps=self.bit_rate_bps,
            pcm_type=xtce_1_3.Pcmtype(self.pcm_type.value),
            inverted=self.inverted,
            choice=self.ref._to_v1_3(policy),
            stream_ref=self.stream_ref._to_v1_3(policy)
            if self.stream_ref is not None
            else None,
            sync_strategy=self.sync_strategy._to_v1_3(policy),
            sync_aperture_in_bits=self.sync_aperture_bits,
            frame_length_in_bits=self.frame_length_bits,
        )


class Flag(XtceBaseModel):
    """Define a flag used to look for frame synchronization."""

    flag_size_bits: int = Field(default=6, ge=1)
    """The size of the flag in bits."""

    flag_bit_type: FlagBit = Field(default=FlagBit.ONES)
    """The type of bits used in the flag."""

    @classmethod
    def _from_v1_1(
        cls: type[Self], raw_obj: xtce_1_1.VariableFrameStreamType.SyncStrategy.Flag
    ) -> Self:
        return cls(
            flag_size_bits=raw_obj.flag_size_in_bits,
            flag_bit_type=FlagBit(raw_obj.flag_bit_type.value),
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.FlagType) -> Self:
        return cls(
            flag_size_bits=raw_obj.flag_size_in_bits,
            flag_bit_type=FlagBit(raw_obj.flag_bit_type.value),
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.FlagType) -> Self:
        return cls(
            flag_size_bits=raw_obj.flag_size_in_bits,
            flag_bit_type=FlagBit(raw_obj.flag_bit_type.value),
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.VariableFrameStreamType.SyncStrategy.Flag:
        return xtce_1_1.VariableFrameStreamType.SyncStrategy.Flag(
            flag_size_in_bits=self.flag_size_bits,
            flag_bit_type=xtce_1_1.FlagFlagBitType(self.flag_bit_type.value),
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.FlagType:
        return xtce_1_2.FlagType(
            flag_size_in_bits=self.flag_size_bits,
            flag_bit_type=xtce_1_2.FlagBitType(self.flag_bit_type.value),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.FlagType:
        return xtce_1_3.FlagType(
            flag_size_in_bits=self.flag_size_bits,
            flag_bit_type=xtce_1_3.FlagBitType(self.flag_bit_type.value),
        )


class VariableFrameSyncStrategy(SyncStrategy):
    """Define a variable frame synchronization strategy."""

    flag: Flag

    @classmethod
    def _from_v1_1(
        cls: type[Self], raw_obj: xtce_1_1.VariableFrameStreamType.SyncStrategy
    ) -> Self:
        return cls(
            auto_invert=AutoInvert._from_v1_1(raw_obj.auto_invert)
            if raw_obj.auto_invert is not None
            else None,
            verify_to_lock_good_frames=raw_obj.verify_to_lock_good_frames,
            check_to_lock_good_frames=raw_obj.check_to_lock_good_frames,
            max_bit_errors_in_sync_pattern=raw_obj.max_bit_errors_in_sync_pattern,
            flag=Flag._from_v1_1(raw_obj.flag),
        )

    @classmethod
    def _from_v1_2(
        cls: type[Self], raw_obj: xtce_1_2.VariableFrameSyncStrategyType
    ) -> Self:
        return cls(
            auto_invert=AutoInvert._from_v1_2(raw_obj.auto_invert)
            if raw_obj.auto_invert is not None
            else None,
            verify_to_lock_good_frames=raw_obj.verify_to_lock_good_frames,
            check_to_lock_good_frames=raw_obj.check_to_lock_good_frames,
            max_bit_errors_in_sync_pattern=raw_obj.max_bit_errors_in_sync_pattern,
            flag=Flag._from_v1_2(raw_obj.flag),
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], raw_obj: xtce_1_3.VariableFrameSyncStrategyType
    ) -> Self:
        return cls(
            auto_invert=AutoInvert._from_v1_3(raw_obj.auto_invert)
            if raw_obj.auto_invert is not None
            else None,
            verify_to_lock_good_frames=raw_obj.verify_to_lock_good_frames,
            check_to_lock_good_frames=raw_obj.check_to_lock_good_frames,
            max_bit_errors_in_sync_pattern=raw_obj.max_bit_errors_in_sync_pattern,
            flag=Flag._from_v1_3(raw_obj.flag),
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.VariableFrameStreamType.SyncStrategy:
        return xtce_1_1.VariableFrameStreamType.SyncStrategy(
            auto_invert=self.auto_invert._to_v1_1(policy)
            if self.auto_invert is not None
            else None,
            verify_to_lock_good_frames=self.verify_to_lock_good_frames,
            check_to_lock_good_frames=self.check_to_lock_good_frames,
            max_bit_errors_in_sync_pattern=self.max_bit_errors_in_sync_pattern,
            flag=self.flag._to_v1_1(policy),
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.VariableFrameSyncStrategyType:
        return xtce_1_2.VariableFrameSyncStrategyType(
            auto_invert=self.auto_invert._to_v1_2(policy)
            if self.auto_invert is not None
            else None,
            verify_to_lock_good_frames=self.verify_to_lock_good_frames,
            check_to_lock_good_frames=self.check_to_lock_good_frames,
            max_bit_errors_in_sync_pattern=self.max_bit_errors_in_sync_pattern,
            flag=self.flag._to_v1_2(policy),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.VariableFrameSyncStrategyType:
        return xtce_1_3.VariableFrameSyncStrategyType(
            auto_invert=self.auto_invert._to_v1_3(policy)
            if self.auto_invert is not None
            else None,
            verify_to_lock_good_frames=self.verify_to_lock_good_frames,
            check_to_lock_good_frames=self.check_to_lock_good_frames,
            max_bit_errors_in_sync_pattern=self.max_bit_errors_in_sync_pattern,
            flag=self.flag._to_v1_3(policy),
        )


class VariableFrameStream(FrameStream):
    """Define a stream that contains variable-length frames.

    The frames are found by looking for a series of one's or zero's within the stream.

    """

    sync_strategy: VariableFrameSyncStrategy
    """The strategy used to identify the start of variable-length frames within the
    stream.
    """

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.VariableFrameStreamType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_1(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_1(raw_obj.ancillary_data_set),
            bit_rate_bps=raw_obj.bit_rate_in_bps,
            pcm_type=PcmType(raw_obj.pcm_type.value),
            inverted=raw_obj.inverted,
            ref=ContainerRef._from_v1_1(raw_obj.choice)
            if isinstance(raw_obj.choice, xtce_1_1.ContainerRefType)
            else ServiceRef._from_v1_1(unwrap(raw_obj.choice)),
            stream_ref=StreamRef._from_v1_1(raw_obj.stream_ref)
            if raw_obj.stream_ref is not None
            else None,
            sync_strategy=VariableFrameSyncStrategy._from_v1_1(raw_obj.sync_strategy),
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.VariableFrameStreamType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_2(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_2(raw_obj.ancillary_data_set),
            bit_rate_bps=raw_obj.bit_rate_in_bps,
            pcm_type=PcmType(raw_obj.pcm_type.value),
            inverted=raw_obj.inverted,
            ref=ContainerRef._from_v1_2(raw_obj.choice)
            if isinstance(raw_obj.choice, xtce_1_2.ContainerRefType)
            else ServiceRef._from_v1_2(unwrap(raw_obj.choice)),
            stream_ref=StreamRef._from_v1_2(raw_obj.stream_ref)
            if raw_obj.stream_ref is not None
            else None,
            sync_strategy=VariableFrameSyncStrategy._from_v1_2(raw_obj.sync_strategy),
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.VariableFrameStreamType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_3(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_3(raw_obj.ancillary_data_set),
            bit_rate_bps=raw_obj.bit_rate_in_bps,
            pcm_type=PcmType(raw_obj.pcm_type.value),
            inverted=raw_obj.inverted,
            ref=ContainerRef._from_v1_3(raw_obj.choice)
            if isinstance(raw_obj.choice, xtce_1_3.ContainerRefType)
            else ServiceRef._from_v1_3(unwrap(raw_obj.choice)),
            stream_ref=StreamRef._from_v1_3(raw_obj.stream_ref)
            if raw_obj.stream_ref is not None
            else None,
            sync_strategy=VariableFrameSyncStrategy._from_v1_3(raw_obj.sync_strategy),
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.VariableFrameStreamType:
        return xtce_1_1.VariableFrameStreamType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_1(policy),
            ancillary_data_set=self._ancillary_data_to_v1_1(policy),
            bit_rate_in_bps=self.bit_rate_bps,
            pcm_type=xtce_1_1.PcmstreamTypePcmType(self.pcm_type.value),
            inverted=self.inverted,
            choice=self.ref._to_v1_1(policy),
            stream_ref=self.stream_ref._to_v1_1(policy)
            if self.stream_ref is not None
            else None,
            sync_strategy=self.sync_strategy._to_v1_1(policy),
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.VariableFrameStreamType:
        return xtce_1_2.VariableFrameStreamType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_2(policy),
            ancillary_data_set=self._ancillary_data_to_v1_2(policy),
            bit_rate_in_bps=self.bit_rate_bps,
            pcm_type=xtce_1_2.Pcmtype(self.pcm_type.value),
            inverted=self.inverted,
            choice=self.ref._to_v1_2(policy),
            stream_ref=self.stream_ref._to_v1_2(policy)
            if self.stream_ref is not None
            else None,
            sync_strategy=self.sync_strategy._to_v1_2(policy),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.VariableFrameStreamType:
        return xtce_1_3.VariableFrameStreamType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_3(policy),
            ancillary_data_set=self._ancillary_data_to_v1_3(policy),
            bit_rate_in_bps=self.bit_rate_bps,
            pcm_type=xtce_1_3.Pcmtype(self.pcm_type.value),
            inverted=self.inverted,
            choice=self.ref._to_v1_3(policy),
            stream_ref=self.stream_ref._to_v1_3(policy)
            if self.stream_ref is not None
            else None,
            sync_strategy=self.sync_strategy._to_v1_3(policy),
        )


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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.RateInStreamType) -> Self:
        return cls(
            basis=Basis(raw_obj.basis.value),
            minimum_value=raw_obj.minimum_value,
            maximum_value=raw_obj.maximum_value,
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.RateInStreamType) -> Self:
        return cls(
            basis=Basis(raw_obj.basis.value),
            minimum_value=raw_obj.minimum_value,
            maximum_value=raw_obj.maximum_value,
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.RateInStreamType) -> Self:
        return cls(
            basis=Basis(raw_obj.basis.value),
            minimum_value=raw_obj.minimum_value,
            maximum_value=raw_obj.maximum_value,
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.RateInStreamType:
        return xtce_1_1.RateInStreamType(
            basis=xtce_1_1.RateInStreamTypeBasis(self.basis.value),
            minimum_value=self.minimum_value,
            maximum_value=self.maximum_value,
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.RateInStreamType:
        return xtce_1_2.RateInStreamType(
            basis=xtce_1_2.BasisType(self.basis.value),
            minimum_value=self.minimum_value,
            maximum_value=self.maximum_value,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.RateInStreamType:
        return xtce_1_3.RateInStreamType(
            basis=xtce_1_3.BasisType(self.basis.value),
            minimum_value=self.minimum_value,
            maximum_value=self.maximum_value,
        )


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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(
        cls: type[Self], raw_obj: xtce_1_2.RateInStreamWithStreamNameType
    ) -> Self:
        return cls(
            basis=Basis(raw_obj.basis.value),
            minimum_value=raw_obj.minimum_value,
            maximum_value=raw_obj.maximum_value,
            stream_ref=XtcePath(raw_obj.stream_ref),
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], raw_obj: xtce_1_3.RateInStreamWithStreamNameType
    ) -> Self:
        return cls(
            basis=Basis(raw_obj.basis.value),
            minimum_value=raw_obj.minimum_value,
            maximum_value=raw_obj.maximum_value,
            stream_ref=XtcePath(raw_obj.stream_ref),
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.RateInStreamWithStreamNameType:
        return xtce_1_2.RateInStreamWithStreamNameType(
            basis=xtce_1_2.BasisType(self.basis.value),
            minimum_value=self.minimum_value,
            maximum_value=self.maximum_value,
            stream_ref=str(self.stream_ref),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.RateInStreamWithStreamNameType:
        return xtce_1_3.RateInStreamWithStreamNameType(
            basis=xtce_1_3.BasisType(self.basis.value),
            minimum_value=self.minimum_value,
            maximum_value=self.maximum_value,
            stream_ref=str(self.stream_ref),
        )
