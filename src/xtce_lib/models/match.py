"""Match models."""

from pydantic import Field

from ._base import XtceBaseModel


class MatchCriteria(XtceBaseModel):
    pass


class DiscreteLookup(MatchCriteria):
    pass


class ContextMatch(MatchCriteria):
    pass


class DiscreteLookupList(XtceBaseModel):
    """Describe an ordered table of integer values and associated conditions, forming a
    lookup table.

    The list may have duplicates. The table is evaluated from first to last, the first
    condition to be true returns the value associated with it.

    """

    lookups: list[DiscreteLookup] = Field(default_factory=list, min_length=1)
    """Describe a lookup condition set using discrete values from parameters."""

    default_value: int = Field(...)
    """In the event that no lookup condition evaluates to true, then this value will be
    used.
    """
