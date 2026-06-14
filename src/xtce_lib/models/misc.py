"""Miscellaneous models."""

from pydantic import Field

from ._base import XtceBaseModel
from .codec import DynamicValue
from .processing import DiscreteLookupList


class Repeat(XtceBaseModel):
    count: int | DynamicValue | DiscreteLookupList | None = Field(default=None)
    offset: int | DynamicValue | DiscreteLookupList | None = Field(default=None)


class Constant(XtceBaseModel):
    constant_name: str = Field(...)
    value: str = Field(
        ...
    )  # TODO figure out how this is represented in xsd, should I enforce some types here?
