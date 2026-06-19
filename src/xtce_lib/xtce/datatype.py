"""Data type models."""

import datetime
from typing import Literal

from pydantic import Field

from ._base import XtceBaseModel
from .codec import (
    ArgumentBinaryDataEncoding,
    ArgumentStringDataEncoding,
    BinaryDataEncoding,
    FloatDataEncoding,
    IntegerDataEncoding,
    StringDataEncoding,
    TimeEncoding,
)
from .common import NameDescriptionBase
from .enum import FloatingPointNotation, Radix, UnitForm
from .range import IntegerRange, ValidFloatRange, ValidIntegerRange
from .time import ReferenceTime


class Unit(XtceBaseModel):
    """Describe the exponent, factor, form, and description for a unit."""

    # TODO maybe move to a different module
    # TODO maybe add property that builds the unit text

    unit: str = Field(..., examples=["m/s^2", "V", "byte"])
    """The unit text content."""

    factor: str = Field(default="1", examples=["1", "2", "0.5"])
    """Optional attribute used in conjunction with the "power" attribute where some
    programs choose to specify the unit definition with these machine processable
    algebraic features.

    For example, a unit text of "meters" may have a "factor" attribute of 2, resulting
    "2 times meters" as the actual unit. This is not commonly used. The most common
    method for "2 times meters" is to use the str 'unit' attribute in a form like "2*m".

    """

    power: float = Field(default=1.0, examples=[1.0, 2.0, -1.0])
    """Optional attribute used in conjunction with the "factor" attribute where some
    programs choose to specify the unit definition with these machine processable
    algebraic features.

    For example, a unit text of "meters" may have a "power" attribute of 2, resulting
    "meters squared" as the actual unit. This is not commonly used. The most common
    method for "meters squared" is to use the str 'unit' attribute in a form like "m^2".

    """

    form: UnitForm = Field(default=UnitForm.CALIBRATED)
    """The default value "calibrated" is most common practice to specify units at the
    engineering/calibrated value, it is possible to specify an additional Unit element
    for the raw/uncalibrated value.
    """

    description: str | None = Field(
        default=None,
        examples=[
            "meters per second squared is of a property of acceleration.",
            "voltage is of a property of electric potential difference.",
            "represents the length of a buffer in bytes.",
        ],
    )
    """A description of the unit, which may be for expanded human readability or for
    specification of the nature/property of the unit.
    """


class BaseData(NameDescriptionBase):
    """An abstract schema type used by within the schema to derive the other
    simple/primitive engineering form data types.
    """

    units: list[Unit] = Field(default_factory=list)
    """When appropriate, describe the units of measure that are represented by this
    parameter value.
    """

    # TODO validate that there aren't duplicate unit forms

    encoding_type: (
        IntegerDataEncoding
        | FloatDataEncoding
        | StringDataEncoding
        | BinaryDataEncoding
        | None
    ) = Field(...)
    """Optional encoding information for this data type.

    This is only necessary if this data type is telemetered in some form. Local
    variables and derived typically do not require encoding.

    """

    base_type: str | None = Field(
        default=None, pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )
    """Used to derive one Data Type from another - will inherit all the attributes from the baseType any of which may be redefined in this type definition."""


class ArgumentBaseData(NameDescriptionBase):
    units: list[Unit] = Field(default_factory=list)
    encoding_type: (
        IntegerDataEncoding
        | FloatDataEncoding
        | ArgumentStringDataEncoding
        | ArgumentBinaryDataEncoding
        | None
    ) = Field(...)
    base_type: str | None = Field(
        default=None, pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )


class NumberFormat(XtceBaseModel):
    number_base: Radix = Field(default=Radix.DECIMAL)
    minimum_fraction_digits: int = Field(default=0, ge=0)
    maximum_fraction_digits: int | None = Field(default=None, ge=0)
    minimum_integer_digits: int = Field(default=1, ge=0)
    maximum_integer_digits: int | None = Field(default=None, ge=0)
    negative_suffix: str = Field(default="")
    positive_suffix: str = Field(default="")
    negative_prefix: str = Field(default="-")
    positive_prefix: str = Field(default="")
    show_thousands_grouping: bool = Field(default=False)
    notation: FloatingPointNotation = Field(default=FloatingPointNotation.NORMAL)


class ToString(XtceBaseModel):
    number_format: NumberFormat = Field(...)


class IntegerData(BaseData):
    to_string: ToString | None = Field(default=None)
    valid_range: ValidIntegerRange | None = Field(default=None)
    initial_value: int | None = Field(default=None)
    size_in_bits: int = Field(default=32, ge=1)
    signed: bool = Field(default=True)


class ArgumentIntegerData(ArgumentBaseData):
    to_string: ToString | None = Field(default=None)
    initial_value: int | None = Field(default=None)
    size_in_bits: int = Field(default=32, ge=1)
    signed: bool = Field(default=True)


class FloatData(BaseData):
    to_string: ToString | None = Field(default=None)
    valid_range: ValidFloatRange | None = Field(default=None)
    initial_value: float | None = Field(default=None)
    size_in_bits: Literal[16, 32, 40, 48, 64, 80, 128] = Field(default=32)


class ArgumentFloatData(ArgumentBaseData):
    to_string: ToString | None = Field(default=None)
    initial_value: float | None = Field(default=None)
    size_in_bits: Literal[16, 32, 40, 48, 64, 80, 128] = Field(default=32)


class StringData(BaseData):
    size_range_in_characters: IntegerRange | None = Field(default=None)
    initial_value: str | None = Field(default=None)
    restriction_pattern: str | None = Field(default=None)
    character_width: Literal[8, 16, 32] | None = Field(
        default=None
    )  # TODO make sure this works


class ArgumentStringData(ArgumentBaseData):
    size_range_in_characters: IntegerRange | None = Field(default=None)
    initial_value: str | None = Field(default=None)
    restriction_pattern: str | None = Field(default=None)
    character_width: Literal[8, 16, 32] | None = Field(
        default=None
    )  # TODO make sure this works


class BinaryData(BaseData):
    initial_value: bytes | None = Field(default=None)


class ArgumentBinaryData(ArgumentBaseData):
    initial_value: bytes | None = Field(default=None)


class BooleanData(BaseData):
    initial_value: str | None = Field(default=None)
    one_string_value: str = Field(default="True")
    zero_string_value: str = Field(default="False")


class ArgumentBooleanData(ArgumentBaseData):
    initial_value: str | None = Field(default=None)
    one_string_value: str = Field(default="True")
    zero_string_value: str = Field(default="False")


class ValueEnumeration(XtceBaseModel):
    value: int = Field(...)
    max_value: int | None = Field(default=None)
    label: str = Field(...)
    short_description: str | None = Field(default=None)


class EnumeratedData(BaseData):
    enumerations: list[ValueEnumeration] = Field(default_factory=list, min_length=1)
    initial_value: str | None = Field(default=None)


class ArgumentEnumeratedData(ArgumentBaseData):
    enumerations: list[ValueEnumeration] = Field(default_factory=list, min_length=1)
    initial_value: str | None = Field(default=None)


class ArrayData(NameDescriptionBase):
    array_type_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )
    initial_value: str | None = Field(default=None)
    # TODO probably want to enforce type or attempt to cast to list? not sure how pydantic handles converting strings to list or if need to use ast.literal_eval


class Member(NameDescriptionBase):
    type_ref: str = Field(..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+")
    initial_value: str | None = Field(default=None)


class AggregateData(NameDescriptionBase):
    members: list[Member] = Field(default_factory=list, min_length=1)
    initial_value: str | None = Field(default=None)
    # TODO probably want to enforce type or attempt to cast to dict?


class BaseTimeData(NameDescriptionBase):
    encoding: TimeEncoding | None = Field(default=None)
    reference_time: ReferenceTime | None = Field(default=None)
    base_type: str | None = Field(
        default=None, pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )


class ArgumentBaseTimeData(NameDescriptionBase):
    # TODO figure out what the difference is actually supposed to be...
    encoding: TimeEncoding | None = Field(default=None)
    reference_time: ReferenceTime | None = Field(default=None)
    base_type: str | None = Field(
        default=None, pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )


class RelativeTimeData(BaseTimeData):
    initial_value: datetime.timedelta | None = Field(default=None)  # XmlDuration


class ArgumentRelativeTimeData(ArgumentBaseTimeData):
    initial_value: datetime.timedelta | None = Field(default=None)  # XmlDuration


class AbsoluteTimeData(BaseTimeData):
    initial_value: datetime.datetime | None = Field(default=None)  # XmlDateTime


class ArgumentAbsoluteTimeData(ArgumentBaseTimeData):
    initial_value: datetime.datetime | None = Field(default=None)  # XmlDateTime
