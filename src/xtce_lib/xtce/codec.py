"""Encoding/decoding models."""

from typing import Any, Literal, Self

from pydantic import Field

from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy, XtceUnsupportedError
from xtce_lib.generated import xtce_1_2, xtce_1_3

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
from .condition import ArgumentDiscreteLookupList, DiscreteLookupList
from .enum import (
    BitOrder,
    Endian,
    FloatEncoding,
    IntegerEncoding,
    StringEncoding,
    TimeUnits,
)
from .reference import ArgumentInstanceRef, ParameterInstanceRef


class DynamicValue(XtceBaseModel):
    """A value obtained by a reference to a parameter instance.

    The parameter value may be optionally adjusted by a linear function.

    """

    instance: ParameterInstanceRef
    """The parameter instance being referenced."""

    linear_adjustment: LinearAdjustment | None = None
    """An optional linear adjustment applied to the referenced parameter value."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.DynamicValueType) -> Self:
        return cls(
            instance=ParameterInstanceRef._from_v1_2(raw_obj.parameter_instance_ref),
            linear_adjustment=LinearAdjustment._from_v1_2(raw_obj.linear_adjustment)
            if raw_obj.linear_adjustment
            else None,
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.DynamicValueType) -> Self:
        return cls(
            instance=ParameterInstanceRef._from_v1_3(raw_obj.parameter_instance_ref),
            linear_adjustment=LinearAdjustment._from_v1_3(raw_obj.linear_adjustment)
            if raw_obj.linear_adjustment
            else None,
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.DynamicValueType:
        return xtce_1_2.DynamicValueType(
            parameter_instance_ref=self.instance._to_v1_2(policy),
            linear_adjustment=self.linear_adjustment._to_v1_2(policy)
            if self.linear_adjustment
            else None,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.DynamicValueType:
        return xtce_1_3.DynamicValueType(
            parameter_instance_ref=self.instance._to_v1_3(policy),
            linear_adjustment=self.linear_adjustment._to_v1_3(policy)
            if self.linear_adjustment
            else None,
        )


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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.ArgumentDynamicValueType) -> Self:
        if isinstance(raw_obj.choice, xtce_1_2.ArgumentInstanceRefType):
            instance = ArgumentInstanceRef._from_v1_2(raw_obj.choice)
        else:
            instance = ParameterInstanceRef._from_v1_2(unwrap(raw_obj.choice))

        return cls(
            instance=instance,
            linear_adjustment=LinearAdjustment._from_v1_2(raw_obj.linear_adjustment)
            if raw_obj.linear_adjustment
            else None,
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.ArgumentDynamicValueType) -> Self:
        if isinstance(raw_obj.choice, xtce_1_3.ArgumentInstanceRefType):
            instance = ArgumentInstanceRef._from_v1_3(raw_obj.choice)
        else:
            instance = ParameterInstanceRef._from_v1_3(unwrap(raw_obj.choice))

        return cls(
            instance=instance,
            linear_adjustment=LinearAdjustment._from_v1_3(raw_obj.linear_adjustment)
            if raw_obj.linear_adjustment
            else None,
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ArgumentDynamicValueType:
        return xtce_1_2.ArgumentDynamicValueType(
            choice=self.instance._to_v1_2(policy),
            linear_adjustment=self.linear_adjustment._to_v1_2(policy)
            if self.linear_adjustment
            else None,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ArgumentDynamicValueType:
        return xtce_1_3.ArgumentDynamicValueType(
            choice=self.instance._to_v1_3(policy),
            linear_adjustment=self.linear_adjustment._to_v1_3(policy)
            if self.linear_adjustment
            else None,
        )


class LeadingSize(XtceBaseModel):
    size_in_bits_of_size_tag: int = Field(default=16, ge=1)


class TerminationCharacter(XtceBaseModel):
    character: bytes = Field(default=b"\x00")
    # TODO make sure this matches xsd def, it doesn't exist in xsdata generated models because it gets obfuscated for some reason


class VariableString(XtceBaseModel):
    """A variable string whose length may change between samples."""

    length_source: DynamicValue | DiscreteLookupList | None = Field(default=None)
    """The source of the length value, either from a parameter instance or a lookup
    table.
    """

    string_boundary: LeadingSize | TerminationCharacter
    """The method used to determine the end of the string, either by a leading size or a
    termination character.
    """

    max_size_in_bits: int = Field(..., ge=1)
    """The upper bound of the size of this string data type so that the implementation
    can reserve/allocate enough memory to capture all reported instances of the
    string.
    """


class ArgumentVariableString(XtceBaseModel):
    length_source: ArgumentDynamicValue | ArgumentDiscreteLookupList | None = Field(
        default=None
    )
    string_boundary: LeadingSize | TerminationCharacter
    max_size_in_bits: int = Field(..., ge=1)


class DataEncoding(XtceBaseModel):
    """Describes how a particular piece of data is sent or received from some device."""

    error_detect_correct: list[Checksum | CRC | XOR | Parity] | None = Field(
        default=None
    )
    """DEPRECATED: Use the ErrorDetectCorrect element in the container elements
    instead.
    """

    # TODO update reference to the correct element or if 1.1 or 1.2 support this

    bit_order: BitOrder = Field(default=BitOrder.MOST_SIGNIFICANT_BIT_FIRST)
    """The bit order of the encoded value."""

    byte_order: Endian | list[int] = Field(
        default=Endian.BIG,
        examples=[Endian.BIG, Endian.LITTLE, [3, 2, 1, 0], [0, 1, 2, 3]],
    )
    """The endiannes of the encoded value.

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


class IntegerDataEncoding(DataEncoding):
    """Describes how an integer value is sent or received from some device."""

    default_calibrator: Calibrator | None = Field(default=None)
    """Calibrator to be applied to the raw uncalibrated value to arrive at the
    engineering/calibrated value when no context calibrators are provided or evaluate to
    true, based on their match criteria.
    """

    context_calibrators: list[ContextCalibrator] = Field(default_factory=list)
    """Calibrator to be applied to the raw uncalibrated value to arrive at the
    engineering/calibrated value when the match criteria evaluates to true.

    The first in the list to match takes precedence.

    """

    encoding: IntegerEncoding = Field(default=IntegerEncoding.UNSIGNED)
    """The raw encoding of the integer value."""

    size_in_bits: int = Field(default=8, ge=1, examples=[8, 16, 32, 64])
    """Number of bits to use for the raw encoding."""

    # TODO add valid bit sizes and associated encodings in docstring

    change_threshold: int | None = Field(default=None, ge=0)
    """Used to inform systems of the minimum change in value that is significant.

    This is used by some systems to limit the telemetry processing and/or recording
    requirements, such as for an analog-to-digital converter that dithers in the least
    significant bit. If the value is unspecified or zero, any change is significant.

    """

    # TODO validate size in bits is valid for encoding type
    # TODO maybe require default calibrator if context calibrators are provided?


class FloatDataEncoding(DataEncoding):
    """Describes how a floating point value is sent or received from some device."""

    default_calibrator: Calibrator | None = Field(default=None)
    """Calibrator to be applied to the raw uncalibrated value to arrive at the
    engineering/calibrated value when no context calibrators are provided or evaluate to
    true, based on their match criteria.
    """

    context_calibrators: list[ContextCalibrator] = Field(default_factory=list)
    """Calibrator to be applied to the raw uncalibrated value to arrive at the
    engineering/calibrated value when the match criteria evaluates to true.

    The first in the list to match takes precedence.

    """

    encoding: FloatEncoding = Field(default=FloatEncoding.IEEE754_1985)
    """The raw encoding of the float value."""

    size_in_bits: Literal[16, 32, 40, 48, 64, 80, 128] = Field(default=32)
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

    change_threshold: float | None = Field(default=None)
    """Used to inform systems of the minimum change in value that is significant.

    This is used by some systems to limit the telemetry processing and/or recording
    requirements, such as for an analog-to-digital converter that dithers in the least
    significant bit. If the value is unspecified or zero, any change is significant.

    """

    # TODO validate size in bits is valid for encoding type


class StringDataEncoding(DataEncoding):
    """Describes how a string value is sent or received from some device."""

    size_in_bits: int | VariableString = Field(..., ge=1)
    """Number of bits to use for the raw encoding.

    Can either be an integer representing a fixed size, or a variable length represented
    by a dynamic value, leading size, termination character.

    """

    encoding: StringEncoding = Field(default=StringEncoding.UTF_8)
    """The raw encoding of the string value."""

    # TODO validate size in bits is valid for encoding type


class ArgumentStringDataEncoding(DataEncoding):
    size_in_bits: int | ArgumentVariableString = Field(..., ge=1)
    encoding: StringEncoding = Field(default=StringEncoding.UTF_8)


class BinaryDataEncoding(DataEncoding):
    """Describes how a binary value is sent or received from some device."""

    size_in_bits: int | DynamicValue | DiscreteLookupList = Field(..., ge=1)
    """Number of bits to use for the raw encoding."""

    from_binary_transform_algorithm: InputAlgorithm | None = Field(default=None)
    """Used to convert from binary data to an application data type."""

    to_binary_transform_algorithm: InputAlgorithm | None = Field(default=None)
    """Used to convert to binary data from an application data type."""


class ArgumentBinaryDataEncoding(DataEncoding):
    size_in_bits: int | ArgumentDynamicValue | ArgumentDiscreteLookupList | None = (
        Field(default=None, ge=1)
    )
    from_binary_transform_algorithm: ArgumentInputAlgorithm | None = Field(default=None)
    to_binary_transform_algorithm: ArgumentInputAlgorithm | None = Field(default=None)


class TimeEncoding(XtceBaseModel):
    encoding_type: (
        IntegerDataEncoding
        | FloatDataEncoding
        | StringDataEncoding
        | BinaryDataEncoding
        | None
    ) = Field(default=None)
    units: TimeUnits = Field(default=TimeUnits.SECONDS)
    scale: float = Field(default=1.0)
    offset: float = Field(default=0.0)
