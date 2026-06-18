"""Range models."""

from pydantic import Field

from ._base import XtceBaseModel
from .enum import ConcernLevel, RangeForm


class IntegerRange(XtceBaseModel):
    min_inclusive: int | None = Field(default=None)
    max_inclusive: int | None = Field(default=None)


class ValidIntegerRange(IntegerRange):
    valid_range_applies_to_calibrated: bool = Field(default=True)


# TODO figure out what to do with the int/float valid ranges cause they're nested in their data type classes
class ValidIntegerRanges(XtceBaseModel):
    valid_ranges: list[IntegerRange] = Field(default_factory=list, min_length=1)
    valid_range_applies_to_calibrated: bool = Field(default=True)


class FloatRange(XtceBaseModel):
    min_inclusive: float | None = Field(default=None)
    min_exclusive: float | None = Field(default=None)
    max_inclusive: float | None = Field(default=None)
    max_exclusive: float | None = Field(default=None)


class ValidFloatRange(FloatRange):
    valid_range_applies_to_calibrated: bool = Field(default=True)


class ValidFloatRanges(XtceBaseModel):
    valid_ranges: list[FloatRange] = Field(default_factory=list, min_length=1)
    valid_range_applies_to_calibrated: bool = Field(default=True)


class MultiRangeType(FloatRange):
    range_form: RangeForm = Field(default=RangeForm.OUTSIDE)
    level: ConcernLevel | None = Field(default=None)
