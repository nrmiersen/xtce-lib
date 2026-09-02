"""Container models."""

from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Annotated, Any, Literal

from pydantic import AfterValidator, Field

from xtce_lib.common.xtce_path import XtcePath, require_regex
from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from ._pattern import EXPD_NAME_REF_W_PATH, NAME_REF_W_PATH
from ._type_aliases import XtceHexOrInt
from .algorithm import CRC, XOR, Checksum, InputAlgorithm, Parity
from .array import ArgumentDimension, Dimension
from .codec import (
    pack_argument_integer_value_v1_1,
    pack_argument_integer_value_v1_2,
    pack_argument_integer_value_v1_3,
    pack_integer_value_v1_1,
    pack_integer_value_v1_2,
    pack_integer_value_v1_3,
    parse_argument_integer_value_v1_1,
    parse_argument_integer_value_v1_2,
    parse_argument_integer_value_v1_3,
    parse_integer_value_v1_1,
    parse_integer_value_v1_2,
    parse_integer_value_v1_3,
)
from .common import AncillaryData, NameDescriptionBase
from .condition import ArgumentDiscreteLookupList, ArgumentMatchCriteria, MatchCriteria
from .enum import ReferenceLocation
from .reference import ContainerRef, ParameterInstanceRef
from .stream import RateInStream, RateInStreamWithStreamName
from .time import TimeAssociation

if TYPE_CHECKING:
    from .codec import ArgumentDynamicValue, DiscreteLookupList, DynamicValue


class Repeat(XtceBaseModel):
    """Define a repeat entry within a container."""

    count: int | DynamicValue | DiscreteLookupList = Field(..., ge=1)
    """The number of times the entry appears in the container.

    A count of 1 indicates no repetition.

    """

    offset: int | DynamicValue | DiscreteLookupList = Field(default=0, ge=0)
    """The number of bits between repeats of the entry."""

    # TODO may need to validate >0 for DynamicValue and DiscreteLookupList

    _v1_1_type = xtce_1_1.RepeatType
    _v1_2_type = xtce_1_2.RepeatType
    _v1_3_type = xtce_1_3.RepeatType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.RepeatType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["count"] = parse_integer_value_v1_1(obj.count)
        kwargs["offset"] = parse_integer_value_v1_1(obj.offset) or 0
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.RepeatType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["count"] = parse_integer_value_v1_2(obj.count)
        kwargs["offset"] = parse_integer_value_v1_2(obj.offset) or 0
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.RepeatType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["count"] = parse_integer_value_v1_3(obj.count)
        kwargs["offset"] = parse_integer_value_v1_3(obj.offset) or 0
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["count"] = pack_integer_value_v1_1(self.count, policy)
        kwargs["offset"] = pack_integer_value_v1_1(self.offset, policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["count"] = pack_integer_value_v1_2(self.count, policy)
        kwargs["offset"] = pack_integer_value_v1_2(self.offset, policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["count"] = pack_integer_value_v1_3(self.count, policy)
        kwargs["offset"] = pack_integer_value_v1_3(self.offset, policy)
        return kwargs


class ArgumentRepeat(XtceBaseModel):
    """Define a repeat argument entry within a container."""

    count: int | ArgumentDynamicValue | ArgumentDiscreteLookupList = Field(..., ge=1)
    """The number of times the entry appears in the container.

    A count of 1 indicates no repetition.

    """

    offset: int | ArgumentDynamicValue | ArgumentDiscreteLookupList = Field(
        default=0, ge=0
    )
    """The number of bits between repeats of the entry."""

    _v1_1_type = xtce_1_1.RepeatType
    _v1_2_type = xtce_1_2.ArgumentRepeatType
    _v1_3_type = xtce_1_3.ArgumentRepeatType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.RepeatType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["count"] = parse_argument_integer_value_v1_1(obj.count)
        kwargs["offset"] = parse_argument_integer_value_v1_1(obj.offset) or 0
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ArgumentRepeatType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["count"] = parse_argument_integer_value_v1_2(obj.count)
        kwargs["offset"] = parse_argument_integer_value_v1_2(obj.offset) or 0
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ArgumentRepeatType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["count"] = parse_argument_integer_value_v1_3(obj.count)
        kwargs["offset"] = parse_argument_integer_value_v1_3(obj.offset) or 0
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["count"] = pack_argument_integer_value_v1_1(self.count, policy)
        kwargs["offset"] = pack_argument_integer_value_v1_1(self.offset, policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["count"] = pack_argument_integer_value_v1_2(self.count, policy)
        kwargs["offset"] = pack_argument_integer_value_v1_2(self.offset, policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["count"] = pack_argument_integer_value_v1_3(self.count, policy)
        kwargs["offset"] = pack_argument_integer_value_v1_3(self.offset, policy)
        return kwargs


class LocationInContainer(XtceBaseModel):
    """Define the location of an entry within the container."""

    offset: int | DynamicValue | DiscreteLookupList | None = None
    """The offset of the entry within the container in bits."""

    reference_location: ReferenceLocation = ReferenceLocation.PREVIOUS_ENTRY
    """The reference location for the offset within the container."""

    _v1_1_type = xtce_1_1.SequenceEntryType.LocationInContainerInBits
    _v1_2_type = xtce_1_2.LocationInContainerInBitsType
    _v1_3_type = xtce_1_3.LocationInContainerInBitsType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.SequenceEntryType.LocationInContainerInBits
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        # In the schema, this type inherits IntegerValueType, so just pass the whole
        # object
        kwargs["offset"] = parse_integer_value_v1_1(obj)
        kwargs["reference_location"] = ReferenceLocation(obj.reference_location.value)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.LocationInContainerInBitsType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["offset"] = parse_integer_value_v1_2(obj)
        kwargs["reference_location"] = ReferenceLocation(obj.reference_location.value)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.LocationInContainerInBitsType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["offset"] = parse_integer_value_v1_3(obj)
        kwargs["reference_location"] = ReferenceLocation(obj.reference_location.value)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        offset = pack_integer_value_v1_1(self.offset, policy)
        kwargs["choice"] = offset.choice if offset is not None else None
        kwargs["reference_location"] = (
            xtce_1_1.LocationInContainerInBitsReferenceLocation(
                self.reference_location.value
            )
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        offset = pack_integer_value_v1_2(self.offset, policy)
        kwargs["choice"] = offset.choice if offset is not None else None
        kwargs["reference_location"] = xtce_1_2.ReferenceLocationType(
            self.reference_location.value
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        offset = pack_integer_value_v1_3(self.offset, policy)
        kwargs["choice"] = offset.choice if offset is not None else None
        kwargs["reference_location"] = xtce_1_3.ReferenceLocationType(
            self.reference_location.value
        )
        return kwargs


class ArgumentLocationInContainer(XtceBaseModel):
    """Define the location of an argument entry within the container."""

    offset: int | ArgumentDynamicValue | ArgumentDiscreteLookupList | None = None
    """The offset of the entry within the container in bits."""

    reference_location: ReferenceLocation = ReferenceLocation.PREVIOUS_ENTRY
    """The reference location of the entry within the container."""

    _v1_1_type = xtce_1_1.SequenceEntryType.LocationInContainerInBits
    _v1_2_type = xtce_1_2.ArgumentLocationInContainerInBitsType
    _v1_3_type = xtce_1_3.ArgumentLocationInContainerInBitsType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.SequenceEntryType.LocationInContainerInBits
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        # In the schema, this type inherits ArgumentIntegerValueType, so just pass the
        # whole object
        kwargs["offset"] = parse_argument_integer_value_v1_1(obj)
        kwargs["reference_location"] = ReferenceLocation(obj.reference_location.value)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentLocationInContainerInBitsType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["offset"] = parse_argument_integer_value_v1_2(obj)
        kwargs["reference_location"] = ReferenceLocation(obj.reference_location.value)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentLocationInContainerInBitsType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["offset"] = parse_argument_integer_value_v1_3(obj)
        kwargs["reference_location"] = ReferenceLocation(obj.reference_location.value)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        offset = pack_argument_integer_value_v1_1(self.offset, policy)
        kwargs["choice"] = offset.choice if offset is not None else None
        kwargs["reference_location"] = (
            xtce_1_1.LocationInContainerInBitsReferenceLocation(
                self.reference_location.value
            )
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        offset = pack_argument_integer_value_v1_2(self.offset, policy)
        kwargs["choice"] = offset.choice if offset is not None else None
        kwargs["reference_location"] = xtce_1_2.ReferenceLocationType(
            self.reference_location.value
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        offset = pack_argument_integer_value_v1_3(self.offset, policy)
        kwargs["choice"] = offset.choice if offset is not None else None
        kwargs["reference_location"] = xtce_1_3.ReferenceLocationType(
            self.reference_location.value
        )
        return kwargs


class SequenceEntry(XtceBaseModel, ABC):
    """Abstract base class for a sequence entry in a container."""

    # TODO add more info in docstrings

    location_in_container: LocationInContainer | None = None
    """The location of the entry in the container."""

    repeat_entry: Repeat | None = None
    """Indicates if the entry should be repeated in the container."""

    include_condition: MatchCriteria | None = None
    """The condition that must be met for the entry to be included in the container."""

    time_association: TimeAssociation | None = None
    """Optional timing information associated with the entry."""

    ancillary_data: list[AncillaryData] = Field(default_factory=list)
    """Optional ancillary data associated with the entry."""

    short_description: str | None = Field(default=None, max_length=80)
    """A short description of the entry."""

    _v1_1_type = xtce_1_1.SequenceEntryType
    _v1_2_type = xtce_1_2.SequenceEntryType
    _v1_3_type = xtce_1_3.SequenceEntryType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.SequenceEntryType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["location_in_container"] = (
            LocationInContainer._from_v1_1_kwargs(obj.location_in_container_in_bits)
            if obj.location_in_container_in_bits is not None
            else None
        )
        kwargs["repeat_entry"] = (
            Repeat._from_v1_1_kwargs(obj.repeat_entry)
            if obj.repeat_entry is not None
            else None
        )
        kwargs["include_condition"] = (
            MatchCriteria._from_v1_1_kwargs(obj.include_condition)
            if obj.include_condition is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.SequenceEntryType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["location_in_container"] = (
            LocationInContainer._from_v1_2_kwargs(obj.location_in_container_in_bits)
            if obj.location_in_container_in_bits is not None
            else None
        )
        kwargs["repeat_entry"] = (
            Repeat._from_v1_2_kwargs(obj.repeat_entry)
            if obj.repeat_entry is not None
            else None
        )
        kwargs["include_condition"] = (
            MatchCriteria._from_v1_2_kwargs(obj.include_condition)
            if obj.include_condition is not None
            else None
        )
        kwargs["time_association"] = (
            TimeAssociation._from_v1_2_kwargs(obj.time_association)
            if obj.time_association is not None
            else None
        )
        kwargs["ancillary_data"] = (
            [
                AncillaryData._from_v1_2_kwargs(ad)
                for ad in obj.ancillary_data_set.ancillary_data
            ]
            if obj.ancillary_data_set is not None
            else []
        )
        kwargs["short_description"] = obj.short_description
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.SequenceEntryType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["location_in_container"] = (
            LocationInContainer._from_v1_3_kwargs(obj.location_in_container_in_bits)
            if obj.location_in_container_in_bits is not None
            else None
        )
        kwargs["repeat_entry"] = (
            Repeat._from_v1_3_kwargs(obj.repeat_entry)
            if obj.repeat_entry is not None
            else None
        )
        kwargs["include_condition"] = (
            MatchCriteria._from_v1_3_kwargs(obj.include_condition)
            if obj.include_condition is not None
            else None
        )
        kwargs["time_association"] = (
            TimeAssociation._from_v1_3_kwargs(obj.time_association)
            if obj.time_association is not None
            else None
        )
        kwargs["ancillary_data"] = (
            [
                AncillaryData._from_v1_3_kwargs(ad)
                for ad in obj.ancillary_data_set.ancillary_data
            ]
            if obj.ancillary_data_set is not None
            else []
        )
        kwargs["short_description"] = obj.short_description
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="time_association",
            current_value=self.time_association,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=None,
        )
        self._enforce_unsupported_field(
            field_name="ancillary_data",
            current_value=self.ancillary_data,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=[],
        )
        self._enforce_unsupported_field(
            field_name="short_description",
            current_value=self.short_description,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=None,
        )

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["location_in_container_in_bits"] = (
            self.location_in_container._to_v1_1(policy)
            if self.location_in_container is not None
            else None
        )
        kwargs["repeat_entry"] = (
            self.repeat_entry._to_v1_1(policy)
            if self.repeat_entry is not None
            else None
        )
        kwargs["include_condition"] = (
            self.include_condition._to_v1_1(policy)
            if self.include_condition is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["location_in_container_in_bits"] = (
            self.location_in_container._to_v1_2(policy)
            if self.location_in_container is not None
            else None
        )
        kwargs["repeat_entry"] = (
            self.repeat_entry._to_v1_2(policy)
            if self.repeat_entry is not None
            else None
        )
        kwargs["include_condition"] = (
            self.include_condition._to_v1_2(policy)
            if self.include_condition is not None
            else None
        )
        kwargs["time_association"] = (
            self.time_association._to_v1_2(policy)
            if self.time_association is not None
            else None
        )
        kwargs["ancillary_data_set"] = self._build_set(
            items=self.ancillary_data,
            set_class=xtce_1_2.AncillaryDataSetType,
            kwarg_name="ancillary_data",
            converter=lambda data: data._to_v1_2(policy),
        )
        kwargs["short_description"] = self.short_description
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["location_in_container_in_bits"] = (
            self.location_in_container._to_v1_3(policy)
            if self.location_in_container is not None
            else None
        )
        kwargs["repeat_entry"] = (
            self.repeat_entry._to_v1_3(policy)
            if self.repeat_entry is not None
            else None
        )
        kwargs["include_condition"] = (
            self.include_condition._to_v1_3(policy)
            if self.include_condition is not None
            else None
        )
        kwargs["time_association"] = (
            self.time_association._to_v1_3(policy)
            if self.time_association is not None
            else None
        )
        kwargs["ancillary_data_set"] = self._build_set(
            items=self.ancillary_data,
            set_class=xtce_1_3.AncillaryDataSetType,
            kwarg_name="ancillary_data",
            converter=lambda data: data._to_v1_3(policy),
        )
        kwargs["short_description"] = self.short_description
        return kwargs


class ArgumentSequenceEntry(XtceBaseModel, ABC):
    """Abstract base class for a sequence entry in a container."""

    location_in_container: ArgumentLocationInContainer | None = None
    """The location of the entry in the container."""

    repeat_entry: ArgumentRepeat | None = None
    """Indicates if the entry should be repeated in the container."""

    include_condition: ArgumentMatchCriteria | None = None
    """The condition that must be met for the entry to be included in the container."""

    ancillary_data: list[AncillaryData] = Field(default_factory=list)
    """The ancillary data associated with the entry in the container."""

    short_description: str | None = None
    """A short description of the entry in the container."""

    _v1_1_type = xtce_1_1.SequenceEntryType
    _v1_2_type = xtce_1_2.ArgumentSequenceEntryType
    _v1_3_type = xtce_1_3.ArgumentSequenceEntryType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.SequenceEntryType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["location_in_container"] = (
            LocationInContainer._from_v1_1_kwargs(obj.location_in_container_in_bits)
            if obj.location_in_container_in_bits is not None
            else None
        )
        kwargs["repeat_entry"] = (
            Repeat._from_v1_1_kwargs(obj.repeat_entry)
            if obj.repeat_entry is not None
            else None
        )
        kwargs["include_condition"] = (
            MatchCriteria._from_v1_1_kwargs(obj.include_condition)
            if obj.include_condition is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentSequenceEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["location_in_container"] = (
            ArgumentLocationInContainer._from_v1_2_kwargs(
                obj.location_in_container_in_bits
            )
            if obj.location_in_container_in_bits is not None
            else None
        )
        kwargs["repeat_entry"] = (
            ArgumentRepeat._from_v1_2_kwargs(obj.repeat_entry)
            if obj.repeat_entry is not None
            else None
        )
        kwargs["include_condition"] = (
            ArgumentMatchCriteria._from_v1_2_kwargs(obj.include_condition)
            if obj.include_condition is not None
            else None
        )
        kwargs["ancillary_data"] = (
            [
                AncillaryData._from_v1_2_kwargs(ad)
                for ad in obj.ancillary_data_set.ancillary_data
            ]
            if obj.ancillary_data_set is not None
            else []
        )
        kwargs["short_description"] = obj.short_description
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentSequenceEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["location_in_container"] = (
            ArgumentLocationInContainer._from_v1_3_kwargs(
                obj.location_in_container_in_bits
            )
            if obj.location_in_container_in_bits is not None
            else None
        )
        kwargs["repeat_entry"] = (
            ArgumentRepeat._from_v1_3_kwargs(obj.repeat_entry)
            if obj.repeat_entry is not None
            else None
        )
        kwargs["include_condition"] = (
            ArgumentMatchCriteria._from_v1_3_kwargs(obj.include_condition)
            if obj.include_condition is not None
            else None
        )
        kwargs["ancillary_data"] = (
            [
                AncillaryData._from_v1_3_kwargs(ad)
                for ad in obj.ancillary_data_set.ancillary_data
            ]
            if obj.ancillary_data_set is not None
            else []
        )
        kwargs["short_description"] = obj.short_description
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="ancillary_data",
            current_value=self.ancillary_data,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=[],
        )
        self._enforce_unsupported_field(
            field_name="short_description",
            current_value=self.short_description,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=None,
        )

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["location_in_container_in_bits"] = (
            self.location_in_container._to_v1_1(policy)
            if self.location_in_container is not None
            else None
        )
        kwargs["repeat_entry"] = (
            self.repeat_entry._to_v1_1(policy)
            if self.repeat_entry is not None
            else None
        )
        kwargs["include_condition"] = (
            self.include_condition._to_v1_1(policy)
            if self.include_condition is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["location_in_container_in_bits"] = (
            self.location_in_container._to_v1_2(policy)
            if self.location_in_container is not None
            else None
        )
        kwargs["repeat_entry"] = (
            self.repeat_entry._to_v1_2(policy)
            if self.repeat_entry is not None
            else None
        )
        kwargs["include_condition"] = (
            self.include_condition._to_v1_2(policy)
            if self.include_condition is not None
            else None
        )
        kwargs["ancillary_data_set"] = self._build_set(
            items=self.ancillary_data,
            set_class=xtce_1_2.AncillaryDataSetType,
            kwarg_name="ancillary_data",
            converter=lambda data: data._to_v1_2(policy),
        )
        kwargs["short_description"] = self.short_description
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["location_in_container_in_bits"] = (
            self.location_in_container._to_v1_3(policy)
            if self.location_in_container is not None
            else None
        )
        kwargs["repeat_entry"] = (
            self.repeat_entry._to_v1_3(policy)
            if self.repeat_entry is not None
            else None
        )
        kwargs["include_condition"] = (
            self.include_condition._to_v1_3(policy)
            if self.include_condition is not None
            else None
        )
        kwargs["ancillary_data_set"] = self._build_set(
            items=self.ancillary_data,
            set_class=xtce_1_3.AncillaryDataSetType,
            kwarg_name="ancillary_data",
            converter=lambda data: data._to_v1_3(policy),
        )
        kwargs["short_description"] = self.short_description
        return kwargs


class ParameterRefEntry(SequenceEntry):
    """Define a container entry that is a reference to a parameter."""

    parameter_ref: Annotated[
        XtcePath, AfterValidator(require_regex(EXPD_NAME_REF_W_PATH))
    ] = Field(
        ...,
        examples=["TODO"],
        json_schema_extra={"pattern": EXPD_NAME_REF_W_PATH},
    )
    """A Unix-like path to a parameter."""

    _v1_1_type = xtce_1_1.ParameterRefEntryType
    _v1_2_type = xtce_1_2.ParameterRefEntryType
    _v1_3_type = xtce_1_3.ParameterRefEntryType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.ParameterRefEntryType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["parameter_ref"] = XtcePath(obj.parameter_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ParameterRefEntryType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["parameter_ref"] = XtcePath(obj.parameter_ref)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ParameterRefEntryType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["parameter_ref"] = XtcePath(obj.parameter_ref)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.1 defines this as NameReferenceType
        validator = require_regex(NAME_REF_W_PATH)
        validator(self.parameter_ref)

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["parameter_ref"] = str(self.parameter_ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.2 defines this as NameReferenceType
        validator = require_regex(NAME_REF_W_PATH)
        validator(self.parameter_ref)

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["parameter_ref"] = str(self.parameter_ref)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["parameter_ref"] = str(self.parameter_ref)
        return kwargs


class ArgumentParameterRefEntry(ArgumentSequenceEntry):
    """Define a container argument entry that is a reference to a parameter."""

    parameter_ref: Annotated[
        XtcePath, AfterValidator(require_regex(EXPD_NAME_REF_W_PATH))
    ] = Field(
        ...,
        examples=["TODO"],
        json_schema_extra={"pattern": EXPD_NAME_REF_W_PATH},
    )
    """A Unix-like path to a parameter."""

    _v1_1_type = xtce_1_1.ParameterRefEntryType
    _v1_2_type = xtce_1_2.ArgumentParameterRefEntryType
    _v1_3_type = xtce_1_3.ArgumentParameterRefEntryType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.ParameterRefEntryType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["parameter_ref"] = XtcePath(obj.parameter_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentParameterRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["parameter_ref"] = XtcePath(obj.parameter_ref)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentParameterRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["parameter_ref"] = XtcePath(obj.parameter_ref)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.1 defines this as NameReferenceType
        validator = require_regex(NAME_REF_W_PATH)
        validator(self.parameter_ref)

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["parameter_ref"] = str(self.parameter_ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.2 defines this as NameReferenceType
        validator = require_regex(NAME_REF_W_PATH)
        validator(self.parameter_ref)

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["parameter_ref"] = str(self.parameter_ref)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["parameter_ref"] = str(self.parameter_ref)
        return kwargs


class ParameterSegmentRefEntry(SequenceEntry):
    """Define a container entry that is only a segment of a parameter value."""

    parameter_ref: Annotated[
        XtcePath, AfterValidator(require_regex(EXPD_NAME_REF_W_PATH))
    ] = Field(
        ...,
        examples=["TODO"],
        json_schema_extra={"pattern": EXPD_NAME_REF_W_PATH},
    )
    """A Unix-like path to a parameter segment."""

    order: int | None = Field(default=None, ge=1)
    """The order of the parameter segment within the container."""

    size_in_bits: Literal[-1] | Annotated[int, Field(ge=1)]
    """The size of the parameter segment in bits."""

    _v1_1_type = xtce_1_1.ParameterSegmentRefEntryType
    _v1_2_type = xtce_1_2.ParameterSegmentRefEntryType
    _v1_3_type = xtce_1_3.ParameterSegmentRefEntryType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.ParameterSegmentRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["parameter_ref"] = XtcePath(obj.parameter_ref)
        kwargs["order"] = obj.order
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ParameterSegmentRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["parameter_ref"] = XtcePath(obj.parameter_ref)
        kwargs["order"] = obj.order
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ParameterSegmentRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["parameter_ref"] = XtcePath(obj.parameter_ref)
        kwargs["order"] = obj.order
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.1 defines this as NameReferenceType
        validator = require_regex(NAME_REF_W_PATH)
        validator(self.parameter_ref)

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["parameter_ref"] = str(self.parameter_ref)
        kwargs["order"] = self.order
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.2 defines this as NameReferenceType
        validator = require_regex(NAME_REF_W_PATH)
        validator(self.parameter_ref)

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["parameter_ref"] = str(self.parameter_ref)
        kwargs["order"] = self.order
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["parameter_ref"] = str(self.parameter_ref)
        kwargs["order"] = self.order
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs


class ArgumentParameterSegmentRefEntry(ArgumentSequenceEntry):
    """Define a container argument entry that is only a segment of a parameter value."""

    parameter_ref: Annotated[
        XtcePath, AfterValidator(require_regex(EXPD_NAME_REF_W_PATH))
    ] = Field(
        ...,
        examples=["TODO"],
        json_schema_extra={"pattern": EXPD_NAME_REF_W_PATH},
    )
    """A Unix-like path to a parameter segment."""

    order: int | None = Field(default=None, ge=1)
    """The order of the parameter segment within the container."""

    size_in_bits: Literal[-1] | Annotated[int, Field(ge=1)]
    """The size of the parameter segment in bits."""

    _v1_1_type = xtce_1_1.ParameterSegmentRefEntryType
    _v1_2_type = xtce_1_2.ArgumentParameterSegmentRefEntryType
    _v1_3_type = xtce_1_3.ArgumentParameterSegmentRefEntryType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.ParameterSegmentRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["parameter_ref"] = XtcePath(obj.parameter_ref)
        kwargs["order"] = obj.order
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentParameterSegmentRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["parameter_ref"] = XtcePath(obj.parameter_ref)
        kwargs["order"] = obj.order
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentParameterSegmentRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["parameter_ref"] = XtcePath(obj.parameter_ref)
        kwargs["order"] = obj.order
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.1 defines this as NameReferenceType
        validator = require_regex(NAME_REF_W_PATH)
        validator(self.parameter_ref)

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["parameter_ref"] = str(self.parameter_ref)
        kwargs["order"] = self.order
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.2 defines this as NameReferenceType
        validator = require_regex(NAME_REF_W_PATH)
        validator(self.parameter_ref)

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["parameter_ref"] = str(self.parameter_ref)
        kwargs["order"] = self.order
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["parameter_ref"] = str(self.parameter_ref)
        kwargs["order"] = self.order
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs


class ContainerRefEntry(SequenceEntry):
    """Define a container entry that is a reference to another container."""

    container_ref: Annotated[
        XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))
    ] = Field(
        ...,
        examples=["TODO"],
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to a container."""

    _v1_1_type = xtce_1_1.ContainerRefEntryType
    _v1_2_type = xtce_1_2.ContainerRefEntryType
    _v1_3_type = xtce_1_3.ContainerRefEntryType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.ContainerRefEntryType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["container_ref"] = XtcePath(obj.container_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ContainerRefEntryType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["container_ref"] = XtcePath(obj.container_ref)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ContainerRefEntryType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["container_ref"] = XtcePath(obj.container_ref)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["container_ref"] = str(self.container_ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["container_ref"] = str(self.container_ref)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["container_ref"] = str(self.container_ref)
        return kwargs


class ArgumentContainerRefEntry(ArgumentSequenceEntry):
    """Define a container argument entry that is a reference to another container."""

    container_ref: Annotated[
        XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))
    ] = Field(
        ...,
        examples=["TODO"],
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to a container."""

    _v1_1_type = xtce_1_1.ContainerRefEntryType
    _v1_2_type = xtce_1_2.ArgumentContainerRefEntryType
    _v1_3_type = xtce_1_3.ArgumentContainerRefEntryType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.ContainerRefEntryType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["container_ref"] = XtcePath(obj.container_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentContainerRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["container_ref"] = XtcePath(obj.container_ref)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentContainerRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["container_ref"] = XtcePath(obj.container_ref)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["container_ref"] = str(self.container_ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["container_ref"] = str(self.container_ref)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["container_ref"] = str(self.container_ref)
        return kwargs


class ContainerSegmentRefEntry(SequenceEntry):
    """Define a container entry that is only a segment of a container."""

    container_ref: Annotated[
        XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))
    ] = Field(
        ...,
        examples=["TODO"],
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to a container."""

    order: int | None = Field(default=None, ge=1)
    """The order of the segment within the container."""

    size_in_bits: Literal[-1] | Annotated[int, Field(ge=1)]
    """The size of the segment in bits."""

    _v1_1_type = xtce_1_1.ContainerSegmentRefEntryType
    _v1_2_type = xtce_1_2.ContainerSegmentRefEntryType
    _v1_3_type = xtce_1_3.ContainerSegmentRefEntryType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.ContainerSegmentRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["container_ref"] = XtcePath(obj.container_ref)
        kwargs["order"] = obj.order
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ContainerSegmentRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["container_ref"] = XtcePath(obj.container_ref)
        kwargs["order"] = obj.order
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ContainerSegmentRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["container_ref"] = XtcePath(obj.container_ref)
        kwargs["order"] = obj.order
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["container_ref"] = str(self.container_ref)
        kwargs["order"] = self.order
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["container_ref"] = str(self.container_ref)
        kwargs["order"] = self.order
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["container_ref"] = str(self.container_ref)
        kwargs["order"] = self.order
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs


class ArgumentContainerSegmentRefEntry(ArgumentSequenceEntry):
    """Define a container argument entry that is only a segment of a container."""

    container_ref: Annotated[
        XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))
    ] = Field(
        ...,
        examples=["TODO"],
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to a container."""

    order: int | None = Field(default=None, ge=1)
    """The order of the segment within the container."""

    size_in_bits: Literal[-1] | Annotated[int, Field(ge=1)]
    """The size of the segment in bits."""

    _v1_1_type = xtce_1_1.ContainerSegmentRefEntryType
    _v1_2_type = xtce_1_2.ArgumentContainerSegmentRefEntryType
    _v1_3_type = xtce_1_3.ArgumentContainerSegmentRefEntryType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.ContainerSegmentRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["container_ref"] = XtcePath(obj.container_ref)
        kwargs["order"] = obj.order
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentContainerSegmentRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["container_ref"] = XtcePath(obj.container_ref)
        kwargs["order"] = obj.order
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentContainerSegmentRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["container_ref"] = XtcePath(obj.container_ref)
        kwargs["order"] = obj.order
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["container_ref"] = str(self.container_ref)
        kwargs["order"] = self.order
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["container_ref"] = str(self.container_ref)
        kwargs["order"] = self.order
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["container_ref"] = str(self.container_ref)
        kwargs["order"] = self.order
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs


class StreamSegmentEntry(SequenceEntry):
    """Define a container entry that is a stream segment."""

    stream_ref: Annotated[XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))] = (
        Field(
            ...,
            examples=["TODO"],
            json_schema_extra={"pattern": NAME_REF_W_PATH},
        )
    )
    """A Unix-like path to a stream."""

    order: int | None = Field(default=None, ge=1)
    """The order of the stream segment within the container."""

    size_in_bits: Literal[-1] | Annotated[int, Field(ge=1)]
    """The size of the stream segment in bits."""

    _v1_1_type = xtce_1_1.StreamSegmentEntryType
    _v1_2_type = xtce_1_2.StreamSegmentEntryType
    _v1_3_type = xtce_1_3.StreamSegmentEntryType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.StreamSegmentEntryType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["stream_ref"] = XtcePath(obj.stream_ref)
        kwargs["order"] = obj.order
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.StreamSegmentEntryType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["stream_ref"] = XtcePath(obj.stream_ref)
        kwargs["order"] = obj.order
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.StreamSegmentEntryType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["stream_ref"] = XtcePath(obj.stream_ref)
        kwargs["order"] = obj.order
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["stream_ref"] = str(self.stream_ref)
        kwargs["order"] = self.order
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["stream_ref"] = str(self.stream_ref)
        kwargs["order"] = self.order
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["stream_ref"] = str(self.stream_ref)
        kwargs["order"] = self.order
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs


class ArgumentStreamSegmentEntry(ArgumentSequenceEntry):
    """Define a container argument entry that is a stream segment."""

    stream_ref: Annotated[XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))] = (
        Field(
            ...,
            examples=["TODO"],
            json_schema_extra={"pattern": NAME_REF_W_PATH},
        )
    )
    """A Unix-like path to a stream."""

    order: int | None = Field(default=None, ge=1)
    """The order of the stream segment within the container."""

    size_in_bits: Literal[-1] | Annotated[int, Field(ge=1)]
    """The size of the stream segment in bits."""

    _v1_1_type = xtce_1_1.StreamSegmentEntryType
    _v1_2_type = xtce_1_2.ArgumentStreamSegmentEntryType
    _v1_3_type = xtce_1_3.ArgumentStreamSegmentEntryType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.StreamSegmentEntryType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["stream_ref"] = XtcePath(obj.stream_ref)
        kwargs["order"] = obj.order
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentStreamSegmentEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["stream_ref"] = XtcePath(obj.stream_ref)
        kwargs["order"] = obj.order
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentStreamSegmentEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["stream_ref"] = XtcePath(obj.stream_ref)
        kwargs["order"] = obj.order
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["stream_ref"] = str(self.stream_ref)
        kwargs["order"] = self.order
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["stream_ref"] = str(self.stream_ref)
        kwargs["order"] = self.order
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["stream_ref"] = str(self.stream_ref)
        kwargs["order"] = self.order
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs


class IndirectParameterRefEntry(SequenceEntry):
    """Define a container entry whose name is given by the value of a parameter
    instance.
    """

    parameter_instance: ParameterInstanceRef
    """The parameter instance that defines the name of this container entry."""

    alias_name_space: str | None = None
    """The alias name space for this container entry."""

    _v1_1_type = xtce_1_1.IndirectParameterRefEntryType
    _v1_2_type = xtce_1_2.IndirectParameterRefEntryType
    _v1_3_type = xtce_1_3.IndirectParameterRefEntryType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.IndirectParameterRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["parameter_instance"] = ParameterInstanceRef._from_v1_1_kwargs(
            obj.parameter_instance
        )
        kwargs["alias_name_space"] = obj.alias_name_space
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.IndirectParameterRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["parameter_instance"] = ParameterInstanceRef._from_v1_2_kwargs(
            obj.parameter_instance
        )
        kwargs["alias_name_space"] = obj.alias_name_space
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.IndirectParameterRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["parameter_instance"] = ParameterInstanceRef._from_v1_3_kwargs(
            obj.parameter_instance
        )
        kwargs["alias_name_space"] = obj.alias_name_space
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["parameter_instance"] = self.parameter_instance._to_v1_1(policy)
        kwargs["alias_name_space"] = self.alias_name_space
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["parameter_instance"] = self.parameter_instance._to_v1_2(policy)
        kwargs["alias_name_space"] = self.alias_name_space
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["parameter_instance"] = self.parameter_instance._to_v1_3(policy)
        kwargs["alias_name_space"] = self.alias_name_space
        return kwargs


class ArgumentIndirectParameterRefEntry(ArgumentSequenceEntry):
    """Define a container argument entry whose name is given by the value of a parameter
    instance.
    """

    parameter_instance: ParameterInstanceRef
    """The parameter instance that defines the name of this container entry."""

    alias_name_space: str | None = None
    """The alias name space for this container entry."""

    _v1_1_type = xtce_1_1.IndirectParameterRefEntryType
    _v1_2_type = xtce_1_2.ArgumentIndirectParameterRefEntryType
    _v1_3_type = xtce_1_3.ArgumentIndirectParameterRefEntryType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.IndirectParameterRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["parameter_instance"] = ParameterInstanceRef._from_v1_1_kwargs(
            obj.parameter_instance
        )
        kwargs["alias_name_space"] = obj.alias_name_space
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentIndirectParameterRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["parameter_instance"] = ParameterInstanceRef._from_v1_2_kwargs(
            obj.parameter_instance
        )
        kwargs["alias_name_space"] = obj.alias_name_space
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentIndirectParameterRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["parameter_instance"] = ParameterInstanceRef._from_v1_3_kwargs(
            obj.parameter_instance
        )
        kwargs["alias_name_space"] = obj.alias_name_space
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["parameter_instance"] = self.parameter_instance._to_v1_1(policy)
        kwargs["alias_name_space"] = self.alias_name_space
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["parameter_instance"] = self.parameter_instance._to_v1_2(policy)
        kwargs["alias_name_space"] = self.alias_name_space
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["parameter_instance"] = self.parameter_instance._to_v1_3(policy)
        kwargs["alias_name_space"] = self.alias_name_space
        return kwargs


class ArrayParameterRefEntry(SequenceEntry):
    """Define a container entry that is an array parameter."""

    dimensions: list[Dimension] = Field(default_factory=list)
    """List of dimensions for the array parameter.

    In the form: [1st][2nd]...[Nth].

    """

    parameter_ref: Annotated[
        XtcePath, AfterValidator(require_regex(EXPD_NAME_REF_W_PATH))
    ] = Field(
        ...,
        examples=["TODO"],
        json_schema_extra={"pattern": EXPD_NAME_REF_W_PATH},
    )
    """A Unix-like path to an array parameter."""

    _v1_1_type = xtce_1_1.ArrayParameterRefEntryType
    _v1_2_type = xtce_1_2.ArrayParameterRefEntryType
    _v1_3_type = xtce_1_3.ArrayParameterRefEntryType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.ArrayParameterRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["dimensions"] = [
            Dimension._from_v1_1_kwargs(d) for d in obj.dimension_list.dimension
        ]
        kwargs["parameter_ref"] = XtcePath(obj.parameter_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArrayParameterRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["dimensions"] = (
            [Dimension._from_v1_2_kwargs(d) for d in obj.dimension_list.dimension]
            if obj.dimension_list is not None
            else None
        )
        kwargs["parameter_ref"] = XtcePath(obj.parameter_ref)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArrayParameterRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["dimensions"] = (
            [Dimension._from_v1_3_kwargs(d) for d in obj.dimension_list.dimension]
            if obj.dimension_list is not None
            else None
        )
        kwargs["parameter_ref"] = XtcePath(obj.parameter_ref)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_required_field(
            field_name="dimensions",
            current_value=self.dimensions,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=[],
        )
        # XTCE 1.1 defines this as NameReferenceType
        validator = require_regex(NAME_REF_W_PATH)
        validator(self.parameter_ref)

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["dimension_list"] = self._build_set(
            items=self.dimensions,
            set_class=xtce_1_1.ArrayParameterRefEntryType.DimensionList,
            kwarg_name="dimension",
            converter=lambda d: d._to_v1_1(policy),
            required=True,
        )
        kwargs["parameter_ref"] = str(self.parameter_ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.2 defines this as NameReferenceType
        validator = require_regex(NAME_REF_W_PATH)
        validator(self.parameter_ref)

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["dimension_list"] = self._build_set(
            items=self.dimensions,
            set_class=xtce_1_2.DimensionListType,
            kwarg_name="dimension",
            converter=lambda d: d._to_v1_2(policy),
            required=True,
        )
        kwargs["parameter_ref"] = str(self.parameter_ref)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["dimension_list"] = self._build_set(
            items=self.dimensions,
            set_class=xtce_1_3.DimensionListType,
            kwarg_name="dimension",
            converter=lambda d: d._to_v1_3(policy),
            required=True,
        )
        kwargs["parameter_ref"] = str(self.parameter_ref)
        return kwargs


class ArgumentArrayParameterRefEntry(ArgumentSequenceEntry):
    """Define a container argument entry that is an array parameter."""

    dimensions: list[Dimension] = Field(default_factory=list)
    """List of dimensions for the array parameter.

    In the form: [1st][2nd]...[Nth].

    """

    parameter_ref: Annotated[
        XtcePath, AfterValidator(require_regex(EXPD_NAME_REF_W_PATH))
    ] = Field(
        ...,
        examples=["TODO"],
        json_schema_extra={"pattern": EXPD_NAME_REF_W_PATH},
    )
    """A Unix-like path to an array parameter."""

    last_entry: bool = False
    """Indicates if this is the last entry for the array instance."""

    _v1_1_type = xtce_1_1.CommandContainerEntryListType.ArrayParameterRefEntry
    _v1_2_type = xtce_1_2.ArgumentArrayParameterRefEntryType
    _v1_3_type = xtce_1_3.ArgumentArrayParameterRefEntryType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.ArrayParameterRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["dimensions"] = [
            Dimension._from_v1_1_kwargs(d) for d in obj.dimension_list.dimension
        ]
        kwargs["parameter_ref"] = XtcePath(obj.parameter_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentArrayParameterRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["dimensions"] = (
            [Dimension._from_v1_2_kwargs(d) for d in obj.dimension_list.dimension]
            if obj.dimension_list is not None
            else None
        )
        kwargs["parameter_ref"] = XtcePath(obj.parameter_ref)
        kwargs["last_entry"] = obj.last_entry_for_this_array_instance
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentArrayParameterRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["dimensions"] = (
            [Dimension._from_v1_3_kwargs(d) for d in obj.dimension_list.dimension]
            if obj.dimension_list is not None
            else None
        )
        kwargs["parameter_ref"] = XtcePath(obj.parameter_ref)
        kwargs["last_entry"] = obj.last_entry_for_this_array_instance
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_required_field(
            field_name="dimensions",
            current_value=self.dimensions,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=[],
        )
        self._enforce_unsupported_field(
            field_name="last_entry",
            current_value=self.last_entry,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=False,
        )
        # XTCE 1.1 defines this as NameReferenceType
        validator = require_regex(NAME_REF_W_PATH)
        validator(self.parameter_ref)

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["dimension_list"] = self._build_set(
            items=self.dimensions,
            set_class=xtce_1_1.ArrayParameterRefEntryType.DimensionList,
            kwarg_name="dimension",
            converter=lambda d: d._to_v1_1(policy),
            required=True,
        )
        kwargs["parameter_ref"] = str(self.parameter_ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.2 defines this as NameReferenceType
        validator = require_regex(NAME_REF_W_PATH)
        validator(self.parameter_ref)

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["dimension_list"] = self._build_set(
            items=self.dimensions,
            set_class=xtce_1_2.DimensionListType,
            kwarg_name="dimension",
            converter=lambda d: d._to_v1_2(policy),
            required=True,
        )
        kwargs["parameter_ref"] = str(self.parameter_ref)
        kwargs["last_entry_for_this_array_instance"] = self.last_entry
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["dimension_list"] = self._build_set(
            items=self.dimensions,
            set_class=xtce_1_3.DimensionListType,
            kwarg_name="dimension",
            converter=lambda d: d._to_v1_3(policy),
            required=True,
        )
        kwargs["parameter_ref"] = str(self.parameter_ref)
        kwargs["last_entry_for_this_array_instance"] = self.last_entry
        return kwargs


class ArgumentArgumentRefEntry(ArgumentSequenceEntry):
    """Define a container argument entry that is a reference to another argument."""

    argument_ref: Annotated[
        XtcePath, AfterValidator(require_regex(EXPD_NAME_REF_W_PATH))
    ] = Field(
        ...,
        examples=["TODO"],
        json_schema_extra={"pattern": EXPD_NAME_REF_W_PATH},
    )
    """A Unix-like path to an argument."""

    _v1_1_type = xtce_1_1.CommandContainerEntryListType.ArgumentRefEntry
    _v1_2_type = xtce_1_2.ArgumentArgumentRefEntryType
    _v1_3_type = xtce_1_3.ArgumentArgumentRefEntryType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.CommandContainerEntryListType.ArgumentRefEntry
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["argument_ref"] = XtcePath(obj.argument_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentArgumentRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["argument_ref"] = XtcePath(obj.argument_ref)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentArgumentRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["argument_ref"] = XtcePath(obj.argument_ref)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.1 defines this as NameReferenceType
        validator = require_regex(NAME_REF_W_PATH)
        validator(self.argument_ref)

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["argument_ref"] = str(self.argument_ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.2 defines this as NameReferenceType
        validator = require_regex(NAME_REF_W_PATH)
        validator(self.argument_ref)

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["argument_ref"] = str(self.argument_ref)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["argument_ref"] = str(self.argument_ref)
        return kwargs


class ArgumentArrayArgumentRefEntry(ArgumentSequenceEntry):
    """Define a container argument entry that is a reference to an array argument."""

    dimensions: list[ArgumentDimension] = Field(default_factory=list)
    """List of dimensions for the array parameter.

    In the form: [1st][2nd]...[Nth].

    """

    argument_ref: Annotated[
        XtcePath, AfterValidator(require_regex(EXPD_NAME_REF_W_PATH))
    ] = Field(
        ...,
        examples=["TODO"],
        json_schema_extra={"pattern": EXPD_NAME_REF_W_PATH},
    )
    """A Unix-like path to an array argument."""

    last_entry: bool = False
    """Indicates if this is the last entry for the array instance."""

    _v1_1_type = xtce_1_1.CommandContainerEntryListType.ArrayArgumentRefEntry
    _v1_2_type = xtce_1_2.ArgumentArrayArgumentRefEntryType
    _v1_3_type = xtce_1_3.ArgumentArrayArgumentRefEntryType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.ArrayParameterRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["dimensions"] = [
            ArgumentDimension._from_v1_1_kwargs(d) for d in obj.dimension_list.dimension
        ]
        kwargs["argument_ref"] = XtcePath(obj.parameter_ref)
        kwargs["last_entry"] = obj.last_entry_for_this_array_instance
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentArrayArgumentRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["dimensions"] = (
            [
                ArgumentDimension._from_v1_2_kwargs(d)
                for d in obj.dimension_list.dimension
            ]
            if obj.dimension_list is not None
            else None
        )
        kwargs["argument_ref"] = XtcePath(obj.argument_ref)
        kwargs["last_entry"] = obj.last_entry_for_this_array_instance
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentArrayArgumentRefEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["dimensions"] = (
            [
                ArgumentDimension._from_v1_3_kwargs(d)
                for d in obj.dimension_list.dimension
            ]
            if obj.dimension_list is not None
            else None
        )
        kwargs["argument_ref"] = XtcePath(obj.argument_ref)
        kwargs["last_entry"] = obj.last_entry_for_this_array_instance
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_required_field(
            field_name="dimensions",
            current_value=self.dimensions,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=[],
        )
        self._enforce_unsupported_field(
            field_name="last_entry",
            current_value=self.last_entry,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=False,
        )
        # XTCE 1.1 defines this as NameReferenceType
        validator = require_regex(NAME_REF_W_PATH)
        validator(self.argument_ref)

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["dimension_list"] = self._build_set(
            items=self.dimensions,
            set_class=xtce_1_1.ArrayParameterRefEntryType.DimensionList,
            kwarg_name="dimension",
            converter=lambda d: d._to_v1_1(policy),
            required=True,
        )
        kwargs["parameter_ref"] = str(self.argument_ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.2 defines this as NameReferenceType
        validator = require_regex(NAME_REF_W_PATH)
        validator(self.argument_ref)

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["dimension_list"] = self._build_set(
            items=self.dimensions,
            set_class=xtce_1_2.ArgumentDimensionListType,
            kwarg_name="dimension",
            converter=lambda d: d._to_v1_2(policy),
            required=True,
        )
        kwargs["argument_ref"] = str(self.argument_ref)
        kwargs["last_entry_for_this_array_instance"] = self.last_entry
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["dimension_list"] = self._build_set(
            items=self.dimensions,
            set_class=xtce_1_3.ArgumentDimensionListType,
            kwarg_name="dimension",
            converter=lambda d: d._to_v1_3(policy),
            required=True,
        )
        kwargs["argument_ref"] = str(self.argument_ref)
        kwargs["last_entry_for_this_array_instance"] = self.last_entry
        return kwargs


class ArgumentFixedValueEntry(ArgumentSequenceEntry):
    """Define a container argument entry that has a fixed binary value."""

    name: str | None = None
    """Optional name for the fixed value entry."""

    binary_value: bytes
    """The fixed binary value for the entry."""

    size_in_bits: int
    """The size of the fixed value in bits."""

    _v1_1_type = xtce_1_1.CommandContainerEntryListType.FixedValueEntry
    _v1_2_type = xtce_1_2.ArgumentFixedValueEntryType
    _v1_3_type = xtce_1_3.ArgumentFixedValueEntryType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.CommandContainerEntryListType.FixedValueEntry
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["binary_value"] = obj.binary_value
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentFixedValueEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["name"] = obj.name
        kwargs["binary_value"] = obj.binary_value
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentFixedValueEntryType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["name"] = obj.name
        kwargs["binary_value"] = obj.binary_value
        kwargs["size_in_bits"] = obj.size_in_bits
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="name",
            current_value=self.name,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=None,
        )

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["binary_value"] = self.binary_value
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["name"] = self.name
        kwargs["binary_value"] = self.binary_value
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["name"] = self.name
        kwargs["binary_value"] = self.binary_value
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs


class RestrictionCriteria(MatchCriteria):
    """Define one or more conditions for container inheritance."""

    next_container: ContainerRef | None = None
    """Reference to the named container that must follow this container in the stream
    sequence.
    """

    _v1_1_type = xtce_1_1.SequenceContainerType.BaseContainer.RestrictionCriteria
    _v1_2_type = xtce_1_2.RestrictionCriteriaType
    _v1_3_type = xtce_1_3.RestrictionCriteriaType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.SequenceContainerType.BaseContainer.RestrictionCriteria
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["next_container"] = (
            ContainerRef._from_v1_1_kwargs(obj.next_container)
            if obj.next_container is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.RestrictionCriteriaType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["next_container"] = (
            ContainerRef._from_v1_2_kwargs(obj.next_container)
            if obj.next_container is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.RestrictionCriteriaType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["next_container"] = (
            ContainerRef._from_v1_3_kwargs(obj.next_container)
            if obj.next_container is not None
            else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["next_container"] = (
            self.next_container._to_v1_1(policy)
            if self.next_container is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["next_container"] = (
            self.next_container._to_v1_2(policy)
            if self.next_container is not None
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["next_container"] = (
            self.next_container._to_v1_3(policy)
            if self.next_container is not None
            else None
        )
        return kwargs


class BaseContainer(XtceBaseModel):
    """Define a child/parent container inheritance relationship."""

    restriction_criteria: RestrictionCriteria | None = None
    """The criteria that must be met for this container to be an extension of its base
    container.
    """

    container_ref: Annotated[
        XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))
    ] = Field(
        ...,
        examples=["TODO"],
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to a container."""

    _v1_1_type = xtce_1_1.SequenceContainerType.BaseContainer
    _v1_2_type = xtce_1_2.BaseContainerType
    _v1_3_type = xtce_1_3.BaseContainerType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.SequenceContainerType.BaseContainer
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["restriction_criteria"] = RestrictionCriteria._from_v1_1_kwargs(
            obj.restriction_criteria
        )
        kwargs["container_ref"] = XtcePath(obj.container_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.BaseContainerType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["restriction_criteria"] = (
            RestrictionCriteria._from_v1_2_kwargs(obj.restriction_criteria)
            if obj.restriction_criteria is not None
            else None
        )
        kwargs["container_ref"] = XtcePath(obj.container_ref)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.BaseContainerType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["restriction_criteria"] = (
            RestrictionCriteria._from_v1_3_kwargs(obj.restriction_criteria)
            if obj.restriction_criteria is not None
            else None
        )
        kwargs["container_ref"] = XtcePath(obj.container_ref)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        restriction_criteria: RestrictionCriteria = self._enforce_required_field(
            field_name="restriction_criteria",
            current_value=self.restriction_criteria,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=None,
        )

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["restriction_criteria"] = restriction_criteria._to_v1_1(policy)
        kwargs["container_ref"] = str(self.container_ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["restriction_criteria"] = (
            self.restriction_criteria._to_v1_2(policy)
            if self.restriction_criteria is not None
            else None
        )
        kwargs["container_ref"] = str(self.container_ref)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["restriction_criteria"] = (
            self.restriction_criteria._to_v1_3(policy)
            if self.restriction_criteria is not None
            else None
        )
        kwargs["container_ref"] = str(self.container_ref)
        return kwargs


class ContainerBinaryDataEncoding(XtceBaseModel):
    """Define container binary data that cannot be represented by any other data
    encoding formats.
    """

    error_detect_correct: list[Checksum | CRC | XOR | Parity] | None = None
    """List of error detection and correction algorithms applied to the container binary
    data.
    """

    size_in_bits: (
        Literal[-1]
        | Annotated[int, Field(ge=1)]
        | DynamicValue
        | DiscreteLookupList
        | None
    ) = None
    """Size of the container binary data in bits."""

    from_binary_transform_algorithm: InputAlgorithm | None = None
    """Algorithm used to transform the container binary data from binary
    representation.
    """

    to_binary_transform_algorithm: InputAlgorithm | None = None
    """Algorithm used to transform the container binary data to binary
    representation.
    """

    # TODO figure out support for XTCE 1.1 and 1.2
    # They use BinaryDataEncodingType, which has some additional fields

    _v1_1_type = None
    _v1_2_type = None
    _v1_3_type = xtce_1_3.ContainerBinaryDataEncodingType

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ContainerBinaryDataEncodingType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["error_detect_correct"] = (
            [
                Checksum._from_v1_3(edc)
                if isinstance(edc, xtce_1_3.ChecksumType)
                else CRC._from_v1_3(edc)
                if isinstance(edc, xtce_1_3.Crctype)
                else XOR._from_v1_3(edc)
                if isinstance(edc, xtce_1_3.Xortype)
                else Parity._from_v1_3(edc)
                for edc in obj.error_detect_correct.choice
            ]
            if obj.error_detect_correct is not None
            else None
        )
        kwargs["size_in_bits"] = parse_integer_value_v1_3(obj.size_in_bits)
        kwargs["from_binary_transform_algorithm"] = (
            InputAlgorithm._from_v1_3(obj.from_binary_transform_algorithm)
            if obj.from_binary_transform_algorithm is not None
            else None
        )
        kwargs["to_binary_transform_algorithm"] = (
            InputAlgorithm._from_v1_3(obj.to_binary_transform_algorithm)
            if obj.to_binary_transform_algorithm is not None
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["error_detect_correct"] = self._build_set(
            items=self.error_detect_correct,
            set_class=xtce_1_3.ErrorDetectCorrectType,
            kwarg_name="choice",
            converter=lambda edc: edc._to_v1_3(policy),
        )
        kwargs["size_in_bits"] = pack_integer_value_v1_3(self.size_in_bits, policy)
        kwargs["from_binary_transform_algorithm"] = (
            self.from_binary_transform_algorithm._to_v1_3(policy)
            if self.from_binary_transform_algorithm is not None
            else None
        )
        kwargs["to_binary_transform_algorithm"] = (
            self.to_binary_transform_algorithm._to_v1_3(policy)
            if self.to_binary_transform_algorithm is not None
            else None
        )
        return kwargs


class Container(NameDescriptionBase, ABC):
    """Define an abstract block of data."""

    default_rate_in_stream: RateInStream | None = None
    """The default rate at which data is expected in the stream."""

    rate_in_streams: list[RateInStreamWithStreamName] = Field(default_factory=list)
    """The rates at which data is expected in the stream for different stream names."""

    binary_encoding: ContainerBinaryDataEncoding | None = None
    """The binary encoding used for the container."""

    # TODO maybe consolidate RateInStream and RateInStreamWithStreamName into one model with optional stream_ref

    _v1_1_type = xtce_1_1.ContainerType
    _v1_2_type = xtce_1_2.ContainerType
    _v1_3_type = xtce_1_3.ContainerType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.ContainerType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["default_rate_in_stream"] = (
            RateInStream._from_v1_1_kwargs(obj.default_rate_in_stream)
            if obj.default_rate_in_stream is not None
            else None
        )
        kwargs["rate_in_streams"] = (
            [
                RateInStreamWithStreamName._from_v1_1_kwargs(r)
                for r in obj.rate_in_stream_set.rate_in_stream
            ]
            if obj.rate_in_stream_set is not None
            else []
        )
        kwargs["binary_encoding"] = (
            ContainerBinaryDataEncoding._from_v1_1_kwargs(obj.binary_encoding)
            if obj.binary_encoding is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ContainerType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["default_rate_in_stream"] = (
            RateInStream._from_v1_2_kwargs(obj.default_rate_in_stream)
            if obj.default_rate_in_stream is not None
            else None
        )
        kwargs["rate_in_streams"] = (
            [
                RateInStreamWithStreamName._from_v1_2_kwargs(r)
                for r in obj.rate_in_stream_set.rate_in_stream
            ]
            if obj.rate_in_stream_set is not None
            else []
        )
        kwargs["binary_encoding"] = (
            ContainerBinaryDataEncoding._from_v1_2_kwargs(obj.binary_encoding)
            if obj.binary_encoding is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ContainerType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["default_rate_in_stream"] = (
            RateInStream._from_v1_3_kwargs(obj.default_rate_in_stream)
            if obj.default_rate_in_stream is not None
            else None
        )
        kwargs["rate_in_streams"] = (
            [
                RateInStreamWithStreamName._from_v1_3_kwargs(r)
                for r in obj.rate_in_stream_set.rate_in_stream
            ]
            if obj.rate_in_stream_set is not None
            else []
        )
        kwargs["binary_encoding"] = (
            ContainerBinaryDataEncoding._from_v1_3_kwargs(obj.binary_encoding)
            if obj.binary_encoding is not None
            else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["default_rate_in_stream"] = (
            self.default_rate_in_stream._to_v1_1(policy)
            if self.default_rate_in_stream is not None
            else None
        )
        kwargs["rate_in_stream_set"] = self._build_set(
            items=self.rate_in_streams,
            set_class=xtce_1_1.ContainerType.RateInStreamSet,
            kwarg_name="rate_in_stream",
            converter=lambda r: r._to_v1_1(policy),
        )
        kwargs["binary_encoding"] = (
            self.binary_encoding._to_v1_1(policy)
            if self.binary_encoding is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["default_rate_in_stream"] = (
            self.default_rate_in_stream._to_v1_2(policy)
            if self.default_rate_in_stream is not None
            else None
        )
        kwargs["rate_in_stream_set"] = self._build_set(
            items=self.rate_in_streams,
            set_class=xtce_1_2.RateInStreamSetType,
            kwarg_name="rate_in_stream",
            converter=lambda r: r._to_v1_2(policy),
        )
        kwargs["binary_encoding"] = (
            self.binary_encoding._to_v1_2(policy)
            if self.binary_encoding is not None
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["default_rate_in_stream"] = (
            self.default_rate_in_stream._to_v1_3(policy)
            if self.default_rate_in_stream is not None
            else None
        )
        kwargs["rate_in_stream_set"] = self._build_set(
            items=self.rate_in_streams,
            set_class=xtce_1_3.RateInStreamSetType,
            kwarg_name="rate_in_stream",
            converter=lambda r: r._to_v1_3(policy),
        )
        kwargs["binary_encoding"] = (
            self.binary_encoding._to_v1_3(policy)
            if self.binary_encoding is not None
            else None
        )
        return kwargs


class SequenceContainer(Container):
    """Define the binary layout of data with some related properties."""

    entries: list[
        ParameterRefEntry
        | ParameterSegmentRefEntry
        | ContainerRefEntry
        | ContainerSegmentRefEntry
        | StreamSegmentEntry
        | IndirectParameterRefEntry
        | ArrayParameterRefEntry
    ] = Field(default_factory=list)
    """The list of entries that define the sequence container."""

    base_container: BaseContainer | None = None
    """The base container from which this sequence container inherits."""

    abstract: bool = False
    """Whether this sequence container is abstract and cannot be instantiated."""

    idle_pattern: XtceHexOrInt = 0x0
    """The idle pattern used in this sequence container."""

    _v1_1_type = xtce_1_1.SequenceContainerType
    _v1_2_type = xtce_1_2.SequenceContainerType
    _v1_3_type = xtce_1_3.SequenceContainerType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.SequenceContainerType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["entries"] = [
            ParameterRefEntry._from_v1_1_kwargs(e)
            if isinstance(e, xtce_1_1.ParameterRefEntryType)
            else ParameterSegmentRefEntry._from_v1_1_kwargs(e)
            if isinstance(e, xtce_1_1.ParameterSegmentRefEntryType)
            else ContainerRefEntry._from_v1_1_kwargs(e)
            if isinstance(e, xtce_1_1.ContainerRefEntryType)
            else ContainerSegmentRefEntry._from_v1_1_kwargs(e)
            if isinstance(e, xtce_1_1.ContainerSegmentRefEntryType)
            else StreamSegmentEntry._from_v1_1_kwargs(e)
            if isinstance(e, xtce_1_1.StreamSegmentEntryType)
            else IndirectParameterRefEntry._from_v1_1_kwargs(e)
            if isinstance(e, xtce_1_1.IndirectParameterRefEntryType)
            else ArrayParameterRefEntry._from_v1_1_kwargs(e)
            if isinstance(e, xtce_1_1.ArrayParameterRefEntryType)
            else None
            for e in obj.entry_list.choice
        ]
        kwargs["base_container"] = (
            BaseContainer._from_v1_1_kwargs(obj.base_container)
            if obj.base_container is not None
            else None
        )
        kwargs["abstract"] = obj.abstract
        kwargs["idle_pattern"] = obj.idle_pattern
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.SequenceContainerType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["entries"] = [
            ParameterRefEntry._from_v1_2_kwargs(e)
            if isinstance(e, xtce_1_2.ParameterRefEntryType)
            else ParameterSegmentRefEntry._from_v1_2_kwargs(e)
            if isinstance(e, xtce_1_2.ParameterSegmentRefEntryType)
            else ContainerRefEntry._from_v1_2_kwargs(e)
            if isinstance(e, xtce_1_2.ContainerRefEntryType)
            else ContainerSegmentRefEntry._from_v1_2_kwargs(e)
            if isinstance(e, xtce_1_2.ContainerSegmentRefEntryType)
            else StreamSegmentEntry._from_v1_2_kwargs(e)
            if isinstance(e, xtce_1_2.StreamSegmentEntryType)
            else IndirectParameterRefEntry._from_v1_2_kwargs(e)
            if isinstance(e, xtce_1_2.IndirectParameterRefEntryType)
            else ArrayParameterRefEntry._from_v1_2_kwargs(e)
            if isinstance(e, xtce_1_2.ArrayParameterRefEntryType)
            else None
            for e in obj.entry_list.choice
        ]
        kwargs["base_container"] = (
            BaseContainer._from_v1_2_kwargs(obj.base_container)
            if obj.base_container is not None
            else None
        )
        kwargs["abstract"] = obj.abstract
        kwargs["idle_pattern"] = obj.idle_pattern
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.SequenceContainerType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["entries"] = [
            ParameterRefEntry._from_v1_3_kwargs(e)
            if isinstance(e, xtce_1_3.ParameterRefEntryType)
            else ParameterSegmentRefEntry._from_v1_3_kwargs(e)
            if isinstance(e, xtce_1_3.ParameterSegmentRefEntryType)
            else ContainerRefEntry._from_v1_3_kwargs(e)
            if isinstance(e, xtce_1_3.ContainerRefEntryType)
            else ContainerSegmentRefEntry._from_v1_3_kwargs(e)
            if isinstance(e, xtce_1_3.ContainerSegmentRefEntryType)
            else StreamSegmentEntry._from_v1_3_kwargs(e)
            if isinstance(e, xtce_1_3.StreamSegmentEntryType)
            else IndirectParameterRefEntry._from_v1_3_kwargs(e)
            if isinstance(e, xtce_1_3.IndirectParameterRefEntryType)
            else ArrayParameterRefEntry._from_v1_3_kwargs(e)
            if isinstance(e, xtce_1_3.ArrayParameterRefEntryType)
            else None
            for e in obj.entry_list.choice
        ]
        kwargs["base_container"] = (
            BaseContainer._from_v1_3_kwargs(obj.base_container)
            if obj.base_container is not None
            else None
        )
        kwargs["abstract"] = obj.abstract
        kwargs["idle_pattern"] = obj.idle_pattern
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["entry_list"] = self._build_set(
            items=self.entries,
            set_class=xtce_1_1.EntryListType,
            kwarg_name="choice",
            converter=lambda e: e._to_v1_1(policy),
        )
        kwargs["base_container"] = (
            self.base_container._to_v1_1(policy)
            if self.base_container is not None
            else None
        )
        kwargs["abstract"] = self.abstract
        kwargs["idle_pattern"] = self.idle_pattern
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["entry_list"] = self._build_set(
            items=self.entries,
            set_class=xtce_1_2.EntryListType,
            kwarg_name="choice",
            converter=lambda e: e._to_v1_2(policy),
        )
        kwargs["base_container"] = (
            self.base_container._to_v1_2(policy)
            if self.base_container is not None
            else None
        )
        kwargs["abstract"] = self.abstract
        kwargs["idle_pattern"] = self.idle_pattern
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["entry_list"] = self._build_set(
            items=self.entries,
            set_class=xtce_1_3.EntryListType,
            kwarg_name="choice",
            converter=lambda e: e._to_v1_3(policy),
        )
        kwargs["base_container"] = (
            self.base_container._to_v1_3(policy)
            if self.base_container is not None
            else None
        )
        kwargs["abstract"] = self.abstract
        kwargs["idle_pattern"] = self.idle_pattern
        return kwargs


class CommandContainer(Container):
    """Describe a command container."""

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
    ] = Field(default_factory=list)
    """List of entries in the command container."""

    base_container: BaseContainer | None = None
    """Reference to the base container, if any."""

    _v1_1_type = xtce_1_1.CommandContainerType
    _v1_2_type = xtce_1_2.CommandContainerType
    _v1_3_type = xtce_1_3.CommandContainerType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.CommandContainerType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["entries"] = [
            ArgumentParameterRefEntry._from_v1_1(e)
            if isinstance(e, xtce_1_1.ParameterRefEntryType)
            else ArgumentParameterSegmentRefEntry._from_v1_1(e)
            if isinstance(e, xtce_1_1.ParameterSegmentRefEntryType)
            else ArgumentContainerRefEntry._from_v1_1(e)
            if isinstance(e, xtce_1_1.ContainerRefEntryType)
            else ArgumentContainerSegmentRefEntry._from_v1_1(e)
            if isinstance(e, xtce_1_1.ContainerSegmentRefEntryType)
            else ArgumentStreamSegmentEntry._from_v1_1(e)
            if isinstance(e, xtce_1_1.StreamSegmentEntryType)
            else ArgumentIndirectParameterRefEntry._from_v1_1(e)
            if isinstance(e, xtce_1_1.IndirectParameterRefEntryType)
            else ArgumentArrayParameterRefEntry._from_v1_1(e)
            if isinstance(
                e, xtce_1_1.CommandContainerEntryListType.ArrayParameterRefEntry
            )
            else ArgumentArgumentRefEntry._from_v1_1(e)
            if isinstance(e, xtce_1_1.CommandContainerEntryListType.ArgumentRefEntry)
            else ArgumentArrayArgumentRefEntry._from_v1_1(e)
            if isinstance(
                e, xtce_1_1.CommandContainerEntryListType.ArrayArgumentRefEntry
            )
            else ArgumentFixedValueEntry._from_v1_1(e)
            if isinstance(e, xtce_1_1.CommandContainerEntryListType.FixedValueEntry)
            else None
            for e in obj.entry_list.choice
        ]
        kwargs["base_container"] = (
            BaseContainer._from_v1_1(obj.base_container)
            if obj.base_container is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.CommandContainerType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["entries"] = [
            ArgumentParameterRefEntry._from_v1_2(e)
            if isinstance(e, xtce_1_2.ArgumentParameterRefEntryType)
            else ArgumentParameterSegmentRefEntry._from_v1_2(e)
            if isinstance(e, xtce_1_2.ArgumentParameterSegmentRefEntryType)
            else ArgumentContainerRefEntry._from_v1_2(e)
            if isinstance(e, xtce_1_2.ArgumentContainerRefEntryType)
            else ArgumentContainerSegmentRefEntry._from_v1_2(e)
            if isinstance(e, xtce_1_2.ArgumentContainerSegmentRefEntryType)
            else ArgumentStreamSegmentEntry._from_v1_2(e)
            if isinstance(e, xtce_1_2.ArgumentStreamSegmentEntryType)
            else ArgumentIndirectParameterRefEntry._from_v1_2(e)
            if isinstance(e, xtce_1_2.ArgumentIndirectParameterRefEntryType)
            else ArgumentArrayParameterRefEntry._from_v1_2(e)
            if isinstance(e, xtce_1_2.ArgumentArrayParameterRefEntryType)
            else ArgumentArgumentRefEntry._from_v1_2(e)
            if isinstance(e, xtce_1_2.ArgumentArgumentRefEntryType)
            else ArgumentArrayArgumentRefEntry._from_v1_2(e)
            if isinstance(e, xtce_1_2.ArgumentArrayArgumentRefEntryType)
            else ArgumentFixedValueEntry._from_v1_2(e)
            if isinstance(e, xtce_1_2.ArgumentFixedValueEntryType)
            else None
            for e in obj.entry_list.choice
        ]
        kwargs["base_container"] = (
            BaseContainer._from_v1_2(obj.base_container)
            if obj.base_container is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.CommandContainerType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["entries"] = [
            ArgumentParameterRefEntry._from_v1_3(e)
            if isinstance(e, xtce_1_3.ArgumentParameterRefEntryType)
            else ArgumentParameterSegmentRefEntry._from_v1_3(e)
            if isinstance(e, xtce_1_3.ArgumentParameterSegmentRefEntryType)
            else ArgumentContainerRefEntry._from_v1_3(e)
            if isinstance(e, xtce_1_3.ArgumentContainerRefEntryType)
            else ArgumentContainerSegmentRefEntry._from_v1_3(e)
            if isinstance(e, xtce_1_3.ArgumentContainerSegmentRefEntryType)
            else ArgumentStreamSegmentEntry._from_v1_3(e)
            if isinstance(e, xtce_1_3.ArgumentStreamSegmentEntryType)
            else ArgumentIndirectParameterRefEntry._from_v1_3(e)
            if isinstance(e, xtce_1_3.ArgumentIndirectParameterRefEntryType)
            else ArgumentArrayParameterRefEntry._from_v1_3(e)
            if isinstance(e, xtce_1_3.ArgumentArrayParameterRefEntryType)
            else ArgumentArgumentRefEntry._from_v1_3(e)
            if isinstance(e, xtce_1_3.ArgumentArgumentRefEntryType)
            else ArgumentArrayArgumentRefEntry._from_v1_3(e)
            if isinstance(e, xtce_1_3.ArgumentArrayArgumentRefEntryType)
            else ArgumentFixedValueEntry._from_v1_3(e)
            if isinstance(e, xtce_1_3.ArgumentFixedValueEntryType)
            else None
            for e in obj.entry_list.choice
        ]
        kwargs["base_container"] = (
            BaseContainer._from_v1_3(obj.base_container)
            if obj.base_container is not None
            else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["entry_list"] = self._build_set(
            items=self.entries,
            set_class=xtce_1_1.CommandContainerEntryListType,
            kwarg_name="choice",
            converter=lambda e: e._to_v1_1(policy),
        )
        kwargs["base_container"] = (
            self.base_container._to_v1_1(policy)
            if self.base_container is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["entry_list"] = self._build_set(
            items=self.entries,
            set_class=xtce_1_2.CommandContainerEntryListType,
            kwarg_name="choice",
            converter=lambda e: e._to_v1_2(policy),
        )
        kwargs["base_container"] = (
            self.base_container._to_v1_2(policy)
            if self.base_container is not None
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["entry_list"] = self._build_set(
            items=self.entries,
            set_class=xtce_1_3.CommandContainerEntryListType,
            kwarg_name="choice",
            converter=lambda e: e._to_v1_3(policy),
        )
        kwargs["base_container"] = (
            self.base_container._to_v1_3(policy)
            if self.base_container is not None
            else None
        )
        return kwargs
