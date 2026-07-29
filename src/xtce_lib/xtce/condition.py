"""Condition models."""

from __future__ import annotations

import datetime
from abc import ABC
from typing import TYPE_CHECKING, Any

from pydantic import Field

from xtce_lib.common.xtce_path import XtcePath
from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3
from xtce_lib.xtce._util import coerce, uncoerce, unwrap

from ._base import XtceBaseModel
from .enum import ComparisonOperator
from .reference import ArgumentInstanceRef, ParameterInstanceRef

if TYPE_CHECKING:
    from .algorithm import ArgumentInputAlgorithm, InputAlgorithm


class BaseComparison(XtceBaseModel, ABC):
    """Define shared behavior for comparison checks."""


class Comparison(ParameterInstanceRef):
    """Define a comparison of a parameter instance to a value."""

    comparison_operator: ComparisonOperator = ComparisonOperator.EQ
    """The operator to use for the comparison."""

    value: int | float | str | bool | bytes | datetime.timedelta | datetime.datetime
    """The value to compare the parameter instance against."""

    _v1_1_type = xtce_1_1.ComparisonType
    _v1_2_type = xtce_1_2.ComparisonType
    _v1_3_type = xtce_1_3.ComparisonType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.ComparisonType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.parameter_ref)
        kwargs["instance"] = obj.instance
        kwargs["use_calibrated_value"] = obj.use_calibrated_value
        kwargs["comparison_operator"] = ComparisonOperator._from_v1_1(
            obj.comparison_operator
        )
        kwargs["value"] = coerce(obj.value)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ComparisonType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.parameter_ref)
        kwargs["instance"] = obj.instance
        kwargs["use_calibrated_value"] = obj.use_calibrated_value
        kwargs["comparison_operator"] = ComparisonOperator._from_v1_2(
            obj.comparison_operator
        )
        kwargs["value"] = coerce(obj.value)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ComparisonType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.parameter_ref)
        kwargs["instance"] = obj.instance
        kwargs["use_calibrated_value"] = obj.use_calibrated_value
        kwargs["comparison_operator"] = ComparisonOperator._from_v1_3(
            obj.comparison_operator
        )
        kwargs["value"] = coerce(obj.value)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["parameter_ref"] = str(self.ref)
        kwargs["instance"] = self.instance
        kwargs["use_calibrated_value"] = self.use_calibrated_value
        kwargs["comparison_operator"] = self.comparison_operator._to_v1_1(policy)
        kwargs["value"] = uncoerce(self.value)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["parameter_ref"] = str(self.ref)
        kwargs["instance"] = self.instance
        kwargs["use_calibrated_value"] = self.use_calibrated_value
        kwargs["comparison_operator"] = self.comparison_operator._to_v1_2(policy)
        kwargs["value"] = uncoerce(self.value)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["parameter_ref"] = str(self.ref)
        kwargs["instance"] = self.instance
        kwargs["use_calibrated_value"] = self.use_calibrated_value
        kwargs["comparison_operator"] = self.comparison_operator._to_v1_3(policy)
        kwargs["value"] = uncoerce(self.value)
        return kwargs


class ArgumentComparison(XtceBaseModel):
    """Define a comparison of a parameter or argument instance to a value."""

    instance_ref: ParameterInstanceRef | ArgumentInstanceRef
    """The instance of the parameter or argument to compare."""

    comparison_operator: ComparisonOperator = ComparisonOperator.EQ
    """The operator to use for the comparison."""

    value: int | float | str | bool | bytes | datetime.timedelta | datetime.datetime
    """The value to compare the parameter or argument instance against."""

    _v1_1_type = None
    _v1_2_type = xtce_1_2.ArgumentComparisonType
    _v1_3_type = xtce_1_3.ArgumentComparisonType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ArgumentComparisonType) -> dict[str, Any]:
        if isinstance(obj.choice, xtce_1_2.ParameterInstanceRefType):
            instance = ParameterInstanceRef._from_v1_2(obj.choice)
        else:
            instance = ArgumentInstanceRef._from_v1_2(unwrap(obj.choice))

        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["instance_ref"] = instance
        kwargs["comparison_operator"] = ComparisonOperator._from_v1_2(
            obj.comparison_operator
        )
        kwargs["value"] = coerce(obj.value)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ArgumentComparisonType) -> dict[str, Any]:
        if isinstance(obj.choice, xtce_1_3.ParameterInstanceRefType):
            instance = ParameterInstanceRef._from_v1_3(obj.choice)
        else:
            instance = ArgumentInstanceRef._from_v1_3(unwrap(obj.choice))

        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["instance_ref"] = instance
        kwargs["comparison_operator"] = ComparisonOperator._from_v1_3(
            obj.comparison_operator
        )
        kwargs["value"] = coerce(obj.value)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = self.instance_ref._to_v1_2(policy)
        kwargs["comparison_operator"] = self.comparison_operator._to_v1_2(policy)
        kwargs["value"] = uncoerce(self.value)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = self.instance_ref._to_v1_3(policy)
        kwargs["comparison_operator"] = self.comparison_operator._to_v1_3(policy)
        kwargs["value"] = uncoerce(self.value)
        return kwargs


class ComparisonCheck(BaseComparison):
    """Define a comparison against either a literal value or another parameter."""

    # The xsdata representation of this is very odd. The first element is a 2 or 3
    # element array of either:
    # [ParameterInstanceRef, ComparisonOperator]
    # [ParameterInstanceRef, ComparisonOperator, ParameterInstanceRef]
    # Then a single optional `value` element. It ends up being a pretty rough API. This
    # structure below is a better representation of the XSD structure but requires some
    # additional steps to handle the translation

    left: ParameterInstanceRef
    """The left-hand side of the comparison."""

    comparison_operator: ComparisonOperator
    """The operator to use for the comparison."""

    right: (
        ParameterInstanceRef
        | int
        | float
        | str
        | bool
        | bytes
        | datetime.timedelta
        | datetime.datetime
    )
    """The right-hand side of the comparison.

    Can be either a parameter instance reference or a literal value.

    """

    _v1_1_type = xtce_1_1.ComparisonCheckType
    _v1_2_type = xtce_1_2.ComparisonCheckType
    _v1_3_type = xtce_1_3.ComparisonCheckType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.ComparisonCheckType) -> dict[str, Any]:
        items = list(obj.choice)

        left_raw, op_raw = items[0], items[1]

        if not isinstance(left_raw, xtce_1_1.ParameterInstanceRefType):
            raise TypeError(
                "invalid ComparisonCheckType.choice[0]: expected "
                "ParameterInstanceRefType, got "
                f"{type(left_raw).__name__}"
            )
        if not isinstance(op_raw, xtce_1_1.ComparisonOperatorsType):
            raise TypeError(
                "invalid ComparisonCheckType.choice[1]: expected "
                "ComparisonOperatorsType, got "
                f"{type(op_raw).__name__}"
            )

        if len(items) == 3:
            right_raw = items[2]
            if not isinstance(right_raw, xtce_1_1.ParameterInstanceRefType):
                raise TypeError(
                    "invalid ComparisonCheckType.choice[2]: expected "
                    "ParameterInstanceRefType, got "
                    f"{type(right_raw).__name__}"
                )
            right = ParameterInstanceRef._from_v1_1(right_raw)
        else:
            if obj.value is None:
                raise ValueError("missing right-hand side value for comparison")
            right = coerce(obj.value)

        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["left"] = ParameterInstanceRef._from_v1_1(left_raw)
        kwargs["comparison_operator"] = ComparisonOperator._from_v1_1(op_raw)
        kwargs["right"] = right
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ComparisonCheckType) -> dict[str, Any]:
        items = list(obj.choice)

        left_raw, op_raw = items[0], items[1]

        if not isinstance(left_raw, xtce_1_2.ParameterInstanceRefType):
            raise TypeError(
                "invalid ComparisonCheckType.choice[0]: expected "
                "ParameterInstanceRefType, got "
                f"{type(left_raw).__name__}"
            )
        if not isinstance(op_raw, xtce_1_2.ComparisonOperatorsType):
            raise TypeError(
                "invalid ComparisonCheckType.choice[1]: expected "
                "ComparisonOperatorsType, got "
                f"{type(op_raw).__name__}"
            )

        if len(items) == 3:
            right_raw = items[2]
            if not isinstance(right_raw, xtce_1_2.ParameterInstanceRefType):
                raise TypeError(
                    "invalid ComparisonCheckType.choice[2]: expected "
                    "ParameterInstanceRefType, got "
                    f"{type(right_raw).__name__}"
                )
            right = ParameterInstanceRef._from_v1_2(right_raw)
        else:
            if obj.value is None:
                raise ValueError("missing right-hand side value for comparison")
            right = coerce(obj.value)

        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["left"] = ParameterInstanceRef._from_v1_2(left_raw)
        kwargs["comparison_operator"] = ComparisonOperator._from_v1_2(op_raw)
        kwargs["right"] = right
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ComparisonCheckType) -> dict[str, Any]:
        items = list(obj.choice)

        left_raw, op_raw = items[0], items[1]

        if not isinstance(left_raw, xtce_1_3.ParameterInstanceRefType):
            raise TypeError(
                "invalid ComparisonCheckType.choice[0]: expected "
                "ParameterInstanceRefType, got "
                f"{type(left_raw).__name__}"
            )
        if not isinstance(op_raw, xtce_1_3.ComparisonOperatorsType):
            raise TypeError(
                "invalid ComparisonCheckType.choice[1]: expected "
                "ComparisonOperatorsType, got "
                f"{type(op_raw).__name__}"
            )

        if len(items) == 3:
            right_raw = items[2]
            if not isinstance(right_raw, xtce_1_3.ParameterInstanceRefType):
                raise TypeError(
                    "invalid ComparisonCheckType.choice[2]: expected "
                    "ParameterInstanceRefType, got "
                    f"{type(right_raw).__name__}"
                )
            right = ParameterInstanceRef._from_v1_3(right_raw)
        else:
            if obj.value is None:
                raise ValueError("missing right-hand side value for comparison")
            right = coerce(obj.value)

        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["left"] = ParameterInstanceRef._from_v1_3(left_raw)
        kwargs["comparison_operator"] = ComparisonOperator._from_v1_3(op_raw)
        kwargs["right"] = right
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        choice = [
            self.left._to_v1_1(policy),
            self.comparison_operator._to_v1_1(policy),
        ]
        if isinstance(self.right, ParameterInstanceRef):
            choice.append(self.right._to_v1_1(policy))
            value = None
        else:
            value = uncoerce(self.right)

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["choice"] = choice
        kwargs["value"] = value
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        choice = [
            self.left._to_v1_2(policy),
            self.comparison_operator._to_v1_2(policy),
        ]
        if isinstance(self.right, ParameterInstanceRef):
            choice.append(self.right._to_v1_2(policy))
            value = None
        else:
            value = uncoerce(self.right)

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = choice
        kwargs["value"] = value
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        choice = [
            self.left._to_v1_3(policy),
            self.comparison_operator._to_v1_3(policy),
        ]
        if isinstance(self.right, ParameterInstanceRef):
            choice.append(self.right._to_v1_3(policy))
            value = None
        else:
            value = uncoerce(self.right)

        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = choice
        kwargs["value"] = value
        return kwargs


class ArgumentComparisonCheck(BaseComparison):
    """Define a comparison against either a literal value or another instance."""

    # The xsdata representation of this is very odd. The first element is a 1 or 2
    # element array of either:
    # [ParameterInstanceRefType]
    # [ArgumentInstanceRefType]
    # [ParameterInstanceRefType, ArgumentInstanceRefType]
    # [ParameterInstanceRefType, ParameterInstanceRefType]
    # [ArgumentInstanceRefType, ArgumentInstanceRefType]
    # [ParameterInstanceRefType, ArgumentInstanceRefType]
    # Then a single optional `value` element. It ends up being a pretty rough API. This
    # structure below is a better representation of the XSD structure but requires some
    # additional steps to handle the translation

    left: ParameterInstanceRef | ArgumentInstanceRef
    """The left-hand side of the comparison."""

    comparison_operator: ComparisonOperator
    """The operator to use for the comparison."""

    right: (
        ParameterInstanceRef
        | ArgumentInstanceRef
        | int
        | float
        | str
        | bool
        | bytes
        | datetime.timedelta
        | datetime.datetime
    )
    """The right-hand side of the comparison.

    Can be either a parameter or argument instance reference or a literal value.

    """

    _v1_1_type = None
    _v1_2_type = xtce_1_2.ArgumentComparisonCheckType
    _v1_3_type = xtce_1_3.ArgumentComparisonCheckType

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentComparisonCheckType
    ) -> dict[str, Any]:
        def unpack_instance_ref(
            raw: xtce_1_2.ParameterInstanceRefType | xtce_1_2.ArgumentInstanceRefType,
        ):
            if isinstance(raw, xtce_1_2.ParameterInstanceRefType):
                return ParameterInstanceRef._from_v1_2(raw)
            elif isinstance(raw, xtce_1_2.ArgumentInstanceRefType):
                return ArgumentInstanceRef._from_v1_2(raw)
            else:
                raise TypeError(
                    "invalid ArgumentComparisonCheckType.choice element: expected "
                    "ParameterInstanceRefType or ArgumentInstanceRefType, got "
                    f"{type(raw).__name__}"
                )

        items = list(obj.choice)

        if len(items) == 1:
            left_raw, right_raw = items[0], None
        else:
            left_raw, right_raw = items[0], items[1]

        if right_raw is not None:
            right = unpack_instance_ref(right_raw)
        else:
            if obj.value is None:
                raise ValueError("missing right-hand side value for comparison")
            right = coerce(obj.value)

        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["left"] = unpack_instance_ref(left_raw)
        kwargs["comparison_operator"] = ComparisonOperator._from_v1_2(
            obj.comparison_operator
        )
        kwargs["right"] = right
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentComparisonCheckType
    ) -> dict[str, Any]:
        def unpack_instance_ref(
            raw: xtce_1_3.ParameterInstanceRefType | xtce_1_3.ArgumentInstanceRefType,
        ):
            if isinstance(raw, xtce_1_3.ParameterInstanceRefType):
                return ParameterInstanceRef._from_v1_3(raw)
            elif isinstance(raw, xtce_1_3.ArgumentInstanceRefType):
                return ArgumentInstanceRef._from_v1_3(raw)
            else:
                raise TypeError(
                    "invalid ArgumentComparisonCheckType.choice element: expected "
                    "ParameterInstanceRefType or ArgumentInstanceRefType, got "
                    f"{type(raw).__name__}"
                )

        items = list(obj.choice)

        if len(items) == 1:
            left_raw, right_raw = items[0], None
        else:
            left_raw, right_raw = items[0], items[1]

        if right_raw is not None:
            right = unpack_instance_ref(right_raw)
        else:
            if obj.value is None:
                raise ValueError("missing right-hand side value for comparison")
            right = coerce(obj.value)

        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["left"] = unpack_instance_ref(left_raw)
        kwargs["comparison_operator"] = ComparisonOperator._from_v1_3(
            obj.comparison_operator
        )
        kwargs["right"] = right
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        choice = [self.left._to_v1_2(policy)]
        if isinstance(self.right, (ParameterInstanceRef, ArgumentInstanceRef)):
            choice.append(self.right._to_v1_2(policy))
            value = None
        else:
            value = uncoerce(self.right)

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = choice
        kwargs["comparison_operator"] = self.comparison_operator._to_v1_2(policy)
        kwargs["value"] = value
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        choice = [self.left._to_v1_3(policy)]
        if isinstance(self.right, (ParameterInstanceRef, ArgumentInstanceRef)):
            choice.append(self.right._to_v1_3(policy))
            value = None
        else:
            value = uncoerce(self.right)

        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = choice
        kwargs["comparison_operator"] = self.comparison_operator._to_v1_3(policy)
        kwargs["value"] = value
        return kwargs


class BaseConditions(XtceBaseModel, ABC):
    """Define shared behavior for grouped condition expressions."""


class AndedConditions(BaseConditions):
    """Define a logical AND of multiple conditions."""

    conditions: list[ComparisonCheck | OredConditions] = Field(min_length=2)
    """The list of conditions that are ANDed together."""

    _v1_1_type = xtce_1_1.AndedConditionsType
    _v1_2_type = xtce_1_2.AndedConditionsType
    _v1_3_type = xtce_1_3.AndedConditionsType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.AndedConditionsType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["conditions"] = [
            ComparisonCheck._from_v1_1(c)
            if isinstance(c, xtce_1_1.ComparisonCheckType)
            else OredConditions._from_v1_1(c)
            for c in obj.choice
        ]
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.AndedConditionsType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["conditions"] = [
            ComparisonCheck._from_v1_2(c)
            if isinstance(c, xtce_1_2.ComparisonCheckType)
            else OredConditions._from_v1_2(c)
            for c in obj.choice
        ]
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.AndedConditionsType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["conditions"] = [
            ComparisonCheck._from_v1_3(c)
            if isinstance(c, xtce_1_3.ComparisonCheckType)
            else OredConditions._from_v1_3(c)
            for c in obj.choice
        ]
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["choice"] = [c._to_v1_1(policy) for c in self.conditions]
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = [c._to_v1_2(policy) for c in self.conditions]
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = [c._to_v1_3(policy) for c in self.conditions]
        return kwargs


class ArgumentAndedConditions(BaseConditions):
    """Define a logical AND of multiple argument conditions."""

    conditions: list[ArgumentComparisonCheck | ArgumentOredConditions] = Field(
        min_length=2
    )
    """The list of conditions that are ANDed together."""

    _v1_1_type = None
    _v1_2_type = xtce_1_2.ArgumentAndedConditionsType
    _v1_3_type = xtce_1_3.ArgumentAndedConditionsType

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentAndedConditionsType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["conditions"] = [
            ArgumentComparisonCheck._from_v1_2(c)
            if isinstance(c, xtce_1_2.ArgumentComparisonCheckType)
            else ArgumentOredConditions._from_v1_2(c)
            for c in obj.choice
        ]
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentAndedConditionsType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["conditions"] = [
            ArgumentComparisonCheck._from_v1_3(c)
            if isinstance(c, xtce_1_3.ArgumentComparisonCheckType)
            else ArgumentOredConditions._from_v1_3(c)
            for c in obj.choice
        ]
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = [c._to_v1_2(policy) for c in self.conditions]
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = [c._to_v1_3(policy) for c in self.conditions]
        return kwargs


class OredConditions(BaseConditions):
    """Define a logical OR of multiple conditions."""

    conditions: list[ComparisonCheck | AndedConditions] = Field(min_length=2)
    """The list of conditions that are ORed together."""

    _v1_1_type = xtce_1_1.OredConditionsType
    _v1_2_type = xtce_1_2.OredConditionsType
    _v1_3_type = xtce_1_3.OredConditionsType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.OredConditionsType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["conditions"] = [
            ComparisonCheck._from_v1_1(c)
            if isinstance(c, xtce_1_1.ComparisonCheckType)
            else AndedConditions._from_v1_1(c)
            for c in obj.choice
        ]
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.OredConditionsType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["conditions"] = [
            ComparisonCheck._from_v1_2(c)
            if isinstance(c, xtce_1_2.ComparisonCheckType)
            else AndedConditions._from_v1_2(c)
            for c in obj.choice
        ]
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.OredConditionsType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["conditions"] = [
            ComparisonCheck._from_v1_3(c)
            if isinstance(c, xtce_1_3.ComparisonCheckType)
            else AndedConditions._from_v1_3(c)
            for c in obj.choice
        ]
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["choice"] = [c._to_v1_1(policy) for c in self.conditions]
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = [c._to_v1_2(policy) for c in self.conditions]
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = [c._to_v1_3(policy) for c in self.conditions]
        return kwargs


class ArgumentOredConditions(BaseConditions):
    """Define a logical OR of multiple argument conditions."""

    conditions: list[ArgumentComparisonCheck | ArgumentAndedConditions] = Field(
        min_length=2
    )
    """The list of argument conditions that are ORed together."""

    _v1_1_type = None
    _v1_2_type = xtce_1_2.ArgumentOredConditionsType
    _v1_3_type = xtce_1_3.ArgumentOredConditionsType

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentOredConditionsType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["conditions"] = [
            ArgumentComparisonCheck._from_v1_2(c)
            if isinstance(c, xtce_1_2.ArgumentComparisonCheckType)
            else ArgumentAndedConditions._from_v1_2(c)
            for c in obj.choice
        ]
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentOredConditionsType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["conditions"] = [
            ArgumentComparisonCheck._from_v1_3(c)
            if isinstance(c, xtce_1_3.ArgumentComparisonCheckType)
            else ArgumentAndedConditions._from_v1_3(c)
            for c in obj.choice
        ]
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = [c._to_v1_2(policy) for c in self.conditions]
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = [c._to_v1_3(policy) for c in self.conditions]
        return kwargs


class BooleanExpression(XtceBaseModel):
    """Define an arbitrarily complex boolean expression."""

    comparison: ComparisonCheck | AndedConditions | OredConditions
    """The boolean expression representing the condition."""

    _v1_1_type = xtce_1_1.BooleanExpressionType
    _v1_2_type = xtce_1_2.BooleanExpressionType
    _v1_3_type = xtce_1_3.BooleanExpressionType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.BooleanExpressionType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["comparison"] = (
            ComparisonCheck._from_v1_1(obj.choice)
            if isinstance(obj.choice, xtce_1_1.ComparisonCheckType)
            else AndedConditions._from_v1_1(obj.choice)
            if isinstance(obj.choice, xtce_1_1.AndedConditionsType)
            else OredConditions._from_v1_1(unwrap(obj.choice))
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.BooleanExpressionType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["comparison"] = (
            ComparisonCheck._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.ComparisonCheckType)
            else AndedConditions._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.AndedConditionsType)
            else OredConditions._from_v1_2(unwrap(obj.choice))
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.BooleanExpressionType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["comparison"] = (
            ComparisonCheck._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.ComparisonCheckType)
            else AndedConditions._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.AndedConditionsType)
            else OredConditions._from_v1_3(unwrap(obj.choice))
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["choice"] = self.comparison._to_v1_1(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = self.comparison._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = self.comparison._to_v1_3(policy)
        return kwargs


class ArgumentBooleanExpression(XtceBaseModel):
    """Define an arbitrarily complex boolean expression for arguments."""

    comparison: (
        ArgumentComparisonCheck | ArgumentAndedConditions | ArgumentOredConditions
    )

    _v1_1_type = None
    _v1_2_type = xtce_1_2.ArgumentBooleanExpressionType
    _v1_3_type = xtce_1_3.ArgumentBooleanExpressionType

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentBooleanExpressionType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["comparison"] = (
            ArgumentComparisonCheck._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.ArgumentComparisonCheckType)
            else ArgumentAndedConditions._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.ArgumentAndedConditionsType)
            else ArgumentOredConditions._from_v1_2(unwrap(obj.choice))
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentBooleanExpressionType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["comparison"] = (
            ArgumentComparisonCheck._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.ArgumentComparisonCheckType)
            else ArgumentAndedConditions._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.ArgumentAndedConditionsType)
            else ArgumentOredConditions._from_v1_3(unwrap(obj.choice))
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = self.comparison._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = self.comparison._to_v1_3(policy)
        return kwargs


class MatchCriteria(XtceBaseModel):
    """Define criteria used to match a particular condition."""

    criteria: Comparison | list[Comparison] | BooleanExpression | InputAlgorithm
    """The criteria used to match a particular condition."""

    _v1_1_type = xtce_1_1.MatchCriteriaType
    _v1_2_type = xtce_1_2.MatchCriteriaType
    _v1_3_type = xtce_1_3.MatchCriteriaType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.MatchCriteriaType) -> dict[str, Any]:
        from .algorithm import InputAlgorithm

        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["criteria"] = (
            [Comparison._from_v1_1(c) for c in obj.choice.comparison]
            if isinstance(obj.choice, xtce_1_1.MatchCriteriaType.ComparisonList)
            else Comparison._from_v1_1(obj.choice)
            if isinstance(obj.choice, xtce_1_1.ComparisonType)
            else BooleanExpression._from_v1_1(obj.choice)
            if isinstance(obj.choice, xtce_1_1.BooleanExpressionType)
            else InputAlgorithm._from_v1_1(unwrap(obj.choice))
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.MatchCriteriaType) -> dict[str, Any]:
        from .algorithm import InputAlgorithm

        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["criteria"] = (
            [Comparison._from_v1_2(c) for c in obj.choice.comparison]
            if isinstance(obj.choice, xtce_1_2.ComparisonListType)
            else Comparison._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.ComparisonType)
            else BooleanExpression._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.BooleanExpressionType)
            else InputAlgorithm._from_v1_2(unwrap(obj.choice))
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.MatchCriteriaType) -> dict[str, Any]:
        from .algorithm import InputAlgorithm

        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["criteria"] = (
            [Comparison._from_v1_3(c) for c in obj.choice.comparison]
            if isinstance(obj.choice, xtce_1_3.ComparisonListType)
            else Comparison._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.ComparisonType)
            else BooleanExpression._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.BooleanExpressionType)
            else InputAlgorithm._from_v1_3(unwrap(obj.choice))
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["choice"] = (
            xtce_1_1.MatchCriteriaType.ComparisonList(
                comparison=[c._to_v1_1(policy) for c in self.criteria]
            )
            if isinstance(self.criteria, list)
            else self.criteria._to_v1_1(policy)
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = (
            xtce_1_2.ComparisonListType(
                comparison=[c._to_v1_2(policy) for c in self.criteria]
            )
            if isinstance(self.criteria, list)
            else self.criteria._to_v1_2(policy)
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = (
            xtce_1_3.ComparisonListType(
                comparison=[c._to_v1_3(policy) for c in self.criteria]
            )
            if isinstance(self.criteria, list)
            else self.criteria._to_v1_3(policy)
        )
        return kwargs


class ArgumentMatchCriteria(XtceBaseModel):
    """Define criteria used to match a particular argument condition."""

    criteria: (
        ArgumentComparison
        | list[ArgumentComparison]
        | ArgumentBooleanExpression
        | ArgumentInputAlgorithm
    )
    """The criteria used to match a particular condition."""

    _v1_1_type = None
    _v1_2_type = xtce_1_2.ArgumentMatchCriteriaType
    _v1_3_type = xtce_1_3.ArgumentMatchCriteriaType

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentMatchCriteriaType
    ) -> dict[str, Any]:
        from .algorithm import ArgumentInputAlgorithm

        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["criteria"] = (
            [ArgumentComparison._from_v1_2(c) for c in obj.choice.comparison]
            if isinstance(obj.choice, xtce_1_2.ArgumentComparisonListType)
            else ArgumentComparison._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.ArgumentComparisonType)
            else ArgumentBooleanExpression._from_v1_2(obj.choice)
            if isinstance(obj.choice, xtce_1_2.ArgumentBooleanExpressionType)
            else ArgumentInputAlgorithm._from_v1_2(unwrap(obj.choice))
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentMatchCriteriaType
    ) -> dict[str, Any]:
        from .algorithm import ArgumentInputAlgorithm

        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["criteria"] = (
            [ArgumentComparison._from_v1_3(c) for c in obj.choice.comparison]
            if isinstance(obj.choice, xtce_1_3.ArgumentComparisonListType)
            else ArgumentComparison._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.ArgumentComparisonType)
            else ArgumentBooleanExpression._from_v1_3(obj.choice)
            if isinstance(obj.choice, xtce_1_3.ArgumentBooleanExpressionType)
            else ArgumentInputAlgorithm._from_v1_3(unwrap(obj.choice))
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = (
            xtce_1_2.ArgumentComparisonListType(
                comparison=[c._to_v1_2(policy) for c in self.criteria]
            )
            if isinstance(self.criteria, list)
            else self.criteria._to_v1_2(policy)
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = (
            xtce_1_3.ArgumentComparisonListType(
                comparison=[c._to_v1_3(policy) for c in self.criteria]
            )
            if isinstance(self.criteria, list)
            else self.criteria._to_v1_3(policy)
        )
        return kwargs


class ContextMatch(MatchCriteria):
    """Define match criteria for context-based selection."""

    _v1_1_type = None
    _v1_2_type = xtce_1_2.ContextMatchType
    _v1_3_type = xtce_1_3.ContextMatchType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ContextMatchType) -> dict[str, Any]:
        return super()._from_v1_2_kwargs(obj)

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ContextMatchType) -> dict[str, Any]:
        return super()._from_v1_3_kwargs(obj)

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        return super()._to_v1_2_kwargs(policy)

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        return super()._to_v1_3_kwargs(policy)


class DiscreteLookup(MatchCriteria):
    """Define one discrete lookup mapping from condition criteria to a value."""

    value: int
    """The value to use when the lookup conditions are true."""

    _v1_1_type = None
    _v1_2_type = xtce_1_2.DiscreteLookupType
    _v1_3_type = xtce_1_3.DiscreteLookupType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.DiscreteLookupType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["value"] = obj.value
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.DiscreteLookupType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["value"] = obj.value
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["value"] = self.value
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["value"] = self.value
        return kwargs


class ArgumentDiscreteLookup(ArgumentMatchCriteria):
    """Define one argument discrete lookup mapping to an integer."""

    value: int

    _v1_1_type = None
    _v1_2_type = xtce_1_2.ArgumentDiscreteLookupType
    _v1_3_type = xtce_1_3.ArgumentDiscreteLookupType

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentDiscreteLookupType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["value"] = obj.value
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentDiscreteLookupType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["value"] = obj.value
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["value"] = self.value
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["value"] = self.value
        return kwargs


class DiscreteLookupList(XtceBaseModel):
    """Define an ordered table of integer values and associated conditions, forming a
    lookup table.

    The list may have duplicates. The table is evaluated from first to last, the first
    condition to be true returns the value associated with it.

    """

    lookups: list[DiscreteLookup] = Field(default_factory=list)
    """A lookup condition set using discrete values from parameters."""

    default_value: int
    """In the event that no lookup condition evaluates to true, then this value will be
    used.

    Applicable since: XTCE 1.3

    """

    _v1_1_type = None
    _v1_2_type = xtce_1_2.DiscreteLookupListType
    _v1_3_type = xtce_1_3.DiscreteLookupListType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.DiscreteLookupListType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["lookups"] = [DiscreteLookup._from_v1_2(l) for l in obj.discrete_lookup]
        kwargs["default_value"] = 0
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.DiscreteLookupListType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["lookups"] = [DiscreteLookup._from_v1_3(l) for l in obj.discrete_lookup]
        kwargs["default_value"] = obj.default_value
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="default_value",
            current_value=self.default_value,
            target_version=XtceVersion.V1_2,
            policy=policy,
        )

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["discrete_lookup"] = [l._to_v1_2(policy) for l in self.lookups]
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["discrete_lookup"] = [l._to_v1_3(policy) for l in self.lookups]
        kwargs["default_value"] = self.default_value
        return kwargs


class ArgumentDiscreteLookupList(XtceBaseModel):
    """Define an ordered table of integer values and associated conditions, forming a
    lookup table for arguments.

    The list may have duplicates. The table is evaluated from first to last, the first
    condition to be true returns the value associated with it.

    """

    lookups: list[ArgumentDiscreteLookup] = Field(default_factory=list)
    """A lookup condition set using discrete values from arguments."""

    default_value: int
    """In the event that no lookup condition evaluates to true, then this value will be
    used.
    """

    _v1_1_type = None
    _v1_2_type = xtce_1_2.ArgumentDiscreteLookupListType
    _v1_3_type = xtce_1_3.ArgumentDiscreteLookupListType

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentDiscreteLookupListType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["lookups"] = [
            ArgumentDiscreteLookup._from_v1_2(l) for l in obj.discrete_lookup
        ]
        kwargs["default_value"] = 0
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentDiscreteLookupListType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["lookups"] = [
            ArgumentDiscreteLookup._from_v1_3(l) for l in obj.discrete_lookup
        ]
        kwargs["default_value"] = obj.default_value
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="default_value",
            current_value=self.default_value,
            target_version=XtceVersion.V1_2,
            policy=policy,
        )

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["discrete_lookup"] = [l._to_v1_2(policy) for l in self.lookups]
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["discrete_lookup"] = [l._to_v1_3(policy) for l in self.lookups]
        kwargs["default_value"] = self.default_value
        return kwargs
