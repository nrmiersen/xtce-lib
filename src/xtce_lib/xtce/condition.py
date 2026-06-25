"""Condition models."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from ._base import XtceBaseModel
from .enum import ComparisonOperator
from .reference import ArgumentInstanceRef, ParameterInstanceRef

if TYPE_CHECKING:
    from .algorithm import ArgumentInputAlgorithm, InputAlgorithm


class BaseComparison(XtceBaseModel):
    # Nothing
    pass


class Comparison(ParameterInstanceRef):
    comparison_operator: ComparisonOperator = Field(
        default=ComparisonOperator.EQUALS_SIGN_EQUALS_SIGN
    )

    value: str = Field(...)  # TODO enforce type?


class ArgumentComparison(XtceBaseModel):
    instance: ParameterInstanceRef | ArgumentInstanceRef | None = Field(default=None)
    comparison_operator: ComparisonOperator = Field(
        default=ComparisonOperator.EQUALS_SIGN_EQUALS_SIGN
    )
    value: str = Field(...)


class ComparisonCheck(BaseComparison):
    todo_name: list[ParameterInstanceRef | ComparisonOperator] = Field(
        default_factory=list,
        min_length=2,
        max_length=3,
    )
    value: str | None = Field(default=None)  # TODO enforce type?


class ArgumentComparisonCheck(BaseComparison):
    refs: list[ParameterInstanceRef | ArgumentInstanceRef] = Field(
        default_factory=list, max_length=2
    )
    comparison_operator: ComparisonOperator = Field(...)
    value: str | None = Field(default=None)


class BaseConditions(XtceBaseModel):
    # Nothing
    pass


class AndedConditions(BaseConditions):
    conditions: list[ComparisonCheck | OredConditions] = Field(
        default_factory=list, min_length=2
    )


class ArgumentAndedConditions(BaseConditions):
    conditions: list[ArgumentComparisonCheck | ArgumentOredConditions] = Field(
        default_factory=list, min_length=2
    )


class OredConditions(BaseConditions):
    conditions: list[ComparisonCheck | AndedConditions] = Field(
        default_factory=list, min_length=2
    )


class ArgumentOredConditions(BaseConditions):
    conditions: list[ArgumentComparisonCheck | ArgumentAndedConditions] = Field(
        default_factory=list, min_length=2
    )


class BooleanExpression(XtceBaseModel):
    comparison: ComparisonCheck | AndedConditions | OredConditions | None = Field(
        default=None
    )


class ArgumentBooleanExpression(XtceBaseModel):
    comparison: (
        ArgumentComparisonCheck
        | ArgumentAndedConditions
        | ArgumentOredConditions
        | None
    ) = Field(default=None)


class MatchCriteria(XtceBaseModel):
    criteria: (
        Comparison | list[Comparison] | BooleanExpression | InputAlgorithm | None
    ) = Field(
        default=None, min_length=1
    )  # TODO maybe still use separate ComparisonList object


class ArgumentMatchCriteria(XtceBaseModel):
    criteria: (
        ArgumentComparison
        | list[ArgumentComparison]
        | ArgumentBooleanExpression
        | ArgumentInputAlgorithm
        | None
    ) = Field(default=None, min_length=1)


class ContextMatch(MatchCriteria):
    # Nothing
    pass


class DiscreteLookup(MatchCriteria):
    value: int = Field(...)


class ArgumentDiscreteLookup(ArgumentMatchCriteria):
    value: int = Field(...)


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

class ArgumentDiscreteLookupList(XtceBaseModel):
    lookups: list[ArgumentDiscreteLookup] = Field(default_factory=list, min_length=1)
    default_value: int = Field(...)
