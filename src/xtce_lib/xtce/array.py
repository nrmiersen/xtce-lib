"""Array models."""

from __future__ import annotations

from typing import Any, Self

from pydantic import model_validator
from typing_extensions import assert_never

from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy, XtceUnsupportedError
from xtce_lib.generated import xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from .codec import ArgumentDynamicValue, DynamicValue
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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], dimension: xtce_1_2.DimensionType) -> Self:
        version = XtceVersion.V1_2

        def unpack_index(
            integer_value: xtce_1_2.IntegerValueType,
        ) -> int | DynamicValue | DiscreteLookupList:
            match integer_value.choice:
                case int():
                    return integer_value.choice
                case xtce_1_2.DynamicValueType():
                    return DynamicValue.from_xsdata(
                        integer_value.choice,
                        version,
                    )
                case xtce_1_2.DiscreteLookupListType():
                    return DiscreteLookupList.from_xsdata(
                        integer_value.choice,
                        version,
                    )
                case None:
                    raise ValueError(
                        "invalid XTCE XML: dimension index is missing a value"
                    )
                case _:
                    assert_never(integer_value.choice)

        return cls(
            start_index=unpack_index(dimension.starting_index),
            end_index=unpack_index(dimension.ending_index),
        )

    @classmethod
    def _from_v1_3(cls: type[Self], dimension: xtce_1_3.DimensionType) -> Self:
        version = XtceVersion.V1_3

        def unpack_index(
            integer_value: xtce_1_3.IntegerValueType,
        ) -> int | DynamicValue | DiscreteLookupList:
            match integer_value.choice:
                case int():
                    return integer_value.choice
                case xtce_1_3.DynamicValueType():
                    return DynamicValue.from_xsdata(
                        integer_value.choice,
                        version,
                    )
                case xtce_1_3.DiscreteLookupListType():
                    return DiscreteLookupList.from_xsdata(
                        integer_value.choice,
                        version,
                    )
                case None:
                    raise ValueError(
                        "invalid XTCE XML: dimension index is missing a value"
                    )
                case _:
                    assert_never(integer_value.choice)

        return cls(
            start_index=unpack_index(dimension.starting_index),
            end_index=unpack_index(dimension.ending_index),
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.DimensionType:
        def pack_index(
            value: int | DynamicValue | DiscreteLookupList,
        ) -> xtce_1_2.IntegerValueType:
            match value:
                case int():
                    return xtce_1_2.IntegerValueType(choice=value)
                case DynamicValue():
                    return xtce_1_2.IntegerValueType(choice=value._to_v1_2(policy))
                case DiscreteLookupList():
                    return xtce_1_2.IntegerValueType(choice=value._to_v1_2(policy))

        return xtce_1_2.DimensionType(
            starting_index=pack_index(self.start_index),
            ending_index=pack_index(self.end_index),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.DimensionType:
        def pack_index(
            value: int | DynamicValue | DiscreteLookupList,
        ) -> xtce_1_3.IntegerValueType:
            match value:
                case int():
                    return xtce_1_3.IntegerValueType(choice=value)
                case DynamicValue():
                    return xtce_1_3.IntegerValueType(choice=value._to_v1_3(policy))
                case DiscreteLookupList():
                    return xtce_1_3.IntegerValueType(choice=value._to_v1_3(policy))

        return xtce_1_3.DimensionType(
            starting_index=pack_index(self.start_index),
            ending_index=pack_index(self.end_index),
        )


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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], dimension: xtce_1_2.ArgumentDimensionType) -> Self:
        version = XtceVersion.V1_2

        def unpack_index(
            integer_value: xtce_1_2.ArgumentIntegerValueType,
        ) -> int | ArgumentDynamicValue | ArgumentDiscreteLookupList:
            match integer_value.choice:
                case int():
                    return integer_value.choice
                case xtce_1_2.ArgumentDynamicValueType():
                    return ArgumentDynamicValue.from_xsdata(
                        integer_value.choice,
                        version,
                    )
                case xtce_1_2.ArgumentDiscreteLookupListType():
                    return ArgumentDiscreteLookupList.from_xsdata(
                        integer_value.choice,
                        version,
                    )
                case None:
                    raise ValueError(
                        "invalid XTCE XML: dimension index is missing a value"
                    )
                case _:
                    assert_never(integer_value.choice)

        return cls(
            start_index=unpack_index(dimension.starting_index),
            end_index=unpack_index(dimension.ending_index),
        )

    @classmethod
    def _from_v1_3(cls: type[Self], dimension: xtce_1_3.ArgumentDimensionType) -> Self:
        version = XtceVersion.V1_3

        def unpack_index(
            integer_value: xtce_1_3.ArgumentIntegerValueType,
        ) -> int | ArgumentDynamicValue | ArgumentDiscreteLookupList:
            match integer_value.choice:
                case int():
                    return integer_value.choice
                case xtce_1_3.ArgumentDynamicValueType():
                    return ArgumentDynamicValue.from_xsdata(
                        integer_value.choice,
                        version,
                    )
                case xtce_1_3.ArgumentDiscreteLookupListType():
                    return ArgumentDiscreteLookupList.from_xsdata(
                        integer_value.choice,
                        version,
                    )
                case None:
                    raise ValueError(
                        "invalid XTCE XML: dimension index is missing a value"
                    )
                case _:
                    assert_never(integer_value.choice)

        return cls(
            start_index=unpack_index(dimension.starting_index),
            end_index=unpack_index(dimension.ending_index),
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ArgumentDimensionType:
        def pack_index(
            value: int | ArgumentDynamicValue | ArgumentDiscreteLookupList,
        ) -> xtce_1_2.ArgumentIntegerValueType:
            match value:
                case int():
                    return xtce_1_2.ArgumentIntegerValueType(choice=value)
                case ArgumentDynamicValue():
                    return xtce_1_2.ArgumentIntegerValueType(
                        choice=value._to_v1_2(policy)
                    )
                case ArgumentDiscreteLookupList():
                    return xtce_1_2.ArgumentIntegerValueType(
                        choice=value._to_v1_2(policy)
                    )

        return xtce_1_2.ArgumentDimensionType(
            starting_index=pack_index(self.start_index),
            ending_index=pack_index(self.end_index),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ArgumentDimensionType:
        def pack_index(
            value: int | ArgumentDynamicValue | ArgumentDiscreteLookupList,
        ) -> xtce_1_3.ArgumentIntegerValueType:
            match value:
                case int():
                    return xtce_1_3.ArgumentIntegerValueType(choice=value)
                case ArgumentDynamicValue():
                    return xtce_1_3.ArgumentIntegerValueType(
                        choice=value._to_v1_3(policy)
                    )
                case ArgumentDiscreteLookupList():
                    return xtce_1_3.ArgumentIntegerValueType(
                        choice=value._to_v1_3(policy)
                    )

        return xtce_1_3.ArgumentDimensionType(
            starting_index=pack_index(self.start_index),
            ending_index=pack_index(self.end_index),
        )
