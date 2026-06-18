"""Miscellaneous models."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from ._base import XtceBaseModel

if TYPE_CHECKING:
    from .codec import ArgumentDynamicValue, DynamicValue
    from .processing import ArgumentDiscreteLookupList, DiscreteLookupList


class Repeat(XtceBaseModel):
    count: int | DynamicValue | DiscreteLookupList | None = Field(default=None)
    offset: int | DynamicValue | DiscreteLookupList | None = Field(default=None)


class ArgumentRepeat(XtceBaseModel):
    count: int | ArgumentDynamicValue | ArgumentDiscreteLookupList | None = Field(
        default=None
    )
    offset: int | ArgumentDynamicValue | ArgumentDiscreteLookupList | None = Field(
        default=None
    )


class Constant(XtceBaseModel):
    constant_name: str = Field(...)
    value: str = Field(
        ...
    )  # TODO figure out how this is represented in xsd, should I enforce some types here?
