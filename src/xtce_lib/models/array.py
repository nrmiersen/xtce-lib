"""Array models."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from ._base import XtceBaseModel
from .processing import DiscreteLookupList

if TYPE_CHECKING:
    from .codec import DynamicValue


class Dimension(XtceBaseModel):
    starting_index: int | DynamicValue | DiscreteLookupList = Field(..., ge=1)
    ending_index: int | DynamicValue | DiscreteLookupList = Field(..., ge=1)
