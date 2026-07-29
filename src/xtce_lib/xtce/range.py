"""Range models."""

from typing import Any, Self

from pydantic import Field, model_validator

from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from ._util import coerce_optional_int, unwrap
from .enum import ConcernLevel, RangeForm


class IntegerRange(XtceBaseModel):
    """A range of integer numbers."""

    min_inclusive: int | str | None = Field(default=None)
    """The minimum value of the range, including itself.

    Hex, octal, and binary literals are accepted as strings for XTCE 1.1 compatibility,
    but will be coerced to integers for all future versions.

    """

    max_inclusive: int | str | None = Field(default=None)
    """The maximum value of the range, including itself.

    Hex, octal, and binary literals are accepted as strings for XTCE 1.1 compatibility,
    but will be coerced to integers for all future versions.

    """

    @model_validator(mode="after")
    def validate_range(self) -> Self:
        """Validate that the minimum value is less than or equal to the maximum
        value.
        """
        min_val = coerce_optional_int(self.min_inclusive)
        max_val = coerce_optional_int(self.max_inclusive)

        if min_val is None and max_val is None:
            raise ValueError(
                "at least one of min_inclusive or max_inclusive must be set"
            )

        if min_val is not None and max_val is not None:
            if min_val > max_val:
                raise ValueError(
                    f"minimum value ({min_val}) cannot be greater than maximum "
                    f"value ({max_val})"
                )

        return self

    _v1_1_type = xtce_1_1.IntegerRangeType
    _v1_2_type = xtce_1_2.IntegerRangeType
    _v1_3_type = xtce_1_3.IntegerRangeType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.IntegerRangeType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["min_inclusive"] = coerce_optional_int(obj.min_inclusive)
        kwargs["max_inclusive"] = coerce_optional_int(obj.max_inclusive)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.IntegerRangeType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["min_inclusive"] = obj.min_inclusive
        kwargs["max_inclusive"] = obj.max_inclusive
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.IntegerRangeType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["min_inclusive"] = obj.min_inclusive
        kwargs["max_inclusive"] = obj.max_inclusive
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["min_inclusive"] = self.min_inclusive
        kwargs["max_inclusive"] = self.max_inclusive
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["min_inclusive"] = coerce_optional_int(self.min_inclusive)
        kwargs["max_inclusive"] = coerce_optional_int(self.max_inclusive)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["min_inclusive"] = coerce_optional_int(self.min_inclusive)
        kwargs["max_inclusive"] = coerce_optional_int(self.max_inclusive)
        return kwargs


class ValidIntegerRange(IntegerRange):
    """A range of integer numbers.

    Contains an optional flag to indicate whether the range applies to calibrated
    values.

    """

    applies_to_calibrated: bool = Field(default=True)
    """Whether this valid range applies to calibrated values.

    If False, it applies to raw values.

    """

    _v1_1_type = None
    _v1_2_type = xtce_1_2.IntegerDataType.ValidRange
    _v1_3_type = xtce_1_3.IntegerDataType.ValidRange

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.IntegerDataType.ValidRange
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["applies_to_calibrated"] = obj.valid_range_applies_to_calibrated
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.IntegerDataType.ValidRange
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["applies_to_calibrated"] = obj.valid_range_applies_to_calibrated
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["valid_range_applies_to_calibrated"] = self.applies_to_calibrated
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["valid_range_applies_to_calibrated"] = self.applies_to_calibrated
        return kwargs


class ValidIntegerRanges(XtceBaseModel):
    """A collection of valid integer ranges.

    A single range is the most common, but multiple ranges can be used to specify non-
    contiguous valid values.

    """

    valid_ranges: list[IntegerRange] = Field(default_factory=list, min_length=1)
    """Defines one or more valid ranges.

    Multiple ranges can be used to specify non- contiguous valid values. Typically, only
    one range is used. In cases where multiple ranges are used, then the value is valid
    when it is valid in any of the provided ranges.

    """

    applies_to_calibrated: bool = Field(default=True)
    """Whether these valid ranges apply to calibrated values.

    If False, they apply to raw values.

    """

    _v1_1_type = None
    _v1_2_type = xtce_1_2.ValidIntegerRangeSetType
    _v1_3_type = xtce_1_3.ValidIntegerRangeSetType

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ValidIntegerRangeSetType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["valid_ranges"] = [
            IntegerRange._from_v1_2(range) for range in obj.valid_range
        ]
        kwargs["applies_to_calibrated"] = obj.valid_range_applies_to_calibrated
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ValidIntegerRangeSetType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["valid_ranges"] = [
            IntegerRange._from_v1_3(range) for range in obj.valid_range
        ]
        kwargs["applies_to_calibrated"] = obj.valid_range_applies_to_calibrated
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["valid_range"] = [range._to_v1_2(policy) for range in self.valid_ranges]
        kwargs["valid_range_applies_to_calibrated"] = self.applies_to_calibrated
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["valid_range"] = [range._to_v1_3(policy) for range in self.valid_ranges]
        kwargs["valid_range_applies_to_calibrated"] = self.applies_to_calibrated
        return kwargs


class FloatRange(XtceBaseModel):
    """A range of floating-point numbers.

    Options for both inclusive and exclusive minimum and maximum values are provided,
    but only one of the minimum options and one of the maximum options can be used at a
    time.

    """

    min_inclusive: float | None = Field(default=None)
    """The minimum value of the range, including itself."""

    min_exclusive: float | None = Field(default=None)
    """The minimum value of the range, excluding itself."""

    max_inclusive: float | None = Field(default=None)
    """The maximum value of the range, including itself."""

    max_exclusive: float | None = Field(default=None)
    """The maximum value of the range, excluding itself."""

    @model_validator(mode="after")
    def validate_range(self) -> Self:
        """Validate that the minimum value is less than or equal to the maximum value,
        and that only one of the minimum options and one of the maximum options are used
        at a time.
        """
        if self.min_inclusive is not None and self.min_exclusive is not None:
            raise ValueError("only one of min_inclusive and min_exclusive can be set")

        if self.max_inclusive is not None and self.max_exclusive is not None:
            raise ValueError("only one of max_inclusive and max_exclusive can be set")

        effective_min = (
            self.min_inclusive if self.min_inclusive is not None else self.min_exclusive
        )
        effective_max = (
            self.max_inclusive if self.max_inclusive is not None else self.max_exclusive
        )

        if effective_min is None and effective_max is None:
            raise ValueError(
                "at least one of the minimum or maximum values must be set"
            )

        if (
            effective_min is not None
            and effective_max is not None
            and effective_min > effective_max
        ):
            raise ValueError(
                f"minimum value ({effective_min}) cannot be greater than maximum "
                f"value ({effective_max})"
            )

        return self

    _v1_1_type = xtce_1_1.FloatRangeType
    _v1_2_type = xtce_1_2.FloatRangeType
    _v1_3_type = xtce_1_3.FloatRangeType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.FloatRangeType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["min_inclusive"] = obj.min_inclusive
        kwargs["min_exclusive"] = obj.min_exclusive
        kwargs["max_inclusive"] = obj.max_inclusive
        kwargs["max_exclusive"] = obj.max_exclusive
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.FloatRangeType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["min_inclusive"] = obj.min_inclusive
        kwargs["min_exclusive"] = obj.min_exclusive
        kwargs["max_inclusive"] = obj.max_inclusive
        kwargs["max_exclusive"] = obj.max_exclusive
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.FloatRangeType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["min_inclusive"] = obj.min_inclusive
        kwargs["min_exclusive"] = obj.min_exclusive
        kwargs["max_inclusive"] = obj.max_inclusive
        kwargs["max_exclusive"] = obj.max_exclusive
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["min_inclusive"] = self.min_inclusive
        kwargs["min_exclusive"] = self.min_exclusive
        kwargs["max_inclusive"] = self.max_inclusive
        kwargs["max_exclusive"] = self.max_exclusive
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["min_inclusive"] = self.min_inclusive
        kwargs["min_exclusive"] = self.min_exclusive
        kwargs["max_inclusive"] = self.max_inclusive
        kwargs["max_exclusive"] = self.max_exclusive
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["min_inclusive"] = self.min_inclusive
        kwargs["min_exclusive"] = self.min_exclusive
        kwargs["max_inclusive"] = self.max_inclusive
        kwargs["max_exclusive"] = self.max_exclusive
        return kwargs


class ValidFloatRange(FloatRange):
    """A range of floating-point numbers.

    Contains an optional flag to indicate whether the range applies to calibrated
    values.

    """

    applies_to_calibrated: bool = Field(default=True)

    _v1_1_type = None
    _v1_2_type = xtce_1_2.FloatDataType.ValidRange
    _v1_3_type = xtce_1_3.FloatDataType.ValidRange

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.FloatDataType.ValidRange
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["applies_to_calibrated"] = obj.valid_range_applies_to_calibrated
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.FloatDataType.ValidRange
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["applies_to_calibrated"] = obj.valid_range_applies_to_calibrated
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["valid_range_applies_to_calibrated"] = self.applies_to_calibrated
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["valid_range_applies_to_calibrated"] = self.applies_to_calibrated
        return kwargs


class ValidFloatRanges(XtceBaseModel):
    """A collection of valid float ranges.

    A single range is the most common, but multiple ranges can be used to specify non-
    contiguous valid values.

    """

    valid_ranges: list[FloatRange] = Field(default_factory=list, min_length=1)
    """Defines one or more valid ranges.

    Multiple ranges can be used to specify non- contiguous valid values. Typically, only
    one range is used. In cases where multiple ranges are used, then the value is valid
    when it is valid in any of the provided ranges.

    """

    applies_to_calibrated: bool = Field(default=True)
    """Whether these valid ranges apply to calibrated values.

    If False, they apply to raw values.

    """

    _v1_1_type = None
    _v1_2_type = xtce_1_2.ValidFloatRangeSetType
    _v1_3_type = xtce_1_3.ValidFloatRangeSetType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ValidFloatRangeSetType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["valid_ranges"] = [
            FloatRange._from_v1_2(range) for range in obj.valid_range
        ]
        kwargs["applies_to_calibrated"] = obj.valid_range_applies_to_calibrated
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ValidFloatRangeSetType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["valid_ranges"] = [
            FloatRange._from_v1_3(range) for range in obj.valid_range
        ]
        kwargs["applies_to_calibrated"] = obj.valid_range_applies_to_calibrated
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["valid_range"] = [range._to_v1_2(policy) for range in self.valid_ranges]
        kwargs["valid_range_applies_to_calibrated"] = self.applies_to_calibrated
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["valid_range"] = [range._to_v1_3(policy) for range in self.valid_ranges]
        kwargs["valid_range_applies_to_calibrated"] = self.applies_to_calibrated
        return kwargs


class MultiRange(FloatRange):
    """An entry in a multi-range alarm definition.

    This allows for alarm ranges that go beyond the typical "inside" and "outside" range
    definitions.

    """

    range_form: RangeForm = Field(default=RangeForm.OUTSIDE)
    """The form of the range.

    A value of `OUTSIDE` specifies that the most severe range is outside all the other
    ranges:

        -severe -critical -distress -warning -watch
        normal
        +watch +warning +distress +critical +severe

    This means each min, max pair are a range: (-inf, min) or (-inf, min], and
    [max, inf) or (max, inf). However a value of `INSIDE` "inverts" these bands:

        -normal -watch -warning -distress -critical
        severe
        +critical +distress +warning +watch +normal

    This means each min, max pair form a range of (min, max) or [min, max) or (min, max]
    or [min, max]. The most common form used is `OUTSIDE` and it is the default (The set
    notation used defines parenthesis as exclusive and square brackets as inclusive).

    """

    level: ConcernLevel
    """The concern level of this alarm range."""

    _v1_1_type = None
    _v1_2_type = xtce_1_2.MultiRangeType
    _v1_3_type = xtce_1_3.MultiRangeType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.MultiRangeType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["range_form"] = RangeForm(obj.range_form.value)
        kwargs["level"] = ConcernLevel(unwrap(obj.level).value)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.MultiRangeType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["range_form"] = RangeForm(obj.range_form.value)
        kwargs["level"] = ConcernLevel(unwrap(obj.level).value)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["range_form"] = xtce_1_2.RangeFormType(self.range_form)
        kwargs["level"] = xtce_1_2.ConcernLevelsType(self.level)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["range_form"] = xtce_1_3.RangeFormType(self.range_form)
        kwargs["level"] = xtce_1_3.ConcernLevelsType(self.level)
        return kwargs
