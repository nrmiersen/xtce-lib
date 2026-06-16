"""Array models."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from ._base import XtceBaseModel
from .processing import ArgumentDiscreteLookupList, DiscreteLookupList

if TYPE_CHECKING:
    from .codec import ArgumentDynamicValue, DynamicValue


class Dimension(XtceBaseModel):
    starting_index: int | DynamicValue | DiscreteLookupList | None = Field(
        default=None, ge=1
    )
    ending_index: int | DynamicValue | DiscreteLookupList | None = Field(
        default=None, ge=1
    )


class ArgumentDimension(XtceBaseModel):
    starting_index: int | ArgumentDynamicValue | ArgumentDiscreteLookupList | None = (
        Field(default=None, ge=1)
    )
    ending_index: int | ArgumentDynamicValue | ArgumentDiscreteLookupList | None = (
        Field(default=None, ge=1)
    )
