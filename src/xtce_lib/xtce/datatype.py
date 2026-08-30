"""Data type models."""

import datetime
import json
from abc import ABC
from typing import Annotated, Any, Literal

from pydantic import AfterValidator, Field
from xsdata.models.datatype import XmlDateTime

from xtce_lib.common.xtce_path import XtcePath, require_regex
from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from ._pattern import NAME_REF_NO_PATH, NAME_REF_W_PATH
from ._type_aliases import XtceHexOrInt
from ._util import (
    coerce,
    timedelta_to_xml_duration,
    uncoerce,
    unwrap,
    xml_duration_to_timedelta,
)
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
from .range import (
    FloatRange,
    IntegerRange,
    ValidFloatRange,
    ValidIntegerRange,
)
from .time import ReferenceTime

# TODO add some information about what size in bits means in the data type classes compared to what they mean in the encoding classes


class Unit(XtceBaseModel):
    """Describe the exponent, factor, form, and description for a unit."""

    # TODO maybe add property that builds the unit text

    symbol: str = Field(..., examples=["m/s^2", "V", "byte"])
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

    form: UnitForm = UnitForm.CALIBRATED
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

    _v1_1_type = xtce_1_1.UnitType
    _v1_2_type = xtce_1_2.UnitType
    _v1_3_type = xtce_1_3.UnitType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.UnitType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["symbol"] = cls._extract_mixed_field(obj.content)
        kwargs["factor"] = obj.factor
        kwargs["power"] = obj.power
        kwargs["description"] = obj.description
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.UnitType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["symbol"] = cls._extract_mixed_field(obj.content)
        kwargs["factor"] = obj.factor
        kwargs["power"] = obj.power
        kwargs["form"] = UnitForm(obj.form.value)
        kwargs["description"] = obj.description
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.UnitType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["symbol"] = cls._extract_mixed_field(obj.content)
        kwargs["factor"] = obj.factor
        kwargs["power"] = obj.power
        kwargs["form"] = UnitForm(obj.form.value)
        kwargs["description"] = obj.description
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="form",
            current_value=self.form,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=UnitForm.CALIBRATED,
        )

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["content"] = [self.symbol]
        kwargs["factor"] = self.factor
        kwargs["power"] = self.power
        kwargs["description"] = self.description
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["content"] = [self.symbol]
        kwargs["factor"] = self.factor
        kwargs["power"] = self.power
        kwargs["form"] = xtce_1_2.UnitFormType(self.form.value)
        kwargs["description"] = self.description
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["content"] = [self.symbol]
        kwargs["factor"] = self.factor
        kwargs["power"] = self.power
        kwargs["form"] = xtce_1_2.UnitFormType(self.form.value)
        kwargs["description"] = self.description
        return kwargs


class ValueEnumeration(XtceBaseModel):
    """Define a value and associated string label."""

    value: int
    """The value associated with the label."""

    max_value: int | None = None
    """If specified, the label maps to a range where `value` is less than or equal to
    `max_value`.

    The range is inclusive.

    Applicable since: XTCE 1.2

    """

    label: str
    """The string label associated with the value."""

    short_description: str | None = None
    """A brief description of the value enumeration.

    Applicable since: XTCE 1.2

    """

    _v1_1_type = xtce_1_1.ValueEnumerationType
    _v1_2_type = xtce_1_2.ValueEnumerationType
    _v1_3_type = xtce_1_3.ValueEnumerationType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.ValueEnumerationType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["value"] = obj.value
        kwargs["label"] = obj.label
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ValueEnumerationType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["value"] = obj.value
        kwargs["max_value"] = obj.max_value
        kwargs["label"] = obj.label
        kwargs["short_description"] = obj.short_description
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ValueEnumerationType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["value"] = obj.value
        kwargs["max_value"] = obj.max_value
        kwargs["label"] = obj.label
        kwargs["short_description"] = obj.short_description
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="max_value",
            current_value=self.max_value,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=None,
        )
        self._enforce_unsupported_field(
            field_name="short_description",
            current_value=self.short_description,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=None,
        )

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["value"] = self.value
        kwargs["label"] = self.label
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["value"] = self.value
        kwargs["max_value"] = self.max_value
        kwargs["label"] = self.label
        kwargs["short_description"] = self.short_description
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["value"] = self.value
        kwargs["max_value"] = self.max_value
        kwargs["label"] = self.label
        kwargs["short_description"] = self.short_description
        return kwargs


class BaseData(NameDescriptionBase, ABC):
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
    )
    """Optional encoding information for this data type.

    This is only necessary if this data type is telemetered in some form. Local
    variables and derived typically do not require encoding.

    """

    base_type: Annotated[
        XtcePath | None, AfterValidator(require_regex(NAME_REF_W_PATH))
    ] = Field(
        default=None,
        examples=[],
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """Used to derive one Data Type from another.

    Will inherit all the attributes from the baseType any of which may be redefined in
    this type definition.

    """

    # TODO validate against circular derivations

    _v1_1_type = xtce_1_1.BaseDataType
    _v1_2_type = xtce_1_2.BaseDataType
    _v1_3_type = xtce_1_3.BaseDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.BaseDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["units"] = [Unit._from_v1_1(u) for u in obj.unit_set.unit]
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
        kwargs["base_type"] = (
            XtcePath(obj.base_type) if obj.base_type is not None else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.BaseDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["units"] = (
            [Unit._from_v1_2(u) for u in obj.unit_set.unit]
            if obj.unit_set is not None
            else None
        )
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
        kwargs["base_type"] = (
            XtcePath(obj.base_type) if obj.base_type is not None else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.BaseDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["units"] = (
            [Unit._from_v1_3(u) for u in obj.unit_set.unit]
            if obj.unit_set is not None
            else None
        )
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
        kwargs["base_type"] = (
            XtcePath(obj.base_type) if obj.base_type is not None else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        if self.base_type is not None:
            # XTCE 1.1 defines this as NameReferenceType
            validator = require_regex(NAME_REF_NO_PATH)
            validator(self.base_type)

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["unit_set"] = self._build_set(
            items=self.units,
            set_class=xtce_1_1.BaseDataType.UnitSet,
            kwarg_name="unit",
            converter=lambda u: u._to_v1_1(policy),
            required=True,
        )
        kwargs["choice"] = (
            self.encoding_type._to_v1_1(policy)
            if self.encoding_type is not None
            else None
        )
        kwargs["base_type"] = (
            str(self.base_type) if self.base_type is not None else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        if self.base_type is not None:
            # XTCE 1.2 defines this as NameReferenceType
            validator = require_regex(NAME_REF_NO_PATH)
            validator(self.base_type)

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["unit_set"] = self._build_set(
            items=self.units,
            set_class=xtce_1_2.UnitSetType,
            kwarg_name="unit",
            converter=lambda u: u._to_v1_2(policy),
            required=True,
        )
        kwargs["choice"] = (
            self.encoding_type._to_v1_2(policy)
            if self.encoding_type is not None
            else None
        )
        kwargs["base_type"] = (
            str(self.base_type) if self.base_type is not None else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["unit_set"] = self._build_set(
            items=self.units,
            set_class=xtce_1_3.UnitSetType,
            kwarg_name="unit",
            converter=lambda u: u._to_v1_3(policy),
            required=True,
        )
        kwargs["choice"] = (
            self.encoding_type._to_v1_3(policy)
            if self.encoding_type is not None
            else None
        )
        kwargs["base_type"] = (
            str(self.base_type) if self.base_type is not None else None
        )
        return kwargs


class ArgumentBaseData(NameDescriptionBase, ABC):
    """Abstract base class for argument base data types."""

    units: list[Unit] = Field(default_factory=list)
    """List of units associated with the argument base data type."""

    encoding_type: (
        IntegerDataEncoding
        | FloatDataEncoding
        | ArgumentStringDataEncoding
        | ArgumentBinaryDataEncoding
        | None
    )
    """The type of encoding used to encode this data type."""

    base_type: Annotated[
        XtcePath | None, AfterValidator(require_regex(NAME_REF_W_PATH))
    ] = Field(
        default=None,
        examples=[],
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """Used to derive one Data Type from another.

    Will inherit all the attributes from the baseType any of which may be redefined in
    this type definition.

    """

    # TODO validate against circular derivations

    _v1_1_type = xtce_1_1.BaseDataType
    _v1_2_type = xtce_1_2.ArgumentBaseDataType
    _v1_3_type = xtce_1_3.ArgumentBaseDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.BaseDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["units"] = [Unit._from_v1_1(u) for u in obj.unit_set.unit]
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
        kwargs["base_type"] = (
            XtcePath(obj.base_type) if obj.base_type is not None else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ArgumentBaseDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["units"] = (
            [Unit._from_v1_2(u) for u in obj.unit_set.unit]
            if obj.unit_set is not None
            else None
        )
        kwargs["encoding_type"] = (
            IntegerDataEncoding._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.IntegerDataEncodingType)
            else FloatDataEncoding._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.FloatDataEncodingType)
            else ArgumentStringDataEncoding._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.ArgumentStringDataEncodingType)
            else ArgumentBinaryDataEncoding._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.ArgumentBinaryDataEncodingType)
            else None
        )
        kwargs["base_type"] = (
            XtcePath(obj.base_type) if obj.base_type is not None else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ArgumentBaseDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["units"] = (
            [Unit._from_v1_3(u) for u in obj.unit_set.unit]
            if obj.unit_set is not None
            else None
        )
        kwargs["encoding_type"] = (
            IntegerDataEncoding._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.IntegerDataEncodingType)
            else FloatDataEncoding._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.FloatDataEncodingType)
            else ArgumentStringDataEncoding._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.ArgumentStringDataEncodingType)
            else ArgumentBinaryDataEncoding._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.ArgumentBinaryDataEncodingType)
            else None
        )
        kwargs["base_type"] = (
            XtcePath(obj.base_type) if obj.base_type is not None else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        if self.base_type is not None:
            # XTCE 1.1 defines this as NameReferenceType
            validator = require_regex(NAME_REF_NO_PATH)
            validator(self.base_type)

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["unit_set"] = self._build_set(
            items=self.units,
            set_class=xtce_1_1.BaseDataType.UnitSet,
            kwarg_name="unit",
            converter=lambda u: u._to_v1_1(policy),
            required=True,
        )
        kwargs["choice"] = (
            self.encoding_type._to_v1_1(policy)
            if self.encoding_type is not None
            else None
        )
        kwargs["base_type"] = (
            str(self.base_type) if self.base_type is not None else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        if self.base_type is not None:
            # XTCE 1.2 defines this as NameReferenceType
            validator = require_regex(NAME_REF_NO_PATH)
            validator(self.base_type)

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["unit_set"] = self._build_set(
            items=self.units,
            set_class=xtce_1_2.UnitSetType,
            kwarg_name="unit",
            converter=lambda u: u._to_v1_2(policy),
            required=True,
        )
        kwargs["choice"] = (
            self.encoding_type._to_v1_2(policy)
            if self.encoding_type is not None
            else None
        )
        kwargs["base_type"] = (
            str(self.base_type) if self.base_type is not None else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["unit_set"] = self._build_set(
            items=self.units,
            set_class=xtce_1_3.UnitSetType,
            kwarg_name="unit",
            converter=lambda u: u._to_v1_3(policy),
            required=True,
        )
        kwargs["choice"] = (
            self.encoding_type._to_v1_3(policy)
            if self.encoding_type is not None
            else None
        )
        kwargs["base_type"] = (
            str(self.base_type) if self.base_type is not None else None
        )
        return kwargs


class NumberFormat(XtceBaseModel):
    """Define how a calibrated value of a number should be displayed."""

    number_base: Radix = Radix.DECIMAL
    """Define the base for the number format."""

    minimum_fraction_digits: int = Field(default=0, ge=0)
    """Define the minimum number of fraction digits to display."""

    maximum_fraction_digits: int | None = Field(default=None, ge=0)
    """Define the maximum number of fraction digits to display."""

    minimum_integer_digits: int = Field(default=1, ge=0)
    """Define the minimum number of integer digits to display."""

    maximum_integer_digits: int | None = Field(default=None, ge=0)
    """Define the maximum number of integer digits to display."""

    negative_prefix: str = "-"
    """Define the prefix to use for negative numbers."""

    positive_prefix: str = ""
    """Define the prefix to use for positive numbers."""

    negative_suffix: str = ""
    """Define the suffix to use for negative numbers."""

    positive_suffix: str = ""
    """Define the suffix to use for positive numbers."""

    show_thousands_grouping: bool = False
    """Define whether to show thousands grouping."""

    notation: FloatingPointNotation = FloatingPointNotation.NORMAL
    """Define the notation to use for floating point numbers."""

    _v1_1_type = xtce_1_1.NumberToStringType.NumberFormat
    _v1_2_type = xtce_1_2.NumberFormatType
    _v1_3_type = xtce_1_3.NumberFormatType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.NumberToStringType.NumberFormat
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["number_base"] = Radix(unwrap(obj.number_base).value)
        kwargs["minimum_fraction_digits"] = obj.minimum_fraction_digits
        kwargs["maximum_fraction_digits"] = obj.maximum_fraction_digits
        kwargs["minimum_integer_digits"] = obj.minimum_integer_digits
        kwargs["maximum_integer_digits"] = obj.maximum_integer_digits
        kwargs["negative_prefix"] = obj.negative_prefix
        kwargs["positive_prefix"] = obj.positive_prefix
        kwargs["negative_suffix"] = obj.negative_suffix
        kwargs["positive_suffix"] = obj.positive_suffix
        kwargs["show_thousands_grouping"] = obj.show_thousands_grouping
        kwargs["notation"] = FloatingPointNotation(obj.notation.value)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.NumberFormatType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["number_base"] = Radix(obj.number_base.value)
        kwargs["minimum_fraction_digits"] = obj.minimum_fraction_digits
        kwargs["maximum_fraction_digits"] = obj.maximum_fraction_digits
        kwargs["minimum_integer_digits"] = obj.minimum_integer_digits
        kwargs["maximum_integer_digits"] = obj.maximum_integer_digits
        kwargs["negative_prefix"] = obj.negative_prefix
        kwargs["positive_prefix"] = obj.positive_prefix
        kwargs["negative_suffix"] = obj.negative_suffix
        kwargs["positive_suffix"] = obj.positive_suffix
        kwargs["show_thousands_grouping"] = obj.show_thousands_grouping
        kwargs["notation"] = FloatingPointNotation(obj.notation.value)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.NumberFormatType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["number_base"] = Radix(obj.number_base.value)
        kwargs["minimum_fraction_digits"] = obj.minimum_fraction_digits
        kwargs["maximum_fraction_digits"] = obj.maximum_fraction_digits
        kwargs["minimum_integer_digits"] = obj.minimum_integer_digits
        kwargs["maximum_integer_digits"] = obj.maximum_integer_digits
        kwargs["negative_prefix"] = obj.negative_prefix
        kwargs["positive_prefix"] = obj.positive_prefix
        kwargs["negative_suffix"] = obj.negative_suffix
        kwargs["positive_suffix"] = obj.positive_suffix
        kwargs["show_thousands_grouping"] = obj.show_thousands_grouping
        kwargs["notation"] = FloatingPointNotation(obj.notation.value)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["number_base"] = xtce_1_1.RadixType(self.number_base.value)
        kwargs["minimum_fraction_digits"] = self.minimum_fraction_digits
        kwargs["maximum_fraction_digits"] = self.maximum_fraction_digits
        kwargs["minimum_integer_digits"] = self.minimum_integer_digits
        kwargs["maximum_integer_digits"] = self.maximum_integer_digits
        kwargs["negative_prefix"] = self.negative_prefix
        kwargs["positive_prefix"] = self.positive_prefix
        kwargs["negative_suffix"] = self.negative_suffix
        kwargs["positive_suffix"] = self.positive_suffix
        kwargs["show_thousands_grouping"] = self.show_thousands_grouping
        kwargs["notation"] = xtce_1_1.NumberFormatNotation(self.notation)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["number_base"] = xtce_1_2.RadixType(self.number_base.value)
        kwargs["minimum_fraction_digits"] = self.minimum_fraction_digits
        kwargs["maximum_fraction_digits"] = self.maximum_fraction_digits
        kwargs["minimum_integer_digits"] = self.minimum_integer_digits
        kwargs["maximum_integer_digits"] = self.maximum_integer_digits
        kwargs["negative_prefix"] = self.negative_prefix
        kwargs["positive_prefix"] = self.positive_prefix
        kwargs["negative_suffix"] = self.negative_suffix
        kwargs["positive_suffix"] = self.positive_suffix
        kwargs["show_thousands_grouping"] = self.show_thousands_grouping
        kwargs["notation"] = xtce_1_2.FloatingPointNotationType(self.notation)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["number_base"] = xtce_1_3.RadixType(self.number_base.value)
        kwargs["minimum_fraction_digits"] = self.minimum_fraction_digits
        kwargs["maximum_fraction_digits"] = self.maximum_fraction_digits
        kwargs["minimum_integer_digits"] = self.minimum_integer_digits
        kwargs["maximum_integer_digits"] = self.maximum_integer_digits
        kwargs["negative_prefix"] = self.negative_prefix
        kwargs["positive_prefix"] = self.positive_prefix
        kwargs["negative_suffix"] = self.negative_suffix
        kwargs["positive_suffix"] = self.positive_suffix
        kwargs["show_thousands_grouping"] = self.show_thousands_grouping
        kwargs["notation"] = xtce_1_3.FloatingPointNotationType(self.notation)
        return kwargs


class ToString(XtceBaseModel):
    """Define how a numeric value should be displayed as a string."""

    number_format: NumberFormat | ValueEnumeration | FloatRange
    """The number format to use when converting the numeric value to a string.

    Type compatibility:
        - `NumberFormat`: All versions.
        - `ValueEnumeration`: XTCE 1.1.
        - `FloatRange`: XTCE 1.1.

    """

    # TODO add more details about what the enums represent

    _v1_1_type = xtce_1_1.NumberToStringType
    _v1_2_type = xtce_1_2.ToStringType
    _v1_3_type = xtce_1_3.ToStringType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.NumberToStringType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        # XTCE 1.1 models this as a list (even though only one entry is meaningful)
        choice = unwrap(obj.choice[0]) if obj.choice else None
        kwargs["number_format"] = (
            NumberFormat._from_v1_1(choice)
            if isinstance(choice, xtce_1_1.NumberToStringType.NumberFormat)
            else ValueEnumeration._from_v1_1(choice)
            if isinstance(choice, xtce_1_1.ValueEnumerationType)
            else FloatRange._from_v1_1(choice)
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ToStringType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["number_format"] = NumberFormat._from_v1_2(obj.number_format)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ToStringType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["number_format"] = NumberFormat._from_v1_3(obj.number_format)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        # XTCE 1.1 models this as a list (even though only one entry is meaningful)
        kwargs["choice"] = [self.number_format._to_v1_1(policy)]
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        number_format = self._enforce_restricted_type(
            field_name="number_format",
            current_value=self.number_format,
            allowed_types=(NumberFormat,),
            target_version=XtceVersion.V1_2,
            policy=policy,
            require_match=True,
        )

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["number_format"] = number_format._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        number_format = self._enforce_restricted_type(
            field_name="number_format",
            current_value=self.number_format,
            allowed_types=(NumberFormat,),
            target_version=XtceVersion.V1_3,
            policy=policy,
            require_match=True,
        )

        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["number_format"] = number_format._to_v1_3(policy)
        return kwargs


class IntegerData(BaseData, ABC):
    """Abstract base class for integer data types."""

    to_string: ToString | None = None
    """Define how the integer data should be displayed as a string."""

    valid_range: ValidIntegerRange | None = None
    """The valid range of integer values for this data type."""

    initial_value: XtceHexOrInt | None = None
    """The initial value for this integer data type."""

    size_in_bits: int = Field(default=32, ge=1)
    """The size of the integer data type in bits."""

    signed: bool = True
    """Indicates whether the integer data type is signed."""

    _v1_1_type = xtce_1_1.IntegerDataType
    _v1_2_type = xtce_1_2.IntegerDataType
    _v1_3_type = xtce_1_3.IntegerDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.IntegerDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["to_string"] = (
            ToString._from_v1_1(obj.to_string) if obj.to_string else None
        )
        # XTCE 1.1 has `valid_range_applies_to_calibrated` in IntegerDataType (inherited
        # from NumericDataType), so it needs to be passed in to the constructor here
        kwargs["valid_range"] = (
            ValidIntegerRange._from_v1_1_kwargs(
                obj.valid_range,
                applies_to_calibrated=obj.valid_range_applies_to_calibrated,
            )
            if obj.valid_range is not None
            else None
        )
        kwargs["initial_value"] = obj.initial_value
        kwargs["size_in_bits"] = obj.size_in_bits
        kwargs["signed"] = obj.signed
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.IntegerDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["to_string"] = (
            ToString._from_v1_2(obj.to_string) if obj.to_string else None
        )
        kwargs["valid_range"] = (
            ValidIntegerRange._from_v1_2(obj.valid_range)
            if obj.valid_range is not None
            else None
        )
        kwargs["initial_value"] = obj.initial_value
        kwargs["size_in_bits"] = obj.size_in_bits
        kwargs["signed"] = obj.signed
        kwargs["name"] = obj.name
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.IntegerDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["to_string"] = (
            ToString._from_v1_3(obj.to_string) if obj.to_string else None
        )
        kwargs["valid_range"] = (
            ValidIntegerRange._from_v1_3(obj.valid_range)
            if obj.valid_range is not None
            else None
        )
        kwargs["initial_value"] = obj.initial_value
        kwargs["size_in_bits"] = obj.size_in_bits
        kwargs["signed"] = obj.signed
        kwargs["name"] = obj.name
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["to_string"] = (
            self.to_string._to_v1_1(policy) if self.to_string else None
        )
        kwargs["valid_range"] = (
            self.valid_range._to_v1_1(policy) if self.valid_range is not None else None
        )
        # XTCE 1.1 has `valid_range_applies_to_calibrated` in IntegerDataType (inherited
        # from NumericDataType), so it needs to be extracted from `valid_range`
        kwargs["valid_range_applies_to_calibrated"] = (
            self.valid_range.applies_to_calibrated
            if self.valid_range is not None
            else None
        )
        kwargs["initial_value"] = self.initial_value
        kwargs["size_in_bits"] = self.size_in_bits
        kwargs["signed"] = self.signed
        kwargs["name"] = self.name
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["to_string"] = (
            self.to_string._to_v1_2(policy) if self.to_string else None
        )
        kwargs["valid_range"] = (
            self.valid_range._to_v1_2(policy) if self.valid_range is not None else None
        )
        if self.initial_value is not None:
            # XTCE 1.2 requires a base 10 integer
            if isinstance(self.initial_value, str):
                kwargs["initial_value"] = int(self.initial_value, 0)
            else:
                kwargs["initial_value"] = self.initial_value
        kwargs["size_in_bits"] = self.size_in_bits
        kwargs["signed"] = self.signed
        kwargs["name"] = self.name
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["to_string"] = (
            self.to_string._to_v1_3(policy) if self.to_string else None
        )
        kwargs["valid_range"] = (
            self.valid_range._to_v1_3(policy) if self.valid_range is not None else None
        )
        if self.initial_value is not None:
            # XTCE 1.3 requires a base 10 integer
            if isinstance(self.initial_value, str):
                kwargs["initial_value"] = int(self.initial_value, 0)
            else:
                kwargs["initial_value"] = self.initial_value
        kwargs["size_in_bits"] = self.size_in_bits
        kwargs["signed"] = self.signed
        kwargs["name"] = self.name
        return kwargs


class ArgumentIntegerData(ArgumentBaseData, ABC):
    """Abstract base class for argument integer data types."""

    to_string: ToString | None = None
    """Define how the integer data should be displayed as a string."""

    valid_range: ValidIntegerRange | None = None
    """The valid range of integer values for this data type.

    Only applicable for: XTCE 1.1.

    """

    initial_value: XtceHexOrInt | None = None
    """The initial value for this integer data type."""

    size_in_bits: int = 32
    """The size of the integer data type in bits."""

    signed: bool = True
    """Indicates whether the integer data type is signed."""

    _v1_1_type = xtce_1_1.IntegerDataType
    _v1_2_type = xtce_1_2.ArgumentIntegerDataType
    _v1_3_type = xtce_1_3.ArgumentIntegerDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.IntegerDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["to_string"] = (
            ToString._from_v1_1(obj.to_string) if obj.to_string else None
        )
        # XTCE 1.1 has `valid_range_applies_to_calibrated` in IntegerDataType (inherited
        # from NumericDataType), so it needs to be passed in to the constructor here
        kwargs["valid_range"] = (
            ValidIntegerRange._from_v1_1_kwargs(
                obj.valid_range,
                applies_to_calibrated=obj.valid_range_applies_to_calibrated,
            )
            if obj.valid_range is not None
            else None
        )
        kwargs["initial_value"] = obj.initial_value
        kwargs["size_in_bits"] = obj.size_in_bits
        kwargs["signed"] = obj.signed
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ArgumentIntegerDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["to_string"] = (
            ToString._from_v1_2(obj.to_string) if obj.to_string else None
        )
        kwargs["initial_value"] = obj.initial_value
        kwargs["size_in_bits"] = obj.size_in_bits
        kwargs["signed"] = obj.signed
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ArgumentIntegerDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["to_string"] = (
            ToString._from_v1_3(obj.to_string) if obj.to_string else None
        )
        kwargs["initial_value"] = obj.initial_value
        kwargs["size_in_bits"] = obj.size_in_bits
        kwargs["signed"] = obj.signed
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["to_string"] = (
            self.to_string._to_v1_1(policy) if self.to_string is not None else None
        )
        kwargs["valid_range"] = (
            self.valid_range._to_v1_1(policy) if self.valid_range is not None else None
        )
        # XTCE 1.1 has `valid_range_applies_to_calibrated` in IntegerDataType (inherited
        # from NumericDataType), so it needs to be extracted from `valid_range`
        kwargs["valid_range_applies_to_calibrated"] = (
            self.valid_range.applies_to_calibrated
            if self.valid_range is not None
            else None
        )
        kwargs["initial_value"] = self.initial_value
        kwargs["size_in_bits"] = self.size_in_bits
        kwargs["signed"] = self.signed
        kwargs["name"] = self.name
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="valid_range",
            current_value=self.valid_range,
            target_version=XtceVersion.V1_2,
            policy=policy,
            empty_value=None,
        )

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["to_string"] = (
            self.to_string._to_v1_2(policy) if self.to_string is not None else None
        )
        if self.initial_value is not None:
            # XTCE 1.2 requires a base 10 integer
            if isinstance(self.initial_value, str):
                kwargs["initial_value"] = int(self.initial_value, 0)
            else:
                kwargs["initial_value"] = self.initial_value
        kwargs["size_in_bits"] = self.size_in_bits
        kwargs["signed"] = self.signed
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="valid_range",
            current_value=self.valid_range,
            target_version=XtceVersion.V1_3,
            policy=policy,
            empty_value=None,
        )

        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["to_string"] = (
            self.to_string._to_v1_3(policy) if self.to_string is not None else None
        )
        if self.initial_value is not None:
            # XTCE 1.3 requires a base 10 integer
            if isinstance(self.initial_value, str):
                kwargs["initial_value"] = int(self.initial_value, 0)
            else:
                kwargs["initial_value"] = self.initial_value
        kwargs["size_in_bits"] = self.size_in_bits
        kwargs["signed"] = self.signed
        return kwargs


class FloatData(BaseData, ABC):
    """Abstract base class for float data types."""

    to_string: ToString | None = None
    """Define how the float data should be displayed as a string."""

    valid_range: ValidFloatRange | None = None
    """The valid range of float values for this data type."""

    initial_value: float | None = None
    """The initial value for this float data type."""

    size_in_bits: Literal[32, 64, 128] = 32
    """The size of the float data type in bits."""

    _v1_1_type = xtce_1_1.FloatDataType
    _v1_2_type = xtce_1_2.FloatDataType
    _v1_3_type = xtce_1_3.FloatDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.FloatDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["to_string"] = (
            ToString._from_v1_1_kwargs(obj.to_string)
            if obj.to_string is not None
            else None
        )
        kwargs["valid_range"] = (
            ValidFloatRange._from_v1_1_kwargs(
                obj.valid_range,
                applies_to_calibrated=obj.valid_range_applies_to_calibrated,
            )
            if obj.valid_range is not None
            else None
        )
        kwargs["initial_value"] = obj.initial_value
        kwargs["size_in_bits"] = obj.size_in_bits.value
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.FloatDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["to_string"] = (
            ToString._from_v1_2_kwargs(obj.to_string)
            if obj.to_string is not None
            else None
        )
        kwargs["valid_range"] = (
            ValidFloatRange._from_v1_2_kwargs(obj.valid_range)
            if obj.valid_range is not None
            else None
        )
        kwargs["initial_value"] = obj.initial_value
        kwargs["size_in_bits"] = obj.size_in_bits.value
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.FloatDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["to_string"] = (
            ToString._from_v1_3_kwargs(obj.to_string)
            if obj.to_string is not None
            else None
        )
        kwargs["valid_range"] = (
            ValidFloatRange._from_v1_3_kwargs(obj.valid_range)
            if obj.valid_range is not None
            else None
        )
        kwargs["initial_value"] = obj.initial_value
        kwargs["size_in_bits"] = obj.size_in_bits.value
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["to_string"] = (
            self.to_string._to_v1_1(policy) if self.to_string is not None else None
        )
        kwargs["valid_range"] = (
            self.valid_range._to_v1_1(policy) if self.valid_range is not None else None
        )
        # XTCE 1.1 has `valid_range_applies_to_calibrated` in FloatDataType (inherited
        # from NumericDataType), so it needs to be extracted from `valid_range`
        kwargs["valid_range_applies_to_calibrated"] = (
            self.valid_range.applies_to_calibrated
            if self.valid_range is not None
            else None
        )
        kwargs["initial_value"] = self.initial_value
        kwargs["size_in_bits"] = xtce_1_1.FloatDataTypeSizeInBits(self.size_in_bits)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["to_string"] = (
            self.to_string._to_v1_2(policy) if self.to_string is not None else None
        )
        kwargs["valid_range"] = (
            self.valid_range._to_v1_2(policy) if self.valid_range is not None else None
        )
        kwargs["initial_value"] = self.initial_value
        kwargs["size_in_bits"] = xtce_1_2.FloatSizeInBitsType(self.size_in_bits)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["to_string"] = (
            self.to_string._to_v1_3(policy) if self.to_string is not None else None
        )
        kwargs["valid_range"] = (
            self.valid_range._to_v1_3(policy) if self.valid_range is not None else None
        )
        kwargs["initial_value"] = self.initial_value
        kwargs["size_in_bits"] = xtce_1_3.FloatSizeInBitsType(self.size_in_bits)
        return kwargs


class ArgumentFloatData(ArgumentBaseData, ABC):
    """Abstract base class for argument float data types."""

    to_string: ToString | None = None
    """Define how the float data should be displayed as a string."""

    valid_range: ValidFloatRange | None = None
    """The valid range of float values for this data type.

    Only applicable for: XTCE 1.1.

    """

    initial_value: float | None = None
    """The initial value for this float data type."""

    size_in_bits: Literal[32, 64, 128] = 32
    """The size of the float data type in bits."""

    _v1_1_type = xtce_1_1.FloatDataType
    _v1_2_type = xtce_1_2.ArgumentFloatDataType
    _v1_3_type = xtce_1_3.ArgumentFloatDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.FloatDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["to_string"] = (
            ToString._from_v1_1_kwargs(obj.to_string)
            if obj.to_string is not None
            else None
        )
        kwargs["valid_range"] = (
            ValidFloatRange._from_v1_1_kwargs(
                obj.valid_range,
                applies_to_calibrated=obj.valid_range_applies_to_calibrated,
            )
            if obj.valid_range is not None
            else None
        )
        kwargs["initial_value"] = obj.initial_value
        kwargs["size_in_bits"] = obj.size_in_bits.value
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ArgumentFloatDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["to_string"] = (
            ToString._from_v1_2_kwargs(obj.to_string)
            if obj.to_string is not None
            else None
        )
        kwargs["initial_value"] = obj.initial_value
        kwargs["size_in_bits"] = obj.size_in_bits.value
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ArgumentFloatDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["to_string"] = (
            ToString._from_v1_3_kwargs(obj.to_string)
            if obj.to_string is not None
            else None
        )
        kwargs["initial_value"] = obj.initial_value
        kwargs["size_in_bits"] = obj.size_in_bits.value
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["to_string"] = (
            self.to_string._to_v1_1(policy) if self.to_string is not None else None
        )
        kwargs["valid_range"] = (
            self.valid_range._to_v1_1(policy) if self.valid_range is not None else None
        )
        # XTCE 1.1 has `valid_range_applies_to_calibrated` in FloatDataType (inherited
        # from NumericDataType), so it needs to be extracted from `valid_range`
        kwargs["valid_range_applies_to_calibrated"] = (
            self.valid_range.applies_to_calibrated
            if self.valid_range is not None
            else None
        )
        kwargs["initial_value"] = self.initial_value
        kwargs["size_in_bits"] = xtce_1_1.FloatDataTypeSizeInBits(self.size_in_bits)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="valid_range",
            current_value=self.valid_range,
            target_version=XtceVersion.V1_2,
            policy=policy,
            empty_value=None,
        )

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["to_string"] = (
            self.to_string._to_v1_2(policy) if self.to_string is not None else None
        )
        kwargs["initial_value"] = self.initial_value
        kwargs["size_in_bits"] = xtce_1_2.FloatSizeInBitsType(self.size_in_bits)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="valid_range",
            current_value=self.valid_range,
            target_version=XtceVersion.V1_3,
            policy=policy,
            empty_value=None,
        )

        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["to_string"] = (
            self.to_string._to_v1_3(policy) if self.to_string is not None else None
        )
        kwargs["initial_value"] = self.initial_value
        kwargs["size_in_bits"] = xtce_1_3.FloatSizeInBitsType(self.size_in_bits)
        return kwargs


class StringData(BaseData, ABC):
    """Abstract base class for string data types."""

    size_range_in_characters: IntegerRange | None = None
    """The range of allowed sizes for the string, in characters."""

    initial_value: str | None = None
    """The initial value of the string."""

    restriction_pattern: str | None = None
    """The regular expression pattern that the string must match, if any."""

    character_width: Literal[8, 16, 32] | None = None
    """The width of each character in bits."""

    # TODO maybe validate that restriction pattern is a valid regular expression
    # TODO maybe validate the initial value matches the pattern (may be hard if non-python pattern)

    _v1_1_type = xtce_1_1.StringDataType
    _v1_2_type = xtce_1_2.StringDataType
    _v1_3_type = xtce_1_3.StringDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.StringDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["size_range_in_characters"] = (
            IntegerRange._from_v1_1(obj.size_range_in_characters)
            if obj.size_range_in_characters is not None
            else None
        )
        kwargs["initial_value"] = obj.initial_value
        kwargs["restriction_pattern"] = obj.restriction_pattern
        kwargs["character_width"] = (
            obj.character_width.value if obj.character_width is not None else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.StringDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["size_range_in_characters"] = (
            IntegerRange._from_v1_2(obj.size_range_in_characters)
            if obj.size_range_in_characters is not None
            else None
        )
        kwargs["initial_value"] = obj.initial_value
        kwargs["restriction_pattern"] = obj.restriction_pattern
        kwargs["character_width"] = (
            obj.character_width.value if obj.character_width is not None else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.StringDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["size_range_in_characters"] = (
            IntegerRange._from_v1_3(obj.size_range_in_characters)
            if obj.size_range_in_characters is not None
            else None
        )
        kwargs["initial_value"] = obj.initial_value
        kwargs["restriction_pattern"] = obj.restriction_pattern
        kwargs["character_width"] = (
            obj.character_width.value if obj.character_width is not None else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["size_range_in_characters"] = (
            self.size_range_in_characters._to_v1_1(policy)
            if self.size_range_in_characters is not None
            else None
        )
        kwargs["initial_value"] = self.initial_value
        kwargs["restriction_pattern"] = self.restriction_pattern
        kwargs["character_width"] = (
            xtce_1_1.StringDataTypeCharacterWidth(self.character_width)
            if self.character_width is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["size_range_in_characters"] = (
            self.size_range_in_characters._to_v1_2(policy)
            if self.size_range_in_characters is not None
            else None
        )
        kwargs["initial_value"] = self.initial_value
        kwargs["restriction_pattern"] = self.restriction_pattern
        kwargs["character_width"] = (
            xtce_1_2.CharacterWidthType(self.character_width)
            if self.character_width is not None
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["size_range_in_characters"] = (
            self.size_range_in_characters._to_v1_3(policy)
            if self.size_range_in_characters is not None
            else None
        )
        kwargs["initial_value"] = self.initial_value
        kwargs["restriction_pattern"] = self.restriction_pattern
        kwargs["character_width"] = (
            xtce_1_3.CharacterWidthType(self.character_width)
            if self.character_width is not None
            else None
        )
        return kwargs


class ArgumentStringData(ArgumentBaseData, ABC):
    """Abstract base class for argument string data types."""

    size_range_in_characters: IntegerRange | None = None
    """The range of allowed sizes for the string, in characters."""

    initial_value: str | None = None
    """The initial value of the string."""

    restriction_pattern: str | None = None
    """The regular expression pattern that the string must match, if any."""

    character_width: Literal[8, 16, 32] | None = None
    """The width of each character in bits."""

    _v1_1_type = xtce_1_1.StringDataType
    _v1_2_type = xtce_1_2.ArgumentStringDataType
    _v1_3_type = xtce_1_3.ArgumentStringDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.StringDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["size_range_in_characters"] = (
            IntegerRange._from_v1_1(obj.size_range_in_characters)
            if obj.size_range_in_characters is not None
            else None
        )
        kwargs["initial_value"] = obj.initial_value
        kwargs["restriction_pattern"] = obj.restriction_pattern
        kwargs["character_width"] = (
            obj.character_width.value if obj.character_width is not None else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ArgumentStringDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["size_range_in_characters"] = (
            IntegerRange._from_v1_2(obj.size_range_in_characters)
            if obj.size_range_in_characters is not None
            else None
        )
        kwargs["initial_value"] = obj.initial_value
        kwargs["restriction_pattern"] = obj.restriction_pattern
        kwargs["character_width"] = (
            obj.character_width.value if obj.character_width is not None else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ArgumentStringDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["size_range_in_characters"] = (
            IntegerRange._from_v1_3(obj.size_range_in_characters)
            if obj.size_range_in_characters is not None
            else None
        )
        kwargs["initial_value"] = obj.initial_value
        kwargs["restriction_pattern"] = obj.restriction_pattern
        kwargs["character_width"] = (
            obj.character_width.value if obj.character_width is not None else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["size_range_in_characters"] = (
            self.size_range_in_characters._to_v1_1(policy)
            if self.size_range_in_characters is not None
            else None
        )
        kwargs["initial_value"] = self.initial_value
        kwargs["restriction_pattern"] = self.restriction_pattern
        kwargs["character_width"] = (
            xtce_1_1.StringDataTypeCharacterWidth(self.character_width)
            if self.character_width is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["size_range_in_characters"] = (
            self.size_range_in_characters._to_v1_2(policy)
            if self.size_range_in_characters is not None
            else None
        )
        kwargs["initial_value"] = self.initial_value
        kwargs["restriction_pattern"] = self.restriction_pattern
        kwargs["character_width"] = (
            xtce_1_2.CharacterWidthType(self.character_width)
            if self.character_width is not None
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["size_range_in_characters"] = (
            self.size_range_in_characters._to_v1_3(policy)
            if self.size_range_in_characters is not None
            else None
        )
        kwargs["initial_value"] = self.initial_value
        kwargs["restriction_pattern"] = self.restriction_pattern
        kwargs["character_width"] = (
            xtce_1_3.CharacterWidthType(self.character_width)
            if self.character_width is not None
            else None
        )
        return kwargs


class BinaryData(BaseData, ABC):
    """Abstract base class for binary data types."""

    initial_value: bytes | None = None
    """The initial value of the binary data."""

    _v1_1_type = xtce_1_1.BinaryDataType
    _v1_2_type = xtce_1_2.BinaryDataType
    _v1_3_type = xtce_1_3.BinaryDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.BinaryDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["initial_value"] = obj.initial_value
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.BinaryDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["initial_value"] = obj.initial_value
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.BinaryDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["initial_value"] = obj.initial_value
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["initial_value"] = self.initial_value
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["initial_value"] = self.initial_value
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["initial_value"] = self.initial_value
        return kwargs


class ArgumentBinaryData(ArgumentBaseData):
    """Abstract base class for argument binary data types."""

    initial_value: bytes | None = None
    """The initial value of the binary data."""

    _v1_1_type = xtce_1_1.BinaryDataType
    _v1_2_type = xtce_1_2.ArgumentBinaryDataType
    _v1_3_type = xtce_1_3.ArgumentBinaryDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.BinaryDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["initial_value"] = obj.initial_value
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ArgumentBinaryDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["initial_value"] = obj.initial_value
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ArgumentBinaryDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["initial_value"] = obj.initial_value
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["initial_value"] = self.initial_value
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["initial_value"] = self.initial_value
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["initial_value"] = self.initial_value
        return kwargs


class BooleanData(BaseData, ABC):
    """Abstract base class for boolean data types."""

    initial_value: str | None = None
    """The initial value of the boolean data."""

    one_string_value: str = "True"
    """The string representation of the boolean value True."""

    zero_string_value: str = "False"
    """The string representation of the boolean value False."""

    _v1_1_type = xtce_1_1.BooleanDataType
    _v1_2_type = xtce_1_2.BooleanDataType
    _v1_3_type = xtce_1_3.BooleanDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.BooleanDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["initial_value"] = obj.initial_value
        kwargs["one_string_value"] = obj.one_string_value
        kwargs["zero_string_value"] = obj.zero_string_value
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.BooleanDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["initial_value"] = obj.initial_value
        kwargs["one_string_value"] = obj.one_string_value
        kwargs["zero_string_value"] = obj.zero_string_value
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.BooleanDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["initial_value"] = obj.initial_value
        kwargs["one_string_value"] = obj.one_string_value
        kwargs["zero_string_value"] = obj.zero_string_value
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["initial_value"] = self.initial_value
        kwargs["one_string_value"] = self.one_string_value
        kwargs["zero_string_value"] = self.zero_string_value
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["initial_value"] = self.initial_value
        kwargs["one_string_value"] = self.one_string_value
        kwargs["zero_string_value"] = self.zero_string_value
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["initial_value"] = self.initial_value
        kwargs["one_string_value"] = self.one_string_value
        kwargs["zero_string_value"] = self.zero_string_value
        return kwargs


class ArgumentBooleanData(ArgumentBaseData, ABC):
    """Abstract base class for argument boolean data types."""

    initial_value: str | None = None
    """The initial value of the argument boolean data."""

    one_string_value: str = "True"
    """The string representation of the argument boolean value True."""

    zero_string_value: str = "False"
    """The string representation of the argument boolean value False."""

    _v1_1_type = xtce_1_1.BooleanDataType
    _v1_2_type = xtce_1_2.ArgumentBooleanDataType
    _v1_3_type = xtce_1_3.ArgumentBooleanDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.BooleanDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["initial_value"] = obj.initial_value
        kwargs["one_string_value"] = obj.one_string_value
        kwargs["zero_string_value"] = obj.zero_string_value
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ArgumentBooleanDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["initial_value"] = obj.initial_value
        kwargs["one_string_value"] = obj.one_string_value
        kwargs["zero_string_value"] = obj.zero_string_value
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ArgumentBooleanDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["initial_value"] = obj.initial_value
        kwargs["one_string_value"] = obj.one_string_value
        kwargs["zero_string_value"] = obj.zero_string_value
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["initial_value"] = self.initial_value
        kwargs["one_string_value"] = self.one_string_value
        kwargs["zero_string_value"] = self.zero_string_value
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["initial_value"] = self.initial_value
        kwargs["one_string_value"] = self.one_string_value
        kwargs["zero_string_value"] = self.zero_string_value
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["initial_value"] = self.initial_value
        kwargs["one_string_value"] = self.one_string_value
        kwargs["zero_string_value"] = self.zero_string_value
        return kwargs


class EnumeratedData(BaseData, ABC):
    """Abstract base class for enumerated data types."""

    enumerations: list[ValueEnumeration] = Field(..., min_length=1)
    """A list of value/label enumerations."""

    initial_value: str | None = None
    """The initial value of the enumerated data type."""

    _v1_1_type = xtce_1_1.EnumeratedDataType
    _v1_2_type = xtce_1_2.EnumeratedDataType
    _v1_3_type = xtce_1_3.EnumeratedDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.EnumeratedDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["enumerations"] = [
            ValueEnumeration._from_v1_1(e) for e in obj.enumeration_list.enumeration
        ]
        kwargs["initial_value"] = obj.initial_value
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.EnumeratedDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["enumerations"] = [
            ValueEnumeration._from_v1_2(e) for e in obj.enumeration_list.enumeration
        ]
        kwargs["initial_value"] = obj.initial_value
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.EnumeratedDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["enumerations"] = [
            ValueEnumeration._from_v1_3(e) for e in obj.enumeration_list.enumeration
        ]
        kwargs["initial_value"] = obj.initial_value
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["enumeration_list"] = self._build_set(
            items=self.enumerations,
            set_class=xtce_1_1.EnumeratedDataType.EnumerationList,
            kwarg_name="enumeration",
            converter=lambda e: e._to_v1_1(policy),
            required=True,
        )
        kwargs["initial_value"] = self.initial_value
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["enumeration_list"] = self._build_set(
            items=self.enumerations,
            set_class=xtce_1_2.EnumerationListType,
            kwarg_name="enumeration",
            converter=lambda e: e._to_v1_2(policy),
            required=True,
        )
        kwargs["initial_value"] = self.initial_value
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["enumeration_list"] = self._build_set(
            items=self.enumerations,
            set_class=xtce_1_3.EnumerationListType,
            kwarg_name="enumeration",
            converter=lambda e: e._to_v1_3(policy),
            required=True,
        )
        kwargs["initial_value"] = self.initial_value
        return kwargs


class ArgumentEnumeratedData(ArgumentBaseData, ABC):
    """Abstract base class for argument enumerated data types."""

    enumerations: list[ValueEnumeration] = Field(..., min_length=1)
    """A list of value/label enumerations."""

    initial_value: str | None = None
    """The initial value of the enumerated data type."""

    _v1_1_type = xtce_1_1.EnumeratedDataType
    _v1_2_type = xtce_1_2.ArgumentEnumeratedDataType
    _v1_3_type = xtce_1_3.ArgumentEnumeratedDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.EnumeratedDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["enumerations"] = [
            ValueEnumeration._from_v1_1(e) for e in obj.enumeration_list.enumeration
        ]
        kwargs["initial_value"] = obj.initial_value
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentEnumeratedDataType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["enumerations"] = [
            ValueEnumeration._from_v1_2(e) for e in obj.enumeration_list.enumeration
        ]
        kwargs["initial_value"] = obj.initial_value
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentEnumeratedDataType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["enumerations"] = [
            ValueEnumeration._from_v1_3(e) for e in obj.enumeration_list.enumeration
        ]
        kwargs["initial_value"] = obj.initial_value
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["enumeration_list"] = self._build_set(
            items=self.enumerations,
            set_class=xtce_1_1.EnumeratedDataType.EnumerationList,
            kwarg_name="enumeration",
            converter=lambda e: e._to_v1_1(policy),
            required=True,
        )
        kwargs["initial_value"] = self.initial_value
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["enumeration_list"] = self._build_set(
            items=self.enumerations,
            set_class=xtce_1_2.EnumerationListType,
            kwarg_name="enumeration",
            converter=lambda e: e._to_v1_2(policy),
            required=True,
        )
        kwargs["initial_value"] = self.initial_value
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["enumeration_list"] = self._build_set(
            items=self.enumerations,
            set_class=xtce_1_3.EnumerationListType,
            kwarg_name="enumeration",
            converter=lambda e: e._to_v1_3(policy),
            required=True,
        )
        kwargs["initial_value"] = self.initial_value
        return kwargs


class ArrayData(NameDescriptionBase, ABC):
    """Abstract base class for array data types."""

    array_type_ref: Annotated[
        XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))
    ] = Field(
        ...,
        examples=[],  # TODO
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to the data type that defines the array elements."""

    initial_value: (
        list[int | float | str | bool | bytes | datetime.timedelta | datetime.datetime]
        | None
    ) = None
    """The initial value of the array data type."""

    # TODO validate that the initial value contents match the array type

    _v1_1_type = xtce_1_1.ArrayDataTypeType
    _v1_2_type = xtce_1_2.ArrayDataTypeType
    _v1_3_type = xtce_1_3.ArrayDataTypeType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.ArrayDataTypeType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["array_type_ref"] = XtcePath(obj.array_type_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ArrayDataTypeType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["array_type_ref"] = XtcePath(obj.array_type_ref)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ArrayDataTypeType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["array_type_ref"] = XtcePath(obj.array_type_ref)
        # The initial value is just a string in the XML representation, need to parse
        # to list. Pydantic will handle validation if necessary
        # TODO may need some better validation here
        kwargs["initial_value"] = (
            [coerce(e) for e in json.loads(obj.initial_value)]
            if obj.initial_value is not None
            else None
        )
        return kwargs

    def _to_v1_1_kwargs(
        self,
        policy: DowngradePolicy,
        number_of_dimensions: int,
    ) -> dict[str, Any]:
        # XTCE 1.1 defines this as NameReferenceType
        validator = require_regex(NAME_REF_NO_PATH)
        validator(self.array_type_ref)

        self._enforce_unsupported_field(
            field_name="initial_value",
            current_value=self.initial_value,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=None,
        )

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["array_type_ref"] = str(self.array_type_ref)
        # XTCE 1.1 has `number_of_dimensions` defined here rather than in the child
        # classes in XTCE 1.2+
        kwargs["number_of_dimensions"] = number_of_dimensions
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.2 defines this as NameReferenceType
        validator = require_regex(NAME_REF_NO_PATH)
        validator(self.array_type_ref)

        self._enforce_unsupported_field(
            field_name="initial_value",
            current_value=self.initial_value,
            target_version=XtceVersion.V1_2,
            policy=policy,
            empty_value=None,
        )

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["array_type_ref"] = str(self.array_type_ref)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["array_type_ref"] = str(self.array_type_ref)
        kwargs["initial_value"] = (
            json.dumps([uncoerce(e) for e in self.initial_value])
            if self.initial_value is not None
            else None
        )
        return kwargs


class Member(NameDescriptionBase):
    """Define a member field in an aggregate data structure."""

    type_ref: Annotated[XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))] = (
        Field(
            ...,
            examples=[],  # TODO
            json_schema_extra={"pattern": NAME_REF_W_PATH},
        )
    )
    """A Unix-like path to the data type that defines the aggregate member."""

    initial_value: (
        int | float | str | bool | bytes | datetime.timedelta | datetime.datetime | None
    ) = None
    """The initial value for the aggregate member.

    This will overwrite the initial value defined in the data type. The value must match
    the type of the aggregate member.

    """

    _v1_1_type = xtce_1_1.AggregateDataType.MemberList.Member
    _v1_2_type = xtce_1_2.MemberType
    _v1_3_type = xtce_1_3.MemberType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.AggregateDataType.MemberList.Member
    ) -> dict[str, Any]:
        # Annoyingly, Member in XTCE 1.1 does not inherit from NameDescriptionType, so
        # have to only extract the name
        kwargs = {}
        kwargs["name"] = obj.name
        kwargs["type_ref"] = XtcePath(obj.type_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.MemberType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["type_ref"] = XtcePath(obj.type_ref)
        kwargs["initial_value"] = (
            coerce(obj.initial_value) if obj.initial_value is not None else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.MemberType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["type_ref"] = XtcePath(obj.type_ref)
        kwargs["initial_value"] = (
            coerce(obj.initial_value) if obj.initial_value is not None else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.1 defines this as NameReferenceType
        validator = require_regex(NAME_REF_NO_PATH)
        validator(self.type_ref)

        # Because Member in XTCE 1.1 does not inherit from NameDescriptionType, need to
        # enforce that NameDescriptionBase fields are handled accordingly
        self._enforce_unsupported_field(
            field_name="short_description",
            current_value=self.short_description,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=None,
        )
        self._enforce_unsupported_field(
            field_name="aliases",
            current_value=self.aliases,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=[],
        )
        self._enforce_unsupported_field(
            field_name="ancillary_data",
            current_value=self.ancillary_data,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=[],
        )
        self._enforce_unsupported_field(
            field_name="initial_value",
            current_value=self.initial_value,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=None,
        )

        kwargs = {}
        kwargs["name"] = self.name
        kwargs["type_ref"] = str(self.type_ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.2 defines this as NameReferenceType
        validator = require_regex(NAME_REF_NO_PATH)
        validator(self.type_ref)

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["type_ref"] = str(self.type_ref)
        kwargs["initial_value"] = (
            uncoerce(self.initial_value) if self.initial_value is not None else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["type_ref"] = str(self.type_ref)
        kwargs["initial_value"] = (
            uncoerce(self.initial_value) if self.initial_value is not None else None
        )
        return kwargs


class AggregateData(NameDescriptionBase, ABC):
    """Abstract base class for aggregate data types."""

    members: list[Member] = Field(..., min_length=1)
    """Ordered list of member fields."""

    initial_value: (
        dict[
            str,
            int | float | str | bool | bytes | datetime.timedelta | datetime.datetime,
        ]
        | None
    ) = None
    """Initial values for the aggregate data type, keyed by member name.

    Initial values defined in the `Member` objects will override these defaults. These
    may recurse into nested aggregates.

    """

    _v1_1_type = xtce_1_1.AggregateDataType
    _v1_2_type = xtce_1_2.AggregateDataType
    _v1_3_type = xtce_1_3.AggregateDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.AggregateDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["members"] = [
            Member._from_v1_1_kwargs(m) for m in obj.member_list.member
        ]
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.AggregateDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["members"] = [
            Member._from_v1_2_kwargs(m) for m in obj.member_list.member
        ]
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.AggregateDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["members"] = [
            Member._from_v1_3_kwargs(m) for m in obj.member_list.member
        ]
        kwargs["initial_value"] = (
            {k: coerce(v) for k, v in json.loads(obj.initial_value).items()}
            if obj.initial_value is not None
            else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="initial_value",
            current_value=self.initial_value,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=None,
        )

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["member_list"] = self._build_set(
            items=self.members,
            set_class=xtce_1_1.AggregateDataType.MemberList,
            kwarg_name="member",
            converter=lambda m: m._to_v1_1(policy),
            required=True,
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="initial_value",
            current_value=self.initial_value,
            target_version=XtceVersion.V1_2,
            policy=policy,
            empty_value=None,
        )

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["member_list"] = self._build_set(
            items=self.members,
            set_class=xtce_1_2.MemberListType,
            kwarg_name="member",
            converter=lambda m: m._to_v1_2(policy),
            required=True,
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["member_list"] = self._build_set(
            items=self.members,
            set_class=xtce_1_3.MemberListType,
            kwarg_name="member",
            converter=lambda m: m._to_v1_3(policy),
            required=True,
        )
        kwargs["initial_value"] = (
            json.dumps({k: uncoerce(v) for k, v in self.initial_value.items()})
            if self.initial_value is not None
            else None
        )
        return kwargs


class BaseTimeData(NameDescriptionBase, ABC):
    """Abstract base class for time data types."""

    encoding: TimeEncoding
    """Encoding information for this data type."""

    reference_time: ReferenceTime | None = None
    """Describe the origin (epoch or reference) of this time type."""

    base_type: Annotated[
        XtcePath | None, AfterValidator(require_regex(NAME_REF_W_PATH))
    ] = Field(
        default=None,
        examples=[],  # TODO
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to the data type that defines the base time data type."""

    _v1_1_type = xtce_1_1.BaseTimeDataType
    _v1_2_type = xtce_1_2.BaseTimeDataType
    _v1_3_type = xtce_1_3.BaseTimeDataType

    # For some reason, the schema makes 'encoding' optional, even though in the
    # documentation attributes it states it 'must be set'. I am assuming that this is a
    # mistake in the schema, and that it should be required

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.BaseTimeDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["encoding"] = TimeEncoding._from_v1_1_kwargs(unwrap(obj.encoding))
        kwargs["reference_time"] = (
            ReferenceTime._from_v1_1_kwargs(obj.reference_time)
            if obj.reference_time is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.BaseTimeDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["encoding"] = TimeEncoding._from_v1_2_kwargs(unwrap(obj.encoding))
        kwargs["reference_time"] = (
            ReferenceTime._from_v1_2_kwargs(unwrap(obj.reference_time))
            if obj.reference_time is not None
            else None
        )
        kwargs["base_type"] = (
            XtcePath(obj.base_type) if obj.base_type is not None else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.BaseTimeDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["encoding"] = TimeEncoding._from_v1_3_kwargs(unwrap(obj.encoding))
        kwargs["reference_time"] = (
            ReferenceTime._from_v1_3_kwargs(unwrap(obj.reference_time))
            if obj.reference_time is not None
            else None
        )
        kwargs["base_type"] = (
            XtcePath(obj.base_type) if obj.base_type is not None else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="base_type",
            current_value=self.base_type,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=None,
        )

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["encoding"] = self.encoding._to_v1_1(policy)
        kwargs["reference_time"] = (
            self.reference_time._to_v1_1(policy)
            if self.reference_time is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["encoding"] = self.encoding._to_v1_2(policy)
        kwargs["reference_time"] = (
            self.reference_time._to_v1_2(policy)
            if self.reference_time is not None
            else None
        )
        kwargs["base_type"] = (
            str(self.base_type) if self.base_type is not None else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["encoding"] = self.encoding._to_v1_3(policy)
        kwargs["reference_time"] = (
            self.reference_time._to_v1_3(policy)
            if self.reference_time is not None
            else None
        )
        kwargs["base_type"] = (
            str(self.base_type) if self.base_type is not None else None
        )
        return kwargs


class ArgumentBaseTimeData(NameDescriptionBase, ABC):
    """Abstract base class for argument time data types."""

    encoding: TimeEncoding
    """Encoding information for this data type."""

    reference_time: ReferenceTime | None = None
    """Describe the origin (epoch or reference) of this time type."""

    base_type: Annotated[
        XtcePath | None, AfterValidator(require_regex(NAME_REF_W_PATH))
    ] = Field(
        default=None,
        examples=[],  # TODO
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to the data type that defines the base time data type."""

    _v1_1_type = xtce_1_1.BaseTimeDataType
    _v1_2_type = xtce_1_2.ArgumentBaseTimeDataType
    _v1_3_type = xtce_1_3.ArgumentBaseTimeDataType

    # For some reason, the schema makes 'encoding' optional, even though in the
    # documentation attributes it states it 'must be set'. I am assuming that this is a
    # mistake in the schema, and that it should be required

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.BaseTimeDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["encoding"] = TimeEncoding._from_v1_1_kwargs(unwrap(obj.encoding))
        kwargs["reference_time"] = (
            ReferenceTime._from_v1_1_kwargs(obj.reference_time)
            if obj.reference_time is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentBaseTimeDataType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["encoding"] = TimeEncoding._from_v1_2_kwargs(unwrap(obj.encoding))
        kwargs["reference_time"] = (
            ReferenceTime._from_v1_2_kwargs(unwrap(obj.reference_time))
            if obj.reference_time is not None
            else None
        )
        kwargs["base_type"] = (
            XtcePath(obj.base_type) if obj.base_type is not None else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentBaseTimeDataType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["encoding"] = TimeEncoding._from_v1_3_kwargs(unwrap(obj.encoding))
        kwargs["reference_time"] = (
            ReferenceTime._from_v1_3_kwargs(unwrap(obj.reference_time))
            if obj.reference_time is not None
            else None
        )
        kwargs["base_type"] = (
            XtcePath(obj.base_type) if obj.base_type is not None else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="base_type",
            current_value=self.base_type,
            target_version=XtceVersion.V1_1,
            policy=policy,
            empty_value=None,
        )

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["encoding"] = self.encoding._to_v1_1(policy)
        kwargs["reference_time"] = (
            self.reference_time._to_v1_1(policy)
            if self.reference_time is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["encoding"] = self.encoding._to_v1_2(policy)
        kwargs["reference_time"] = (
            self.reference_time._to_v1_2(policy)
            if self.reference_time is not None
            else None
        )
        kwargs["base_type"] = (
            str(self.base_type) if self.base_type is not None else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["encoding"] = self.encoding._to_v1_3(policy)
        kwargs["reference_time"] = (
            self.reference_time._to_v1_3(policy)
            if self.reference_time is not None
            else None
        )
        kwargs["base_type"] = (
            str(self.base_type) if self.base_type is not None else None
        )
        return kwargs


class RelativeTimeData(BaseTimeData, ABC):
    """Abstract base class for relative time data types."""

    initial_value: datetime.timedelta | None = None
    """The initial value of the relative time data type."""

    _v1_1_type = xtce_1_1.RelativeTimeDataType
    _v1_2_type = xtce_1_2.RelativeTimeDataType
    _v1_3_type = xtce_1_3.RelativeTimeDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.RelativeTimeDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["initial_value"] = (
            xml_duration_to_timedelta(obj.initial_value)
            if obj.initial_value is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.RelativeTimeDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["initial_value"] = (
            xml_duration_to_timedelta(obj.initial_value)
            if obj.initial_value is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.RelativeTimeDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["initial_value"] = (
            xml_duration_to_timedelta(obj.initial_value)
            if obj.initial_value is not None
            else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["initial_value"] = (
            timedelta_to_xml_duration(self.initial_value)
            if self.initial_value is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["initial_value"] = (
            timedelta_to_xml_duration(self.initial_value)
            if self.initial_value is not None
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["initial_value"] = (
            timedelta_to_xml_duration(self.initial_value)
            if self.initial_value is not None
            else None
        )
        return kwargs


class ArgumentRelativeTimeData(ArgumentBaseTimeData, ABC):
    """Abstract base class for argument relative time data types."""

    initial_value: datetime.timedelta | None = None
    """The initial value of the relative time data type."""

    # XTCE 1.1 has no ArgumentRelativeTimeDataType, so this casts to RelativeTimeDataType
    _v1_1_type = xtce_1_1.RelativeTimeDataType
    _v1_2_type = xtce_1_2.ArgumentRelativeTimeDataType
    _v1_3_type = xtce_1_3.ArgumentRelativeTimeDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.RelativeTimeDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["initial_value"] = (
            xml_duration_to_timedelta(obj.initial_value)
            if obj.initial_value is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentRelativeTimeDataType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["initial_value"] = (
            xml_duration_to_timedelta(obj.initial_value)
            if obj.initial_value is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentRelativeTimeDataType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["initial_value"] = (
            xml_duration_to_timedelta(obj.initial_value)
            if obj.initial_value is not None
            else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["initial_value"] = (
            timedelta_to_xml_duration(self.initial_value)
            if self.initial_value is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["initial_value"] = (
            timedelta_to_xml_duration(self.initial_value)
            if self.initial_value is not None
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["initial_value"] = (
            timedelta_to_xml_duration(self.initial_value)
            if self.initial_value is not None
            else None
        )
        return kwargs


class AbsoluteTimeData(BaseTimeData, ABC):
    """Abstract base class for absolute time data types."""

    initial_value: datetime.datetime | None = None
    """The initial value of the absolute time data type."""

    _v1_1_type = xtce_1_1.AbsoluteTimeDataType
    _v1_2_type = xtce_1_2.AbsoluteTimeDataType
    _v1_3_type = xtce_1_3.AbsoluteTimeDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.AbsoluteTimeDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["initial_value"] = (
            obj.initial_value.to_datetime() if obj.initial_value is not None else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.AbsoluteTimeDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["initial_value"] = (
            obj.initial_value.to_datetime() if obj.initial_value is not None else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.AbsoluteTimeDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["initial_value"] = (
            obj.initial_value.to_datetime() if obj.initial_value is not None else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["initial_value"] = (
            XmlDateTime.from_datetime(self.initial_value)
            if self.initial_value is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["initial_value"] = (
            XmlDateTime.from_datetime(self.initial_value)
            if self.initial_value is not None
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["initial_value"] = (
            XmlDateTime.from_datetime(self.initial_value)
            if self.initial_value is not None
            else None
        )
        return kwargs


class ArgumentAbsoluteTimeData(ArgumentBaseTimeData, ABC):
    """Abstract base class for argument absolute time data types."""

    initial_value: datetime.datetime | None = None
    """The initial value of the absolute time data type."""

    # XTCE 1.1 has no ArgumentAbsoluteTimeDataType, so this casts to AbsoluteTimeDataType
    _v1_1_type = xtce_1_1.AbsoluteTimeDataType
    _v1_2_type = xtce_1_2.ArgumentAbsoluteTimeDataType
    _v1_3_type = xtce_1_3.ArgumentAbsoluteTimeDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.AbsoluteTimeDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["initial_value"] = (
            obj.initial_value.to_datetime() if obj.initial_value is not None else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentAbsoluteTimeDataType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["initial_value"] = (
            obj.initial_value.to_datetime() if obj.initial_value is not None else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentAbsoluteTimeDataType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["initial_value"] = (
            obj.initial_value.to_datetime() if obj.initial_value is not None else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["initial_value"] = (
            XmlDateTime.from_datetime(self.initial_value)
            if self.initial_value is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["initial_value"] = (
            XmlDateTime.from_datetime(self.initial_value)
            if self.initial_value is not None
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["initial_value"] = (
            XmlDateTime.from_datetime(self.initial_value)
            if self.initial_value is not None
            else None
        )
        return kwargs
