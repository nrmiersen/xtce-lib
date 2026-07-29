"""Array models."""

from __future__ import annotations

from typing import Any, Self

from pydantic import model_validator
from typing_extensions import assert_never

from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from .codec import ArgumentDynamicValue, DynamicValue
from .condition import ArgumentDiscreteLookupList, DiscreteLookupList


def _parse_integer_value_v1_2(
    integer_value: xtce_1_2.IntegerValueType,
) -> int | DynamicValue | DiscreteLookupList:
    """Parse an IntegerValueType into the unified model types."""
    match integer_value.choice:
        case int() as val:
            return val
        case xtce_1_2.DynamicValueType() as val:
            return DynamicValue._from_v1_2(val)
        case xtce_1_2.DiscreteLookupListType() as val:
            return DiscreteLookupList._from_v1_2(val)
        case None:
            raise ValueError("invalid XTCE XML: dimension index is missing a value")
        case _:
            assert_never(integer_value.choice)


def _parse_integer_value_v1_3(
    integer_value: xtce_1_3.IntegerValueType,
) -> int | DynamicValue | DiscreteLookupList:
    """Parse an IntegerValueType into the unified model types."""
    match integer_value.choice:
        case int() as val:
            return val
        case xtce_1_3.DynamicValueType() as val:
            return DynamicValue._from_v1_3(val)
        case xtce_1_3.DiscreteLookupListType() as val:
            return DiscreteLookupList._from_v1_3(val)
        case None:
            raise ValueError("invalid XTCE XML: dimension index is missing a value")
        case _:
            assert_never(integer_value.choice)


def _pack_integer_value_v1_2(
    value: int | DynamicValue | DiscreteLookupList,
    policy: DowngradePolicy,
) -> xtce_1_2.IntegerValueType:
    """Pack a unified model index value into an IntegerValueType."""
    match value:
        case int():
            return xtce_1_2.IntegerValueType(choice=value)
        case DynamicValue():
            return xtce_1_2.IntegerValueType(choice=value._to_v1_2(policy))
        case DiscreteLookupList():
            return xtce_1_2.IntegerValueType(choice=value._to_v1_2(policy))


def _pack_integer_value_v1_3(
    value: int | DynamicValue | DiscreteLookupList,
    policy: DowngradePolicy,
) -> xtce_1_3.IntegerValueType:
    """Pack a unified model index value into an IntegerValueType."""
    match value:
        case int():
            return xtce_1_3.IntegerValueType(choice=value)
        case DynamicValue():
            return xtce_1_3.IntegerValueType(choice=value._to_v1_3(policy))
        case DiscreteLookupList():
            return xtce_1_3.IntegerValueType(choice=value._to_v1_3(policy))


def _parse_argument_integer_value_v1_2(
    integer_value: xtce_1_2.ArgumentIntegerValueType,
) -> int | ArgumentDynamicValue | ArgumentDiscreteLookupList:
    """Parse an ArgumentIntegerValueType into the unified model types."""
    match integer_value.choice:
        case int() as val:
            return val
        case xtce_1_2.ArgumentDynamicValueType() as val:
            return ArgumentDynamicValue._from_v1_2(val)
        case xtce_1_2.ArgumentDiscreteLookupListType() as val:
            return ArgumentDiscreteLookupList._from_v1_2(val)
        case None:
            raise ValueError("invalid XTCE XML: dimension index is missing a value")
        case _:
            assert_never(integer_value.choice)


def _parse_argument_integer_value_v1_3(
    integer_value: xtce_1_3.ArgumentIntegerValueType,
) -> int | ArgumentDynamicValue | ArgumentDiscreteLookupList:
    """Parse an ArgumentIntegerValueType into the unified model types."""
    match integer_value.choice:
        case int() as val:
            return val
        case xtce_1_3.ArgumentDynamicValueType() as val:
            return ArgumentDynamicValue._from_v1_3(val)
        case xtce_1_3.ArgumentDiscreteLookupListType() as val:
            return ArgumentDiscreteLookupList._from_v1_3(val)
        case None:
            raise ValueError("invalid XTCE XML: dimension index is missing a value")
        case _:
            assert_never(integer_value.choice)


def _pack_argument_integer_value_v1_2(
    value: int | ArgumentDynamicValue | ArgumentDiscreteLookupList,
    policy: DowngradePolicy,
) -> xtce_1_2.ArgumentIntegerValueType:
    """Pack a unified model argument index value into an ArgumentIntegerValueType."""
    match value:
        case int():
            return xtce_1_2.ArgumentIntegerValueType(choice=value)
        case ArgumentDynamicValue():
            return xtce_1_2.ArgumentIntegerValueType(choice=value._to_v1_2(policy))
        case ArgumentDiscreteLookupList():
            return xtce_1_2.ArgumentIntegerValueType(choice=value._to_v1_2(policy))


def _pack_argument_integer_value_v1_3(
    value: int | ArgumentDynamicValue | ArgumentDiscreteLookupList,
    policy: DowngradePolicy,
) -> xtce_1_3.ArgumentIntegerValueType:
    """Pack a unified model argument index value into an ArgumentIntegerValueType."""
    match value:
        case int():
            return xtce_1_3.ArgumentIntegerValueType(choice=value)
        case ArgumentDynamicValue():
            return xtce_1_3.ArgumentIntegerValueType(choice=value._to_v1_3(policy))
        case ArgumentDiscreteLookupList():
            return xtce_1_3.ArgumentIntegerValueType(choice=value._to_v1_3(policy))


class Dimension(XtceBaseModel):
    """Used to define a subset of an array."""

    start_index: int | DynamicValue | DiscreteLookupList
    """The start index of the array.

    Must be less than or equal to the end index.

    """

    end_index: int | DynamicValue | DiscreteLookupList
    """The end index of the array.

    Must be greater than or equal to the start index.

    """

    @staticmethod
    def _resolve_index(value: int | DynamicValue | DiscreteLookupList) -> int | None:
        """Return an index value when validation is possible."""
        if isinstance(value, int):
            if value < 0:
                raise ValueError("array index must be greater than or equal to 0")
            return value
        if isinstance(value, DiscreteLookupList):
            if value.default_value < 0:
                raise ValueError("array index must be greater than or equal to 0")
            return value.default_value
        return None

    @model_validator(mode="after")
    def validate_indices(self) -> Self:
        """Validate that the start index is less than or equal to the end index."""
        start_index = self._resolve_index(self.start_index)
        end_index = self._resolve_index(self.end_index)

        if start_index is None or end_index is None:
            # Cannot validate a dynamic value
            return self

        if start_index > end_index:
            raise ValueError(
                f"start index ({start_index}) must be less than or equal to "
                f"end index ({end_index})"
            )

        return self

    _v1_1_type = None
    _v1_2_type = xtce_1_2.DimensionType
    _v1_3_type = xtce_1_3.DimensionType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.DimensionType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["start_index"] = _parse_integer_value_v1_2(obj.starting_index)
        kwargs["end_index"] = _parse_integer_value_v1_2(obj.ending_index)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.DimensionType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["start_index"] = _parse_integer_value_v1_3(obj.starting_index)
        kwargs["end_index"] = _parse_integer_value_v1_3(obj.ending_index)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["starting_index"] = _pack_integer_value_v1_2(self.start_index, policy)
        kwargs["ending_index"] = _pack_integer_value_v1_2(self.end_index, policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["starting_index"] = _pack_integer_value_v1_3(self.start_index, policy)
        kwargs["ending_index"] = _pack_integer_value_v1_3(self.end_index, policy)
        return kwargs


class ArgumentDimension(XtceBaseModel):
    """Used to define a subset of an array."""

    start_index: int | ArgumentDynamicValue | ArgumentDiscreteLookupList
    """The start index of the array.

    Must be less than or equal to the end index.

    """

    end_index: int | ArgumentDynamicValue | ArgumentDiscreteLookupList
    """The end index of the array.

    Must be greater than or equal to the start index.

    """

    @staticmethod
    def _resolve_index(
        value: int | ArgumentDynamicValue | ArgumentDiscreteLookupList,
    ) -> int | None:
        """Return an index value when validation is possible."""
        if isinstance(value, int):
            if value < 0:
                raise ValueError("array index must be greater than or equal to 0")
            return value
        if isinstance(value, ArgumentDiscreteLookupList):
            if value.default_value < 0:
                raise ValueError("array index must be greater than or equal to 0")
            return value.default_value
        return None

    @model_validator(mode="after")
    def validate_indices(self) -> Self:
        """Validate that the start index is less than or equal to the end index."""
        start_index = self._resolve_index(self.start_index)
        end_index = self._resolve_index(self.end_index)

        if start_index is None or end_index is None:
            # Cannot validate a dynamic value
            return self

        if start_index > end_index:
            raise ValueError(
                f"start index ({start_index}) must be less than or equal to "
                f"end index ({end_index})"
            )

        return self

    _v1_1_type = None
    _v1_2_type = xtce_1_2.ArgumentDimensionType
    _v1_3_type = xtce_1_3.ArgumentDimensionType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ArgumentDimensionType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["start_index"] = _parse_argument_integer_value_v1_2(obj.starting_index)
        kwargs["end_index"] = _parse_argument_integer_value_v1_2(obj.ending_index)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ArgumentDimensionType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["start_index"] = _parse_argument_integer_value_v1_3(obj.starting_index)
        kwargs["end_index"] = _parse_argument_integer_value_v1_3(obj.ending_index)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["starting_index"] = _pack_argument_integer_value_v1_2(
            self.start_index, policy
        )
        kwargs["ending_index"] = _pack_argument_integer_value_v1_2(
            self.end_index, policy
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["starting_index"] = _pack_argument_integer_value_v1_3(
            self.start_index, policy
        )
        kwargs["ending_index"] = _pack_argument_integer_value_v1_3(
            self.end_index, policy
        )
        return kwargs
