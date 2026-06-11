"""Range models."""

from pydantic import Field

from ._base import XtceBaseModel
from .enums import ConcernLevel, RangeForm


class FloatRange(XtceBaseModel):
    min_inclusive: float | None = Field(default=None)
    min_exclusive: float | None = Field(default=None)
    max_inclusive: float | None = Field(default=None)
    max_exclusive: float | None = Field(default=None)


class MultiRangeType(FloatRange):
    range_form: RangeForm = Field(default=RangeForm.OUTSIDE)
    level: ConcernLevel | None = Field(default=None)
