"""Stream models."""

from pydantic import Field

from ._base import XtceBaseModel
from .common import NameDescriptionBase
from .enum import Basis, FlagBit, PcmType
from .processing import InputAlgorithm, InputOutputAlgorithm
from .reference import ContainerRef, ServiceRef, StreamRef


class PcmStream(NameDescriptionBase):
    bit_rate_bps: float | None = Field(default=None)
    pcm_type: PcmType = Field(default=PcmType.NRZL)
    inverted: bool = Field(default=False)


class CustomStream(PcmStream):
    encoding_algorithm: InputAlgorithm = Field(...)
    decoding_algorithm: InputOutputAlgorithm = Field(...)
    encoded_stream_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )
    decoded_stream_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )


class FrameStream(PcmStream):
    ref: ContainerRef | ServiceRef | None = Field(default=None)
    stream_ref: StreamRef | None = Field(default=None)


class AutoInvert(XtceBaseModel):
    invert_algorithm: InputAlgorithm | None = Field(default=None)
    bad_frames_to_auto_invert: int | None = Field(default=1024, ge=1)


class SyncStrategy(XtceBaseModel):
    auto_invert: AutoInvert | None = Field(default=None)
    verify_to_lock_good_frames: int = Field(default=4, ge=0)
    check_to_lock_good_frames: int = Field(default=1, ge=0)
    max_bit_errors_in_sync_pattern: int = Field(default=0, ge=0)


class SyncPattern(XtceBaseModel):
    pattern: bytes = Field(..., min_length=1)  # TODO check min
    bit_location_from_start_of_container: int = Field(default=0)
    mask: bytes | None = Field(default=None)
    mask_length_in_bits: int | None = Field(default=None, ge=1)
    pattern_length_in_bits: int = Field(..., ge=1)


class FixedFrameSyncStrategy(SyncStrategy):
    sync_pattern: SyncPattern = Field(...)


class FixedFrameStream(FrameStream):
    sync_strategy: FixedFrameSyncStrategy = Field(...)
    sync_aperture_in_bits: int = Field(default=0, ge=0)
    frame_length_in_bits: int = Field(...)


class Flag(XtceBaseModel):
    flag_size_in_bits: int = Field(default=6, ge=1)
    flag_bit_type: FlagBit = Field(default=FlagBit.ONES)


class VariableFrameSyncStrategy(SyncStrategy):
    flag: Flag = Field(...)


class VariableFrameStream(FrameStream):
    sync_strategy: VariableFrameSyncStrategy = Field(...)


class RateInStream(XtceBaseModel):
    basis: Basis = Field(default=Basis.PER_SECOND)
    minimum_value: float | None = Field(default=None)
    maximum_value: float | None = Field(default=None)


class RateInStreamWithStreamName(RateInStream):
    stream_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )
