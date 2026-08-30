"""Argument models."""

from typing import Any

from pydantic import Field

from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from .array import ArgumentDimension
from .datatype import (
    AggregateData,
    ArgumentAbsoluteTimeData,
    ArgumentBinaryData,
    ArgumentBooleanData,
    ArgumentEnumeratedData,
    ArgumentFloatData,
    ArgumentIntegerData,
    ArgumentRelativeTimeData,
    ArgumentStringData,
    ArrayData,
)
from .range import ValidFloatRanges, ValidIntegerRanges


class IntegerArgument(ArgumentIntegerData):
    """Define an integer argument."""

    valid_ranges: ValidIntegerRanges | None = None
    """The valid range of input values for the argument.

    If not specified, all values are valid.

    """

    _v1_1_type = xtce_1_1.ArgumentTypeSetType.IntegerArgumentType
    _v1_2_type = xtce_1_2.IntegerArgumentType
    _v1_3_type = xtce_1_3.IntegerArgumentType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.ArgumentTypeSetType.IntegerArgumentType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["valid_ranges"] = (
            ValidIntegerRanges._from_v1_1_kwargs(obj.valid_range_set)
            if obj.valid_range_set is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.IntegerArgumentType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["valid_ranges"] = (
            ValidIntegerRanges._from_v1_2_kwargs(obj.valid_range_set)
            if obj.valid_range_set is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.IntegerArgumentType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["valid_ranges"] = (
            ValidIntegerRanges._from_v1_3_kwargs(obj.valid_range_set)
            if obj.valid_range_set is not None
            else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["valid_range_set"] = (
            self.valid_ranges._to_v1_1(policy)
            if self.valid_ranges is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["valid_range_set"] = (
            self.valid_ranges._to_v1_2(policy)
            if self.valid_ranges is not None
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["valid_range_set"] = (
            self.valid_ranges._to_v1_3(policy)
            if self.valid_ranges is not None
            else None
        )
        return kwargs


class FloatArgument(ArgumentFloatData):
    """Define a float argument."""

    valid_ranges: ValidFloatRanges | None = None
    """The valid range of input values for the argument.

    If not specified, all values are valid.

    """

    _v1_1_type = xtce_1_1.ArgumentTypeSetType.FloatArgumentType
    _v1_2_type = xtce_1_2.FloatArgumentType
    _v1_3_type = xtce_1_3.FloatArgumentType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.ArgumentTypeSetType.FloatArgumentType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["valid_ranges"] = (
            ValidFloatRanges._from_v1_1_kwargs(obj.valid_range_set)
            if obj.valid_range_set is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.FloatArgumentType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["valid_ranges"] = (
            ValidFloatRanges._from_v1_2_kwargs(obj.valid_range_set)
            if obj.valid_range_set is not None
            else None
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.FloatArgumentType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["valid_ranges"] = (
            ValidFloatRanges._from_v1_3_kwargs(obj.valid_range_set)
            if obj.valid_range_set is not None
            else None
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["valid_range_set"] = (
            self.valid_ranges._to_v1_1(policy)
            if self.valid_ranges is not None
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["valid_range_set"] = (
            self.valid_ranges._to_v1_2(policy)
            if self.valid_ranges is not None
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["valid_range_set"] = (
            self.valid_ranges._to_v1_3(policy)
            if self.valid_ranges is not None
            else None
        )
        return kwargs


class StringArgument(ArgumentStringData):
    """Define a string argument."""

    _v1_1_type = xtce_1_1.StringDataType
    _v1_2_type = xtce_1_2.StringArgumentType
    _v1_3_type = xtce_1_3.StringArgumentType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.StringDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.StringArgumentType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.StringArgumentType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        return kwargs


class BinaryArgument(ArgumentBinaryData):
    """Define a binary argument."""

    _v1_1_type = xtce_1_1.BinaryDataType
    _v1_2_type = xtce_1_2.BinaryArgumentType
    _v1_3_type = xtce_1_3.BinaryArgumentType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.BinaryDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.BinaryArgumentType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.BinaryArgumentType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        return kwargs


class BooleanArgument(ArgumentBooleanData):
    """Define a boolean argument."""

    _v1_1_type = xtce_1_1.BooleanDataType
    _v1_2_type = xtce_1_2.BooleanArgumentType
    _v1_3_type = xtce_1_3.BooleanArgumentType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.BooleanDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.BooleanArgumentType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.BooleanArgumentType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        return kwargs


class EnumeratedArgument(ArgumentEnumeratedData):
    """Define an enumerated argument."""

    _v1_1_type = xtce_1_1.EnumeratedDataType
    _v1_2_type = xtce_1_2.EnumeratedArgumentType
    _v1_3_type = xtce_1_3.EnumeratedArgumentType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.EnumeratedDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.EnumeratedArgumentType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.EnumeratedArgumentType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        return kwargs


class ArrayArgument(ArrayData):
    """Define an array argument."""

    dimensions: list[ArgumentDimension] = Field(default_factory=list, min_length=1)
    """The dimensions of the array."""

    _v1_1_type = xtce_1_1.ArrayDataTypeType
    _v1_2_type = xtce_1_2.ArrayArgumentType
    _v1_3_type = xtce_1_3.ArrayArgumentType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.ArrayDataTypeType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        # TODO maybe find a better way to handle this
        kwargs["dimensions"] = [
            ArgumentDimension(start_index=0, end_index=1)
            for _ in range(obj.number_of_dimensions)
        ]
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ArrayArgumentType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["dimensions"] = [
            ArgumentDimension._from_v1_2(d) for d in obj.dimension_list.dimension
        ]
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ArrayArgumentType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["dimensions"] = [
            ArgumentDimension._from_v1_3(d) for d in obj.dimension_list.dimension
        ]
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(
            policy, number_of_dimensions=len(self.dimensions)
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["dimension_list"] = self._build_set(
            items=self.dimensions,
            set_class=xtce_1_2.DimensionListType,
            kwarg_name="dimension",
            converter=lambda d: d._to_v1_2(policy),
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["dimension_list"] = self._build_set(
            items=self.dimensions,
            set_class=xtce_1_3.DimensionListType,
            kwarg_name="dimension",
            converter=lambda d: d._to_v1_3(policy),
        )
        return kwargs


class AggregateArgument(AggregateData):
    """Define an aggregate argument."""

    _v1_1_type = xtce_1_1.AggregateDataType
    _v1_2_type = xtce_1_2.AggregateArgumentType
    _v1_3_type = xtce_1_3.AggregateArgumentType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.AggregateDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.AggregateArgumentType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.AggregateArgumentType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        return kwargs


class RelativeTimeArgument(ArgumentRelativeTimeData):
    """Define a relative time argument."""

    _v1_1_type = xtce_1_1.RelativeTimeDataType
    _v1_2_type = xtce_1_2.ArgumentRelativeTimeDataType
    _v1_3_type = xtce_1_3.ArgumentRelativeTimeDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.RelativeTimeDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentRelativeTimeDataType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentRelativeTimeDataType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        return kwargs


class AbsoluteTimeArgument(ArgumentAbsoluteTimeData):
    """Define an absolute time argument."""

    _v1_1_type = xtce_1_1.AbsoluteTimeDataType
    _v1_2_type = xtce_1_2.ArgumentAbsoluteTimeDataType
    _v1_3_type = xtce_1_3.ArgumentAbsoluteTimeDataType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.AbsoluteTimeDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentAbsoluteTimeDataType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentAbsoluteTimeDataType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        return kwargs
