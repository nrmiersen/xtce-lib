"""Condition models."""

from __future__ import annotations

import datetime
from abc import ABC
from typing import TYPE_CHECKING, Self

from pydantic import Field

from xtce_lib.common.xtce_path import XtcePath
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3
from xtce_lib.xtce._util import coerce

from ._base import XtceBaseModel
from .enum import ComparisonOperator
from .reference import ArgumentInstanceRef, ParameterInstanceRef

if TYPE_CHECKING:
    from .algorithm import ArgumentInputAlgorithm, InputAlgorithm


class BaseComparison(XtceBaseModel, ABC):
    """Base class for comparison checks."""


class Comparison(ParameterInstanceRef):
    """A comparison of a parameter instance to a value."""

    comparison_operator: ComparisonOperator = ComparisonOperator.EQ
    """The operator to use for the comparison."""

    value: int | float | str | bool | bytes | datetime.timedelta | datetime.datetime
    """The value to compare the parameter instance against."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.ComparisonType) -> Self:
        return cls(
            ref=XtcePath(raw_obj.parameter_ref),
            instance=raw_obj.instance,
            use_calibrated_value=raw_obj.use_calibrated_value,
            comparison_operator=ComparisonOperator._from_v1_1(
                raw_obj.comparison_operator
            ),
            value=coerce(raw_obj.value),
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.ComparisonType) -> Self:
        return cls(
            ref=XtcePath(raw_obj.parameter_ref),
            instance=raw_obj.instance,
            use_calibrated_value=raw_obj.use_calibrated_value,
            comparison_operator=ComparisonOperator._from_v1_2(
                raw_obj.comparison_operator
            ),
            value=coerce(raw_obj.value),
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.ComparisonType) -> Self:
        return cls(
            ref=XtcePath(raw_obj.parameter_ref),
            instance=raw_obj.instance,
            use_calibrated_value=raw_obj.use_calibrated_value,
            comparison_operator=ComparisonOperator._from_v1_3(
                raw_obj.comparison_operator
            ),
            value=coerce(raw_obj.value),
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.ComparisonType:
        return xtce_1_1.ComparisonType(
            parameter_ref=str(self.ref),
            instance=self.instance,
            use_calibrated_value=self.use_calibrated_value,
            comparison_operator=self.comparison_operator._to_v1_1(policy),
            value=str(self.value),
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ComparisonType:
        return xtce_1_2.ComparisonType(
            parameter_ref=str(self.ref),
            instance=self.instance,
            use_calibrated_value=self.use_calibrated_value,
            comparison_operator=self.comparison_operator._to_v1_2(policy),
            value=str(self.value),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ComparisonType:
        return xtce_1_3.ComparisonType(
            parameter_ref=str(self.ref),
            instance=self.instance,
            use_calibrated_value=self.use_calibrated_value,
            comparison_operator=self.comparison_operator._to_v1_3(policy),
            value=str(self.value),
        )


class ArgumentComparison(XtceBaseModel):
    instance: ParameterInstanceRef | ArgumentInstanceRef | None = Field(default=None)
    comparison_operator: ComparisonOperator = Field(default=ComparisonOperator.EQ)
    value: str


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
    comparison_operator: ComparisonOperator
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
    value: int


class ArgumentDiscreteLookup(ArgumentMatchCriteria):
    value: int


class DiscreteLookupList(XtceBaseModel):
    """Describe an ordered table of integer values and associated conditions, forming a
    lookup table.

    The list may have duplicates. The table is evaluated from first to last, the first
    condition to be true returns the value associated with it.

    """

    lookups: list[DiscreteLookup] = Field(default_factory=list, min_length=1)
    """Describe a lookup condition set using discrete values from parameters."""

    default_value: int
    """In the event that no lookup condition evaluates to true, then this value will be
    used.
    """

class ArgumentDiscreteLookupList(XtceBaseModel):
    lookups: list[ArgumentDiscreteLookup] = Field(default_factory=list, min_length=1)
    default_value: int
