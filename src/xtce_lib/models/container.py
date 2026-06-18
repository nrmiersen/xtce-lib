"""Container models."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from ._base import XtceBaseModel
from .array import ArgumentDimension, Dimension
from .common import AncillaryData, NameDescriptionBase
from .enum import ReferenceLocation
from .misc import ArgumentRepeat, Repeat
from .processing import (
    CRC,
    XOR,
    ArgumentDiscreteLookupList,
    ArgumentMatchCriteria,
    Checksum,
    InputAlgorithm,
    MatchCriteria,
    Parity,
)
from .reference import ContainerRef, ParameterInstanceRef
from .stream import RateInStream, RateInStreamWithStreamName
from .time import TimeAssociation

if TYPE_CHECKING:
    from .codec import ArgumentDynamicValue, DiscreteLookupList, DynamicValue

# IntegerValueType = int | DynamicValue | DiscreteLookupList


class LocationInContainer(XtceBaseModel):
    offset: int | DynamicValue | DiscreteLookupList | None = Field(default=None)
    reference_location: ReferenceLocation = Field(
        default=ReferenceLocation.PREVIOUS_ENTRY
    )

    # TODO make sure 'offset' is an appropriate attribute name for all cases


class ArgumentLocationInContainer(XtceBaseModel):
    offset: int | ArgumentDynamicValue | ArgumentDiscreteLookupList | None = Field(
        default=None
    )
    reference_location: ReferenceLocation = Field(
        default=ReferenceLocation.PREVIOUS_ENTRY
    )

    # TODO make sure 'offset' is an appropriate attribute name for all cases


class SequenceEntry(XtceBaseModel):
    location_in_container: LocationInContainer | None = Field(default=None)
    repeat_entry: Repeat | None = Field(default=None)
    include_condition: MatchCriteria | None = Field(default=None)
    time_association: TimeAssociation | None = Field(default=None)
    ancillary_data: list[AncillaryData] = Field(default_factory=list, min_length=1)
    short_description: str | None = Field(default=None, max_length=80)


class ArgumentSequenceEntry(XtceBaseModel):
    location_in_container_in_bits: ArgumentLocationInContainer | None = Field(
        default=None
    )
    repeat_entry: ArgumentRepeat | None = Field(default=None)
    include_condition: ArgumentMatchCriteria | None = Field(default=None)
    ancillary_data: list[AncillaryData] = Field(default_factory=list, min_length=1)
    short_description: str | None = Field(default=None)


class ParameterRefEntry(SequenceEntry):
    parameter_ref: str = Field(
        ...,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
    )


class ArgumentParameterRefEntry(ArgumentSequenceEntry):
    parameter_ref: str = Field(
        ...,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
    )


class ParameterSegmentRefEntry(SequenceEntry):
    parameter_ref: str = Field(
        ...,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
    )
    order: int | None = Field(default=None, ge=1)
    size_in_bits: int = Field(..., ge=1)


class ArgumentParameterSegmentRefEntry(ArgumentSequenceEntry):
    parameter_ref: str = Field(
        ...,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
    )
    order: int | None = Field(default=None, ge=1)
    size_in_bits: int = Field(..., ge=1)


class ContainerRefEntry(SequenceEntry):
    container_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )


class ArgumentContainerRefEntry(ArgumentSequenceEntry):
    container_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )


class ContainerSegmentRefEntry(SequenceEntry):
    container_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )
    order: int | None = Field(default=None, ge=1)
    size_in_bits: int = Field(..., ge=1)


class ArgumentContainerSegmentRefEntry(ArgumentSequenceEntry):
    container_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )
    order: int | None = Field(default=None, ge=1)
    size_in_bits: int = Field(..., ge=1)


class StreamSegmentEntry(SequenceEntry):
    stream_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )
    order: int | None = Field(default=None, ge=1)
    size_in_bits: int = Field(..., ge=1)


class ArgumentStreamSegmentEntry(ArgumentSequenceEntry):
    stream_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )
    order: int | None = Field(default=None, ge=1)
    size_in_bits: int = Field(..., ge=1)


class IndirectParameterRefEntry(SequenceEntry):
    parameter_instance: ParameterInstanceRef = Field(...)
    alias_name_space: str | None = Field(default=None)


class ArgumentIndirectParameterRefEntry(ArgumentSequenceEntry):
    parameter_instance: ParameterInstanceRef = Field(...)
    alias_name_space: str | None = Field(default=None)


class ArrayParameterRefEntry(SequenceEntry):
    dimensions: list[Dimension] = Field(default_factory=list, min_length=1)
    parameter_ref: str = Field(
        ...,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
    )


class ArgumentArrayParameterRefEntry(ArgumentSequenceEntry):
    dimensions: list[Dimension] = Field(default_factory=list, min_length=1)
    parameter_ref: str = Field(
        ...,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
    )
    last_entry_for_this_array_instance: bool = Field(default=False)


class RestrictionCriteria(MatchCriteria):
    next_container: ContainerRef | None = Field(default=None)


class BaseContainer(XtceBaseModel):
    restriction_criteria: RestrictionCriteria | None = Field(default=None)
    container_ref: str | None = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )


class ContainerBinaryDataEncoding(XtceBaseModel):
    error_detect_correct: list[Checksum | CRC | XOR | Parity] | None = Field(
        default=None
    )
    size_in_bits: int | DynamicValue | DiscreteLookupList | None = Field(default=None)
    from_binary_transform_algorithm: InputAlgorithm | None = Field(default=None)
    to_binary_transform_algorithm: InputAlgorithm | None = Field(default=None)


class Container(NameDescriptionBase):
    default_rate_in_stream: RateInStream | None = Field(default=None)
    rate_in_streams: list[RateInStreamWithStreamName] = Field(
        default_factory=list, min_length=1
    )
    binary_encoding: ContainerBinaryDataEncoding | None = Field(default=None)

    # TODO maybe consolidate RateInStream and RateInStreamWithStreamName into one model with optional stream_ref


class SequenceContainer(Container):
    entries: list[
        ParameterRefEntry
        | ParameterSegmentRefEntry
        | ContainerRefEntry
        | ContainerSegmentRefEntry
        | StreamSegmentEntry
        | IndirectParameterRefEntry
        | ArrayParameterRefEntry
    ]
    base_container: BaseContainer | None = Field(default=None)
    abstract: bool = Field(default=False)
    idle_pattern: int | str = Field(default=0, pattern=r"0[xX][0-9a-fA-F]+")


class ArgumentArgumentRefEntry(ArgumentSequenceEntry):
    argument_ref: str = Field(
        ..., pattern=r"([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)"
    )


class ArgumentArrayArgumentRefEntry(ArgumentSequenceEntry):
    dimensions: list[ArgumentDimension] = Field(default_factory=list, min_length=1)
    argument_ref: str = Field(
        ..., pattern=r"([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)"
    )
    last_entry_for_this_array_instance: bool = Field(default=False)


class ArgumentFixedValueEntry(ArgumentSequenceEntry):
    name: str | None = Field(default=None)
    binary_value: bytes = Field(...)
    size_in_bits: int = Field(...)


class CommandContainer(Container):
    entries: list[
        ArgumentParameterRefEntry
        | ArgumentParameterSegmentRefEntry
        | ArgumentContainerRefEntry
        | ArgumentContainerSegmentRefEntry
        | ArgumentStreamSegmentEntry
        | ArgumentIndirectParameterRefEntry
        | ArgumentArrayParameterRefEntry
        | ArgumentArgumentRefEntry
        | ArgumentArrayArgumentRefEntry
        | ArgumentFixedValueEntry
    ]
    base_container: BaseContainer | None = Field(default=None)
