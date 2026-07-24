"""Stream models."""

from abc import ABC
from typing import Any, Self

from pydantic import Field

from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy, XtceUnsupportedError

from ._base import XtceBaseModel
from .algorithm import InputAlgorithm, InputOutputAlgorithm
from .common import NameDescriptionBase
from .enum import Basis, FlagBit, PcmType
from .reference import ContainerRef, ServiceRef, StreamRef


class PcmStream(NameDescriptionBase, ABC):
    bit_rate_bps: float | None = Field(default=None)
    pcm_type: PcmType = Field(default=PcmType.NRZL)
    inverted: bool = Field(default=False)

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_2, cls.__name__)

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_3, cls.__name__)

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_2, self.__class__.__name__)

    def _to_v1_3(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_3, self.__class__.__name__)


class CustomStream(PcmStream):
    encoding_algorithm: InputAlgorithm
    decoding_algorithm: InputOutputAlgorithm
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
    sync_pattern: SyncPattern


class FixedFrameStream(FrameStream):
    sync_strategy: FixedFrameSyncStrategy
    sync_aperture_in_bits: int = Field(default=0, ge=0)
    frame_length_in_bits: int


class Flag(XtceBaseModel):
    flag_size_in_bits: int = Field(default=6, ge=1)
    flag_bit_type: FlagBit = Field(default=FlagBit.ONES)


class VariableFrameSyncStrategy(SyncStrategy):
    flag: Flag


class VariableFrameStream(FrameStream):
    sync_strategy: VariableFrameSyncStrategy


class RateInStream(XtceBaseModel):
    basis: Basis = Field(default=Basis.PER_SECOND)
    minimum_value: float | None = Field(default=None)
    maximum_value: float | None = Field(default=None)


class RateInStreamWithStreamName(RateInStream):
    stream_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )
