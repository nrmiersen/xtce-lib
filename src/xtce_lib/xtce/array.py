"""Array models."""

from __future__ import annotations

from typing import Any, Self

from pydantic import model_validator

from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from .codec import (
    ArgumentDynamicValue,
    DynamicValue,
    pack_argument_integer_value_v1_1,
    pack_argument_integer_value_v1_2,
    pack_argument_integer_value_v1_3,
    pack_integer_value_v1_1,
    pack_integer_value_v1_2,
    pack_integer_value_v1_3,
    parse_argument_integer_value_v1_1,
    parse_argument_integer_value_v1_2,
    parse_argument_integer_value_v1_3,
    parse_integer_value_v1_1,
    parse_integer_value_v1_2,
    parse_integer_value_v1_3,
)
from .condition import ArgumentDiscreteLookupList, DiscreteLookupList


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
            if value.default_value is None or value.default_value < 0:
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

    _v1_1_type = xtce_1_1.ArrayParameterRefEntryType.DimensionList.Dimension
    _v1_2_type = xtce_1_2.DimensionType
    _v1_3_type = xtce_1_3.DimensionType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.ArrayParameterRefEntryType.DimensionList.Dimension
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["start_index"] = parse_integer_value_v1_1(obj.starting_index)
        kwargs["end_index"] = parse_integer_value_v1_1(obj.ending_index)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.DimensionType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["start_index"] = parse_integer_value_v1_2(obj.starting_index)
        kwargs["end_index"] = parse_integer_value_v1_2(obj.ending_index)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.DimensionType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["start_index"] = parse_integer_value_v1_3(obj.starting_index)
        kwargs["end_index"] = parse_integer_value_v1_3(obj.ending_index)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["starting_index"] = pack_integer_value_v1_1(self.start_index, policy)
        kwargs["ending_index"] = pack_integer_value_v1_1(self.end_index, policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["starting_index"] = pack_integer_value_v1_2(self.start_index, policy)
        kwargs["ending_index"] = pack_integer_value_v1_2(self.end_index, policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["starting_index"] = pack_integer_value_v1_3(self.start_index, policy)
        kwargs["ending_index"] = pack_integer_value_v1_3(self.end_index, policy)
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
            if value.default_value is None or value.default_value < 0:
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

    _v1_1_type = xtce_1_1.ArrayParameterRefEntryType.DimensionList.Dimension
    _v1_2_type = xtce_1_2.ArgumentDimensionType
    _v1_3_type = xtce_1_3.ArgumentDimensionType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.ArrayParameterRefEntryType.DimensionList.Dimension
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["start_index"] = parse_argument_integer_value_v1_1(obj.starting_index)
        kwargs["end_index"] = parse_argument_integer_value_v1_1(obj.ending_index)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ArgumentDimensionType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["start_index"] = parse_argument_integer_value_v1_2(obj.starting_index)
        kwargs["end_index"] = parse_argument_integer_value_v1_2(obj.ending_index)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ArgumentDimensionType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["start_index"] = parse_argument_integer_value_v1_3(obj.starting_index)
        kwargs["end_index"] = parse_argument_integer_value_v1_3(obj.ending_index)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["starting_index"] = pack_argument_integer_value_v1_1(
            self.start_index, policy
        )
        kwargs["ending_index"] = pack_argument_integer_value_v1_1(
            self.end_index, policy
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["starting_index"] = pack_argument_integer_value_v1_2(
            self.start_index, policy
        )
        kwargs["ending_index"] = pack_argument_integer_value_v1_2(
            self.end_index, policy
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["starting_index"] = pack_argument_integer_value_v1_3(
            self.start_index, policy
        )
        kwargs["ending_index"] = pack_argument_integer_value_v1_3(
            self.end_index, policy
        )
        return kwargs
