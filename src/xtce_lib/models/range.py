"""Range models."""

from pydantic import Field

from ._base import XtceBaseModel
from .enum import ConcernLevel, RangeForm


class FloatRange(XtceBaseModel):
    min_inclusive: float | None = Field(default=None)
    min_exclusive: float | None = Field(default=None)
    max_inclusive: float | None = Field(default=None)
    max_exclusive: float | None = Field(default=None)


class IntegerRange(XtceBaseModel):
    min_inclusive: int | None = Field(default=None)
    max_inclusive: int | None = Field(default=None)


class MultiRangeType(FloatRange):
    range_form: RangeForm = Field(default=RangeForm.OUTSIDE)
    level: ConcernLevel | None = Field(default=None)


class ValidIntegerRange(IntegerRange):
    valid_range_applies_to_calibrated: bool = Field(default=True)


class ValidFloatRange(FloatRange):
    valid_range_applies_to_calibrated: bool = Field(default=True)


# TODO figure out what to do with the int/float valid ranges cause they're nested in their data type classes
