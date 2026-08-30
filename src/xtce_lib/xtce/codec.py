"""Encoding/decoding models."""

from __future__ import annotations

from abc import ABC
from typing import Annotated, Any, Literal, Self, assert_never

from pydantic import Field, model_validator

from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from ._util import unwrap
from .algorithm import (
    CRC,
    XOR,
    ArgumentInputAlgorithm,
    Checksum,
    InputAlgorithm,
    Parity,
)
from .calibrator import Calibrator, ContextCalibrator, LinearAdjustment
from .condition import (
    ArgumentDiscreteLookupList,
    DiscreteLookupList,
)
from .enum import (
    BitOrder,
    Endian,
    FloatEncoding,
    IntegerEncoding,
    StringEncoding,
    TimeUnits,
)
from .reference import ArgumentInstanceRef, ParameterInstanceRef


def parse_integer_value_v1_1(
    integer_value: xtce_1_1.IntegerValueType | None,
) -> int | DynamicValue | DiscreteLookupList | None:
    """Parse an IntegerValueType into the unified model types."""
    if integer_value is None:
        return None
    match integer_value.choice:
        case int() as val:
            return val
        case str() as val:
            return int(val, 0)
        case xtce_1_1.IntegerValueType.DynamicValue() as val:
            return DynamicValue._from_v1_1(val)
        case xtce_1_1.IntegerValueType.DiscreteLookupList() as val:
            return DiscreteLookupList._from_v1_1(val)
        case None:
            raise ValueError("invalid XTCE XML: dimension index is missing a value")
        case _:
            assert_never(integer_value.choice)


def parse_integer_value_v1_2(
    integer_value: xtce_1_2.IntegerValueType | None,
) -> int | DynamicValue | DiscreteLookupList | None:
    """Parse an IntegerValueType into the unified model types."""
    if integer_value is None:
        return None
    match integer_value.choice:
        case int() as val:
            return val
        case xtce_1_2.DynamicValueType() as val:
            return DynamicValue._from_v1_2(val)
        case xtce_1_2.DiscreteLookupListType() as val:
            return DiscreteLookupList._from_v1_2(val)
        case None:
            raise ValueError("invalid XTCE XML: dimension index is missing a value")
        case _:
            assert_never(integer_value.choice)


def parse_integer_value_v1_3(
    integer_value: xtce_1_3.IntegerValueType | None,
) -> int | DynamicValue | DiscreteLookupList | None:
    """Parse an IntegerValueType into the unified model types."""
    if integer_value is None:
        return None
    match integer_value.choice:
        case int() as val:
            return val
        case xtce_1_3.DynamicValueType() as val:
            return DynamicValue._from_v1_3(val)
        case xtce_1_3.DiscreteLookupListType() as val:
            return DiscreteLookupList._from_v1_3(val)
        case None:
            raise ValueError("invalid XTCE XML: dimension index is missing a value")
        case _:
            assert_never(integer_value.choice)


def pack_integer_value_v1_1(
    value: int | DynamicValue | DiscreteLookupList | None,
    policy: DowngradePolicy,
) -> xtce_1_1.IntegerValueType | None:
    """Pack a unified model index value into an IntegerValueType."""
    if value is None:
        return None
    match value:
        case int():
            return xtce_1_1.IntegerValueType(choice=value)
        case DynamicValue():
            return xtce_1_1.IntegerValueType(choice=value._to_v1_1(policy))
        case DiscreteLookupList():
            return xtce_1_1.IntegerValueType(choice=value._to_v1_1(policy))


def pack_integer_value_v1_2(
    value: int | DynamicValue | DiscreteLookupList | None,
    policy: DowngradePolicy,
) -> xtce_1_2.IntegerValueType | None:
    """Pack a unified model index value into an IntegerValueType."""
    if value is None:
        return None
    match value:
        case int():
            return xtce_1_2.IntegerValueType(choice=value)
        case DynamicValue():
            return xtce_1_2.IntegerValueType(choice=value._to_v1_2(policy))
        case DiscreteLookupList():
            return xtce_1_2.IntegerValueType(choice=value._to_v1_2(policy))


def pack_integer_value_v1_3(
    value: int | DynamicValue | DiscreteLookupList | None,
    policy: DowngradePolicy,
) -> xtce_1_3.IntegerValueType | None:
    """Pack a unified model index value into an IntegerValueType."""
    if value is None:
        return None
    match value:
        case int():
            return xtce_1_3.IntegerValueType(choice=value)
        case DynamicValue():
            return xtce_1_3.IntegerValueType(choice=value._to_v1_3(policy))
        case DiscreteLookupList():
            return xtce_1_3.IntegerValueType(choice=value._to_v1_3(policy))


def parse_argument_integer_value_v1_1(
    integer_value: xtce_1_1.IntegerValueType | None,
) -> int | ArgumentDynamicValue | ArgumentDiscreteLookupList | None:
    """Parse an ArgumentIntegerValueType into the unified model types."""
    if integer_value is None:
        return None
    match integer_value.choice:
        case int() as val:
            return val
        case str() as val:
            return int(val, 0)
        case xtce_1_1.IntegerValueType.DynamicValue() as val:
            return ArgumentDynamicValue._from_v1_1(val)
        case xtce_1_1.IntegerValueType.DiscreteLookupList() as val:
            return ArgumentDiscreteLookupList._from_v1_1(val)
        case None:
            raise ValueError("invalid XTCE XML: dimension index is missing a value")
        case _:
            assert_never(integer_value.choice)


def parse_argument_integer_value_v1_2(
    integer_value: xtce_1_2.ArgumentIntegerValueType | None,
) -> int | ArgumentDynamicValue | ArgumentDiscreteLookupList | None:
    """Parse an ArgumentIntegerValueType into the unified model types."""
    if integer_value is None:
        return None
    match integer_value.choice:
        case int() as val:
            return val
        case xtce_1_2.ArgumentDynamicValueType() as val:
            return ArgumentDynamicValue._from_v1_2(val)
        case xtce_1_2.ArgumentDiscreteLookupListType() as val:
            return ArgumentDiscreteLookupList._from_v1_2(val)
        case None:
            raise ValueError("invalid XTCE XML: dimension index is missing a value")
        case _:
            assert_never(integer_value.choice)


def parse_argument_integer_value_v1_3(
    integer_value: xtce_1_3.ArgumentIntegerValueType | None,
) -> int | ArgumentDynamicValue | ArgumentDiscreteLookupList | None:
    """Parse an ArgumentIntegerValueType into the unified model types."""
    if integer_value is None:
        return None
    match integer_value.choice:
        case int() as val:
            return val
        case xtce_1_3.ArgumentDynamicValueType() as val:
            return ArgumentDynamicValue._from_v1_3(val)
        case xtce_1_3.ArgumentDiscreteLookupListType() as val:
            return ArgumentDiscreteLookupList._from_v1_3(val)
        case None:
            raise ValueError("invalid XTCE XML: dimension index is missing a value")
        case _:
            assert_never(integer_value.choice)


def pack_argument_integer_value_v1_1(
    value: int | ArgumentDynamicValue | ArgumentDiscreteLookupList | None,
    policy: DowngradePolicy,
) -> xtce_1_1.IntegerValueType | None:
    """Pack a unified model argument index value into an ArgumentIntegerValueType."""
    if value is None:
        return None
    match value:
        case int():
            return xtce_1_1.IntegerValueType(choice=value)
        case ArgumentDynamicValue():
            return xtce_1_1.IntegerValueType(choice=value._to_v1_1(policy))
        case ArgumentDiscreteLookupList():
            return xtce_1_1.IntegerValueType(choice=value._to_v1_1(policy))


def pack_argument_integer_value_v1_2(
    value: int | ArgumentDynamicValue | ArgumentDiscreteLookupList | None,
    policy: DowngradePolicy,
) -> xtce_1_2.ArgumentIntegerValueType | None:
    """Pack a unified model argument index value into an ArgumentIntegerValueType."""
    if value is None:
        return None
    match value:
        case int():
            return xtce_1_2.ArgumentIntegerValueType(choice=value)
        case ArgumentDynamicValue():
            return xtce_1_2.ArgumentIntegerValueType(choice=value._to_v1_2(policy))
        case ArgumentDiscreteLookupList():
            return xtce_1_2.ArgumentIntegerValueType(choice=value._to_v1_2(policy))


def pack_argument_integer_value_v1_3(
    value: int | ArgumentDynamicValue | ArgumentDiscreteLookupList | None,
    policy: DowngradePolicy,
) -> xtce_1_3.ArgumentIntegerValueType | None:
    """Pack a unified model argument index value into an ArgumentIntegerValueType."""
    if value is None:
        return None
    match value:
        case int():
            return xtce_1_3.ArgumentIntegerValueType(choice=value)
        case ArgumentDynamicValue():
            return xtce_1_3.ArgumentIntegerValueType(choice=value._to_v1_3(policy))
        case ArgumentDiscreteLookupList():
            return xtce_1_3.ArgumentIntegerValueType(choice=value._to_v1_3(policy))


class DynamicValue(XtceBaseModel):
    """A value obtained by a reference to a parameter instance.

    The parameter value may be optionally adjusted by a linear function.

    """

    instance: ParameterInstanceRef
    """The parameter instance being referenced."""

    linear_adjustment: LinearAdjustment | None = None
    """An optional linear adjustment applied to the referenced parameter value."""

    _v1_1_type = xtce_1_1.IntegerValueType.DynamicValue
    _v1_2_type = xtce_1_2.DynamicValueType
    _v1_3_type = xtce_1_3.DynamicValueType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.IntegerValueType.DynamicValue
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["instance"] = ParameterInstanceRef._from_v1_1(obj.parameter_instance_ref)
        kwargs["linear_adjustment"] = (
            LinearAdjustment._from_v1_1(obj.linear_adjustment)
            if obj.linear_adjustment
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.DynamicValueType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["instance"] = ParameterInstanceRef._from_v1_2(obj.parameter_instance_ref)
        kwargs["linear_adjustment"] = (
            LinearAdjustment._from_v1_2(obj.linear_adjustment)
            if obj.linear_adjustment
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.DynamicValueType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["instance"] = ParameterInstanceRef._from_v1_3(obj.parameter_instance_ref)
        kwargs["linear_adjustment"] = (
            LinearAdjustment._from_v1_3(obj.linear_adjustment)
            if obj.linear_adjustment
            else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["parameter_instance_ref"] = self.instance._to_v1_1(policy)
        kwargs["linear_adjustment"] = (
            self.linear_adjustment._to_v1_1(policy) if self.linear_adjustment else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["parameter_instance_ref"] = self.instance._to_v1_2(policy)
        kwargs["linear_adjustment"] = (
            self.linear_adjustment._to_v1_2(policy) if self.linear_adjustment else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["parameter_instance_ref"] = self.instance._to_v1_3(policy)
        kwargs["linear_adjustment"] = (
            self.linear_adjustment._to_v1_3(policy) if self.linear_adjustment else None
        )
        return kwargs


class ArgumentDynamicValue(XtceBaseModel):
    """A value obtained by a reference to an argument or parameter instance.

    The argument or parameter value may be optionally adjusted by a linear function.

    """

    instance: ArgumentInstanceRef | ParameterInstanceRef
    """The argument or parameter instance being referenced."""

    linear_adjustment: LinearAdjustment | None = None
    """An optional linear adjustment applied to the referenced argument or parameter
    value.
    """

    _v1_1_type = xtce_1_1.IntegerValueType.DynamicValue
    _v1_2_type = xtce_1_2.ArgumentDynamicValueType
    _v1_3_type = xtce_1_3.ArgumentDynamicValueType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.IntegerValueType.DynamicValue
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["instance"] = ParameterInstanceRef._from_v1_1(obj.parameter_instance_ref)
        kwargs["linear_adjustment"] = (
            LinearAdjustment._from_v1_1(obj.linear_adjustment)
            if obj.linear_adjustment
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentDynamicValueType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["instance"] = (
            ArgumentInstanceRef._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.ArgumentInstanceRefType)
            else ParameterInstanceRef._from_v1_2(unwrap(obj.choice))
        )
        kwargs["linear_adjustment"] = (
            LinearAdjustment._from_v1_2(obj.linear_adjustment)
            if obj.linear_adjustment
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentDynamicValueType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["instance"] = (
            ArgumentInstanceRef._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.ArgumentInstanceRefType)
            else ParameterInstanceRef._from_v1_3(unwrap(obj.choice))
        )
        kwargs["linear_adjustment"] = (
            LinearAdjustment._from_v1_3(obj.linear_adjustment)
            if obj.linear_adjustment
            else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        instance = self._enforce_restricted_type(
            field_name="instance",
            current_value=self.instance,
            allowed_types=(ParameterInstanceRef,),
            target_version=XtceVersion.V1_1,
            policy=policy,
            require_match=True,
        )

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["parameter_instance_ref"] = instance._to_v1_1(policy)
        kwargs["linear_adjustment"] = (
            self.linear_adjustment._to_v1_1(policy) if self.linear_adjustment else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = self.instance._to_v1_2(policy)
        kwargs["linear_adjustment"] = (
            self.linear_adjustment._to_v1_2(policy) if self.linear_adjustment else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = self.instance._to_v1_3(policy)
        kwargs["linear_adjustment"] = (
            self.linear_adjustment._to_v1_3(policy) if self.linear_adjustment else None
        )
        return kwargs


class LeadingSize(XtceBaseModel):
    """Define a leading size for variable-length strings."""

    size_in_bits: int = Field(default=16, ge=1)
    """The size of the leading size field in bits."""

    _v1_1_type = xtce_1_1.StringDataEncodingType.SizeInBits.LeadingSize
    _v1_2_type = xtce_1_2.LeadingSizeType
    _v1_3_type = xtce_1_3.LeadingSizeType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.StringDataEncodingType.SizeInBits.LeadingSize
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["size_in_bits"] = obj.size_in_bits_of_size_tag
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.LeadingSizeType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["size_in_bits"] = obj.size_in_bits_of_size_tag
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.LeadingSizeType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["size_in_bits"] = obj.size_in_bits_of_size_tag
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["size_in_bits_of_size_tag"] = self.size_in_bits
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["size_in_bits_of_size_tag"] = self.size_in_bits
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["size_in_bits_of_size_tag"] = self.size_in_bits
        return kwargs


class DataEncoding(XtceBaseModel, ABC):
    """Describes how a particular piece of data is sent or received from some device."""

    error_detect_correct: list[Checksum | CRC | XOR | Parity] | None = Field(
        default=None
    )
    """DEPRECATED: Use the ErrorDetectCorrect element in the container elements instead.

    Only one of the error detection/correction types is allowed for v1.1 and v1.2. XTCE
    1.1 only supports Parity and Checksum, while XTCE 1.2 supports Parity, Checksum, and
    CRC. XTCE 1.3 supports Parity, Checksum, CRC, and XOR. If multiple types are
    provided, the first in the list will be used for v1.1 and v1.2, while all types will
    be used for v1.3.

    """

    # TODO update reference to the correct element or if 1.1 or 1.2 support this

    bit_order: BitOrder = BitOrder.MOST_SIGNIFICANT_BIT_FIRST
    """The bit order of the encoded value."""

    byte_order: Endian | list[int] = Field(
        default=Endian.BIG,
        examples=[Endian.BIG, Endian.LITTLE, [3, 2, 1, 0], [0, 1, 2, 3]],
    )
    """The endianness of the encoded value.

    A list of integers may be used to specify a custom byte order. The list is viewed as
    representing memory, the first item in the list is address 0. For
    mostSignificantByteFirst/big endian, the high order byte is the first byte in the
    list and has the highest significance followed by the less significant bytes ending
    with the least significant byte. For leastSignificantByteFirst/little endian, the
    first byte starts with the least significant byte which is first in the least and
    ends at the highest significant byte. For example given the value 0x0A0B0C0D the
    following example orderings can be formed. For mostSignificantByteFirst/big endian
    the significances would be listed as 3 (0x0A), 2 (0x0B), 1 (0x0C), 0 (0x0D) with 3
    being first in the list, and for leastSignificantByteFirst/little endian as 0
    (0x0D), 1 (0x0C), 2 (0x0B), 3 (0x0A) with 0 being first in the list.

    """

    # TODO probably need a field validator to make sure byte order list has no negatives

    _v1_1_type = xtce_1_1.DataEncodingType
    _v1_2_type = xtce_1_2.DataEncodingType
    _v1_3_type = xtce_1_3.DataEncodingType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.DataEncodingType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["error_detect_correct"] = (
            [
                Parity._from_v1_1(obj.error_detect_correct.choice)
                if isinstance(
                    obj.error_detect_correct.choice,
                    xtce_1_1.ErrorDetectCorrectType.Parity,
                )
                else Checksum._from_v1_1(obj.error_detect_correct.choice)
            ]
            if obj.error_detect_correct is not None
            and obj.error_detect_correct.choice is not None
            else None
        )
        kwargs["bit_order"] = BitOrder(obj.bit_order.value)
        # byte_order has no default at the XSD level (v1.1 makes it optional), so only
        # set it when present - omitting the key lets the model's Endian.BIG default apply
        if obj.byte_order_list is not None:
            kwargs["byte_order"] = [
                b.byte_significance for b in obj.byte_order_list.byte
            ]
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.DataEncodingType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["error_detect_correct"] = (
            [
                Checksum._from_v1_2(obj.error_detect_correct.choice)
                if isinstance(
                    obj.error_detect_correct.choice,
                    xtce_1_2.ChecksumType,
                )
                else CRC._from_v1_2(obj.error_detect_correct.choice)
                if isinstance(
                    obj.error_detect_correct.choice,
                    xtce_1_2.Crctype,
                )
                else Parity._from_v1_2(obj.error_detect_correct.choice)
            ]
            if obj.error_detect_correct is not None
            and obj.error_detect_correct.choice is not None
            else None
        )
        kwargs["bit_order"] = BitOrder(obj.bit_order.value)
        kwargs["byte_order"] = (
            [int(b) for b in obj.byte_order.split(",")]
            if isinstance(obj.byte_order, str)
            else Endian(obj.byte_order.value)
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.DataEncodingType) -> dict[str, Any]:
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
        kwargs["bit_order"] = BitOrder(obj.bit_order.value)
        kwargs["byte_order"] = (
            [int(b) for b in obj.byte_order.split(",")]
            if isinstance(obj.byte_order, str)
            else Endian(obj.byte_order.value)
        )
        return kwargs

    def _to_v1_1_kwargs(
        self, policy: DowngradePolicy, size_in_bits: int | None = None
    ) -> dict[str, Any]:
        error_detect_correct_list = self._enforce_list_length(
            field_name="error_detect_correct",
            current_value=self.error_detect_correct,
            min_length=0,
            max_length=1,
            target_version=XtceVersion.V1_1,
            policy=policy,
            fallback=self.error_detect_correct[:1]
            if self.error_detect_correct
            else None,
        )
        error_detect_correct = (
            error_detect_correct_list[0] if error_detect_correct_list else None
        )
        if error_detect_correct is not None:
            self._enforce_restricted_type(
                field_name="error_detect_correct",
                current_value=error_detect_correct,
                allowed_types=(Checksum, Parity),
                target_version=XtceVersion.V1_1,
                policy=policy,
                require_match=True,
            )

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["error_detect_correct"] = (
            xtce_1_1.ErrorDetectCorrectType(
                choice=error_detect_correct._to_v1_1(policy)
            )
            if error_detect_correct is not None
            else None
        )
        kwargs["bit_order"] = xtce_1_1.DataEncodingTypeBitOrder(self.bit_order.value)
        kwargs["byte_order_list"] = (
            xtce_1_1.ByteOrderType(
                byte=[
                    xtce_1_1.ByteOrderType.Byte(byte_significance=b)
                    for b in self.byte_order
                ]
                if isinstance(self.byte_order, list)
                else [  # Big endian byte order list
                    xtce_1_1.ByteOrderType.Byte(byte_significance=b)
                    for b in range(size_in_bits // 8 - 1, -1, -1)
                ]
                if self.byte_order == Endian.BIG
                else [  # Little endian byte order list
                    xtce_1_1.ByteOrderType.Byte(byte_significance=b)
                    for b in range(size_in_bits // 8)
                ]
            )
            if size_in_bits is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        error_detect_correct_list = self._enforce_list_length(
            field_name="error_detect_correct",
            current_value=self.error_detect_correct,
            min_length=0,
            max_length=1,
            target_version=XtceVersion.V1_2,
            policy=policy,
            fallback=self.error_detect_correct[:1]
            if self.error_detect_correct
            else None,
        )
        # ErrorDetectCorrectType only ever holds a single entry, so unwrap the list
        error_detect_correct = (
            error_detect_correct_list[0] if error_detect_correct_list else None
        )
        if error_detect_correct is not None:
            error_detect_correct = self._enforce_restricted_type(
                field_name="error_detect_correct",
                current_value=error_detect_correct,
                allowed_types=(Checksum, CRC, Parity),
                target_version=XtceVersion.V1_2,
                policy=policy,
                require_match=True,
            )

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["error_detect_correct"] = (
            xtce_1_2.ErrorDetectCorrectType(
                choice=error_detect_correct._to_v1_2(policy)
            )
            if error_detect_correct is not None
            else None
        )
        kwargs["bit_order"] = xtce_1_2.BitOrderType(self.bit_order.value)
        kwargs["byte_order"] = (
            ",".join(str(b) for b in self.byte_order)
            if isinstance(self.byte_order, list)
            else xtce_1_2.ByteOrderCommonType(self.byte_order.value)
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
        kwargs["bit_order"] = xtce_1_3.BitOrderType(self.bit_order.value)
        kwargs["byte_order"] = (
            ",".join(str(b) for b in self.byte_order)
            if isinstance(self.byte_order, list)
            else xtce_1_3.ByteOrderCommonType(self.byte_order.value)
        )
        return kwargs


class IntegerDataEncoding(DataEncoding):
    """Describes how an integer value is sent or received from some device."""

    default_calibrator: Calibrator | None = None
    """Calibrator to be applied to the raw uncalibrated value to arrive at the
    engineering/calibrated value when no context calibrators are provided or evaluate to
    true, based on their match criteria.
    """

    context_calibrators: list[ContextCalibrator] = Field(default_factory=list)
    """Calibrator to be applied to the raw uncalibrated value to arrive at the
    engineering/calibrated value when the match criteria evaluates to true.

    The first in the list to match takes precedence.

    """

    encoding: IntegerEncoding = IntegerEncoding.UNSIGNED
    """The raw encoding of the integer value."""

    size_in_bits: int = Field(default=8, ge=1, examples=[8, 16, 32, 64])
    """Number of bits to use for the raw encoding."""

    # TODO add valid bit sizes and associated encodings in docstring

    change_threshold: int | None = Field(default=None, ge=0)
    """Used to inform systems of the minimum change in value that is significant.

    This is used by some systems to limit the telemetry processing and/or recording
    requirements, such as for an analog-to-digital converter that dithers in the least
    significant bit. If the value is unspecified or zero, any change is significant.

    Applicable since: XTCE 1.2

    """

    # TODO validate size in bits is valid for encoding type
    # TODO maybe require default calibrator if context calibrators are provided?

    _v1_1_type = xtce_1_1.IntegerDataEncodingType
    _v1_2_type = xtce_1_2.IntegerDataEncodingType
    _v1_3_type = xtce_1_3.IntegerDataEncodingType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.IntegerDataEncodingType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["default_calibrator"] = (
            Calibrator._from_v1_1(obj.default_calibrator)
            if obj.default_calibrator
            else None
        )
        kwargs["context_calibrators"] = (
            [
                ContextCalibrator._from_v1_1(c)
                for c in obj.context_calibrator_list.context_calibrator
            ]
            if obj.context_calibrator_list
            else []
        )
        kwargs["encoding"] = IntegerEncoding._from_v1_1(obj.encoding)
        kwargs["size_in_bits"] = obj.size_in_bits
        kwargs["change_threshold"] = None  # Not supported in v1.1
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.IntegerDataEncodingType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["default_calibrator"] = (
            Calibrator._from_v1_2(obj.default_calibrator)
            if obj.default_calibrator
            else None
        )
        kwargs["context_calibrators"] = (
            [
                ContextCalibrator._from_v1_2(c)
                for c in obj.context_calibrator_list.context_calibrator
            ]
            if obj.context_calibrator_list
            else []
        )
        kwargs["encoding"] = IntegerEncoding._from_v1_2(obj.encoding)
        kwargs["size_in_bits"] = obj.size_in_bits
        kwargs["change_threshold"] = obj.change_threshold
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.IntegerDataEncodingType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["default_calibrator"] = (
            Calibrator._from_v1_3(obj.default_calibrator)
            if obj.default_calibrator
            else None
        )
        kwargs["context_calibrators"] = (
            [
                ContextCalibrator._from_v1_3(c)
                for c in obj.context_calibrator_list.context_calibrator
            ]
            if obj.context_calibrator_list
            else []
        )
        kwargs["encoding"] = IntegerEncoding._from_v1_3(obj.encoding)
        kwargs["size_in_bits"] = obj.size_in_bits
        kwargs["change_threshold"] = obj.change_threshold
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="change_threshold",
            current_value=self.change_threshold,
            target_version=XtceVersion.V1_1,
            policy=policy,
        )

        kwargs = super()._to_v1_1_kwargs(policy, self.size_in_bits)
        kwargs["default_calibrator"] = (
            self.default_calibrator._to_v1_1(policy)
            if self.default_calibrator
            else None
        )
        kwargs["context_calibrator_list"] = self._build_set(
            items=self.context_calibrators,
            set_class=xtce_1_1.IntegerDataEncodingType.ContextCalibratorList,
            kwarg_name="context_calibrator",
            converter=lambda c: c._to_v1_1(policy),
        )
        kwargs["encoding"] = self.encoding._to_v1_1(policy)
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["default_calibrator"] = (
            self.default_calibrator._to_v1_2(policy)
            if self.default_calibrator
            else None
        )
        kwargs["context_calibrator_list"] = self._build_set(
            items=self.context_calibrators,
            set_class=xtce_1_2.ContextCalibratorListType,
            kwarg_name="context_calibrator",
            converter=lambda c: c._to_v1_2(policy),
        )
        kwargs["encoding"] = self.encoding._to_v1_2(policy)
        kwargs["size_in_bits"] = self.size_in_bits
        kwargs["change_threshold"] = self.change_threshold
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["default_calibrator"] = (
            self.default_calibrator._to_v1_3(policy)
            if self.default_calibrator
            else None
        )
        kwargs["context_calibrator_list"] = self._build_set(
            items=self.context_calibrators,
            set_class=xtce_1_3.ContextCalibratorListType,
            kwarg_name="context_calibrator",
            converter=lambda c: c._to_v1_3(policy),
        )
        kwargs["encoding"] = self.encoding._to_v1_3(policy)
        kwargs["size_in_bits"] = self.size_in_bits
        kwargs["change_threshold"] = self.change_threshold
        return kwargs


class FloatDataEncoding(DataEncoding):
    """Describes how a floating point value is sent or received from some device."""

    default_calibrator: Calibrator | None = None
    """Calibrator to be applied to the raw uncalibrated value to arrive at the
    engineering/calibrated value when no context calibrators are provided or evaluate to
    true, based on their match criteria.
    """

    context_calibrators: list[ContextCalibrator] = Field(default_factory=list)
    """Calibrator to be applied to the raw uncalibrated value to arrive at the
    engineering/calibrated value when the match criteria evaluates to true.

    The first in the list to match takes precedence.

    """

    encoding: FloatEncoding = FloatEncoding.IEEE754_1985
    """The raw encoding of the float value."""

    size_in_bits: Literal[16, 32, 40, 48, 64, 80, 128] = 32
    """Number of bits to use for the raw encoding.

    Valid bit sizes and their associated standards:
    - `16`: IEEE754, MILSTD_1750A
    - `32`: IEEE754, MILSTD_1750A, DEC, IBM, TI
    - `40`: TI
    - `48`: MILSTD_1750A
    - `64`: IEEE754, DEC, IBM
    - `80`: IEEE754_1985
    - `128`: IEEE754

    """

    change_threshold: float | None = None
    """Used to inform systems of the minimum change in value that is significant.

    This is used by some systems to limit the telemetry processing and/or recording
    requirements, such as for an analog-to-digital converter that dithers in the least
    significant bit. If the value is unspecified or zero, any change is significant.

    """

    # TODO validate size in bits is valid for encoding type

    _v1_1_type = xtce_1_1.FloatDataEncodingType
    _v1_2_type = xtce_1_2.FloatDataEncodingType
    _v1_3_type = xtce_1_3.FloatDataEncodingType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.FloatDataEncodingType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["default_calibrator"] = (
            Calibrator._from_v1_1(obj.default_calibrator)
            if obj.default_calibrator
            else None
        )
        kwargs["context_calibrators"] = (
            [
                ContextCalibrator._from_v1_1(c)
                for c in obj.context_calibrator_list.context_calibrator
            ]
            if obj.context_calibrator_list
            else []
        )
        kwargs["encoding"] = FloatEncoding._from_v1_1(obj.encoding)
        kwargs["size_in_bits"] = obj.size_in_bits
        kwargs["change_threshold"] = None  # Not supported in v1.1
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.FloatDataEncodingType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["default_calibrator"] = (
            Calibrator._from_v1_2(obj.default_calibrator)
            if obj.default_calibrator
            else None
        )
        kwargs["context_calibrators"] = (
            [
                ContextCalibrator._from_v1_2(c)
                for c in obj.context_calibrator_list.context_calibrator
            ]
            if obj.context_calibrator_list
            else []
        )
        kwargs["encoding"] = FloatEncoding._from_v1_2(obj.encoding)
        kwargs["size_in_bits"] = obj.size_in_bits
        kwargs["change_threshold"] = obj.change_threshold
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.FloatDataEncodingType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["default_calibrator"] = (
            Calibrator._from_v1_3(obj.default_calibrator)
            if obj.default_calibrator
            else None
        )
        kwargs["context_calibrators"] = (
            [
                ContextCalibrator._from_v1_3(c)
                for c in obj.context_calibrator_list.context_calibrator
            ]
            if obj.context_calibrator_list
            else []
        )
        kwargs["encoding"] = FloatEncoding._from_v1_3(obj.encoding)
        kwargs["size_in_bits"] = obj.size_in_bits
        kwargs["change_threshold"] = obj.change_threshold
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="change_threshold",
            current_value=self.change_threshold,
            target_version=XtceVersion.V1_1,
            policy=policy,
        )

        kwargs = super()._to_v1_1_kwargs(policy, self.size_in_bits)
        kwargs["default_calibrator"] = (
            self.default_calibrator._to_v1_1(policy)
            if self.default_calibrator
            else None
        )
        kwargs["context_calibrator_list"] = self._build_set(
            items=self.context_calibrators,
            set_class=xtce_1_1.FloatDataEncodingType.ContextCalibratorList,
            kwarg_name="context_calibrator",
            converter=lambda c: c._to_v1_1(policy),
        )
        kwargs["encoding"] = self.encoding._to_v1_1(policy)
        kwargs["size_in_bits"] = self.size_in_bits
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["default_calibrator"] = (
            self.default_calibrator._to_v1_2(policy)
            if self.default_calibrator
            else None
        )
        kwargs["context_calibrator_list"] = self._build_set(
            items=self.context_calibrators,
            set_class=xtce_1_2.ContextCalibratorListType,
            kwarg_name="context_calibrator",
            converter=lambda c: c._to_v1_2(policy),
        )
        kwargs["encoding"] = self.encoding._to_v1_2(policy)
        kwargs["size_in_bits"] = self.size_in_bits
        kwargs["change_threshold"] = self.change_threshold
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["default_calibrator"] = (
            self.default_calibrator._to_v1_3(policy)
            if self.default_calibrator
            else None
        )
        kwargs["context_calibrator_list"] = self._build_set(
            items=self.context_calibrators,
            set_class=xtce_1_3.ContextCalibratorListType,
            kwarg_name="context_calibrator",
            converter=lambda c: c._to_v1_3(policy),
        )
        kwargs["encoding"] = self.encoding._to_v1_3(policy)
        kwargs["size_in_bits"] = self.size_in_bits
        kwargs["change_threshold"] = self.change_threshold
        return kwargs


class StringDataEncoding(DataEncoding):
    """Define how a string value is encoded.

    Can either be fixed or variable length. The rules are as follows:

    Fixed length:
    - `allocation_size`: Should be set to `int`.
    - `max_size_in_bits`: Unused.
    - `termination_character`: Optional to indicate the end of the string within the
        allocated space.
    - `leading_size`: Optional to indicate the length of the string within the allocated
        space.

    Variable length:
    - `allocation_size`: Should be set to `None`, `DynamicValue`, or
        `DiscreteLookupList`.
    - `max_size_in_bits`: Required to define the maximum size of the string.
    - `termination_character` or `leading_size`: Required to determine the end of the
        string.

    """

    # TODO fix rules

    allocation_size: int | DynamicValue | DiscreteLookupList | None = None
    """Define the allocation size for the string value.

    - `int`: A fixed allocation size for the string value.
    - `DynamicValue` or `DiscreteLookupList`: A dynamic allocation size determined at
        runtime.
    - `None`: The size is determined by the string content itself, either with a leading
        size or a termination character.

    """

    max_size_in_bits: int | None = None
    """Define the maximum size in bits for the string value.

    Required if using a dynamic allocation size for the string value (`DynamicValue`,
    `DiscreteLookupList`, or `None`).

    """

    termination_character: bytes | None = None
    """Define the termination character for the string value.

    If this is a fixed length string, the termination character is used to determine the
    end of the string within the allocated space.

    If this is a variable length string, the termination character is used to determine
    the end of the string when reading the data.

    """

    leading_size: LeadingSize | None = None
    """Define the leading size for the string value.

    If this is a fixed length string, the leading size is used to determine the actual
    length of the string within the allocated space.

    If this is a variable length string, the leading size is used to determine the
    length of the string when reading the data.

    """

    encoding: StringEncoding = StringEncoding.UTF_8
    """The raw encoding of the string value."""

    # TODO validate size in bits is valid for encoding type

    _v1_1_type = xtce_1_1.StringDataEncodingType
    _v1_2_type = xtce_1_2.StringDataEncodingType
    _v1_3_type = xtce_1_3.StringDataEncodingType

    @model_validator(mode="after")
    def validate_string_type(self) -> Self:
        """Validate the correct attributes are set based on the string type (fixed or
        variable length).
        """
        if self.termination_character is not None and self.leading_size is not None:
            raise ValueError(
                "cannot have both a termination_character and a leading_size"
            )
        is_variable_string = not isinstance(self.allocation_size, int)
        if is_variable_string:
            if self.termination_character is None and self.leading_size is None:
                raise ValueError(
                    "variable strings must define either a termination_character or a "
                    "leading_size"
                )
        return self

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.StringDataEncodingType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["max_size_in_bits"] = None
        match unwrap(obj.size_in_bits.choice):
            case xtce_1_1.IntegerValueType() as val:
                kwargs["allocation_size"] = parse_integer_value_v1_1(val)
                kwargs["termination_character"] = None
                kwargs["leading_size"] = None
            case bytes() as val:
                kwargs["allocation_size"] = None
                kwargs["termination_character"] = val
                kwargs["leading_size"] = None
            case xtce_1_1.StringDataEncodingType.SizeInBits.LeadingSize() as val:
                kwargs["allocation_size"] = None
                kwargs["termination_character"] = None
                kwargs["leading_size"] = LeadingSize(
                    size_in_bits=val.size_in_bits_of_size_tag
                )
            case _:
                assert_never(obj.size_in_bits.choice)
        kwargs["encoding"] = StringEncoding._from_v1_1(obj.encoding)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.StringDataEncodingType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        match obj.choice:
            case xtce_1_2.SizeInBitsType() as size_in_bits:
                kwargs["allocation_size"] = size_in_bits.fixed.fixed_value
                kwargs["max_size_in_bits"] = None
                if size_in_bits.leading_size is not None:
                    kwargs["leading_size"] = LeadingSize._from_v1_2(
                        size_in_bits.leading_size
                    )
                    kwargs["termination_character"] = None
                else:
                    kwargs["leading_size"] = None
                    kwargs["termination_character"] = size_in_bits.termination_char
            case xtce_1_2.VariableStringType() as variable_string:
                kwargs["max_size_in_bits"] = variable_string.max_size_in_bits
                match variable_string.choice:
                    case xtce_1_2.DynamicValueType() as val:
                        kwargs["allocation_size"] = DynamicValue._from_v1_2(val)
                    case xtce_1_2.DiscreteLookupListType() as val:
                        kwargs["allocation_size"] = DiscreteLookupList._from_v1_2(val)
                    case None:
                        kwargs["allocation_size"] = None
                    case _:
                        assert_never(variable_string.choice)
                if variable_string.leading_size is not None:
                    kwargs["leading_size"] = LeadingSize._from_v1_2(
                        variable_string.leading_size
                    )
                    kwargs["termination_character"] = None
                else:
                    kwargs["leading_size"] = None
                    kwargs["termination_character"] = variable_string.termination_char
            case None:
                pass  # Not possible due to XSD validation
            case _:
                assert_never(obj.choice)
        kwargs["encoding"] = StringEncoding._from_v1_2(obj.encoding)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.StringDataEncodingType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        match obj.choice:
            case xtce_1_3.SizeInBitsType() as size_in_bits:
                kwargs["allocation_size"] = size_in_bits.fixed.fixed_value
                kwargs["max_size_in_bits"] = None
                if size_in_bits.leading_size is not None:
                    kwargs["leading_size"] = LeadingSize._from_v1_3(
                        size_in_bits.leading_size
                    )
                    kwargs["termination_character"] = None
                else:
                    kwargs["leading_size"] = None
                    kwargs["termination_character"] = size_in_bits.termination_char
            case xtce_1_3.VariableStringType() as variable_string:
                kwargs["max_size_in_bits"] = variable_string.max_size_in_bits
                match variable_string.choice:
                    case xtce_1_3.DynamicValueType() as val:
                        kwargs["allocation_size"] = DynamicValue._from_v1_3(val)
                    case xtce_1_3.DiscreteLookupListType() as val:
                        kwargs["allocation_size"] = DiscreteLookupList._from_v1_3(val)
                    case None:
                        kwargs["allocation_size"] = None
                    case _:
                        assert_never(variable_string.choice)
                match variable_string.choice_1:
                    case xtce_1_3.LeadingSizeType() as val:
                        kwargs["leading_size"] = LeadingSize._from_v1_3(val)
                        kwargs["termination_character"] = None
                    case bytes() as val:
                        kwargs["leading_size"] = None
                        kwargs["termination_character"] = val
                    case None:
                        kwargs["leading_size"] = None
                        kwargs["termination_character"] = None
                    case _:
                        assert_never(variable_string.choice_1)
            case None:
                pass  # Not possible due to XSD validation
            case _:
                assert_never(obj.choice)
        kwargs["encoding"] = StringEncoding._from_v1_3(obj.encoding)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="max_size_in_bits",
            current_value=self.max_size_in_bits,
            target_version=XtceVersion.V1_1,
            policy=policy,
        )

        kwargs = super()._to_v1_1_kwargs(policy)
        if self.allocation_size is not None:
            # This is a fixed string
            self._enforce_unsupported_field(
                field_name="termination_character (on fixed-allocation strings)",
                current_value=self.termination_character,
                target_version=XtceVersion.V1_1,
                policy=policy,
            )
            self._enforce_unsupported_field(
                field_name="leading_size (on fixed-allocation strings)",
                current_value=self.leading_size,
                target_version=XtceVersion.V1_1,
                policy=policy,
            )
            kwargs["size_in_bits"] = xtce_1_1.StringDataEncodingType.SizeInBits(
                choice=pack_integer_value_v1_1(self.allocation_size, policy)
            )
        else:
            # This is a variable string
            if self.termination_character is not None:
                kwargs["size_in_bits"] = xtce_1_1.StringDataEncodingType.SizeInBits(
                    choice=self.termination_character
                )
            elif self.leading_size is not None:
                kwargs["size_in_bits"] = xtce_1_1.StringDataEncodingType.SizeInBits(
                    choice=xtce_1_1.StringDataEncodingType.SizeInBits.LeadingSize(
                        size_in_bits_of_size_tag=self.leading_size.size_in_bits
                    )
                )
            else:
                raise ValueError(
                    "Variable strings must define a termination character or leading size."
                )
        kwargs["encoding"] = self.encoding._to_v1_1(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.2 does not allow allocation_size to be unset
        self._enforce_restricted_type(
            field_name="allocation_size",
            current_value=self.allocation_size,
            allowed_types=(int, DynamicValue, DiscreteLookupList),
            target_version=XtceVersion.V1_2,
            policy=policy,
            require_match=True,
        )

        kwargs = super()._to_v1_2_kwargs(policy)
        if isinstance(self.allocation_size, int):
            # This is a fixed string
            kwargs["choice"] = xtce_1_2.SizeInBitsType(
                fixed=xtce_1_2.SizeInBitsType.Fixed(fixed_value=self.allocation_size),
                termination_char=self.termination_character,
                leading_size=(
                    self.leading_size._to_v1_2(policy)
                    if self.leading_size is not None
                    else None
                ),
            )
        else:
            # This is a variable string
            max_size_in_bits = self._enforce_required_field(
                field_name="max_size_in_bits",
                current_value=self.max_size_in_bits,
                target_version=XtceVersion.V1_2,
                policy=policy,
            )
            kwargs["choice"] = xtce_1_2.VariableStringType(
                choice=unwrap(self.allocation_size)._to_v1_2(policy),
                leading_size=(
                    self.leading_size._to_v1_2(policy)
                    if self.leading_size is not None
                    else None
                ),
                termination_char=self.termination_character,
                max_size_in_bits=max_size_in_bits,
            )
        kwargs["encoding"] = self.encoding._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        if isinstance(self.allocation_size, int):
            # This is a fixed string
            kwargs["choice"] = xtce_1_3.SizeInBitsType(
                fixed=xtce_1_3.SizeInBitsType.Fixed(fixed_value=self.allocation_size),
                termination_char=self.termination_character,
                leading_size=(
                    self.leading_size._to_v1_3(policy)
                    if self.leading_size is not None
                    else None
                ),
            )
        else:
            # This is a variable string
            max_size_in_bits = self._enforce_required_field(
                field_name="max_size_in_bits",
                current_value=self.max_size_in_bits,
                target_version=XtceVersion.V1_3,
                policy=policy,
            )
            if self.leading_size is not None:
                content_choice = self.leading_size._to_v1_3(policy)
            else:
                content_choice = self.termination_character or b"\x00"
            kwargs["choice"] = xtce_1_3.VariableStringType(
                choice=(
                    self.allocation_size._to_v1_3(policy)
                    if self.allocation_size is not None
                    else None
                ),
                choice_1=content_choice,
                max_size_in_bits=max_size_in_bits,
            )
        kwargs["encoding"] = self.encoding._to_v1_3(policy)
        return kwargs


class ArgumentStringDataEncoding(DataEncoding):
    """Define how a string value is encoded.

    Can either be fixed or variable length. The rules are as follows:

    """

    # TODO add rules

    allocation_size: int | ArgumentDynamicValue | ArgumentDiscreteLookupList | None = (
        None
    )
    """Define the allocation size for the string value.

    - `int`: A fixed allocation size for the string value.
    - `ArgumentDynamicValue` or `ArgumentDiscreteLookupList`: A dynamic allocation size
        determined at runtime.
    - `None`: The size is determined by the string content itself, either with a leading
        size or a termination character.

    """

    max_size_in_bits: int | None = None
    """Define the maximum size in bits for the string value.

    Required if using a dynamic allocation size for the string value
    (`ArgumentDynamicValue`, `ArgumentDiscreteLookupList`, or `None`).

    """

    termination_character: bytes | None = None
    """Define the termination character for the string value.

    If this is a fixed length string, the termination character is used to determine the
    end of the string within the allocated space.

    If this is a variable length string, the termination character is used to determine
    the end of the string when reading the data.

    """

    leading_size: LeadingSize | None = None
    """Define the leading size for the string value.

    If this is a fixed length string, the leading size is used to determine the actual
    length of the string within the allocated space.

    If this is a variable length string, the leading size is used to determine the
    length of the string when reading the data.

    """

    encoding: StringEncoding = StringEncoding.UTF_8
    """The raw encoding of the string value."""

    # TODO validate size in bits is valid for encoding type

    _v1_1_type = xtce_1_1.StringDataEncodingType
    _v1_2_type = xtce_1_2.ArgumentStringDataEncodingType
    _v1_3_type = xtce_1_3.ArgumentStringDataEncodingType

    @model_validator(mode="after")
    def validate_string_type(self) -> Self:
        """Validate the correct attributes are set based on the string type (fixed or
        variable length).
        """
        if self.termination_character is not None and self.leading_size is not None:
            raise ValueError(
                "cannot have both a termination_character and a leading_size"
            )
        is_variable_string = not isinstance(self.allocation_size, int)
        if is_variable_string:
            if self.termination_character is None and self.leading_size is None:
                raise ValueError(
                    "variable strings must define either a termination_character or a "
                    "leading_size"
                )
        return self

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.StringDataEncodingType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["max_size_in_bits"] = None
        match unwrap(obj.size_in_bits.choice):
            case xtce_1_1.IntegerValueType() as val:
                kwargs["allocation_size"] = parse_argument_integer_value_v1_1(val)
                kwargs["termination_character"] = None
                kwargs["leading_size"] = None
            case bytes() as val:
                kwargs["allocation_size"] = None
                kwargs["termination_character"] = val
                kwargs["leading_size"] = None
            case xtce_1_1.StringDataEncodingType.SizeInBits.LeadingSize() as val:
                kwargs["allocation_size"] = None
                kwargs["termination_character"] = None
                kwargs["leading_size"] = LeadingSize(
                    size_in_bits=val.size_in_bits_of_size_tag
                )
            case _:
                assert_never(obj.size_in_bits.choice)
        kwargs["encoding"] = StringEncoding._from_v1_1(obj.encoding)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentStringDataEncodingType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        match obj.choice:
            case xtce_1_2.SizeInBitsType() as size_in_bits:
                kwargs["allocation_size"] = size_in_bits.fixed.fixed_value
                kwargs["max_size_in_bits"] = None
                if size_in_bits.leading_size is not None:
                    kwargs["leading_size"] = LeadingSize._from_v1_2(
                        size_in_bits.leading_size
                    )
                    kwargs["termination_character"] = None
                else:
                    kwargs["leading_size"] = None
                    kwargs["termination_character"] = size_in_bits.termination_char
            case xtce_1_2.ArgumentVariableStringType() as variable_string:
                kwargs["max_size_in_bits"] = variable_string.max_size_in_bits
                match variable_string.choice:
                    case xtce_1_2.ArgumentDynamicValueType() as val:
                        kwargs["allocation_size"] = ArgumentDynamicValue._from_v1_2(val)
                    case xtce_1_2.ArgumentDiscreteLookupListType() as val:
                        kwargs["allocation_size"] = (
                            ArgumentDiscreteLookupList._from_v1_2(val)
                        )
                    case None:
                        kwargs["allocation_size"] = None
                    case _:
                        assert_never(variable_string.choice)
                if variable_string.leading_size is not None:
                    kwargs["leading_size"] = LeadingSize._from_v1_2(
                        variable_string.leading_size
                    )
                    kwargs["termination_character"] = None
                else:
                    kwargs["leading_size"] = None
                    kwargs["termination_character"] = variable_string.termination_char
            case None:
                pass  # Not possible due to XSD validation
            case _:
                assert_never(obj.choice)
        kwargs["encoding"] = StringEncoding._from_v1_2(obj.encoding)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentStringDataEncodingType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        match obj.choice:
            case xtce_1_3.SizeInBitsType() as size_in_bits:
                kwargs["allocation_size"] = size_in_bits.fixed.fixed_value
                kwargs["max_size_in_bits"] = None
                if size_in_bits.leading_size is not None:
                    kwargs["leading_size"] = LeadingSize._from_v1_3(
                        size_in_bits.leading_size
                    )
                    kwargs["termination_character"] = None
                else:
                    kwargs["leading_size"] = None
                    kwargs["termination_character"] = size_in_bits.termination_char
            case xtce_1_3.ArgumentVariableStringType() as variable_string:
                kwargs["max_size_in_bits"] = variable_string.max_size_in_bits
                match variable_string.choice:
                    case xtce_1_3.ArgumentDynamicValueType() as val:
                        kwargs["allocation_size"] = ArgumentDynamicValue._from_v1_3(val)
                    case xtce_1_3.ArgumentDiscreteLookupListType() as val:
                        kwargs["allocation_size"] = (
                            ArgumentDiscreteLookupList._from_v1_3(val)
                        )
                    case None:
                        kwargs["allocation_size"] = None
                    case _:
                        assert_never(variable_string.choice)
                match variable_string.choice_1:
                    case xtce_1_3.LeadingSizeType() as val:
                        kwargs["leading_size"] = LeadingSize._from_v1_3(val)
                        kwargs["termination_character"] = None
                    case bytes() as val:
                        kwargs["leading_size"] = None
                        kwargs["termination_character"] = val
                    case None:
                        kwargs["leading_size"] = None
                        kwargs["termination_character"] = None
                    case _:
                        assert_never(variable_string.choice_1)
            case None:
                pass  # Not possible due to XSD validation
            case _:
                assert_never(obj.choice)
        kwargs["encoding"] = StringEncoding._from_v1_3(obj.encoding)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="max_size_in_bits",
            current_value=self.max_size_in_bits,
            target_version=XtceVersion.V1_1,
            policy=policy,
        )

        kwargs = super()._to_v1_1_kwargs(policy)
        if self.allocation_size is not None:
            # This is a fixed string
            self._enforce_unsupported_field(
                field_name="termination_character (on fixed-allocation strings)",
                current_value=self.termination_character,
                target_version=XtceVersion.V1_1,
                policy=policy,
            )
            self._enforce_unsupported_field(
                field_name="leading_size (on fixed-allocation strings)",
                current_value=self.leading_size,
                target_version=XtceVersion.V1_1,
                policy=policy,
            )
            kwargs["size_in_bits"] = xtce_1_1.StringDataEncodingType.SizeInBits(
                choice=pack_argument_integer_value_v1_1(self.allocation_size, policy)
            )
        else:
            # This is a variable string
            if self.termination_character is not None:
                kwargs["size_in_bits"] = xtce_1_1.StringDataEncodingType.SizeInBits(
                    choice=self.termination_character
                )
            elif self.leading_size is not None:
                kwargs["size_in_bits"] = xtce_1_1.StringDataEncodingType.SizeInBits(
                    choice=xtce_1_1.StringDataEncodingType.SizeInBits.LeadingSize(
                        size_in_bits_of_size_tag=self.leading_size.size_in_bits
                    )
                )
            else:
                raise ValueError(
                    "Variable strings must define a termination character or leading size."
                )
        kwargs["encoding"] = self.encoding._to_v1_1(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.2 does not allow allocation_size to be unset
        self._enforce_restricted_type(
            field_name="allocation_size",
            current_value=self.allocation_size,
            allowed_types=(int, ArgumentDynamicValue, ArgumentDiscreteLookupList),
            target_version=XtceVersion.V1_2,
            policy=policy,
            require_match=True,
        )

        kwargs = super()._to_v1_2_kwargs(policy)
        if isinstance(self.allocation_size, int):
            # This is a fixed string
            kwargs["choice"] = xtce_1_2.SizeInBitsType(
                fixed=xtce_1_2.SizeInBitsType.Fixed(fixed_value=self.allocation_size),
                termination_char=self.termination_character,
                leading_size=(
                    self.leading_size._to_v1_2(policy)
                    if self.leading_size is not None
                    else None
                ),
            )
        else:
            # This is a variable string
            max_size_in_bits = self._enforce_required_field(
                field_name="max_size_in_bits",
                current_value=self.max_size_in_bits,
                target_version=XtceVersion.V1_2,
                policy=policy,
            )
            kwargs["choice"] = xtce_1_2.ArgumentVariableStringType(
                choice=unwrap(self.allocation_size)._to_v1_2(policy),
                leading_size=(
                    self.leading_size._to_v1_2(policy)
                    if self.leading_size is not None
                    else None
                ),
                termination_char=self.termination_character,
                max_size_in_bits=max_size_in_bits,
            )
        kwargs["encoding"] = self.encoding._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        if isinstance(self.allocation_size, int):
            # This is a fixed string
            kwargs["choice"] = xtce_1_3.SizeInBitsType(
                fixed=xtce_1_3.SizeInBitsType.Fixed(fixed_value=self.allocation_size),
                termination_char=self.termination_character,
                leading_size=(
                    self.leading_size._to_v1_3(policy)
                    if self.leading_size is not None
                    else None
                ),
            )
        else:
            # This is a variable string
            max_size_in_bits = self._enforce_required_field(
                field_name="max_size_in_bits",
                current_value=self.max_size_in_bits,
                target_version=XtceVersion.V1_3,
                policy=policy,
            )
            if self.leading_size is not None:
                content_choice = self.leading_size._to_v1_3(policy)
            else:
                content_choice = self.termination_character or b"\x00"
            kwargs["choice"] = xtce_1_3.ArgumentVariableStringType(
                choice=(
                    self.allocation_size._to_v1_3(policy)
                    if self.allocation_size is not None
                    else None
                ),
                choice_1=content_choice,
                max_size_in_bits=max_size_in_bits,
            )
        kwargs["encoding"] = self.encoding._to_v1_3(policy)
        return kwargs


class BinaryDataEncoding(DataEncoding):
    """Describes how a binary value is sent or received from some device."""

    size_in_bits: Annotated[int, Field(ge=1)] | DynamicValue | DiscreteLookupList = (
        Field(...)
    )
    """Number of bits to use for the raw encoding."""

    from_binary_transform_algorithm: InputAlgorithm | None = None
    """Used to convert from binary data to an application data type."""

    to_binary_transform_algorithm: InputAlgorithm | None = None
    """Used to convert to binary data from an application data type."""

    _v1_1_type = xtce_1_1.BinaryDataEncodingType
    _v1_2_type = xtce_1_2.BinaryDataEncodingType
    _v1_3_type = xtce_1_3.BinaryDataEncodingType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.BinaryDataEncodingType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["size_in_bits"] = parse_integer_value_v1_1(obj.size_in_bits)
        kwargs["from_binary_transform_algorithm"] = (
            InputAlgorithm._from_v1_1(obj.from_binary_transform_algorithm)
            if obj.from_binary_transform_algorithm is not None
            else None
        )
        kwargs["to_binary_transform_algorithm"] = (
            InputAlgorithm._from_v1_1(obj.to_binary_transform_algorithm)
            if obj.to_binary_transform_algorithm is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.BinaryDataEncodingType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["size_in_bits"] = parse_integer_value_v1_2(obj.size_in_bits)
        kwargs["from_binary_transform_algorithm"] = (
            InputAlgorithm._from_v1_2(obj.from_binary_transform_algorithm)
            if obj.from_binary_transform_algorithm is not None
            else None
        )
        kwargs["to_binary_transform_algorithm"] = (
            InputAlgorithm._from_v1_2(obj.to_binary_transform_algorithm)
            if obj.to_binary_transform_algorithm is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.BinaryDataEncodingType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
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

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["size_in_bits"] = pack_integer_value_v1_1(self.size_in_bits, policy)
        kwargs["from_binary_transform_algorithm"] = (
            self.from_binary_transform_algorithm._to_v1_1(policy)
            if self.from_binary_transform_algorithm is not None
            else None
        )
        kwargs["to_binary_transform_algorithm"] = (
            self.to_binary_transform_algorithm._to_v1_1(policy)
            if self.to_binary_transform_algorithm is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["size_in_bits"] = pack_integer_value_v1_2(self.size_in_bits, policy)
        kwargs["from_binary_transform_algorithm"] = (
            self.from_binary_transform_algorithm._to_v1_2(policy)
            if self.from_binary_transform_algorithm is not None
            else None
        )
        kwargs["to_binary_transform_algorithm"] = (
            self.to_binary_transform_algorithm._to_v1_2(policy)
            if self.to_binary_transform_algorithm is not None
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
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


class ArgumentBinaryDataEncoding(DataEncoding):
    """Describes how a binary value is sent to some device."""

    size_in_bits: (
        Annotated[int, Field(ge=1)] | ArgumentDynamicValue | ArgumentDiscreteLookupList
    ) = Field(...)
    """Number of bits to use for the raw encoding."""

    from_binary_transform_algorithm: ArgumentInputAlgorithm | None = None
    """Used to convert from binary data to an application data type."""

    to_binary_transform_algorithm: ArgumentInputAlgorithm | None = None
    """Used to convert to binary data from an application data type."""

    _v1_1_type = xtce_1_1.BinaryDataEncodingType
    _v1_2_type = xtce_1_2.ArgumentBinaryDataEncodingType
    _v1_3_type = xtce_1_3.ArgumentBinaryDataEncodingType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.BinaryDataEncodingType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["size_in_bits"] = parse_argument_integer_value_v1_1(obj.size_in_bits)
        kwargs["from_binary_transform_algorithm"] = (
            ArgumentInputAlgorithm._from_v1_1(obj.from_binary_transform_algorithm)
            if obj.from_binary_transform_algorithm is not None
            else None
        )
        kwargs["to_binary_transform_algorithm"] = (
            ArgumentInputAlgorithm._from_v1_1(obj.to_binary_transform_algorithm)
            if obj.to_binary_transform_algorithm is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentBinaryDataEncodingType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["size_in_bits"] = parse_argument_integer_value_v1_2(obj.size_in_bits)
        kwargs["from_binary_transform_algorithm"] = (
            ArgumentInputAlgorithm._from_v1_2(obj.from_binary_transform_algorithm)
            if obj.from_binary_transform_algorithm is not None
            else None
        )
        kwargs["to_binary_transform_algorithm"] = (
            ArgumentInputAlgorithm._from_v1_2(obj.to_binary_transform_algorithm)
            if obj.to_binary_transform_algorithm is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentBinaryDataEncodingType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["size_in_bits"] = parse_argument_integer_value_v1_3(obj.size_in_bits)
        kwargs["from_binary_transform_algorithm"] = (
            ArgumentInputAlgorithm._from_v1_3(obj.from_binary_transform_algorithm)
            if obj.from_binary_transform_algorithm is not None
            else None
        )
        kwargs["to_binary_transform_algorithm"] = (
            ArgumentInputAlgorithm._from_v1_3(obj.to_binary_transform_algorithm)
            if obj.to_binary_transform_algorithm is not None
            else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["size_in_bits"] = pack_argument_integer_value_v1_1(
            self.size_in_bits, policy
        )
        kwargs["from_binary_transform_algorithm"] = (
            self.from_binary_transform_algorithm._to_v1_1(policy)
            if self.from_binary_transform_algorithm is not None
            else None
        )
        kwargs["to_binary_transform_algorithm"] = (
            self.to_binary_transform_algorithm._to_v1_1(policy)
            if self.to_binary_transform_algorithm is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["size_in_bits"] = pack_argument_integer_value_v1_2(
            self.size_in_bits, policy
        )
        kwargs["from_binary_transform_algorithm"] = (
            self.from_binary_transform_algorithm._to_v1_2(policy)
            if self.from_binary_transform_algorithm is not None
            else None
        )
        kwargs["to_binary_transform_algorithm"] = (
            self.to_binary_transform_algorithm._to_v1_2(policy)
            if self.to_binary_transform_algorithm is not None
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["size_in_bits"] = pack_argument_integer_value_v1_3(
            self.size_in_bits, policy
        )
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


class TimeEncoding(XtceBaseModel):
    """Define the encoding of a time value."""

    encoding_type: (
        IntegerDataEncoding
        | FloatDataEncoding
        | StringDataEncoding
        | BinaryDataEncoding
    )
    units: TimeUnits = TimeUnits.SECONDS
    scale: float = 1.0
    offset: float = 0.0

    _v1_1_type = xtce_1_1.BaseTimeDataType.Encoding
    _v1_2_type = xtce_1_2.EncodingType
    _v1_3_type = xtce_1_3.EncodingType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.BaseTimeDataType.Encoding
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["encoding_type"] = (
            IntegerDataEncoding._from_v1_1(obj.choice)
            if isinstance(obj.choice, xtce_1_1.IntegerDataEncodingType)
            else FloatDataEncoding._from_v1_1(obj.choice)
            if isinstance(obj.choice, xtce_1_1.FloatDataEncodingType)
            else StringDataEncoding._from_v1_1(obj.choice)
            if isinstance(obj.choice, xtce_1_1.StringDataEncodingType)
            else BinaryDataEncoding._from_v1_1(obj.choice)
            if isinstance(obj.choice, xtce_1_1.BinaryDataEncodingType)
            else None
        )
        kwargs["units"] = TimeUnits._from_v1_1(obj.units)
        kwargs["scale"] = obj.scale
        kwargs["offset"] = obj.offset
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.EncodingType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["encoding_type"] = (
            IntegerDataEncoding._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.IntegerDataEncodingType)
            else FloatDataEncoding._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.FloatDataEncodingType)
            else StringDataEncoding._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.StringDataEncodingType)
            else BinaryDataEncoding._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.BinaryDataEncodingType)
            else None
        )
        kwargs["units"] = TimeUnits._from_v1_2(obj.units)
        kwargs["scale"] = obj.scale
        kwargs["offset"] = obj.offset
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.EncodingType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["encoding_type"] = (
            IntegerDataEncoding._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.IntegerDataEncodingType)
            else FloatDataEncoding._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.FloatDataEncodingType)
            else StringDataEncoding._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.StringDataEncodingType)
            else BinaryDataEncoding._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.BinaryDataEncodingType)
            else None
        )
        kwargs["units"] = TimeUnits._from_v1_3(obj.units)
        kwargs["scale"] = obj.scale
        kwargs["offset"] = obj.offset
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["choice"] = self.encoding_type._to_v1_1(policy)
        kwargs["units"] = self.units._to_v1_1(policy)
        kwargs["scale"] = self.scale
        kwargs["offset"] = self.offset
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = self.encoding_type._to_v1_2(policy)
        kwargs["units"] = self.units._to_v1_2(policy)
        kwargs["scale"] = self.scale
        kwargs["offset"] = self.offset
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = self.encoding_type._to_v1_3(policy)
        kwargs["units"] = self.units._to_v1_3(policy)
        kwargs["scale"] = self.scale
        kwargs["offset"] = self.offset
        return kwargs
