"""Condition models."""

from __future__ import annotations

import datetime
from abc import ABC
from typing import TYPE_CHECKING, Any, Self

from pydantic import Field

from xtce_lib.common.xtce_path import XtcePath
from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy, XtceUnsupportedError
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
            value=uncoerce(self.value),
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ComparisonType:
        return xtce_1_2.ComparisonType(
            parameter_ref=str(self.ref),
            instance=self.instance,
            use_calibrated_value=self.use_calibrated_value,
            comparison_operator=self.comparison_operator._to_v1_2(policy),
            value=uncoerce(self.value),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ComparisonType:
        return xtce_1_3.ComparisonType(
            parameter_ref=str(self.ref),
            instance=self.instance,
            use_calibrated_value=self.use_calibrated_value,
            comparison_operator=self.comparison_operator._to_v1_3(policy),
            value=uncoerce(self.value),
        )


class ArgumentComparison(XtceBaseModel):
    """Define a comparison of a parameter or argument instance to a value."""

    instance_ref: ParameterInstanceRef | ArgumentInstanceRef
    """The instance of the parameter or argument to compare."""

    comparison_operator: ComparisonOperator = ComparisonOperator.EQ
    """The operator to use for the comparison."""

    value: int | float | str | bool | bytes | datetime.timedelta | datetime.datetime
    """The value to compare the parameter or argument instance against."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.ArgumentComparisonType) -> Self:
        if isinstance(raw_obj.choice, xtce_1_2.ParameterInstanceRefType):
            instance = ParameterInstanceRef._from_v1_2(raw_obj.choice)
        else:
            instance = ArgumentInstanceRef._from_v1_2(unwrap(raw_obj.choice))

        return cls(
            instance_ref=instance,
            comparison_operator=ComparisonOperator._from_v1_2(
                raw_obj.comparison_operator
            ),
            value=coerce(raw_obj.value),
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.ArgumentComparisonType) -> Self:
        if isinstance(raw_obj.choice, xtce_1_3.ParameterInstanceRefType):
            instance = ParameterInstanceRef._from_v1_3(raw_obj.choice)
        else:
            instance = ArgumentInstanceRef._from_v1_3(unwrap(raw_obj.choice))

        return cls(
            instance_ref=instance,
            comparison_operator=ComparisonOperator._from_v1_3(
                raw_obj.comparison_operator
            ),
            value=coerce(raw_obj.value),
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ArgumentComparisonType:
        return xtce_1_2.ArgumentComparisonType(
            choice=self.instance_ref._to_v1_2(policy),
            comparison_operator=self.comparison_operator._to_v1_2(policy),
            value=uncoerce(self.value),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ArgumentComparisonType:
        return xtce_1_3.ArgumentComparisonType(
            choice=self.instance_ref._to_v1_3(policy),
            comparison_operator=self.comparison_operator._to_v1_3(policy),
            value=uncoerce(self.value),
        )


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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.ComparisonCheckType) -> Self:
        items = list(raw_obj.choice)

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
            if raw_obj.value is None:
                raise ValueError("missing right-hand side value for comparison")
            right = coerce(raw_obj.value)

        return cls(
            left=ParameterInstanceRef._from_v1_1(left_raw),
            comparison_operator=ComparisonOperator._from_v1_1(op_raw),
            right=right,
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.ComparisonCheckType) -> Self:
        items = list(raw_obj.choice)

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
            if raw_obj.value is None:
                raise ValueError("missing right-hand side value for comparison")
            right = coerce(raw_obj.value)

        return cls(
            left=ParameterInstanceRef._from_v1_2(left_raw),
            comparison_operator=ComparisonOperator._from_v1_2(op_raw),
            right=right,
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.ComparisonCheckType) -> Self:
        items = list(raw_obj.choice)

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
            if raw_obj.value is None:
                raise ValueError("missing right-hand side value for comparison")
            right = coerce(raw_obj.value)

        return cls(
            left=ParameterInstanceRef._from_v1_3(left_raw),
            comparison_operator=ComparisonOperator._from_v1_3(op_raw),
            right=right,
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.ComparisonCheckType:
        choice = [
            self.left._to_v1_1(policy),
            self.comparison_operator._to_v1_1(policy),
        ]
        if isinstance(self.right, ParameterInstanceRef):
            choice.append(self.right._to_v1_1(policy))
            value = None
        else:
            value = uncoerce(self.right)

        return xtce_1_1.ComparisonCheckType(choice=choice, value=value)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ComparisonCheckType:
        choice = [
            self.left._to_v1_2(policy),
            self.comparison_operator._to_v1_2(policy),
        ]
        if isinstance(self.right, ParameterInstanceRef):
            choice.append(self.right._to_v1_2(policy))
            value = None
        else:
            value = uncoerce(self.right)

        return xtce_1_2.ComparisonCheckType(choice=choice, value=value)

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ComparisonCheckType:
        choice = [
            self.left._to_v1_3(policy),
            self.comparison_operator._to_v1_3(policy),
        ]
        if isinstance(self.right, ParameterInstanceRef):
            choice.append(self.right._to_v1_3(policy))
            value = None
        else:
            value = uncoerce(self.right)

        return xtce_1_3.ComparisonCheckType(choice=choice, value=value)


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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(
        cls: type[Self], raw_obj: xtce_1_2.ArgumentComparisonCheckType
    ) -> Self:
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

        items = list(raw_obj.choice)

        if len(items) == 1:
            left_raw, right_raw = items[0], None
        else:
            left_raw, right_raw = items[0], items[1]

        if right_raw is not None:
            right = unpack_instance_ref(right_raw)
        else:
            if raw_obj.value is None:
                raise ValueError("missing right-hand side value for comparison")
            right = coerce(raw_obj.value)

        return cls(
            left=unpack_instance_ref(left_raw),
            comparison_operator=ComparisonOperator._from_v1_2(
                raw_obj.comparison_operator
            ),
            right=right,
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], raw_obj: xtce_1_3.ArgumentComparisonCheckType
    ) -> Self:
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

        items = list(raw_obj.choice)

        if len(items) == 1:
            left_raw, right_raw = items[0], None
        else:
            left_raw, right_raw = items[0], items[1]

        if right_raw is not None:
            right = unpack_instance_ref(right_raw)
        else:
            if raw_obj.value is None:
                raise ValueError("missing right-hand side value for comparison")
            right = coerce(raw_obj.value)

        return cls(
            left=unpack_instance_ref(left_raw),
            comparison_operator=ComparisonOperator._from_v1_3(
                raw_obj.comparison_operator
            ),
            right=right,
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ArgumentComparisonCheckType:
        choice = [self.left._to_v1_2(policy)]
        if isinstance(self.right, (ParameterInstanceRef, ArgumentInstanceRef)):
            choice.append(self.right._to_v1_2(policy))
            value = None
        else:
            value = uncoerce(self.right)

        return xtce_1_2.ArgumentComparisonCheckType(
            choice=choice,
            comparison_operator=self.comparison_operator._to_v1_2(policy),
            value=value,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ArgumentComparisonCheckType:
        choice = [self.left._to_v1_3(policy)]
        if isinstance(self.right, (ParameterInstanceRef, ArgumentInstanceRef)):
            choice.append(self.right._to_v1_3(policy))
            value = None
        else:
            value = uncoerce(self.right)

        return xtce_1_3.ArgumentComparisonCheckType(
            choice=choice,
            comparison_operator=self.comparison_operator._to_v1_3(policy),
            value=value,
        )


class BaseConditions(XtceBaseModel, ABC):
    """Define shared behavior for grouped condition expressions."""


class AndedConditions(BaseConditions):
    """Define a logical AND of multiple conditions."""

    conditions: list[ComparisonCheck | OredConditions] = Field(min_length=2)
    """The list of conditions that are ANDed together."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.AndedConditionsType) -> Self:
        return cls(
            conditions=[
                ComparisonCheck._from_v1_1(c)
                if isinstance(c, xtce_1_1.ComparisonCheckType)
                else OredConditions._from_v1_1(c)
                for c in raw_obj.choice
            ]
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.AndedConditionsType) -> Self:
        return cls(
            conditions=[
                ComparisonCheck._from_v1_2(c)
                if isinstance(c, xtce_1_2.ComparisonCheckType)
                else OredConditions._from_v1_2(c)
                for c in raw_obj.choice
            ]
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.AndedConditionsType) -> Self:
        return cls(
            conditions=[
                ComparisonCheck._from_v1_3(c)
                if isinstance(c, xtce_1_3.ComparisonCheckType)
                else OredConditions._from_v1_3(c)
                for c in raw_obj.choice
            ]
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.AndedConditionsType:
        return xtce_1_1.AndedConditionsType(
            choice=[c._to_v1_1(policy) for c in self.conditions]
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.AndedConditionsType:
        return xtce_1_2.AndedConditionsType(
            choice=[c._to_v1_2(policy) for c in self.conditions]
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.AndedConditionsType:
        return xtce_1_3.AndedConditionsType(
            choice=[c._to_v1_3(policy) for c in self.conditions]
        )


class ArgumentAndedConditions(BaseConditions):
    """Define a logical AND of multiple argument conditions."""

    conditions: list[ArgumentComparisonCheck | ArgumentOredConditions] = Field(
        min_length=2
    )
    """The list of conditions that are ANDed together."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(
        cls: type[Self], raw_obj: xtce_1_2.ArgumentAndedConditionsType
    ) -> Self:
        return cls(
            conditions=[
                ArgumentComparisonCheck._from_v1_2(c)
                if isinstance(c, xtce_1_2.ArgumentComparisonCheckType)
                else ArgumentOredConditions._from_v1_2(c)
                for c in raw_obj.choice
            ]
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], raw_obj: xtce_1_3.ArgumentAndedConditionsType
    ) -> Self:
        return cls(
            conditions=[
                ArgumentComparisonCheck._from_v1_3(c)
                if isinstance(c, xtce_1_3.ArgumentComparisonCheckType)
                else ArgumentOredConditions._from_v1_3(c)
                for c in raw_obj.choice
            ]
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ArgumentAndedConditionsType:
        return xtce_1_2.ArgumentAndedConditionsType(
            choice=[c._to_v1_2(policy) for c in self.conditions]
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ArgumentAndedConditionsType:
        return xtce_1_3.ArgumentAndedConditionsType(
            choice=[c._to_v1_3(policy) for c in self.conditions]
        )


class OredConditions(BaseConditions):
    """Define a logical OR of multiple conditions."""

    conditions: list[ComparisonCheck | AndedConditions] = Field(min_length=2)
    """The list of conditions that are ORed together."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.OredConditionsType) -> Self:
        return cls(
            conditions=[
                ComparisonCheck._from_v1_1(c)
                if isinstance(c, xtce_1_1.ComparisonCheckType)
                else AndedConditions._from_v1_1(c)
                for c in raw_obj.choice
            ]
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.OredConditionsType) -> Self:
        return cls(
            conditions=[
                ComparisonCheck._from_v1_2(c)
                if isinstance(c, xtce_1_2.ComparisonCheckType)
                else AndedConditions._from_v1_2(c)
                for c in raw_obj.choice
            ]
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.OredConditionsType) -> Self:
        return cls(
            conditions=[
                ComparisonCheck._from_v1_3(c)
                if isinstance(c, xtce_1_3.ComparisonCheckType)
                else AndedConditions._from_v1_3(c)
                for c in raw_obj.choice
            ]
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.OredConditionsType:
        return xtce_1_1.OredConditionsType(
            choice=[c._to_v1_1(policy) for c in self.conditions]
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.OredConditionsType:
        return xtce_1_2.OredConditionsType(
            choice=[c._to_v1_2(policy) for c in self.conditions]
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.OredConditionsType:
        return xtce_1_3.OredConditionsType(
            choice=[c._to_v1_3(policy) for c in self.conditions]
        )


class ArgumentOredConditions(BaseConditions):
    """Define a logical OR of multiple argument conditions."""

    conditions: list[ArgumentComparisonCheck | ArgumentAndedConditions] = Field(
        min_length=2
    )
    """The list of argument conditions that are ORed together."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(
        cls: type[Self], raw_obj: xtce_1_2.ArgumentOredConditionsType
    ) -> Self:
        return cls(
            conditions=[
                ArgumentComparisonCheck._from_v1_2(c)
                if isinstance(c, xtce_1_2.ArgumentComparisonCheckType)
                else ArgumentAndedConditions._from_v1_2(c)
                for c in raw_obj.choice
            ]
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], raw_obj: xtce_1_3.ArgumentOredConditionsType
    ) -> Self:
        return cls(
            conditions=[
                ArgumentComparisonCheck._from_v1_3(c)
                if isinstance(c, xtce_1_3.ArgumentComparisonCheckType)
                else ArgumentAndedConditions._from_v1_3(c)
                for c in raw_obj.choice
            ]
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ArgumentOredConditionsType:
        return xtce_1_2.ArgumentOredConditionsType(
            choice=[c._to_v1_2(policy) for c in self.conditions]
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ArgumentOredConditionsType:
        return xtce_1_3.ArgumentOredConditionsType(
            choice=[c._to_v1_3(policy) for c in self.conditions]
        )


class BooleanExpression(XtceBaseModel):
    """Define an arbitrarily complex boolean expression."""

    comparison: ComparisonCheck | AndedConditions | OredConditions
    """The boolean expression representing the condition."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.BooleanExpressionType) -> Self:
        return cls(
            comparison=(
                ComparisonCheck._from_v1_1(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_1.ComparisonCheckType)
                else AndedConditions._from_v1_1(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_1.AndedConditionsType)
                else OredConditions._from_v1_1(unwrap(raw_obj.choice))
            )
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.BooleanExpressionType) -> Self:
        return cls(
            comparison=(
                ComparisonCheck._from_v1_2(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_2.ComparisonCheckType)
                else AndedConditions._from_v1_2(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_2.AndedConditionsType)
                else OredConditions._from_v1_2(unwrap(raw_obj.choice))
            )
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.BooleanExpressionType) -> Self:
        return cls(
            comparison=(
                ComparisonCheck._from_v1_3(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_3.ComparisonCheckType)
                else AndedConditions._from_v1_3(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_3.AndedConditionsType)
                else OredConditions._from_v1_3(unwrap(raw_obj.choice))
            )
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.BooleanExpressionType:
        return xtce_1_1.BooleanExpressionType(choice=self.comparison._to_v1_1(policy))

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.BooleanExpressionType:
        return xtce_1_2.BooleanExpressionType(choice=self.comparison._to_v1_2(policy))

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.BooleanExpressionType:
        return xtce_1_3.BooleanExpressionType(choice=self.comparison._to_v1_3(policy))


class ArgumentBooleanExpression(XtceBaseModel):
    """Define an arbitrarily complex boolean expression for arguments."""

    comparison: (
        ArgumentComparisonCheck | ArgumentAndedConditions | ArgumentOredConditions
    )

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(
        cls: type[Self], raw_obj: xtce_1_2.ArgumentBooleanExpressionType
    ) -> Self:
        return cls(
            comparison=(
                ArgumentComparisonCheck._from_v1_2(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_2.ArgumentComparisonCheckType)
                else ArgumentAndedConditions._from_v1_2(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_2.ArgumentAndedConditionsType)
                else ArgumentOredConditions._from_v1_2(unwrap(raw_obj.choice))
            )
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], raw_obj: xtce_1_3.ArgumentBooleanExpressionType
    ) -> Self:
        return cls(
            comparison=(
                ArgumentComparisonCheck._from_v1_3(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_3.ArgumentComparisonCheckType)
                else ArgumentAndedConditions._from_v1_3(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_3.ArgumentAndedConditionsType)
                else ArgumentOredConditions._from_v1_3(unwrap(raw_obj.choice))
            )
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ArgumentBooleanExpressionType:
        return xtce_1_2.ArgumentBooleanExpressionType(
            choice=self.comparison._to_v1_2(policy)
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ArgumentBooleanExpressionType:
        return xtce_1_3.ArgumentBooleanExpressionType(
            choice=self.comparison._to_v1_3(policy)
        )


class MatchCriteria(XtceBaseModel):
    """Define criteria used to match a particular condition."""

    criteria: Comparison | list[Comparison] | BooleanExpression | InputAlgorithm
    """The criteria used to match a particular condition."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.MatchCriteriaType) -> Self:
        from .algorithm import InputAlgorithm

        return cls(
            criteria=(
                [Comparison._from_v1_1(c) for c in raw_obj.choice.comparison]
                if isinstance(raw_obj.choice, xtce_1_1.MatchCriteriaType.ComparisonList)
                else Comparison._from_v1_1(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_1.ComparisonType)
                else BooleanExpression._from_v1_1(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_1.BooleanExpressionType)
                else InputAlgorithm._from_v1_1(unwrap(raw_obj.choice))
            )
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.MatchCriteriaType) -> Self:
        from .algorithm import InputAlgorithm

        return cls(
            criteria=(
                [Comparison._from_v1_2(c) for c in raw_obj.choice.comparison]
                if isinstance(raw_obj.choice, xtce_1_2.ComparisonListType)
                else Comparison._from_v1_2(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_2.ComparisonType)
                else BooleanExpression._from_v1_2(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_2.BooleanExpressionType)
                else InputAlgorithm._from_v1_2(unwrap(raw_obj.choice))
            )
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.MatchCriteriaType) -> Self:
        from .algorithm import InputAlgorithm

        return cls(
            criteria=(
                [Comparison._from_v1_3(c) for c in raw_obj.choice.comparison]
                if isinstance(raw_obj.choice, xtce_1_3.ComparisonListType)
                else Comparison._from_v1_3(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_3.ComparisonType)
                else BooleanExpression._from_v1_3(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_3.BooleanExpressionType)
                else InputAlgorithm._from_v1_3(unwrap(raw_obj.choice))
            )
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.MatchCriteriaType:
        return xtce_1_1.MatchCriteriaType(
            choice=xtce_1_1.MatchCriteriaType.ComparisonList(
                comparison=[c._to_v1_1(policy) for c in self.criteria]
            )
            if isinstance(self.criteria, list)
            else self.criteria._to_v1_1(policy),
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.MatchCriteriaType:
        return xtce_1_2.MatchCriteriaType(
            choice=xtce_1_2.ComparisonListType(
                comparison=[c._to_v1_2(policy) for c in self.criteria]
            )
            if isinstance(self.criteria, list)
            else self.criteria._to_v1_2(policy),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.MatchCriteriaType:
        return xtce_1_3.MatchCriteriaType(
            choice=xtce_1_3.ComparisonListType(
                comparison=[c._to_v1_3(policy) for c in self.criteria]
            )
            if isinstance(self.criteria, list)
            else self.criteria._to_v1_3(policy),
        )


class ArgumentMatchCriteria(XtceBaseModel):
    """Define criteria used to match a particular argument condition."""

    criteria: (
        ArgumentComparison
        | list[ArgumentComparison]
        | ArgumentBooleanExpression
        | ArgumentInputAlgorithm
    )
    """The criteria used to match a particular condition."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(
        cls: type[Self], raw_obj: xtce_1_2.ArgumentMatchCriteriaType
    ) -> Self:
        from .algorithm import ArgumentInputAlgorithm

        return cls(
            criteria=(
                [ArgumentComparison._from_v1_2(c) for c in raw_obj.choice.comparison]
                if isinstance(raw_obj.choice, xtce_1_2.ArgumentComparisonListType)
                else ArgumentComparison._from_v1_2(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_2.ArgumentComparisonType)
                else ArgumentBooleanExpression._from_v1_2(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_2.ArgumentBooleanExpressionType)
                else ArgumentInputAlgorithm._from_v1_2(unwrap(raw_obj.choice))
            )
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], raw_obj: xtce_1_3.ArgumentMatchCriteriaType
    ) -> Self:
        from .algorithm import ArgumentInputAlgorithm

        return cls(
            criteria=(
                [ArgumentComparison._from_v1_3(c) for c in raw_obj.choice.comparison]
                if isinstance(raw_obj.choice, xtce_1_3.ArgumentComparisonListType)
                else ArgumentComparison._from_v1_3(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_3.ArgumentComparisonType)
                else ArgumentBooleanExpression._from_v1_3(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_3.ArgumentBooleanExpressionType)
                else ArgumentInputAlgorithm._from_v1_3(unwrap(raw_obj.choice))
            )
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ArgumentMatchCriteriaType:
        return xtce_1_2.ArgumentMatchCriteriaType(
            choice=xtce_1_2.ArgumentComparisonListType(
                comparison=[c._to_v1_2(policy) for c in self.criteria]
            )
            if isinstance(self.criteria, list)
            else self.criteria._to_v1_2(policy),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ArgumentMatchCriteriaType:
        return xtce_1_3.ArgumentMatchCriteriaType(
            choice=xtce_1_3.ArgumentComparisonListType(
                comparison=[c._to_v1_3(policy) for c in self.criteria]
            )
            if isinstance(self.criteria, list)
            else self.criteria._to_v1_3(policy),
        )


class ContextMatch(MatchCriteria):
    """Define match criteria for context-based selection."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.ContextMatchType) -> Self:
        from .algorithm import InputAlgorithm

        return cls(
            criteria=(
                [Comparison._from_v1_2(c) for c in raw_obj.choice.comparison]
                if isinstance(raw_obj.choice, xtce_1_2.ComparisonListType)
                else Comparison._from_v1_2(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_2.ComparisonType)
                else BooleanExpression._from_v1_2(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_2.BooleanExpressionType)
                else InputAlgorithm._from_v1_2(unwrap(raw_obj.choice))
            )
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.ContextMatchType) -> Self:
        from .algorithm import InputAlgorithm

        return cls(
            criteria=(
                [Comparison._from_v1_3(c) for c in raw_obj.choice.comparison]
                if isinstance(raw_obj.choice, xtce_1_3.ComparisonListType)
                else Comparison._from_v1_3(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_3.ComparisonType)
                else BooleanExpression._from_v1_3(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_3.BooleanExpressionType)
                else InputAlgorithm._from_v1_3(unwrap(raw_obj.choice))
            )
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ContextMatchType:
        return xtce_1_2.ContextMatchType(
            choice=xtce_1_2.ComparisonListType(
                comparison=[c._to_v1_2(policy) for c in self.criteria]
            )
            if isinstance(self.criteria, list)
            else self.criteria._to_v1_2(policy),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ContextMatchType:
        return xtce_1_3.ContextMatchType(
            choice=xtce_1_3.ComparisonListType(
                comparison=[c._to_v1_3(policy) for c in self.criteria]
            )
            if isinstance(self.criteria, list)
            else self.criteria._to_v1_3(policy),
        )


class DiscreteLookup(MatchCriteria):
    """Define one discrete lookup mapping from condition criteria to a value."""

    value: int
    """The value to use when the lookup conditions are true"""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.DiscreteLookupType) -> Self:
        from .algorithm import InputAlgorithm

        return cls(
            criteria=(
                [Comparison._from_v1_2(c) for c in raw_obj.choice.comparison]
                if isinstance(raw_obj.choice, xtce_1_2.ComparisonListType)
                else Comparison._from_v1_2(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_2.ComparisonType)
                else BooleanExpression._from_v1_2(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_2.BooleanExpressionType)
                else InputAlgorithm._from_v1_2(unwrap(raw_obj.choice))
            ),
            value=raw_obj.value,
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.DiscreteLookupType) -> Self:
        from .algorithm import InputAlgorithm

        return cls(
            criteria=(
                [Comparison._from_v1_3(c) for c in raw_obj.choice.comparison]
                if isinstance(raw_obj.choice, xtce_1_3.ComparisonListType)
                else Comparison._from_v1_3(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_3.ComparisonType)
                else BooleanExpression._from_v1_3(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_3.BooleanExpressionType)
                else InputAlgorithm._from_v1_3(unwrap(raw_obj.choice))
            ),
            value=raw_obj.value,
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.DiscreteLookupType:
        return xtce_1_2.DiscreteLookupType(
            choice=xtce_1_2.ComparisonListType(
                comparison=[c._to_v1_2(policy) for c in self.criteria]
            )
            if isinstance(self.criteria, list)
            else self.criteria._to_v1_2(policy),
            value=self.value,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.DiscreteLookupType:
        return xtce_1_3.DiscreteLookupType(
            choice=xtce_1_3.ComparisonListType(
                comparison=[c._to_v1_3(policy) for c in self.criteria]
            )
            if isinstance(self.criteria, list)
            else self.criteria._to_v1_3(policy),
            value=self.value,
        )


class ArgumentDiscreteLookup(ArgumentMatchCriteria):
    """Define one argument discrete lookup mapping to an integer."""

    value: int

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(
        cls: type[Self], raw_obj: xtce_1_2.ArgumentDiscreteLookupType
    ) -> Self:
        from .algorithm import ArgumentInputAlgorithm

        return cls(
            criteria=(
                [ArgumentComparison._from_v1_2(c) for c in raw_obj.choice.comparison]
                if isinstance(raw_obj.choice, xtce_1_2.ArgumentComparisonListType)
                else ArgumentComparison._from_v1_2(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_2.ArgumentComparisonType)
                else ArgumentBooleanExpression._from_v1_2(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_2.ArgumentBooleanExpressionType)
                else ArgumentInputAlgorithm._from_v1_2(unwrap(raw_obj.choice))
            ),
            value=raw_obj.value,
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], raw_obj: xtce_1_3.ArgumentDiscreteLookupType
    ) -> Self:
        from .algorithm import ArgumentInputAlgorithm

        return cls(
            criteria=(
                [ArgumentComparison._from_v1_3(c) for c in raw_obj.choice.comparison]
                if isinstance(raw_obj.choice, xtce_1_3.ArgumentComparisonListType)
                else ArgumentComparison._from_v1_3(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_3.ArgumentComparisonType)
                else ArgumentBooleanExpression._from_v1_3(raw_obj.choice)
                if isinstance(raw_obj.choice, xtce_1_3.ArgumentBooleanExpressionType)
                else ArgumentInputAlgorithm._from_v1_3(unwrap(raw_obj.choice))
            ),
            value=raw_obj.value,
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ArgumentDiscreteLookupType:
        return xtce_1_2.ArgumentDiscreteLookupType(
            choice=xtce_1_2.ArgumentComparisonListType(
                comparison=[c._to_v1_2(policy) for c in self.criteria]
            )
            if isinstance(self.criteria, list)
            else self.criteria._to_v1_2(policy),
            value=self.value,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ArgumentDiscreteLookupType:
        return xtce_1_3.ArgumentDiscreteLookupType(
            choice=xtce_1_3.ArgumentComparisonListType(
                comparison=[c._to_v1_3(policy) for c in self.criteria]
            )
            if isinstance(self.criteria, list)
            else self.criteria._to_v1_3(policy),
            value=self.value,
        )


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
    """

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.DiscreteLookupListType) -> Self:
        return cls(
            lookups=[DiscreteLookup._from_v1_2(l) for l in raw_obj.discrete_lookup],
            default_value=0,
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.DiscreteLookupListType) -> Self:
        return cls(
            lookups=[DiscreteLookup._from_v1_3(l) for l in raw_obj.discrete_lookup],
            default_value=raw_obj.default_value,
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.DiscreteLookupListType:
        self._enforce_unsupported_field(
            field_name="default_value",
            current_value=self.default_value,
            target_version=XtceVersion.V1_2,
            policy=policy,
        )

        return xtce_1_2.DiscreteLookupListType(
            discrete_lookup=[l._to_v1_2(policy) for l in self.lookups]
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.DiscreteLookupListType:
        return xtce_1_3.DiscreteLookupListType(
            discrete_lookup=[l._to_v1_3(policy) for l in self.lookups],
            default_value=self.default_value,
        )


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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(
        cls: type[Self], raw_obj: xtce_1_2.ArgumentDiscreteLookupListType
    ) -> Self:
        return cls(
            lookups=[
                ArgumentDiscreteLookup._from_v1_2(l) for l in raw_obj.discrete_lookup
            ],
            default_value=0,
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], raw_obj: xtce_1_3.ArgumentDiscreteLookupListType
    ) -> Self:
        return cls(
            lookups=[
                ArgumentDiscreteLookup._from_v1_3(l) for l in raw_obj.discrete_lookup
            ],
            default_value=raw_obj.default_value,
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ArgumentDiscreteLookupListType:
        self._enforce_unsupported_field(
            field_name="default_value",
            current_value=self.default_value,
            target_version=XtceVersion.V1_2,
            policy=policy,
        )

        return xtce_1_2.ArgumentDiscreteLookupListType(
            discrete_lookup=[l._to_v1_2(policy) for l in self.lookups]
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ArgumentDiscreteLookupListType:
        return xtce_1_3.ArgumentDiscreteLookupListType(
            discrete_lookup=[l._to_v1_3(policy) for l in self.lookups],
            default_value=self.default_value,
        )
